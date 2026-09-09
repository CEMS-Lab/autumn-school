# Designing a fracture-inverse research programme

## Application 1: three particles ahead of a crack

We prescribe a notched plate, three stiff circular inclusions, material
contrasts and loading. The unknowns are the three centres and radii. The
observations are selected displacement and damage fields; synthetic damage
observations and experimental displacement measurements require different
observation contracts.

The first research question is precise: does increasing a prescribed initial
offset change recovery when everything else stays fixed? Use the same target,
mesh, material parameters, fitting observations, bounds, optimiser and budgets
at both initialisations. Keep particles inside the plate and preserve the
stated upper/lower grouping relative to the initial crack.

Compare four explicitly defined schedules:

| Schedule | Variables updated | Observations used |
|---|---|---|
| A: simultaneous | All nine | All fitting windows |
| B: strict sequential | One particle at a time; earlier estimates frozen | Current window and declared shared frames |
| C: cumulative | Expand from three to six to nine variables | Accumulate fitting windows |
| D: independent-window fusion | All nine independently per window | Separate windows, followed by a declared fusion rule |

All three particles remain in the forward model, even when only one is being
updated. Removing the other particles would change the physical problem.
Fusion weights must be defined from available observations and sensitivities;
selecting a rule using the true geometry would leak the synthetic answer.

Before interpreting the comparison, inspect forward convergence, initial
sensitivities, derivative checks, accepted updates, rejected trials and final
assessment fields. Matching update budgets does not match total forward work.

## Application 2: a distributed degraded stiffness field

For a diffuse weakened region, a useful parameterisation is
$E(\mathbf x)=E_0\,f(\sum_j a_j\phi_j(\mathbf x))$, where
$\phi_j$ are spatial basis functions and $f$ enforces a declared admissible
range. The coefficients $a_j$ replace individual circle parameters.

Basis centres locate functions; they are not independent physical particles.
Increasing their number increases representational freedom and can introduce
weakly observed combinations. Evaluate field error, observable error,
regularisation sensitivity and local parameter information separately.

For a barely visible impact damage motivation, explain the modelling link:
the recovered field represents a chosen stiffness-degradation model. A
synthetic weakened region is not itself an experimental impact-damage map.

## Application 3: selecting observations

Given several available fitting frames, examine which add independent
sensitivity directions. Begin with deterministic ranking and a measurement
budget. A new load case can be more informative than another similar time
frame, but it also requires a new forward experiment.

Reinforcement learning becomes relevant when sequential choices and their
future consequences justify training a policy. It should be compared with
a simpler information-based selection rule. Fracture history belongs to the
state; a damage image alone need not determine subsequent evolution.

## Application 4: uncertainty and generative proposals

If multiple material fields explain the data, a conditional model can propose
several candidates. Each candidate can be checked by PhAST. To interpret them
as a posterior distribution, specify priors, measurement noise and the
likelihood or inference approximation, then check calibration.

Diffusion and flow matching provide possible conditional models. They require
training data and introduce inference costs. Physics guidance can improve
residuals while changing the distribution of samples. Assess both physical
consistency and distributional quality.

## Exercise: a complete experiment card

Write a card for one of the applications. Include the following:

- Unknowns, units and admissible bounds.
- Fixed model, mesh, loading and initial state.
- Fitting observations, normalisation and independent assessment.
- Optimiser and stopping rule available without the true parameters.
- Forward and derivative checks, total work and resource budget.
- Stored fields, source fingerprint and the result needed to support the claim.

:::{admonition} Worked interpretation
:class: dropdown

For the three-particle application, stopping can use objective or step
criteria and a declared budget. True centre/radius errors are post-run
assessment quantities. A passing derivative check supports a local
sensitivity; geometric recovery and predictive agreement are separate
outcomes. Preserve failures and document exactly which assumptions differ
between experiments.
:::

## Research status

The executable exercises in this extension are complete only when their
retained HPC checks pass. Full fracture comparisons, GNN training,
distributional inference and learned experiment design have separate issue
cards. A chapter explaining a proposed method does not mark that research
as completed.
