"""Export course notebooks to percent-cell Python and execute every cell.

Each notebook runs in a fresh kernel against a copied course source. The
Python export is read back and compared byte-for-byte with every code cell
before execution. Existing source notebooks and earlier results are preserved.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import time
import traceback

import nbformat
from nbclient import NotebookClient
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parents[1]
CLASSROOM = ("01_simulate_fracture", "02_gradients_and_recovery", "03_learning_and_hybrid")
LIMIT_SECONDS = 120
CELL_TIMEOUT_SECONDS = 110
PROCESS_TIMEOUT_SECONDS = 115


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def export_python(nb, destination):
    """A normal Python file with editor-friendly # %% cell markers."""
    lines = ["# UKACM Autumn School 2026 — cell-by-cell Python export\n",
             "# Open in a Python editor with cell support, or run with IPython.\n",
             "# Notebook setup, equations and interpretation are retained below.\n", "\n"]
    cells = []
    for i, cell in enumerate(nb.cells):
        marker = " [markdown]" if cell.cell_type == "markdown" else ""
        lines.append(f"# %%{marker} notebook_cell={i}\n")
        start = len(lines)
        source = cell.source
        if cell.cell_type == "code":
            lines.extend(source.splitlines(keepends=True))
            if source and not source.endswith("\n"):
                lines[-1] += "\n"
        else:
            lines.extend("# " + line + "\n" for line in source.splitlines())
        cells.append({"index": i, "cell_type": cell.cell_type, "start_line_zero_based": start,
                      "end_line_exclusive": len(lines), "source_characters": len(source)})
        lines.append("\n")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("".join(lines), encoding="utf-8")
    save_json(destination.with_suffix(".cells.json"), cells)
    return cells


def cell_seconds(cell):
    values = cell.metadata.get("execution", {})
    start, end = values.get("iopub.status.busy"), values.get("iopub.status.idle")
    if not start or not end:
        return None
    return (datetime.fromisoformat(end.replace("Z", "+00:00")) -
            datetime.fromisoformat(start.replace("Z", "+00:00"))).total_seconds()


def worker(out, relative):
    snapshot = out / "course_snapshot"
    source = snapshot / relative
    name = source.stem
    kind = "classroom" if "classroom" in source.parts else "extensions" if "research" in source.parts or "drafts" in source.parts else "reference"
    destination = out / kind / name
    destination.mkdir(parents=True, exist_ok=True)
    nb = nbformat.read(source, as_version=4)
    original = [(c.cell_type, c.source) for c in nb.cells]
    python_file = destination / (name + ".py")
    exported = export_python(nb, python_file)
    python_lines = python_file.read_text(encoding="utf-8").splitlines(keepends=True)
    for cell, record in zip(nb.cells, exported):
        if cell.cell_type == "code":
            extracted = "".join(python_lines[record["start_line_zero_based"]:record["end_line_exclusive"]])
            extracted = extracted[:record["source_characters"]]
            assert extracted == cell.source, "Python export differs from notebook code"
            cell.source = extracted
            cell.outputs, cell.execution_count = [], None
            cell.metadata.pop("execution", None)
    error = None
    try:
        NotebookClient(nb, timeout=CELL_TIMEOUT_SECONDS, kernel_name="python3", allow_errors=False,
                       record_timing=True).execute(cwd=str(source.parent))
    except Exception:
        error = traceback.format_exc()
    assert [(c.cell_type, c.source) for c in nb.cells] == original
    executed_path = destination / (name + ".ipynb")
    nbformat.write(nb, executed_path)
    cells, images, html_outputs, streams = [], [], [], []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        cells.append({"cell_index_zero_based": i, "role": cell.metadata.get("classroom_role"),
                      "seconds": cell_seconds(cell), "execution_count": cell.execution_count,
                      "output_types": [o.output_type for o in cell.outputs]})
        for j, output in enumerate(cell.outputs):
            if output.output_type == "stream":
                streams.append(f"CELL {i}\n{output.text}")
            for mime, extension in (("image/png", "png"), ("image/gif", "gif"), ("image/jpeg", "jpg")):
                data = output.get("data", {}).get(mime)
                if data:
                    image_path = destination / "figures" / f"cell-{i:02d}-output-{j}.{extension}"
                    image_path.parent.mkdir(exist_ok=True)
                    image_path.write_bytes(base64.b64decode(data))
                    images.append(str(image_path.relative_to(out)))
            html = output.get("data", {}).get("text/html")
            if html:
                html_path = destination / "tables" / f"cell-{i:02d}-output-{j}.html"
                html_path.parent.mkdir(exist_ok=True)
                html_path.write_text(html, encoding="utf-8")
                html_outputs.append(str(html_path.relative_to(out)))
    (destination / "cell_output.txt").write_text("\n\n".join(streams), encoding="utf-8")
    errors = [dict(o) for c in nb.cells for o in c.get("outputs", []) if o.output_type == "error"]
    setup = [c for c in cells if c["role"] == "setup"]
    if not setup and cells:
        setup = cells[:1]
    save_json(destination / "worker.json", {
        "name": name, "kind": kind, "source_relative": relative,
        "status": "failed" if error or errors else "passed", "exception": error, "errors": errors,
        "all_code_cells_executed": all(c["execution_count"] is not None for c in cells),
        "python_export_executed_cell_by_cell": True, "export_code_identical": True,
        "setup_cell_seconds": sum(c["seconds"] or 0 for c in setup),
        "post_setup_cell_seconds": sum(c["seconds"] or 0 for c in cells if c not in setup),
        "cells": cells, "figures": images, "html_outputs": html_outputs,
        "source_sha256": sha(source), "executed_sha256": sha(executed_path),
        "code_sha256": hashlib.sha256(json.dumps([c.source for c in nb.cells if c.cell_type == "code"]).encode()).hexdigest(),
        "python_sha256": sha(python_file),
    })
    if error:
        print(error, file=sys.stderr)
    return int(bool(error or errors))


def prepare(out):
    snapshot = out / "course_snapshot"
    if snapshot.exists():
        raise RuntimeError("Choose a new evidence directory; an existing snapshot is preserved")
    for relative in ("notebooks", "configs", "vendor", "source/book/research/notebooks"):
        shutil.copytree(ROOT / relative, snapshot / relative,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "executed", "html"))
    bootstrap = Path("source/notebooks/colab_bootstrap.py")
    (snapshot / bootstrap).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / bootstrap, snapshot / bootstrap)
    hashes = {str(p.relative_to(snapshot)): sha(p) for p in snapshot.rglob("*") if p.is_file()}
    save_json(out / "snapshot_manifest.json", hashes)
    spec = KernelSpecManager().get_kernel_spec("python3")
    assert Path(spec.argv[0]).resolve() == Path(sys.executable).resolve(), spec.argv
    save_json(out / "environment.json", {
        "started_utc": datetime.now(timezone.utc).isoformat(), "source_root": str(ROOT),
        "source_revision": subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(),
        "scope": "fresh local kernels; source code read from matching percent-cell Python exports",
        "python_executable": sys.executable, "python": platform.python_version(), "platform": platform.platform(),
        "versions": {p: importlib.metadata.version(p) for p in ("torch", "numpy", "scipy", "matplotlib", "nbformat", "nbclient", "ipykernel")},
        "dependency_installation_performed": False, "authenticated_colab_validation": False,
        "limit_seconds": LIMIT_SECONDS, "cell_timeout_seconds": CELL_TIMEOUT_SECONDS,
        "whole_process_cap_seconds": PROCESS_TIMEOUT_SECONDS,
    })


def run(out, relative):
    source = out / "course_snapshot" / relative
    kind = "classroom" if "classroom" in source.parts else "extensions" if "research" in source.parts or "drafts" in source.parts else "reference"
    destination = out / kind / source.stem
    if (destination / "receipt.json").exists():
        raise RuntimeError("Run already recorded; use a new evidence directory")
    command = [sys.executable, str(Path(__file__).resolve()), "--out", str(out), "--worker", relative]
    start = time.perf_counter()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=PROCESS_TIMEOUT_SECONDS)
        status = "passed" if process.returncode == 0 else "failed"
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            stdout, stderr = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            try:
                stdout, stderr = process.communicate(timeout=2)
            except subprocess.TimeoutExpired:
                stdout, stderr = "", "Worker termination exceeded its bounded grace period."
        status = "timed_out"
    duration = time.perf_counter() - start
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "stdout.log").write_text(stdout)
    (destination / "stderr.log").write_text(stderr)
    result = json.loads((destination / "worker.json").read_text()) if (destination / "worker.json").exists() else {}
    if status == "passed" and result.get("status") == "failed":
        status = "failed"
    if status == "passed" and not 0 <= duration < LIMIT_SECONDS:
        status = "timed_out"
    result.update(status=status, whole_process_seconds=duration,
                  under_120_seconds=0 <= duration < LIMIT_SECONDS,
                  under_300_seconds=0 <= duration < 300,
                  limit_seconds=LIMIT_SECONDS, cell_timeout_seconds=CELL_TIMEOUT_SECONDS,
                  whole_process_cap_seconds=PROCESS_TIMEOUT_SECONDS,
                  command=command, returncode=process.returncode, authenticated_colab_validation=False,
                  dependency_installation_performed=False)
    snapshot = out / "course_snapshot"
    support = sorted((snapshot / "notebooks/day2_helpers").glob("*.py"))
    support += [snapshot / "source/notebooks/colab_bootstrap.py",
                snapshot / "configs/day2_forward/tiny_notched_tension.json",
                snapshot / "configs/day2_forward/b3_classroom/config.yaml",
                snapshot / "configs/day2_forward/b3_classroom/mesh.msh",
                snapshot / "vendor/PhAST/COURSE_SOURCE_MANIFEST.json"]
    result["support_sha256"] = {str(p.relative_to(snapshot)): sha(p) for p in support}
    save_json(destination / "receipt.json", result)
    print(json.dumps({"notebook": source.stem, "status": status, "seconds": duration, "figures": len(result.get("figures", []))}), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--run", nargs="+")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--worker")
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if args.worker:
        return worker(out, args.worker)
    if args.prepare:
        prepare(out)
    targets = args.run or []
    if args.all:
        targets = [f"notebooks/classroom/{name}.ipynb" for name in CLASSROOM]
        targets += [str(p.relative_to(ROOT)) for p in sorted((ROOT / "notebooks").glob("*.ipynb"))]
        targets += ["notebooks/drafts/06_differentiability_step_by_step.ipynb"]
        targets += ["source/book/research/notebooks/inverse_experiments_source.ipynb"]
    results = [run(out, relative) for relative in targets]
    if results:
        receipts = sorted(out.glob("*/*/receipt.json"))
        save_json(out / "summary.json", {"notebooks": [json.loads(p.read_text()) for p in receipts]})
    return int(any(r["status"] != "passed" or not r["under_120_seconds"] for r in results))


if __name__ == "__main__":
    raise SystemExit(main())
