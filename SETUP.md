# Prepare the Day 3 PhAST notebooks

Open the three practicals through the book's Colab links, or download them into
a local Jupyter environment. Start each notebook from a fresh kernel and run
the cells in order. NB1 and NB2 support a CPU runtime. **For NB3, select a GPU
runtime in Colab before running the setup cell.**

## Python and installation

PhAST requires Python 3.10 or newer. Use the installation cells supplied with
each notebook: the examples deliberately retain their own software versions.
NB1 installs the public PhAST package. NB2 pins revision
`157412953099bfcace1668bb35cb911826a4e95e` for the 1D bar interfaces.
NB3 downloads a frozen source snapshot and its compatible trained model from
[phast_gnn_assets.zip](https://cems-lab.github.io/autumn-school/datasets/phast/phast_gnn_assets.zip).
It verifies the source files and expected checkpoint hash before loading.
Do not substitute unrelated weights or a different source version.

Some installation cells reuse an already importable PhAST package. A fresh
environment avoids accidentally running an older installation. Record the
resolved module path, package versions and device with your results.

For a local notebook environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install notebook
python -m notebook
```

On Windows, activate with `.venv\Scripts\activate`. Then run the chosen
notebook's setup cells. Gmsh's wheel requires system OpenGL libraries; the plate
notebooks install `libglu1-mesa` on Colab. For a local Gmsh import error, check
the platform's Gmsh installation requirements.

## Three practicals

1. **NB1 — Intro to PhAST:** generate a graded mesh, simulate dynamic fracture
   in a notched plate, reload the trajectory and inspect displacement, strain,
   stress and damage. The inclined-notch and changed-parameter exercises are
   additional calculations.
2. **NB2 — Inverse Problem using PhAST:** build a 1D elastic bar, apply one
   fixed 4000 N force and recover its uniform Young's modulus from one observed
   tip displacement. Damage is not part of this example.
3. **NB3 — Hybrid FEM+DL with PhAST:** compare conventional FEM with direct GNN
   replacement of the damage subproblem. The setup downloads the required
   assets automatically; for local use, the ZIP may also be placed beside the
   notebook. No FEM damage correction follows the learned prediction.

## Reading the saved results

All three notebooks contain saved figures and numerical outputs. Their HTML
pages also retain animations. A book rebuild displays those saved results; it
does not rerun the solver. New runs may differ with the software, hardware or
parameters used.

Installation, simulation and export costs depend on the environment. Where
computational performance is studied in NB3, distinguish the damage-update
measurement from the complete solver loop and from total notebook execution.
Report the device and comparison scope alongside any measured time ratio.

## Authoring and rebuilding

Canonical inputs are `notebooks/classroom/*.ipynb`; their filename mapping is
in `notebooks/classroom/day2_edition.json` (a retained historical filename).
Regenerate pages and downloads with:

```bash
python source/book/scripts/build_classroom_pages.py
python -m sphinx -b html -E -a source/book book -W --keep-going
```

This retains numerical code and saved outputs, adds navigation and conceptual
answers, and records import hashes. Earlier execution records apply to their
own notebook revisions, not automatically to the current edition.

Colab links refer to the published `main` branch. Local changes appear online
after a commit, push and successful Pages deployment.
