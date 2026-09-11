"""Execute one curated classroom notebook with a whole-process time limit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NAMES = ("01_simulate_fracture", "02_gradients_and_recovery", "03_learning_and_hybrid")
LIMIT_SECONDS = 120
CELL_TIMEOUT_SECONDS = 110
PROCESS_TIMEOUT_SECONDS = 115


def within_runtime_limit(receipt):
    """Re-evaluate dated receipts against the current classroom budget."""
    seconds = receipt.get("whole_process_seconds", float("inf"))
    return (receipt.get("status") == "passed" and 0 <= seconds < LIMIT_SECONDS
            and receipt.get("under_120_seconds", True) is True)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def retain(name, evidence_dir=None):
    """Retain verified outputs in the tracked canonical notebook for clean clones."""
    source = ROOT / "notebooks/classroom" / (name + ".ipynb")
    record_dir = evidence_dir or ROOT / "evidence/classroom_runs_20260910"
    destination = evidence_dir / "executed" if evidence_dir else ROOT / "notebooks/executed/classroom"
    executed = destination / source.name
    receipt_path = record_dir / (name + ".json")
    receipt = json.loads(receipt_path.read_text())
    code = [c.source for c in nbformat.read(source, 4).cells if c.cell_type == "code"]
    if not within_runtime_limit(receipt):
        raise ValueError("A passing whole-process receipt below 120 seconds is required")
    if hashlib.sha256(json.dumps(code).encode()).hexdigest() != receipt["code_sha256"]:
        raise ValueError("Authored computation differs from execution")
    if digest(executed) != receipt["executed_sha256"]:
        raise ValueError("Executed notebook differs from receipt")
    authored, completed = nbformat.read(source, 4), nbformat.read(executed, 4)
    if [(c.cell_type, c.source) for c in authored.cells] != [(c.cell_type, c.source) for c in completed.cells]:
        raise ValueError("Authored cell content changed after execution")
    if any(o.output_type == "error" for c in completed.cells for o in c.get("outputs", [])):
        raise ValueError("Cannot retain an errored notebook")
    for relative, expected in receipt["support_sha256"].items():
        if digest(ROOT / relative) != expected:
            raise ValueError("Supporting source changed after execution: " + relative)
    source.write_bytes(executed.read_bytes())
    receipt["retained_sha256"] = digest(source)
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=int, choices=(1, 2, 3), required=True)
    parser.add_argument("--retain-only", action="store_true", help="Retain an already verified local execution without running it again")
    parser.add_argument("--evidence-dir", type=Path, help="Dated receipt directory; executed notebooks go in its executed/ subdirectory")
    args = parser.parse_args()
    evidence_dir = (ROOT / args.evidence_dir).resolve() if args.evidence_dir else None
    name = NAMES[args.notebook - 1]
    if args.retain_only:
        retain(name, evidence_dir)
        return
    source = ROOT / "notebooks/classroom" / (name + ".ipynb")
    record_dir = evidence_dir or ROOT / "evidence/classroom_runs_20260910"
    if evidence_dir and (record_dir / (name + ".json")).exists():
        raise ValueError("Receipt already exists; choose a new evidence directory or use --retain-only")
    destination = evidence_dir / "executed" if evidence_dir else ROOT / "notebooks/executed/classroom"
    destination.mkdir(parents=True, exist_ok=True)
    authored = nbformat.read(source, 4)
    code = [c.source for c in authored.cells if c.cell_type == "code"]
    helper_paths = sorted((ROOT / "notebooks/day2_helpers").glob("*.py"))
    helper_paths += [ROOT / "source/notebooks/colab_bootstrap.py",
                     ROOT / "configs/day2_forward/tiny_notched_tension.json",
                     ROOT / "configs/day2_forward/b3_classroom/config.yaml",
                     ROOT / "configs/day2_forward/b3_classroom/mesh.msh",
                     ROOT / "vendor/PhAST/COURSE_SOURCE_MANIFEST.json"]
    source_hashes = {str(p.relative_to(ROOT)): digest(p) for p in helper_paths}
    command = [sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook",
               "--execute", f"--ExecutePreprocessor.timeout={CELL_TIMEOUT_SECONDS}",
               "--output-dir", str(destination), str(source)]
    started = time.perf_counter()
    process = subprocess.Popen(command, cwd=ROOT / "notebooks", stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, start_new_session=True)
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
    elapsed = time.perf_counter() - started
    if status == "passed" and not 0 <= elapsed < LIMIT_SECONDS:
        status = "timed_out"
    print(stdout)
    print(stderr, file=sys.stderr)
    receipt = {
        "name": name, "status": status, "whole_process_seconds": elapsed,
        "limit_seconds": LIMIT_SECONDS, "cell_timeout_seconds": CELL_TIMEOUT_SECONDS,
        "whole_process_cap_seconds": PROCESS_TIMEOUT_SECONDS,
        "under_120_seconds": 0 <= elapsed < LIMIT_SECONDS,
        "under_300_seconds": 0 <= elapsed < 300,
        "scope": "complete notebook process including plots in a pre-provisioned local environment; cold installation measured separately",
        "authenticated_colab_validation": False,
        "dependency_installation_performed": False,
        "platform": platform.system() + " " + platform.machine(),
        "python": platform.python_version(),
        "code_sha256": hashlib.sha256(json.dumps(code).encode()).hexdigest(),
        "source_sha256": digest(source), "support_sha256": source_hashes,
    }
    if status == "passed":
        executed = nbformat.read(destination / source.name, 4)
        if [c.source for c in executed.cells if c.cell_type == "code"] != code:
            raise ValueError("Executed source differs from authored source")
        if any(o.output_type == "error" for c in executed.cells for o in c.get("outputs", [])):
            raise ValueError("Execution contains an error output")
        receipt["executed_sha256"] = digest(destination / source.name)
    record_dir.mkdir(exist_ok=True, parents=True)
    (record_dir / (name + ".json")).write_text(json.dumps(receipt, indent=2) + "\n")
    if within_runtime_limit(receipt):
        retain(name, evidence_dir)
    print(json.dumps(receipt, indent=2))
    raise SystemExit(not within_runtime_limit(receipt))


if __name__ == "__main__":
    main()
