# Lecture 1: Phase-field fracture and PhAST

This lecture connects the physical description of a crack to
the numerical operations used to simulate it. Basic calculus and vectors are
sufficient preparation; the finite-element ideas are introduced as they arise.

We follow a notched specimen under tensile loading. The main question is how
its deformation, damage field and reaction force change as the load increases.
Later lectures ask how these observations depend on material parameters and
where a learned model could contribute to the calculation.

## From a crack to a damage field

A crack creates new surfaces and changes the way a specimen carries load.
Phase-field fracture represents this process with a continuous damage field
$d$: zero denotes intact material and one denotes fully damaged material.
The length scale $\ell$ controls the width of the diffuse transition.
The {doc}`crack-representation chapter <../01_crack_representations>` places this
description alongside sharp-crack, cohesive and enriched finite-element models.

:::{admonition} Reading a diffuse crack profile
:class: note

Compare a notched specimen, its diffuse damage band and a line profile across
the band. Increasing $\ell$ widens an idealised profile. In a computed fracture
field, the material model, loading and mesh also affect the observed profile.

**Learning question:** Which quantity changes when we widen the diffuse band?
:::

## Energy and stiffness degradation

The model balances stored elastic energy, the energy required to create a
diffuse crack, and external work. The fracture energy $G_c$ sets the cost of
creating crack surface. A degradation function reduces the selected elastic
energy as $d$ grows; a small residual stiffness is often retained in the
numerical model. Damage irreversibility records the material's loading history.

Use the existing {ref}`energy-profile figure <fig-energy-profiles>`
to compare AT1 and AT2 profiles and the degradation curve. Their functions,
normalisation and derivations are in the
{doc}`phase-field energy chapter <../02_phase_field_energy>`.

:::{admonition} Interpreting degradation and the length scale
:class: note

Read the degradation curve at intact, partially damaged
and nearly broken states. Then compare a change in $G_c$ with a change in
$\ell$, keeping the other modelling choices fixed. Distinguish the
fracture-energy scale, band width and mesh resolution.

**Learning question:** How do these choices enter the physical model?
:::

## One numerical increment

Finite elements interpolate displacement and damage from values stored at
mesh nodes. A staggered calculation updates displacement with damage held
fixed, evaluates the driving field, and updates damage with the current
mechanics held fixed. A convergence check determines whether to repeat these
updates or accept the increment. The
{ref}`staggered-loop figure <fig-staggered-loop>` shows this ordering;
the {doc}`chapter <../03_staggered_solution>` gives the governing equations.

:::{admonition} Following the staggered calculation
:class: note

Follow mechanics, the driving field, damage and convergence in order within
one fixed load increment. Advance the load after the increment satisfies its
convergence criterion. The accepted damage from the preceding increment
provides the irreversibility reference.

**Learning question:** Which loop repeats at a fixed load, and which step
changes the loading?
:::

## Tensors, matrix-free actions and dynamics

Coordinates describe where nodes lie; connectivity lists the nodes in each
element; field arrays contain their displacement and damage. Gathering local
values, evaluating element contributions and adding them back to the global
field connects the finite-element model to tensor operations. The existing
{ref}`FEM pipeline <fig-fem-pipeline>` and
{doc}`tensor chapter <../04_fem_to_tensors>` develop these operations.

A matrix-free calculation evaluates the effect of a matrix on a vector using
element calculations, without assembling the full matrix. Its cost depends on
the iterative solver and its preconditioner, which helps the iterations
converge. A dynamic calculation also updates velocity and acceleration through
physical time, using a chosen time-integration method and time step.

:::{admonition} One element and its tensor operations
:class: note

Follow one triangle from nodal displacement to strain
and a residual contribution, then sketch an operator action using the same
local data. Add a final state row for displacement, velocity, acceleration and
damage to locate the extra quantities in a dynamic calculation.

**Learning question:** Which arrays represent geometry, fields and physical
time evolution?
:::

## Connect the model to the practical

In {doc}`../classroom/01_simulate_fracture`, inspect the geometry and loading,
run the small PhAST example, and interpret the advancing damage field alongside
the loading history and elastic, fracture and kinetic energies. The selected
configuration uses a 40 mm square glass plate with a 20 mm geometric notch,
explicit dynamics and an implicit spectral AT2 damage update. Students generate
a graded Gmsh mesh with target sizes of 0.25 mm near the crack path and 2 mm
away from it. Actual mesh counts are printed after generation. Equal and
opposite vertical displacements act on the top and bottom; the left and right
edges are restrained horizontally. The ramp lasts 20 microseconds within a
50-microsecond simulation window.

The notebook uses `phast.load_result` and `phast.compute_field` to inspect
displacement, strain, stress and damage, then animate them with fixed colour
scales. Run the horizontal-notch reference first; the inclined-notch exercise
is an additional simulation. Quantitative path and speed accuracy require
mesh refinement.

Finish by choosing one parameter and one observable that could be compared
between runs. {doc}`Lecture 2 <02_differentiability_and_inverse>` follows this
relationship through the computational graph.
