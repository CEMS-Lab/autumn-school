# PhAST: a learn-by-doing introduction to phase-field fracture

```{figure} figures/00_course_map.*
:name: fig-course-map
:width: 100%
:alt: Three 120-minute sessions: understand fracture and FEM with notebook 00; run PhAST and check derivatives with notebooks 01 to 03; train and assess learned proposals with notebooks 04 and 05. Each session includes a ten-minute break.

The six-hour route combines explanation, discussion and notebook activities.
Each two-hour session includes a ten-minute break; computation time is measured
separately.
```

This short textbook develops a reproducible way to reason about phase-field
fracture computations. It moves from a stated fracture model to compact
computational lessons, retained outputs, exercises, and worked solutions in
one reading route. It is not a substitute for a fracture-mechanics text or a
production-solver manual. Its goal is narrower and more practical: connect a
variational fracture model to a mesh, tensors, differentiation, and honest
numerical checks.

The convention throughout is $d=0$ for intact material and $d=1$ for fully
broken material. A small residual stiffness is retained in practical
calculations to avoid a singular elastic operator; it is a numerical device,
not a physical claim that a fully cracked material still carries substantial
load.

```{admonition} How to use this book
:class: tip

For each topic, make a prediction, read the derivation, inspect the code and
its retained output, and answer the exercise before opening the worked
solution. The computational lessons are child pages of their theory chapters,
not a separate collection of notebook exports. Each may also be downloaded for
optional execution in a Jupyter environment.

One lesson contains a small public PhAST quasistatic calculation. The inverse
and learning lessons use original teaching models, not fracture-inverse or
fracture-acceleration results. When you execute a lesson, record the mesh,
parameters, outputs, and observed runtime for that environment. A retained
result card never predicts runtime on another machine.
```

For visual experiments alongside the text, open the
[interactive explorations](../explorations.html). To run the computational
lessons, use the [environment guide](../SETUP.md). The
[printable edition](../ebooks/phast-ukacm-course.pdf) includes the code,
recorded figures and complete worked solutions.

:::{only} html
Select a diagram to open its full-size vector view. On a small screen, enlarge
that view to follow the equation labels and feedback arrows.
:::

```{toctree}
:maxdepth: 2
:numbered:

00_welcome_and_routes
01_crack_representations
02_phase_field_energy
03_staggered_solution
04_fem_to_tensors
05_differentiation_and_inverse
06_learning_adapter
07_practice_references
```

## Optional inverse experiments

The {doc}`inverse visual laboratory <research/08_visual_lab>` connects particle
geometry, sampled loss landscapes and retained fracture fields. Begin with
the {doc}`animated history lesson <research/03_history_visual>` to see how loading
and unloading change a derivative route. These optional readings extend the
six-hour course without replacing its classroom activities. The current
printable edition covers the classroom route; this extension is available
in HTML and downloadable notebooks and figures.

```{toctree}
:maxdepth: 1
:caption: Optional inverse experiments

research/index
```
