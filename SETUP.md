# Prepare once; run short experiments

Read the HTML chapters and executed notebook pages immediately.
To execute the notebooks, keep the full extracted course folder together.

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
For dependency import errors, check the kernel's Python executable before
reinstalling packages.

The five-minute computation budget starts after dependency installation.
The execution report identifies the provisioned reference environment,
package versions and timings. Reproduce setup on the target operating system
before teaching.

## The source snapshot

`vendor/PhAST/` contains the public source at
`f6324f899f0701769810be117f27f1208f7a582e` (version 0.16.2), its licence,
project metadata and a SHA-256 manifest. The notebook helper verifies that
snapshot and prefers it over unrelated installed or development copies.
The bundled snapshot supplies the solver files used by the lessons.

The exercises generate a small structured triangular mesh and run on a CPU.
Set parameters in the notebook or configuration file.

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

Choose a CPU runtime for these small computational exercises. Before teaching
on Colab, rehearse the complete setup and all six notebooks in a fresh runtime;
Python and package availability may change.

1. Follow **Open in Colab** at the top of the selected book lesson. Select a
   CPU runtime with Python 3.10–3.12.
2. Run the first cell. It retrieves the complete public course folder,
   including `vendor/`, `configs/` and notebook helpers, and installs the
   declared PhAST dependencies into that Colab runtime.
3. Read the printed setup record: it gives Python/package versions, the
   resolved course commit and setup time. A fresh session uses the current
   public `main` revision. For a fixed published edition, set
   `os.environ["PHAST_COURSE_REF"]` to its release tag or full commit before
   running the setup cell. Retain that commit in the rehearsal receipt.
4. Choose **Runtime → Run all**. Follow the explanations, inspect the fields
   and response curves, then try the exercises. Use **Restart session and run
   all** when checking that a notebook runs independently from a clean kernel.
5. Download generated NPZ/JSON/figure or model files from the Colab Files pane
   under `autumn-school/assets/`. Keep those results with the setup record.

Notebook variants share their computational cells. Practice files present
the questions; solution files add expandable hints and worked answers.
Colab links open the published course edition. Use the recorded commit and
package versions when comparing your run with the course execution report.

For an offline laptop, download and extract the full course folder and use
the local environment instructions above. The book retains executed outputs
for reading while an environment is being prepared.

The public course source is [CEMS-Lab/autumn-school](https://github.com/CEMS-Lab/autumn-school).
Retain the complete course folder to supply each notebook's local helpers and
source snapshot. Use a fresh-runtime rehearsal to measure classroom runtimes.

## If something fails

Read the first error and the notebook's expected checks. Keep convergence and
source-verification checks active while diagnosing the problem. Start from the
unmodified example and vary one setting at a time. Restart the kernel after
changing environments. For a report,
include Python/PyTorch versions, notebook name, changed parameters, full error,
and whether the unmodified example reproduces the issue.
