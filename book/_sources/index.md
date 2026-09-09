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
one reading route. The aim is to connect a variational fracture model to a
mesh, tensors, differentiation, and interpretable numerical checks.

The convention throughout is $d=0$ for intact material and $d=1$ for fully
broken material. A small residual stiffness is retained in practical
calculations to avoid a singular elastic operator. This numerical
regularisation influences the residual load carried by damaged material and
should be included in the case definition.

```{admonition} How to use this book
:class: tip

For each topic, make a prediction, read the derivation, inspect the code and
its retained output, and answer the exercise before opening the worked
solution. The computational lessons are child pages of their theory chapters.
Each may also be downloaded for execution in a Jupyter environment.
For the six core lessons, keep the complete course folder, including its
solver, configurations and helper modules. The environment guide explains
the local and Colab setup. The optional diffusion companion is standalone.

One lesson contains a small PhAST quasistatic calculation. The inverse
lesson uses an elastic bar, and the learning lessons use a scalar field model
to study model interfaces and correction. When you execute a lesson, record
the mesh, parameters, outputs, and runtime for your environment.
```

For visual experiments alongside the text, open the
[interactive explorations](../explorations.html). To run the computational
lessons, use the [environment guide](../SETUP.md). The HTML lessons include
the code, recorded figures and complete worked solutions, with practice and
solution notebooks available for download.

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
and unloading change a derivative route. Select these readings to extend a
classroom topic or explore the subject after the course. The interactive panels
and animations accompany the downloadable notebooks and figures.

```{toctree}
:maxdepth: 1
:caption: Optional inverse experiments

research/index
```
