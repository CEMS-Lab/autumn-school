# PhAST: fracture simulation, differentiation and learning

How does a cracked body respond to loading? How does that response depend on a
material parameter? Where can a learned model assist the calculation?

This course follows those three questions through phase-field fracture,
differentiable simulation and hybrid learning. Begin with the lecture guides,
then work through the three corresponding practical notebooks. Basic mechanics,
calculus and introductory Python provide the starting point.

## Three connected lectures

| Lecture | Central question |
| --- | --- |
| {doc}`1. Phase-field fracture and PhAST <lectures/01_fracture_and_phast>` | How do geometry, material and loading produce a damage field? |
| {doc}`2. Differentiability and inverse applications <lectures/02_differentiability_and_inverse>` | How can a measured response tell us about an unknown input? |
| {doc}`3. Hybrid numerical and learned methods <lectures/03_hybrid_learning>` | How can a learned prediction work alongside a physical solver? |

The guides connect the existing explanations and illustrations. Labelled example
outlines and animation storyboards identify the material being prepared for
the lecture series.

## Three practical notebooks

Each lab moves through **predict → explain → compute → inspect → exercise →
worked solution**. Short code cells introduce one operation at a time.
Expandable setup and implementation details keep the complete calculation
available for closer study.

| Practical | What you will do |
| --- | --- |
| {doc}`Lab 1 — Simulate and interpret fracture <classroom/01_simulate_fracture>` | Inspect a notched specimen and its loading, run PhAST, and interpret crack propagation, energy curves and saved fields. |
| {doc}`Lab 2 — Gradients and parameter recovery <classroom/02_gradients_and_recovery>` | Check a degradation derivative, trace an elastic-bar sensitivity, and recover a material parameter. |
| {doc}`Lab 3 — Learning and hybrid correction <classroom/03_learning_and_hybrid>` | Train a small field model, save and reload it, then assess and correct its prediction. |

Each notebook page includes **Google Colab**, practice and worked-solution
downloads. Start with the [environment setup guide](../SETUP.md).
The first lab uses PhAST; the second combines a PhAST degradation law with an
elastic-bar teaching model; the third uses a small Helmholtz field model to
make training and correction easy to inspect.

## Foundations to revisit

The reference chapters develop four complementary themes:

- **What Phase-Field Fracture Is:** energy, degradation and the length scale.
- **Hands-on with the PhAST Solver:** geometry, mesh, boundary conditions and results.
- **Differentiability and Inverse Problems:** computational graphs and checked gradients.
- **Deep Learning Integration:** training, model interfaces and physical correction.

Throughout the book, $d=0$ denotes intact material and $d=1$ denotes fully
damaged material. Symbols and assumptions are introduced beside their equations.

```{toctree}
:maxdepth: 1
:caption: Lecture guides

lectures/01_fracture_and_phast
lectures/02_differentiability_and_inverse
lectures/03_hybrid_learning
```

```{toctree}
:maxdepth: 1
:caption: Three practical labs

classroom/01_simulate_fracture
classroom/02_gradients_and_recovery
classroom/03_learning_and_hybrid
```

```{toctree}
:maxdepth: 1
:caption: Reference chapters

00_welcome_and_routes
01_crack_representations
02_phase_field_energy
03_staggered_solution
04_fem_to_tensors
05_differentiation_and_inverse
06_learning_adapter
07_practice_references
further_practice
```

The [interactive visual explorations](../explorations.html) accompany the
equations. The detailed notebooks remain available in {doc}`further_practice`
for independent study.

```{toctree}
:maxdepth: 1
:caption: Optional inverse experiments

research/index
```
