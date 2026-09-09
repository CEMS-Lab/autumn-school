# Prepare once; run short experiments

The HTML companion, PDF book and executed notebook pages can be read immediately
without installing anything. To execute the notebooks, keep the full extracted
course folder together.

## Local Python environment

Use Python 3.10, 3.11 or 3.12. The public PhAST revision supplied here declares
Python >=3.10 and <3.13. From the extracted course directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install ./vendor/PhAST notebook nbformat nbclient nbconvert
python -m notebook notebooks
```

On Windows, replace the activation command with
`.venv\Scripts\activate`. Select the new environment as the notebook kernel.
If the kernel cannot import a dependency, check its Python executable before
reinstalling packages.

Installation downloads dependencies and is not part of the five-minute
computation budget. The tested authoring environment was already provisioned;
the exact execution versions and timings are in the execution report. A clean
installation on every supported operating system has not been rehearsed.

## The source snapshot

`vendor/PhAST/` contains the public source at
`f6324f899f0701769810be117f27f1208f7a582e` (version 0.16.2), its licence,
project metadata and a SHA-256 manifest. The notebook helper verifies that
snapshot and prefers it over unrelated installed or development copies.
No Git history or private solver checkout is needed.

The exercises use a small generated structured triangular mesh and do not
require an interactive meshing application or a GPU. Change parameters in the
notebook/configuration, not inside the solver source.

## Run a single exercise with a hard time budget

After setup, use the notebook interface or the supplied whole-process runner:

```bash
python scripts/run_course.py --notebook 1
```

Choose a number from 0 to 5 (0 is the opening algebraic teaser).
The runner stops an activity before 300 seconds
and writes an executed notebook plus a runtime receipt under `runs/`.
Run exercises sequentially when reproducing the timing measurements.
The notebooks also write small figures, data and model artifacts under
`assets/day2_forward/`.

## Google Colab

The computational exercises are CPU-sized and do not require a paid GPU.
The local timings are not a measurement of Google's current Colab service.
Before teaching on Colab, rehearse the complete setup and all six notebooks
in a fresh runtime; Python and package availability may change.

1. Upload and extract the complete ZIP into the Colab runtime, retaining its
   directory structure, including `vendor/`, `configs/` and `notebooks/`.
2. Check that the runtime's Python version meets the source requirements.
3. In a setup cell, change directory into the extracted course folder and use
   `%pip install ./vendor/PhAST nbformat nbclient nbconvert`.
4. Open/upload the desired notebook and ensure its current directory is the
   extracted course's `notebooks/` directory. Retain the helper folder.
5. Run from the first cell. Record setup and whole-notebook time separately.
   If the service is slow, use the included executed HTML for the discussion.

The public course source is [CEMS-Lab/autumn-school](https://github.com/CEMS-Lab/autumn-school).
Opening a single notebook on Colab does not also supply its local helpers and
source snapshot: retain the complete course folder as described above. A fresh
Colab rehearsal remains necessary before promising classroom runtimes.

## If something fails

Read the first error and the notebook's expected checks. Do not remove
convergence checks, disable source verification, or increase problem size merely
to obtain a plot. Restart the kernel after changing environments. For a report,
include Python/PyTorch versions, notebook name, changed parameters, full error,
and whether the unmodified example reproduces the issue.
