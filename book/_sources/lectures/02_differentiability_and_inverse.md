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

:::{admonition} Animation storyboard · L2-A01
:class: note

**Planned content.** Reveal three forward updates, the observation and the
loss. Reverse the highlighting to follow one VJP at each update and collect
every use of the shared parameter. Show the optimisation update last.

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

:::{admonition} Worked example outline · L2-W01
:class: note

**Planned content.** Use the existing elastic-bar teaching model to compare
an analytical sensitivity, autograd and finite differences over several
perturbation sizes. Alongside it, draw the graphs for a fixed number of
iterations and for a converged residual equation. State which graph each
derivative follows.

**Learning question:** What evidence supports the gradient of the selected
computational map?
:::

## A sequence of fracture inverse applications · 28–50 minutes

The four outlines below reserve a connected progression of applications.
Each asks what is unknown, what is measured and what would support a recovery
claim. They are planned exhibits; numerical results will accompany them when
the corresponding examples have been selected and reviewed.

:::{admonition} Research example outline · L2-R01 · Fracture-energy recovery
:class: note

**Planned content.** Begin with a scalar $G_c$, a fixed specimen and prescribed
loading. Place the target observation, initial prediction and recovered
prediction in a common comparison, followed by the parameter trajectory and
a derivative check.

**Learning question:** Which feature of the response provides information
about $G_c$?
:::

:::{admonition} Research example outline · L2-R02 · Single-particle recovery
:class: note

**Planned content.** Extend the parameter description to one inclusion.
Identify which geometry or material quantities are unknown and show how its
presence affects the observed displacement or crack field. Reserve adjacent
panels for target, initial and recovered configurations using common scales.

**Learning question:** Can the chosen observations distinguish the inclusion
parameters being recovered?
:::

:::{admonition} Research example outline · L2-R03 · Multiple-particle recovery
:class: note

**Planned content.** Extend the single-particle setup to several inclusions.
Compare geometry and observed fields, then examine parameter correlation,
initialisation and observations held out from fitting. Panel positions are
textual outlines at this stage.

**Learning question:** How does adding unknowns change the observations needed
for recovery?
:::

:::{admonition} Research example outline · L2-R04 · A non-particle application
:class: note

**Planned content.** A further inverse problem will connect the same
parameter–state–observation–loss sequence to a different physical setting.
The application is awaiting selection; its parameters, observations and
result panels will be defined together.

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
The fracture exhibits above extend the scientific questions to coupled
damage evolution and require their own evidence.

The same chain rule also computes gradients of neural-model weights.
{doc}`Lecture 3 <03_hybrid_learning>` uses that connection to introduce training
and two different roles for a learned component in a numerical workflow.
