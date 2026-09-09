"""Execute one UKACM notebook with both cell and aggregate time limits.

Example (from the course worktree)::

    python \
      teaching/ukacm_autumn_school_2026/notebooks/run_with_timeout.py \
      notebooks/01_phast_tiny_evolving_fracture.ipynb

The runner deliberately writes only to ``notebooks/executed``.  It is a local
CPU receipt helper, not a Colab validator.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


COURSE_ROOT = Path(__file__).resolve().parents[1]
EXECUTED = COURSE_ROOT / "notebooks" / "executed"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path, help="Notebook path relative to the course root or worktree.")
    parser.add_argument("--timeout", type=int, default=300, help="Aggregate process timeout in seconds.")
    args = parser.parse_args()

    notebook = args.notebook
    if not notebook.is_absolute():
        direct = COURSE_ROOT / notebook
        notebook = direct if direct.is_file() else Path.cwd() / notebook
    notebook = notebook.resolve()
    if not notebook.is_file():
        parser.error("notebook was not found")
    EXECUTED.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        f"--ExecutePreprocessor.timeout={args.timeout}",
        "--output-dir",
        str(EXECUTED),
        str(notebook),
    ]
    started = time.perf_counter()
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=args.timeout, check=False)
    except subprocess.TimeoutExpired:
        print(json.dumps({
            "status": "timed_out",
            "aggregate_timeout_seconds": args.timeout,
            "notebook": notebook.name,
            "elapsed_seconds": round(time.perf_counter() - started, 3),
        }))
        return 124
    print(completed.stdout, end="")
    print(completed.stderr, end="", file=sys.stderr)
    print(json.dumps({
        "status": "completed" if completed.returncode == 0 else "failed",
        "aggregate_timeout_seconds": args.timeout,
        "notebook": notebook.name,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "returncode": completed.returncode,
    }))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
