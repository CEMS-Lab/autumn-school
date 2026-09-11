"""Run one detailed-reference notebook with a strict two-minute budget."""
import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = [
    "00_why_average_predictions_can_fail",
    "01_phast_tiny_evolving_fracture",
    "02_degradation_autograd",
    "03_tiny_derivative_inverse_toy",
    "04_train_save_reload_adapter",
    "05_hybrid_reference_correction",
]
LIMIT_SECONDS = 120
CELL_TIMEOUT_SECONDS = 110
PROCESS_TIMEOUT_SECONDS = 115


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=int, choices=range(0,6), required=True)
    parser.add_argument("--evidence-dir", type=Path,
                        help="New rehearsal directory; each notebook receives its own subdirectory")
    args = parser.parse_args()
    name = NAMES[args.notebook]
    destination = (ROOT / (args.evidence_dir or Path("runs")) / name).resolve()
    if (destination / "runtime.json").exists():
        raise ValueError("Receipt already exists; choose a new --evidence-dir")
    destination.mkdir(parents=True, exist_ok=True)
    source = ROOT / "notebooks" / (name + ".ipynb")
    supporting = sorted((ROOT / "notebooks/day2_helpers").glob("*.py"))
    supporting += [ROOT / "source/notebooks/colab_bootstrap.py",
                   ROOT / "configs/day2_forward/tiny_notched_tension.json",
                   ROOT / "configs/day2_forward/b3_classroom/config.yaml",
                   ROOT / "configs/day2_forward/b3_classroom/mesh.msh",
                   ROOT / "vendor/PhAST/COURSE_SOURCE_MANIFEST.json"]
    source_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    support_sha256 = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                      for path in supporting}
    command = [
        sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute",
        f"--ExecutePreprocessor.timeout={CELL_TIMEOUT_SECONDS}",
        "--output-dir", str(destination),
        str(source),
    ]
    started = time.perf_counter()
    process = subprocess.Popen(command, cwd=ROOT / "notebooks",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, start_new_session=(os.name != "nt"))
    try:
        stdout, stderr = process.communicate(timeout=PROCESS_TIMEOUT_SECONDS)
        status = "passed" if process.returncode == 0 else "failed"
    except subprocess.TimeoutExpired:
        if os.name != "nt":
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
        else:
            process.kill()
        try:
            stdout, stderr = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            if os.name != "nt":
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            else:
                process.kill()
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
    receipt = {"notebook":name,"seconds":elapsed,"status":status,
               "whole_process_seconds": elapsed, "limit_seconds": LIMIT_SECONDS,
               "cell_timeout_seconds": CELL_TIMEOUT_SECONDS,
               "whole_process_cap_seconds": PROCESS_TIMEOUT_SECONDS,
               "under_120_seconds": 0 <= elapsed < LIMIT_SECONDS,
               "under_300_seconds": 0 <= elapsed < 300,
               "source_sha256": source_sha256, "support_sha256": support_sha256,
               "authenticated_colab_validation": False,
               "dependency_installation_performed": False,
               "scope":"whole notebook process including plots in a pre-provisioned environment; cold installation measured separately"}
    (destination / "runtime.json").write_text(json.dumps(receipt,indent=2) + "\n")
    print(json.dumps(receipt,indent=2))
    if status != "passed" or not receipt["under_120_seconds"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
