---
myst:
  all_links_external: false
---

# From gradients to reliable inverse experiments

An inverse problem begins with a measurement. We observe how a specimen
responds and ask which material or geometric parameters can explain that
response. In this part of the book, we develop this idea for a plate containing
stiff particles and for a spatially varying stiffness field.

We will study more than the movement of an optimiser. We will ask what is
measured, what is unknown, how a finite-element calculation produces the
measurement, and which conclusions follow from a numerical test. The examples
progress from short calculations to protocols suitable for a fracture solver.

## Preparation

You should be able to differentiate a scalar function and multiply a matrix
by a vector. Each section introduces the additional notation it uses. The
one-stop notebook includes the derivations, complete numerical and plotting
code, outputs and worked answers for the seven teaching examples.

Our damage convention is $d=0$ for intact material and $d=1$ for complete
damage. A particle is a material inclusion; its centre is an unknown model
parameter on a fixed finite-element mesh.

```{figure} figures/inverse_workflow.png
:width: 100%
:name: fig-research-workflow
:alt: Parameters feed a forward model, observations, loss, reverse sensitivity and a bounded update.

An inverse experiment connects parameters to observations through a forward
model. The arrows describe the information flow used to assess recovery.
Editable LaTeX/TikZ source accompanies this original schematic.
```

## A reading and computation route

Open the [one-stop notebook](notebooks/inverse_experiments.ipynb) for a
continuous explanation with complete code, worked answers and retained plots.
It also has a {download}`downloadable Jupyter copy <notebooks/inverse_experiments.ipynb>`.
The execution receipt distinguishes completed HPC calculations from proposed
full-fracture research protocols.

| Part | Question | Computation |
|---|---|---|
| Geometry | Can a particle move through a fixed mesh smoothly? | Indicator and overlap gradients |
| Observations | Which discrepancy does the loss measure? | Nodal and integrated error |
| Differentiation | Does the computed gradient match the stated map? | AD, adjoint and FD comparison |
| Fracture history | What happens at a kink, a tie or unloading? | Hard forward, smooth forward and surrogate backward |
| Recovery | Why do different starts give different answers? | Conditioning and observation rank |
| Learning | What can a learned component safely contribute? | Initial prediction and exact correction |
| Applications | How do these tests become a fracture study? | A controlled research protocol |

The executable examples in this extension are **analytic and small linear
algebra models**. They isolate specific questions; none is presented as a new
phase-field fracture recovery. The application chapter explains how to repeat
the checks with PhAST and how to keep those results separate.

The [visual laboratory](08_visual_lab.md) adds computed loss surfaces and
three animations. It pairs an explicit geometry-observation toy with retained
FEM samples and a recorded particle recovery, keeping their objectives and
provenance separate. Begin there for a visual connection between the plate,
the particle estimate and the objective.

```{toctree}
:maxdepth: 1

01_geometry
02_observations
03_derivatives
03_history_visual
03_history
04_recovery
05_learning
06_applications
08_visual_lab
07_results
notebooks/inverse_experiments
```

## How to work through an exercise

Before running code, write down your prediction. Change one quantity, repeat
the calculation and compare the result with the prediction. In your answer,
state both the observation and its explanation. A curve that looks smooth
and a programme that exits successfully answer different questions.

For this research edition, all numerical experiments are executed on HPC.
The displayed figures are rendered from retained numerical arrays. Reading
the book requires neither an HPC account nor a live simulation.

## Attribution

The question--derivation--computation--interpretation structure was informed
by [Advanced Deep Learning for Physics](https://tum-pbs.github.io/ADL4P/).
The text, teaching calculations and figures here are original and adapted to
fracture mechanics. The explanations needed for the executed examples are
included here; the reference course is optional further reading. Its
demonstrations provide methodological background, while each result here
is supported by its own retained computation.
