# Train, save, reload, adapters, and checked proposals

:::{figure} figures/06_learning_cycle.*
:name: fig-learning-cycle
:width: 96%
:alt: Offline reference data support training and checkpoint reload. Online model proposals are checked, then accepted or corrected by the reference solver. A dashed conceptual feedback path collects labelled states for another training round.

A learning component is useful only when its inputs, outputs, and physics
checks are stated as clearly as those of the reference calculation.
:::

## Decide what is being learned

The phrase “use machine learning for fracture” hides several different tasks.
Name the role precisely.

- **Surrogate:** approximate a map from stated inputs to a stated output.
- **Proposal model:** supply an initial damage field, displacement field, or
  parameter guess to a mechanics calculation.
- **Adapter:** convert one data representation to another, such as a mesh
  ordering or normalised tensor layout.
- **Corrector:** update a proposal using a residual, an iterative solve, or a
  trusted reference computation.
- **Emulator for an observable:** approximate a scalar response while not
  necessarily reproducing a full field.

These roles can be combined, but a label should not claim more than the
interface actually supports. A model that predicts a useful initialisation is
not automatically a replacement for a fracture solver.

## A small supervised-learning contract

Let $x_i$ be an input representation and $z_i$ a reference target. A simple
training objective is

$$
\mathcal{L}(\theta)
=\frac{1}{N}\sum_{i=1}^N
\left\|f_\theta(x_i)-z_i\right\|_2^2.
$$

Before training, write down:

1. what each channel of $x_i$ means, including coordinates, parameters,
   fields, and units;
2. what target $z_i$ means and at which load step or time it is sampled;
3. how meshes, nodes, or quadrature points are ordered;
4. the training, validation, and test split rule; and
5. the metric and physical diagnostic reported on each split.

Normalisation belongs to this contract. If an input component is transformed
as $\tilde x=(x-\mu)/s$, save $\mu$ and $s$ with the model. A reloaded model
without its preprocessing state is a different computational map.

## Where does the training gradient travel?

Distinguish three computational graphs before choosing a learning method.

**Supervised fitting** compares a prediction with stored targets:

$$
\mathcal L_{\mathrm{sup}}=\|f_\theta(x)-z_{\mathrm{ref}}\|^2.
$$

A solver may have generated the targets offline. Its derivatives are not
needed for this training graph.

**Residual-based training** evaluates a stated equation at the prediction:

$$
\mathcal L_{\mathrm{res}}=\|R(f_\theta(x);p)\|^2.
$$

The gradient passes through the residual evaluation. This does not necessarily
differentiate a converged solve. Boundary conditions and branch selection still
matter, as the opening algebraic teaser illustrates.

**Solver-in-the-loop training** evaluates the consequences of a prediction:

$$
z_0=f_\theta(x),\qquad z_{n+1}=S(z_n,p),\qquad
\mathcal L=\|Cz_N-y_*\|^2.
$$

Here $C$ extracts the observed quantity. With fixed $p$ and a loss depending
only on $z_N$, reverse propagation gives

$$
\bar z_N=2C^T(Cz_N-y_*),\qquad
\bar z_n=\left(\frac{\partial S}{\partial z_n}\right)^T\bar z_{n+1},
\qquad
\nabla_\theta\mathcal L=
\left(\frac{\partial f_\theta}{\partial\theta}\right)^T\bar z_0.
$$

These are vector–Jacobian products; the full Jacobians need not be stored.
An implicit adjoint may replace differentiation through every solver iteration.
The [differentiable-physics introduction](https://physicsbaseddeeplearning.org/diffphys.html)
develops this operator viewpoint. For fracture, history updates, active
constraints, stopping tolerances and any detached arrays require explicit
derivative conventions and checks.

The following notebooks demonstrate supervised training and checked proposals
on a toy field problem. They do not yet implement end-to-end training through
the PhAST fracture solver.

## Train, save, and reload reproducibly

A minimal saved model package should include:

- model weights and architecture configuration;
- input and target normalisation parameters;
- feature/channel names and tensor-shape convention;
- training data identifier and split definition;
- software/library version and numerical precision; and
- a small reload test that compares a saved prediction against the
  in-memory prediction for the same declared input.

## Computational lesson: train, save, reload, and compare a toy field model

The lesson below makes the saved state visible: feature order, normalisation,
mesh signature, data split, checkpoint metadata, and a reload comparison all
appear beside the code and field plots. Begin by predicting which information
must survive serialization for a newly created model object to reproduce the
same output. The lesson uses an original `ToyHelmholtzProblem`, not PhAST
fracture data or a trained fracture-damage model. It is an interface test, not
evidence of a general fracture accelerator.

```{toctree}
:maxdepth: 1

labs/04_train_save_reload_adapter
```

:::{admonition} Reload test
:class: tip

Choose one fixed input record. Run the model before saving, reload into a new
model object, run the same record, and compare the output after applying the
same preprocessing. If the values differ, inspect normalisation, device/dtype,
model mode, feature order, and serialised configuration before training
again.
:::

## What an adapter can and cannot repair

An adapter is a stated map between representations,

$$
a:\mathcal{X}_{\mathrm{source}}
\longrightarrow\mathcal{X}_{\mathrm{target}}.
$$

For example, it may reorder nodes, concatenate a coordinate channel, project
a cell-centred value to nodes, or convert units. These operations can be
necessary and useful. They cannot manufacture missing information or correct
a target whose physical meaning differs from the source.

Ask four questions before accepting an adapter:

- Does it preserve the geometry and coordinate frame?
- Does it preserve the field meaning, units, and load/time index?
- Does it preserve or deliberately change interpolation order?
- Is there a small round-trip or reference example that checks the mapping?

The word “adapter” should not conceal a change from one mesh, material
parameterisation, or loading regime to another. That is a transfer assumption
which needs its own evaluation.

## From a proposal to a checked hybrid calculation

Suppose a learned model proposes $\widehat d$ for a damage field. A
conservative hybrid workflow is

$$
\text{input}\longrightarrow \widehat d
\longrightarrow \text{bounds/residual checks}
\longrightarrow \text{mechanics correction or fallback}
\longrightarrow \text{reported output}.
$$

The checks might include damage bounds, irreversibility relative to the prior
state, a mechanics residual, and a comparison to a reference solve on a
predefined evaluation set. If a correction is used, report the cost and result
of the full route, including prediction, conversion, checks, correction, and
any fallback. Bypassing a solver stage is not automatically a wall-time
improvement.

## Computational lesson: accept a compatible proposal or fall back

The next lesson reuses the toy field-model contract to test a compatible
proposal, reject a deliberately corrupted proposal by a stated residual gate,
and fall back to the reference field. Read the compatibility and residual
checks before treating the four field panels as evidence. The residual belongs
to the course-owned `ToyHelmholtzProblem`; it is not a PhAST AT2 fracture
residual. This is a teaching pattern for auditing a proposal, not a claim that
a learned field is an admissible fracture solution in general.

```{toctree}
:maxdepth: 1

labs/05_hybrid_reference_correction
```

## DAgger-style data aggregation

Distribution shift can appear when a learned proposal visits states absent
from its original training records. Dataset Aggregation (often called DAgger)
is one way to describe an iterative collection loop:

1. train a policy or proposal model on an initial reference dataset;
2. let the current model visit stated inputs or intermediate states;
3. query a trusted reference procedure for targets at those visited states;
4. add the labelled records to the aggregate dataset; and
5. retrain while retaining an evaluation set that was not relabelled for
   selection.

This idea is useful when the model's own trajectory changes the data it sees.
It does not remove the need for a trusted labelling procedure, provenance, or
a distinction between training data and final evaluation data. In mechanics,
the reference procedure may itself fail or be inappropriate outside its
assumptions; record that outcome rather than silently dropping difficult
cases.

## Evaluation: fields, quantities, and failure modes

Field error, reaction error, and residual are related but not interchangeable.
For a candidate $\widehat d$ and reference $d$, possible diagnostics include

$$
e_d=\frac{\|\widehat d-d\|_2}{\max(\|d\|_2,\epsilon)}
$$

alongside a damage-bound check and a mechanics residual after the candidate is
used in the stated equation. A good evaluation card reports:

- the split and cases evaluated;
- the field metric and its weighting;
- at least one mechanics-relevant quantity;
- the frequency and criterion of correction/fallback, if applicable; and
- failures, out-of-distribution cases, or unresolved cases.

A low average field error may coexist with a wrong local crack path. A good
reaction curve may coexist with a poor spatial field. Inspect both.

## Exercise: identify the missing provenance

A colleague shares a file called “best_model” and says it predicts damage on a
new mesh. List four items you need before interpreting the output as a
mechanics field.

:::{admonition} Solution
:class: dropdown

Any four of the following are essential: the architecture and weights; input
feature definitions and ordering; normalisation state; source and target mesh
representation; coordinate frame and units; load/time step represented; the
training/validation/test split; a reload comparison; and the physical checks
used on the proposed field. Without these, even a numerically well-formed
tensor has unclear mechanical meaning. The two computational lessons provide
a concrete version of this answer: the first records the model contract and
reload check; the second refuses an incompatible feature order and performs a
stated residual/fallback check.
:::

## Sources for this chapter

The notebook practices draw on standard reproducible machine-learning ideas:
separate evaluation data, explicit preprocessing, and persistent model state.
For a practical notebook pattern with open exercises and solutions, see the
[Inria scikit-learn MOOC](https://inria.github.io/scikit-learn-mooc/). For the
tensor/autodiff ecosystem used in the companion activities, see the
[PyTorch documentation](https://docs.pytorch.org/docs/stable/index.html).
