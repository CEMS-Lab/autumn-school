"""Retain checked classroom outputs and their data without changing a solve."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

import nbformat
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/notebook_visual_runs_20260911b"
NAMES = ("01_simulate_fracture", "02_gradients_and_recovery", "03_learning_and_hybrid")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    summary = json.loads((EVIDENCE / "summary.json").read_text())
    assert len(summary["notebooks"]) == 11
    assert all(r["status"] == "passed" and r["under_300_seconds"] and r["all_code_cells_executed"]
               for r in summary["notebooks"])
    data = EVIDENCE / "course_snapshot/assets/day2_forward/classroom"
    parity = {}
    for name in ("tiny_notched_tension", "tiny_notched_tension_half_load"):
        before = ROOT / "assets/day2_forward" / (name + "_fields.npz")
        after = data / "01" / before.name
        with np.load(before, allow_pickle=False) as old, np.load(after, allow_pickle=False) as new:
            assert set(old.files) == set(new.files)
            for key in old.files:
                np.testing.assert_array_equal(old[key], new[key])
            parity[name] = {"unchanged_arrays": len(old.files), "exact_array_equality": True}
    (EVIDENCE / "executed").mkdir(exist_ok=True)
    for i, name in enumerate(NAMES, 1):
        folder = EVIDENCE / "classroom" / name
        receipt = json.loads((folder / "receipt.json").read_text())
        executed = folder / (name + ".ipynb")
        canonical = ROOT / "notebooks/classroom" / executed.name
        a, b = nbformat.read(canonical, 4), nbformat.read(executed, 4)
        assert [(c.cell_type, c.source) for c in a.cells] == [(c.cell_type, c.source) for c in b.cells]
        for relative, expected in receipt["support_sha256"].items():
            assert sha(ROOT / relative) == expected, relative
        shutil.copy2(executed, EVIDENCE / "executed" / executed.name)
        (EVIDENCE / (name + ".json")).write_text(json.dumps(receipt, indent=2) + "\n")
        subprocess.run([sys.executable, str(ROOT / "scripts/run_classroom.py"), "--notebook", str(i),
                        "--retain-only", "--evidence-dir", str(EVIDENCE)], check=True)
    shutil.copytree(data, ROOT / "assets/day2_forward/classroom", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    subprocess.run([sys.executable, str(ROOT / "source/book/scripts/build_classroom_pages.py"),
                    "--evidence-dir", str(EVIDENCE)], check=True)
    report = {"scope": "11 distinct lesson notebooks executed; three classroom variants retained",
              "legacy_phast_array_parity": parity, "figures": sum(len(r["figures"]) for r in summary["notebooks"]),
              "notebooks": [{k: r[k] for k in ("name", "status", "whole_process_seconds", "setup_cell_seconds",
                                                 "post_setup_cell_seconds", "all_code_cells_executed")}
                            for r in summary["notebooks"]],
              "python_exports_read_back_and_executed": True, "google_colab_rehearsal": False}
    (EVIDENCE / "final_receipt.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
