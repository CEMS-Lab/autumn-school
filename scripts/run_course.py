"""Run one course notebook with a strict whole-process five-minute budget."""
import argparse
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=int, choices=range(0,6), required=True)
    args = parser.parse_args()
    name = NAMES[args.notebook]
    destination = ROOT / "runs" / name
    destination.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable, "-m", "jupyter", "nbconvert", "--to", "notebook", "--execute",
        "--ExecutePreprocessor.timeout=280",
        "--output-dir", str(destination),
        str(ROOT / "notebooks" / (name + ".ipynb")),
    ]
    started = time.perf_counter()
    process = subprocess.Popen(command, cwd=ROOT / "notebooks",
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, start_new_session=(os.name != "nt"))
    try:
        stdout, stderr = process.communicate(timeout=295)
        elapsed = time.perf_counter() - started
        status = "passed" if process.returncode == 0 else "failed"
        print(stdout)
        print(stderr, file=sys.stderr)
    except subprocess.TimeoutExpired:
        if os.name != "nt":
            os.killpg(process.pid, signal.SIGTERM)
        else:
            process.kill()
        try:
            process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            if os.name != "nt":
                os.killpg(process.pid, signal.SIGKILL)
            else:
                process.kill()
            process.communicate()
        elapsed = time.perf_counter() - started
        status = "timed_out"
    receipt = {"notebook":name,"seconds":elapsed,"status":status,
               "limit_seconds":300,"scope":"whole notebook process after environment setup"}
    (destination / "runtime.json").write_text(json.dumps(receipt,indent=2) + "\n")
    print(json.dumps(receipt,indent=2))
    if status != "passed" or elapsed >= 300:
        sys.exit(1)


if __name__ == "__main__":
    main()
