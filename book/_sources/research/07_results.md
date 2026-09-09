---
myst:
  all_links_external: false
---

# Retained computations and reproducibility

The six numerical teaching experiments were executed on HPC. The figures in
this extension use their retained arrays. These checks concern the stated
teaching models.

## Result card

- Checks passed: 15 / 15.
- Measured experiment-loop time: 0.197 seconds, excluding Python
  startup, package imports, queue wait and figure rendering.
- Python 3.11.15; PyTorch 2.8.0+cu128; NumPy 2.4.2.
- AD log-stiffness derivative: -0.1924.
- Implicit derivative: -0.1924.
- Best sampled FD relative discrepancy: 1.64e-11.

| Check | Outcome |
|---|---|
| overlap gradient finite | Pass |
| coincident centres have zero separating gradient | Pass |
| separated energy zero | Pass |
| tangent energy zero | Pass |
| consistent integral exact on both meshes | Pass |
| nodal average changes with sampling | Pass |
| ad matches implicit | Pass |
| fd has accurate intermediate steps | Pass |
| scaled quadratic objective smaller | Pass |
| both quadratic objectives decrease | Pass |
| one observation has null direction | Pass |
| two observations recover both unknowns | Pass |
| additional observation reduces posterior determinant | Pass |
| corrected solution matches direct solve | Pass |
| zero start also matches direct solve | Pass |

The coincidence check intentionally records a zero separating gradient. A
passing test reproduces that stationary configuration. Separating coincident
particles requires a prescribed perturbation or another tested geometry rule.

## Reproduce and inspect

Download the {download}`experiment script <code/lab.py>` and
{download}`retained arrays and checks <data/teaching_results.json>`.
The {download}`figure renderer <code/render.py>` only reads retained results.
The {download}`workflow source <tex/inverse_workflow.tex>` uses LaTeX/TikZ.
The {download}`rendering receipt <data/rendering_receipt.json>` records
input, generator and figure hashes with the plotting-library version.

```bash
python lab.py --output teaching_results.json
```

NumPy and PyTorch are required. Research executions for this project use HPC.
The script exits unsuccessfully if any declared teaching check fails. The
source SHA-256 stored in the result file is checked by the renderer.

## What this evidence establishes

The tests verify geometry behaviour, quadrature, a smooth linear-solve
derivative, simple optimisation and observation models, and a corrected linear
prediction. Verifying an entire fracture trajectory additionally requires its
specific source, observation rule, history updates and forward/adjoint checks.
The application chapter sets out those separate experiments.
