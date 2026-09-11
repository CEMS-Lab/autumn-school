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

:::{admonition} Worked example outline · L3-W01
:class: note

**Planned content.** Identify the coordinate and parameter inputs and scalar
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

:::{admonition} Animation storyboard · L3-A01
:class: note

**Planned content.** Start from the staggered loop and mark the damage
subsolve. Replace that operation with a labelled learned damage update,
show its input and output fields, and follow the next mechanics update.
Keep the bounds, irreversibility and coupled convergence checks visible.
This is a proposed fracture workflow.

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

:::{admonition} Animation storyboard · L3-A02
:class: note

**Planned content.** Follow input, prediction, residual evaluation, correction
and the final checked field in separate frames. Label direct acceptance and
reference fallback as distinct branches. A final cost strip will identify
prediction, checking, correction and fallback costs without assigning timing
values.

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

:::{admonition} Worked example outline · L3-W02
:class: note

**Planned content.** Use the existing small MLP and RBF field examples to
compare compatible inputs, predictions and saved-model metadata. Add a
conceptual row identifying the representation changes required by a grid or
graph model. Keep architecture comparisons qualitative until matched
computations are available.

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

:::{admonition} Animation storyboard · L3-A03
:class: note

**Planned content.** Show a current model visiting states, reference labelling
of those states, dataset aggregation and another training round. Keep a
separate evaluation set visible. Mark the entire loop as a conceptual
extension to the practical.

**Learning question:** Why might model-visited states add information to the
original training set?
:::

## Connect the routes to the practical · 46–50 minutes

In {doc}`../classroom/03_learning_and_hybrid`, train and reuse a small scalar
Helmholtz field model, inspect a proposal and evaluate the numerical response
to its residual. The example teaches the model interface and reference
correction or fallback in a compact setting. Its field and residual belong to
the Helmholtz teaching problem. A learned fracture damage subsolve and a
complete DAgger rollout are further developments represented by the storyboards.

Discuss both field quality and complete computation time when assessing a
hybrid method. The same comparison links model learning back to the physical
question that opened the course.
