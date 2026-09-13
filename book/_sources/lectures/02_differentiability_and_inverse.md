# Lecture 2: Differentiability and inverse recovery

**55 minutes.** Building on the displacement and damage updates in
{doc}`Lecture 1 <01_fracture_and_phast>`, we ask how a chosen observation changes
with a material or geometry parameter. The lecture uses elementary chain-rule
calculations before connecting them to fracture applications.

## Choose a parameter and an observation · 0–6 minutes

Let $p$ denote the chosen parameters, $y$ the observed response and $J$ a
scalar loss measuring disagreement with target observations. The forward
calculation has the sequence

$$
p \longrightarrow \text{computed states}
\longrightarrow y \longrightarrow J.
$$

For a fracture problem, observations might be sampled displacements, a
load–displacement response or a stated measure of the crack field. The
observation definition, boundary conditions and loading remain part of this
map. Recovering a parameter also depends on how much information these
observations contain.

## Follow the sensitivity backwards · 6–18 minutes

Reverse mode starts from the scalar loss and passes its sensitivity backwards
through each operation. A vector–Jacobian product (VJP) performs one such
local propagation. When a parameter is used at several updates, its
contributions add. An optimisation method then uses the accumulated gradient
to choose a parameter update.

The {ref}`existing backpropagation figure <fig-backpropagation-step-by-step>`
locates these quantities. The
{doc}`three-step worked derivation <../05a_backpropagation_step_by_step>` supplies
a small algebraic calculation that can be checked by hand.

:::{admonition} Three updates and one shared parameter
:class: note

Follow three forward updates, the observation and the loss. Trace the reverse
path through one VJP at each update and add the contributions from every use
of the shared parameter. The optimisation update uses the resulting gradient.

**Learning question:** Why can an early update contribute to the final loss
gradient?
:::

## Specify the derivative being computed · 18–28 minutes

Unrolling differentiates the sequence of operations actually executed.
Implicit differentiation uses the equation defining a converged state, under
appropriate local smoothness and nonsingularity assumptions. Fracture history,
active constraints and branch changes affect that interpretation. The
{doc}`differentiation chapter <../05_differentiation_and_inverse>` develops both
routes and their assumptions.

:::{admonition} Checking the elastic-bar sensitivity
:class: note

Use the elastic-bar teaching model to compare
an analytical sensitivity, autograd and finite differences over several
perturbation sizes. Alongside it, draw the graphs for a fixed number of
iterations and for a converged residual equation. State which graph each
derivative follows.

**Learning question:** What evidence supports the gradient of the selected
computational map?
:::

## A sequence of fracture inverse applications · 28–50 minutes

The following discussion problems extend the inverse formulation to fracture.
For each, specify the unknowns, observations and assumptions, then identify the
comparisons needed to assess a recovered parameter. The worked elastic-bar
calculation in the practical provides a small numerical example of this process.

:::{admonition} Discussion: fracture-energy recovery
:class: note

Consider an unknown scalar $G_c$, a fixed specimen and prescribed loading.
Choose an observation and define a mismatch loss. Explain how you would compare
the target, initial prediction and fitted prediction using common scales,
then assess the parameter trajectory and derivative accuracy.

**Learning question:** Which feature of the response provides information
about $G_c$?
:::

:::{admonition} Discussion: one inclusion
:class: note

Extend the parameter description to one inclusion. Identify which geometry
or material quantities are unknown and explain how its presence could affect
an observed displacement or crack field. Specify a suitable comparison of
target, initial and fitted configurations using common scales.

**Learning question:** Can the chosen observations distinguish the inclusion
parameters being recovered?
:::

:::{admonition} Discussion: several inclusions
:class: note

Extend the single-inclusion description to several inclusions. Discuss how
parameter correlation, initialisation and observations held out from fitting
affect the interpretation of a recovery. Distinguish fitting the measured
fields from uniquely identifying the underlying parameters.

**Learning question:** How does adding unknowns change the observations needed
for recovery?
:::

:::{admonition} Discussion: an unknown load
:class: note

Consider recovering the magnitude of an applied load from displacement
observations while the material properties are known. Define the
parameter–state–observation–loss sequence. Then discuss what changes if both
the load and elastic modulus are unknown.

**Learning question:** Which parts of the inverse workflow transfer to a new
physical problem?
:::

## Connect the examples to the practical · 50–55 minutes

In {doc}`../classroom/02_gradients_and_recovery`, begin with a damaged bar's
force and scalar mismatch loss. Predict the sensitivity signs, calculate the
chain rule, then compare PyTorch's backward pass with analytic derivatives
and finite differences. Next inspect a degradation-law derivative and recover
a modulus in a one-dimensional elastic bar. These teaching models make the
derivative and recovery steps easy to inspect.
The fracture discussion problems extend these scientific questions to coupled
damage evolution. Assessing each recovery requires observations and derivative
checks appropriate to its particular model.

The same chain rule also computes gradients of neural-model weights.
{doc}`Lecture 3 <03_hybrid_learning>` uses that connection to introduce training
and two different roles for a learned component in a numerical workflow.
