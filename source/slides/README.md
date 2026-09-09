# PhAST — from cracks to computation

The primary presentation is [phast_autumn_school_2026.pdf](phast_autumn_school_2026.pdf),
built from [editable LaTeX/Beamer source](phast_autumn_school_2026.tex).
It has 44 slides in 16:9 format. The visual style is plain white,
black academic titles, real LaTeX equations, large scientific plots and short
source/scope footers. Discussion prompts and detailed limitations are in the notes.

The v0.1.1 revision updates the six-hour overview, staggered loop,
assembled/matrix-free comparison, reverse-accumulation diagram, correction
branch and conceptual DAgger loop. The diagrams are original editable TikZ,
with a blue forward path and labelled orange reverse/retry path. See the
course-root `DESIGN_STANDARD.md` for inspected Delft, TUM and ETH references.
Numerical outputs and the three 120-minute allocations are unchanged.

## Teaching route

| Slides | Session | Scheduled teaching time |
| --- | --- | --- |
| 1–2 | Opening and learning journey | Orientation |
| 3–16 | A: fracture, energy, discretisation and solution | 120 minutes, including 10-minute break |
| 17–30 | B: PhAST forward, local derivative and inverse toy | 120 minutes, including 10-minute break |
| 31–44 | C: training, reload, adapters and reference correction | 120 minutes, including 10-minute break |

These are relative teaching allocations, not the published event timetable.
Instruction/activity totals 330 minutes; breaks total 30 minutes.
Detailed durations, exercise prompts and scope are in
[beamer_speaker_notes.md](beamer_speaker_notes.md), generated from the same notes
embedded in the TeX source. [beamer_slide_manifest.json](beamer_slide_manifest.json)
is the machine-readable equivalent. Compute targets are separate from teaching
durations; use `EXECUTION_REPORT.md` at the course root for the local CPU receipt.

Notebook routes, relative to the complete course package root:

1. `notebooks/01_phast_tiny_evolving_fracture.ipynb` — public PhAST AT2 damage evolution.
2. `notebooks/02_degradation_autograd.ipynb` — exact public degradation law, local analytic/AD/FD check.
3. `notebooks/03_tiny_derivative_inverse_toy.ipynb` — original elastic-bar tensor inverse toy.
4. `notebooks/04_train_save_reload_adapter.ipynb` — original Helmholtz-like field toy, MLP/RBF and checkpoint.
5. `notebooks/05_hybrid_reference_correction.ipynb` — original toy adapter/residual/fallback and replay record.

## Rebuild

Run in this directory with Python, NumPy, Matplotlib and a TeX installation
containing Beamer, Latin Modern, TikZ, listings and latexmk:

```sh
python build_beamer_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error phast_autumn_school_2026.tex
```

The checked build used Matplotlib 3.10.8 and TeX Live 2026. The figure generator
does not install dependencies, access the internet, execute notebooks, train a
model or solve fracture. It replots analytic curves and frozen course-owned data.
The TeX source contains no absolute file paths.

All figure dependencies are inside `latex_figures/`; the source directory is
self-contained for building the PDF. In particular:

- `analytic_plot_data.json`: sampled degradation, derivative and AT1/AT2 profile values.
- `forward_fields.npz`, `forward_summary.json`, `forward_config.json`: frozen notebook 01 result/configuration.
- `toy_heldout_arrays.npz`: frozen reference/prediction/error arrays from notebook 04.
- `notebook03_inverse.png`: executed notebook 03 response/history plot.
- `notebook04_heldout.png`, `notebook05_fallback.png`: additional source exhibits retained for teaching; the main deck uses a newly plotted two-panel comparison for notebook 04.

`build_beamer_figures.py` produces PDF figures and PNG previews. Analytic line plots
and schematics are editable through that source. Heatmaps/field shading are
scientific raster layers inside their PDF figure containers; axes and labels
remain vector text. No plot is a screenshot copied from a third-party talk.

Optional QA (requires `pypdf`, Pillow and Poppler's `pdftoppm`):

```sh
python render_beamer.py
```

This renders all 44 pages to `latex_qa/slide-*.png`, creates eight contact sheets,
extracts the speaker notes, and checks page/frame/notes counts, placeholders,
missing-glyph warnings and overfull boxes. Inspect the rendered pages as well as
the structural report. A structurally valid PDF alone is not visual QA.

## Scientific scope

- Convention: `d=0` intact, `d=1` broken; irreversible growth where required.
- The foundational energy is representative; the actual quick PhAST run selects
  isotropic degradation, not the tension/compression split used to explain the energy.
- The normalisation is `c0=4 integral_0^1 sqrt(w(s)) ds`: AT1 `w=d`, `c0=8/3`;
  AT2 `w=d²`, `c0=2`. Degradation is a separate choice.
- The exact quadratic law is `(1-eta)(1-d)²+eta`. Illustrative plots use
  `eta=1e-6`; actual notebooks 01/02 use `eta=1e-7`.
- The cubic illustration is `(1-eta)(1-3d²+2d³)+eta`; the rational illustration is
  `(1-eta)(1-d)²/[(1-d)²+2d(1+d)]+eta`. These are not calibrated PF-CZM comparisons.
- The profile plots are isolated 1D crack-density minimisers, not fracture solves.
- Actual notebook 01 fields show diffuse quasi-static damage evolution beyond a
  prescribed precrack. They do not establish sharp crack-front propagation,
  branching, physical-time dynamics or a matrix-free speedup.
- The bar inverse and Helmholtz-like learning/adapter exercises are separate toys,
  not full PhAST fracture inverse or trained learned-damage results.
- The field toy uses a positive discrete negative-Laplacian on interior nodes and
  Dirichlet boundary rows; its residual is not a PhAST AT2 residual.
- DAgger is explained; notebook 05 logs a replay record. A full aggregated
  retraining loop is optional and is not claimed as executed.
- No unmeasured speed claim, fresh-Colab certification or unpublished research
  result is introduced by the slides. Geometry/Gmsh import and a larger paper
  exhibit remain explicitly labelled extensions/discussion.

## Sources and reuse

- Francfort, G. A. and Marigo, J.-J. (1998). *Revisiting brittle fracture as an
  energy minimization problem*. JMPS 46, 1319–1342.
  [DOI](https://doi.org/10.1016/S0022-5096(98)00034-9).
- Bourdin, B., Francfort, G. A. and Marigo, J.-J. (2000). *Numerical experiments
  in revisited brittle fracture*. JMPS 48, 797–826.
  [DOI](https://doi.org/10.1016/S0022-5096(99)00028-9).
- Miehe, C., Welschinger, F. and Hofacker, M. (2010). *Thermodynamically
  consistent phase-field models of fracture: variational principles and
  multi-field FE implementations*. IJNME 83, 1273–1311.
  [DOI](https://doi.org/10.1002/nme.2861).
- Pham, K., Amor, H., Marigo, J.-J. and Maurini, C. (2011). *Gradient damage
  models and their use to approximate brittle fracture*. IJDM 20, 618–652.
  [DOI](https://doi.org/10.1177/1056789510386852).
- Ross, S., Gordon, G. and Bagnell, D. (2011). *A reduction of imitation learning
  and structured prediction to no-regret online learning*. AISTATS.
  [Paper](https://proceedings.mlr.press/v15/ross11a.html).
- [PyTorch autograd documentation](https://docs.pytorch.org/docs/autograd).
- [Public PhAST source](https://github.com/CEMS-Lab/PhAST), pinned for notebook 01/02
  to `f6324f899f0701769810be117f27f1208f7a582e`, version 0.16.2, MIT licence.
- [CWI SciML Autumn School material](https://github.com/ScientificComputingCWI/SemesterProgramme-SciML)
  informed the physical-example → equation → operation → exercise sequence and
  reference-corrected learning discussion. Representative Sanderse/Agdestein,
  Rackauckas and Walther pages were visually inspected. No CWI slide or figure
  was copied, and no redistribution licence for those archived slides was assumed.

All new schematics and the plot code are original course preparation. Reuse of
the complete course package follows its own licence and publication decision;
this build does not grant a new licence over third-party references or publish
private research assets.
