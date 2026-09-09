# From cracks to computation: learn by doing

## What this course is for

Fracture simulations can look persuasive long before they are understood. A
colour map may show a thin damaged band, a reaction curve may soften, and a
notebook may differentiate an objective. None of those observations alone
identifies the model, the discretisation, or the numerical assumptions that
produced them. This course develops a habit of naming each layer.

By the end of the day, you should be able to:

- distinguish a fracture *formulation* from a finite-element
  *discretisation* and a nonlinear *solution method*;
- write a common phase-field energy and explain the role of its length scale;
- trace a computation from geometry and boundary conditions to arrays, fields,
  and observable quantities;
- use automatic differentiation for a stated computational graph, and compare
  one directional derivative with a finite-difference estimate; and
- describe what a learned proposal, adapter, or correction is allowed to
  claim in a mechanics workflow.

The examples are deliberately small. Their purpose is to make assumptions
inspectable, not to establish a material prediction or a benchmark. Each
computational lesson follows the same rhythm: predict, derive or identify the
relevant quantity, inspect the code and retained output, then test your
interpretation against a worked solution.

## Opening experiment: can a good average be a bad prediction?

Suppose an input admits two valid states. Will a single learned average be
valid too? The short opening experiment compares balanced supervised fitting
with an explicitly selected energy-minimising branch. Predict the answer
before opening the plots; return to its gradient calculation after the
differentiation chapter.

```{toctree}
:maxdepth: 1

labs/00_why_average_predictions_can_fail
```

This original algebraic activity is inspired by the
[Physics-based Deep Learning teaser](https://physicsbaseddeeplearning.org/intro-teaser.html).
It is not a phase-field fracture model. It introduces a recurring question:
does the objective measure the property that we actually want?

## Reading and running the book

The primary route is contained in this book. Read a theory section, continue
to its computational lesson in the local table of contents, and return to the
next theory section with one observation in hand.

**Read and predict.** Read the figures and worked equations first. Before a
code cell, state what sign, field pattern, or check you expect to see.

**Inspect and explain.** The five integrated lessons pair the reviewed code
with its retained figures and result cards: a degradation derivative, a public
PhAST notched-tension calculation, a differentiable elastic-bar toy, a saved
toy field model, and a checked toy proposal with fallback. Use the exercise and
solution in each lesson to distinguish what the output shows from what it does
not establish.

**Execute optionally.** Download a lesson notebook only when you want to alter
an input or repeat the calculation in a Jupyter environment. Read its recorded
result card before running it. The record belongs to the environment in which
it was measured; it is not a portable runtime prediction.

**Extend a local solver deliberately.** Install and document a solver
environment only when you need to alter the physics, mesh, or algorithm. The public
[PhAST source repository](https://github.com/CEMS-Lab/PhAST) is a useful
starting point for source and release information. A local run should record
the software revision, numerical settings, and output location alongside the
physical parameters.

## The result card

For every computational activity, write a compact result card. It separates
what was specified from what was observed.

### Minimum result card

1. **Case:** geometry, material regions, and boundary/loading conditions.
2. **Numerics:** mesh or nodal layout, quadrature convention, load steps,
   tolerances, and the phase-field length $\ell$.
3. **Environment:** software version, device, precision, and seed where a
   random process is used.
4. **Observation:** the selected field, scalar quantity, and a labelled plot.
5. **Check:** a named equilibrium, residual, constraint, or derivative check.
6. **Limit:** one sentence describing what the check does *not* establish.

For example, a monotone increase in $d$ at one node is consistent with a
damage-irreversibility rule, but it does not by itself demonstrate mesh
objectivity. A close directional derivative match at one parameter value
checks a local calculation, not the uniqueness of an inverse recovery.

## A vocabulary for careful claims

Use the following three sentence patterns when describing a numerical result.

- **Specified:** “The calculation used $d=0$ as intact, $d=1$ as broken, a
  stated regularisation length $\ell$, and the listed boundary conditions.”
- **Observed:** “For this discretisation and load increment, the plotted
  damage field localised near the prescribed notch.”
- **Not inferred:** “This observation alone does not identify a physical crack
  path at all mesh resolutions or loading rates.”

This is not cautious wording for its own sake. It tells another reader which
part of a conclusion they can reproduce, challenge, or extend.

## A first prediction before a first computational lesson

Before reading the first computational lesson, make a prediction in words. If the tensile energy
driving damage is high near a notch and the loading increases, where should a
phase-field model first permit the damage variable to grow? What quantity
would you plot to distinguish a narrow diffuse band from a broadly distributed
reduction in stiffness?

After the run, return to the prediction. A useful explanation has four parts:

1. the location and shape actually observed;
2. the terms in the energy that encourage or resist that shape;
3. the numerical choice that may influence it; and
4. one test that would make the explanation stronger.

This pattern will be used throughout the book.

## Exercise: label the layers

Classify each statement as a fracture formulation, spatial discretisation,
solution/sensitivity method, or observable.

1. “Use a scalar damage field and a gradient penalty.”
2. “Add a discontinuous enrichment near a crack.”
3. “Alternate displacement and damage subproblems.”
4. “Compare reaction force against imposed displacement.”
5. “Differentiate a scalar loss with respect to a material multiplier.”

:::{admonition} Solution
:class: dropdown

1. A phase-field **fracture formulation**. The scalar field and gradient
   penalty define a regularised crack representation.
2. **Spatial discretisation**: this describes the central idea of XFEM.
3. A **solution method**: staggered solution can be applied to a chosen
   formulation and discretisation.
4. An **observable** derived from the computed state and boundary data.
5. A **sensitivity method/task**. Automatic differentiation or an adjoint
   may compute the derivative; neither is itself a fracture formulation.
:::

## What to carry into Chapter 1

Keep two questions visible: *what object represents the crack?* and *what
exactly is solved?* The next chapter places phase field, XFEM, and cohesive
models next to one another without treating them as interchangeable labels.
