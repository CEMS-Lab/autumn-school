# Lecture 1: Phase-field fracture and PhAST

**45 minutes.** This lecture connects the physical description of a crack to
the numerical operations used to simulate it. Basic calculus and vectors are
sufficient preparation; the finite-element ideas are introduced as they arise.

We follow a notched specimen under tensile loading. The main question is how
its deformation, damage field and reaction force change as the load increases.
Later lectures ask how these observations depend on material parameters and
where a learned model could contribute to the calculation.

## From a crack to a damage field · 0–6 minutes

A crack creates new surfaces and changes the way a specimen carries load.
Phase-field fracture represents this process with a continuous damage field
$d$: zero denotes intact material and one denotes fully damaged material.
The length scale $\ell$ controls the width of the diffuse transition.
The {doc}`crack-representation chapter <../01_crack_representations>` places this
description alongside sharp-crack, cohesive and enriched finite-element models.

:::{admonition} Animation storyboard · L1-A01
:class: note

**Planned content.** A notched specimen, a diffuse damage band and a line
profile will appear in sequence. A change in $\ell$ will show how the profile
width changes. The frames will distinguish an idealised profile illustration
from a computed fracture field.

**Learning question:** Which quantity changes when we widen the diffuse band?
:::

## Energy and stiffness degradation · 6–18 minutes

The model balances stored elastic energy, the energy required to create a
diffuse crack, and external work. The fracture energy $G_c$ sets the cost of
creating crack surface. A degradation function reduces the selected elastic
energy as $d$ grows; a small residual stiffness is often retained in the
numerical model. Damage irreversibility records the material's loading history.

Use the existing {ref}`energy-profile figure <fig-energy-profiles>`
to compare AT1 and AT2 profiles and the degradation curve. Their functions,
normalisation and derivations are in the
{doc}`phase-field energy chapter <../02_phase_field_energy>`.

:::{admonition} Worked example outline · L1-W01
:class: note

**Planned content.** Read the degradation curve at intact, partially damaged
and nearly broken states. Then compare a change in $G_c$ with a change in
$\ell$, keeping the other modelling choices fixed. The discussion will
separate fracture-energy scale, band width and mesh resolution.

**Learning question:** How do these choices enter the physical model?
:::

## One numerical increment · 18–31 minutes

Finite elements interpolate displacement and damage from values stored at
mesh nodes. A staggered calculation updates displacement with damage held
fixed, evaluates the driving field, and updates damage with the current
mechanics held fixed. A convergence check determines whether to repeat these
updates or accept the increment. The
{ref}`staggered-loop figure <fig-staggered-loop>` shows this ordering;
the {doc}`chapter <../03_staggered_solution>` gives the governing equations.

:::{admonition} Animation storyboard · L1-A02
:class: note

**Planned content.** Highlight mechanics, driving field, damage and convergence
in order within one fixed load increment. A separate final transition will
advance the load. The accepted damage from the preceding increment will stay
visible as the history reference.

**Learning question:** Which loop repeats at a fixed load, and which step
changes the loading?
:::

## Tensors, matrix-free actions and dynamics · 31–41 minutes

Coordinates describe where nodes lie; connectivity lists the nodes in each
element; field arrays contain their displacement and damage. Gathering local
values, evaluating element contributions and adding them back to the global
field connects the finite-element model to tensor operations. The existing
{ref}`FEM pipeline <fig-fem-pipeline>` and
{doc}`tensor chapter <../04_fem_to_tensors>` develop these operations.

A matrix-free route evaluates an operator's action on a vector through local
calculations. Its computational cost depends on the iteration and
preconditioning used. Dynamics additionally evolves velocity and acceleration
through physical time; the selected time integrator and time step become part
of the model's numerical description.

:::{admonition} Worked example outline · L1-W02
:class: note

**Planned content.** Follow one triangle from nodal displacement to strain
and a residual contribution, then sketch an operator action using the same
local data. Add a final state row for displacement, velocity, acceleration and
damage to locate the extra quantities in a dynamic calculation.

**Learning question:** Which arrays represent geometry, fields and physical
time evolution?
:::

## Connect the model to the practical · 41–45 minutes

In {doc}`../classroom/01_simulate_fracture`, inspect the geometry and loading,
run the small PhAST example, and interpret the advancing damage field alongside
the loading history and elastic, fracture and kinetic energies. The selected
configuration uses a geometric single-edge notch, explicit central-difference
dynamics and an implicit spectral AT2 damage update. Projected CG with Jacobi
preconditioning enforces the damage bounds. The imported mesh has 1,091 nodes
and 1,940 triangles. It provides a short qualitative view of a crack crossing
the plate; quantitative path and speed accuracy require mesh refinement.

Finish by choosing one parameter and one observable that could be compared
between runs. {doc}`Lecture 2 <02_differentiability_and_inverse>` follows this
relationship through the computational graph.
