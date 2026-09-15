# Prepare the Day 2 notebooks

The three classroom notebooks install the public PhAST package and run on a
CPU. Open them through the book’s Colab links or download them into a local
Jupyter environment. Run each notebook from a fresh kernel, in cell order.

## Python and installation

PhAST requires Python 3.10 or newer. The bar notebook pins revision
`157412953099bfcace1668bb35cb911826a4e95e`, whose package metadata removes
the former Python 3.12 upper bound. The plate and learned-damage notebooks
select the default PhAST branch unless `PHAST_REF` is set. Supported Python
versions also depend on the availability of compatible dependencies.

The installation cells skip installation when PhAST is already importable.
Use a fresh environment to avoid accidentally running an older installation.
Record the actual revision and package versions with your results. The
learned-damage adapter checkout and installed solver should use the same revision.

For a local environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install notebook "phast @ git+https://github.com/CEMS-Lab/PhAST.git"
python -m notebook
```

On Windows, activate with `.venv\Scripts\activate`. Gmsh’s wheel requires
system OpenGL libraries; the plate notebooks install `libglu1-mesa` on Colab.
For a local Gmsh import error, check the platform’s Gmsh installation requirements.

The older `vendor/PhAST` snapshot supports the detailed reference notebooks.
The Day 2 notebooks install their own public PhAST revision.

## Three practicals

1. **Dynamic plate:** generate a graded Gmsh mesh, run the horizontal-notch
   reference, reload the trajectory and animate displacement, strain, stress
   and damage. The inclined-notch and changed-parameter exercises add runs.
2. **Modulus recovery:** build a 1D elastic bar, apply one fixed 4000 N force,
   record one tip observation and recover the uniform modulus. Figures,
   animation and tables are saved in `bar_results/`.
3. **Learned damage:** obtain the instructor’s `mesh_graph_net.pt` before
   starting. Colab currently requests an upload. Locally, place it at
   `phast_lab2/mesh_graph_net.pt`, the path used by the supplied notebook.
   Only load trusted model files. The notebook prints a checksum; automated
   verification would additionally require a trusted expected checksum.

The learned notebook runs classical damage, a learned initial guess, and
checked direct replacement. Its supplied checkpoint has no public download
linked from this edition. Do not substitute unrelated weights.

## Reading plots and measuring runtime

The bar notebook contains supplied outputs. The dynamic plate and learned
notebooks contain plotting and animation code but no retained run outputs.
Execute those cells to produce their visual results. A book rebuild renders
supplied content; it does not run the numerical calculations.

The teaching target is below two minutes after installation, including plots
and exports. Fresh whole-notebook Colab timing is still required for this
edition. Three comparison solves or additional exercises can exceed a
single-reference timing. Record installation separately, then measure the
complete chosen activity on the actual teaching machine.

## Authoring and rebuilding

Canonical inputs are `notebooks/classroom/*.ipynb`; the supplied file mapping
is in `notebooks/classroom/day2_edition.json`. Regenerate pages and downloads:

```bash
python source/book/scripts/build_classroom_pages.py
python -m sphinx -b html -E -a source/book book -W --keep-going
```

This retains the supplied code and outputs, adds navigation and conceptual
answers, and records import hashes. Earlier classroom execution receipts refer
to earlier notebooks. The historical generation and retention runners must be
reviewed before applying them to these new inputs.

Colab links refer to the published `main` branch. A local book update appears
there only after an approved commit, push and Pages deployment.
