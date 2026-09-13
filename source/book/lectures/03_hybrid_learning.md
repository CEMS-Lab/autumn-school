# Lecture 3: Learning inside a numerical workflow

**50 minutes.** This lecture connects the gradients from
{doc}`Lecture 2 <02_differentiability_and_inverse>` to neural-model training and
hybrid computation. We follow the information passed between a model and a
numerical calculation, then consider how that information changes during use.

## Define and train a small model · 0–8 minutes

A learning task begins with stated input channels and a target output. For
supervised fitting, a loss compares the prediction with stored reference
targets, and backpropagation computes its gradient with respect to model
weights. Residual-based training differentiates an equation evaluated at the
prediction. Solver-in-the-loop training also follows the selected numerical
updates. The {doc}`learning chapter <../06_learning_adapter>` expands these
three computational graphs.

:::{admonition} Training and reusing a small field model
:class: note

Identify the coordinate and parameter inputs and scalar
field target in the existing Helmholtz teaching model. Follow a short training
step, then save and reload the weights together with normalisation and feature
order. Compare the same input before and after reload.

**Learning question:** What information is needed to reuse a trained model?
:::

## Route A: learn the damage subsolve · 8–18 minutes

Within the staggered scheme, the damage subsolve receives the current
mechanical driving quantity and the information needed to describe material,
geometry, loading and history. A learned replacement would produce a damage
update for those inputs. It remains coupled to the next mechanics update and
to the convergence and admissibility checks for the complete increment.

:::{admonition} A learned damage update
:class: note

Start from the staggered loop and identify the damage
subsolve. Replace that operation with a labelled learned damage update,
show its input and output fields, and follow the next mechanics update.
Keep the bounds, irreversibility and coupled convergence checks visible.
The {doc}`single-replacement case study <../w53_direct_replacement>` illustrates
this role with a retained Radius-GNO fracture trajectory and a measured
damage-stage timing comparison.

**Learning question:** Which operation is learned, and what conditions still
govern the accepted state?
:::

## Route B: physically correct a prediction · 18–28 minutes

A second route uses a model to propose a state and evaluates that proposal
with the governing residual and the relevant constraints. A numerical
correction can then refine the state; a reference solve can provide a fallback.
The corrected state needs its own checks. The
{ref}`existing learning-cycle figure <fig-learning-cycle>` introduces
these exchanges.

:::{admonition} Assessing and correcting a prediction
:class: note

Follow the inputs, prediction, residual evaluation, numerical correction and
accepted field. Distinguish direct acceptance from reference fallback.
Include prediction, checking, correction and fallback when measuring the
cost of the complete calculation.

**Learning question:** How can we tell whether the complete hybrid calculation
improves on its reference calculation?
:::

## Compare models through a common interface · 28–38 minutes

An MLP maps a chosen feature vector to an output; convolutional models use
structured grids; graph models use a specified connectivity; neural operators
aim to learn maps between functions through their chosen representations.
Architecture choice follows the available data and the desired field map.
Input meaning, spatial ordering, units and output interpretation must remain
clear when models are exchanged.

:::{admonition} Comparing model interfaces
:class: note

Use the small field-model example to identify its input features, prediction
and saved-model metadata. Consider how an RBF, grid-based model or graph model
would represent the same field. Explain which inputs and spatial information
each architecture requires. A quantitative comparison would use matched
training data, field-error measures and complete computation times.

**Learning question:** Which parts of the model interface must agree for a
comparison to be meaningful?
:::

## Learning from states encountered during use · 38–46 minutes

Online prediction means applying the trained model during a calculation.
Online learning also updates the model using incoming examples. Active
learning selects which examples should receive new reference labels. A
DAgger-style round specifically collects states visited by the current model,
queries a reference procedure there, aggregates those labelled records and
re-trains the model. Held-out evaluation is needed to assess the revised model.

:::{admonition} A conceptual DAgger round
:class: note

Trace the states visited by the current model, reference labelling of those
states, dataset aggregation and another training round. Reserve a separate
evaluation set to assess the updated model. This conceptual extension explains
how the data distribution can change as a learned component is used.

**Learning question:** Why might model-visited states add information to the
original training set?
:::

## Connect the routes to the practical · 46–50 minutes

In {doc}`../classroom/03_learning_and_hybrid`, train and reuse a small scalar
Helmholtz field model, inspect a proposal and evaluate the numerical response
to its residual. The example teaches the model interface and reference
correction or fallback in a compact setting. Its field and residual belong to
the Helmholtz teaching problem. The direct-replacement fracture case study
provides a separate application, while the DAgger discussion introduces an
iterative data-collection and training strategy.

Discuss both field quality and complete computation time when assessing a
hybrid method. The same comparison links model learning back to the physical
question that opened the course.
