# Verify the single-force bar environment

A 100 mm elastic bar with a 10 mm² cross-section extends under a 4000 N force.
Its analytical displacement is `u(x) = F x / (E A)`. This provides a small CPU
check of PhAST installation, equilibrium, differentiation and modulus recovery.
Here `F` is the end force, `A` the cross-sectional area and `E` Young's modulus.
The coordinate `x` measures distance from the fixed end, where displacement is zero.

## Prepare an isolated environment

Use Python 3.10 or newer and install Git. Check that `git --version` works in
the same terminal. Pip uses Git to download the selected PhAST revision.
Run the following commands from the course repository root.

```bash
git --version
python3 -m venv .venv
.venv/bin/python -m pip install -r source/requirements-teaching-preflight.txt
.venv/bin/python -m pip check
.venv/bin/python -m scripts.teaching_preflight
.venv/bin/python -m phast doctor
.venv/bin/python -m pytest -q -s tests/test_teaching_preflight.py tests/test_bar_acceptance.py
```

On Windows use `.venv\Scripts\python.exe` in place of `.venv/bin/python`.
For Colab, start a fresh runtime and install the same pinned requirement.
Gmsh can require platform-specific system libraries even for an installation
whose first numerical example is a bar. Follow the existing SETUP.md guidance.

This example uses the selected, tested PhAST revision
`6d1903e96874ce501f7bd466fdfd9d7b0ea10519`. Dependencies are resolved for the
selected interpreter. Retain `pip freeze` or a pip installation report with
each test record.
The requirements include a SciPy 1.14.1 compatibility pin for macOS with
Python 3.10 to support loading the compiled sparse solver. Other platforms
retain PhAST's dependency constraints and require their own installation check.

## What the checks establish

The environment check reads pip's installation record, compares its repository
and full commit identifier, verifies the resolved import location, and checks installed Python
sources against their wheel RECORD hashes. Run it before importing PhAST in a
fresh interpreter. This prevents a cached package from being accepted after
an installation change. It records package versions and checked source hashes.
PhAST's existing `doctor` command provides broader environment diagnostics.
Installation remains an explicit step in the commands above.

The numerical tests use CPU float64 with PyTorch sparse-invariant checks enabled.
They check the following quantities and results.

- The complete nodal displacement field against the analytical solution.
- A -4000 N support reaction and free-node residual below 1e-6 N.
- Tip and loss derivatives against analytical expressions at 100 GPa.
- Recovery from 100 GPa toward 210 GPa using one fixed force and a synthetic
  tip observation, with the notebook's momentum-SGD settings.

Recovery stops when the relative tip error stays below 1e-4 for five consecutive
evaluations, with at most 80 parameter updates. Each update evaluates PhAST
again. The tests print the measured recovery history and source/environment
record. The environment check also imports the SciPy sparse backend to detect binary
loading errors before numerical work. Runtime depends on the environment.
Record installation, process and inverse-loop time separately.

This example covers first-order derivatives of a fixed-mesh elastic bar.
Two-dimensional models, fracture evolution, learned damage and ParaView output
require additional numerical tests. The recorded local run supports this CPU
example. Complete notebook execution and Colab execution need separate checks.
