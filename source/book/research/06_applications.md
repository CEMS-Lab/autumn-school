# Designing a fracture-inverse research programme

Start with the [visual laboratory](08_visual_lab.md) to connect particle
geometry, a loss surface and recorded crack fields. Its animations distinguish
physical time from inverse updates before we generalize to multiple particles.

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

### Why additional particles make recovery harder

There is no special mathematical failure at the third particle. Each additional
circle introduces three unknowns, while the measured crack can remain sensitive
to only a few combinations of them. Moving a centre and changing its radius can
produce similar deflections. A particle away from the observed crack can have
little influence on the measured data. The elasticity problem still couples
the entire plate, so distance from the crack is only a heuristic for influence.

Let $\theta=(c_{x,1},c_{y,1},r_1,\ldots,c_{x,3},c_{y,3},r_3)$ and let
$g(\theta)=\mathcal O(F(\theta))$ denote the simulated observations. Locally,

$$
g(\theta+\Delta\theta)\approx g(\theta)+J\Delta\theta,
\qquad J=\frac{\partial g}{\partial\theta}.
$$

Small singular values of a consistently scaled $J$ identify combinations that
change the observations weakly. Similar columns indicate parameter trade-offs.
Report the singular values as well as their ratio: a moderate condition number
can accompany uniformly small sensitivities. The interpretation depends on
parameter units, observation weights and measurement noise. Numerical full
rank alone does not establish reliable recovery.

Optimization introduces another difficulty. Early errors change the later crack
trajectory and the recorded loading history. An observation window intended to
identify the third particle can then contain errors caused by the first two.
Simultaneous updates must resolve these coupled effects. Strict sequential
updates carry earlier estimation errors forward. Independent-window estimates
can disagree because each window constrains different combinations.

For example, a fusion rule can take the form

$$
\bar\theta_i=\frac{\sum_k w_{ik}\theta_i^{(k)}}{\sum_k w_{ik}}.
$$

If all weights for one particle are multiplied by the same positive constant,
its fused estimate is unchanged. Thus small absolute weights alone do not
explain failure of this normalized rule. Relative weights, biased window
estimates and nonlinear parameter coupling matter. The average of two
geometries that fit separate windows need not fit either window when replayed.
Accumulated loss-gradient magnitude is also different from a noise-calibrated
information matrix.

Use these observations to separate three questions: does the forward solve
converge; does its derivative match its implemented objective locally; and do
the observations constrain the geometry well enough to recover it? Each needs
its own evidence.

### A sequential algorithm with cumulative correction

A practical extension temporarily fixes parameter blocks, then revisits them
as more observations arrive. All particles remain in the physical model.
The following is a proposed research schedule, rather than a claim of an
already validated fracture algorithm.

```text
Inputs: initial geometry, physical initial state, fixed observation windows,
        bounds, objective weights, derivative checks and iteration budgets.
For stage k = 1, 2, 3:
    Form the unique union of fitting frames through window k.
    Check the local derivative of this stage's objective.
    Update particle k briefly with the other parameter blocks fixed.
    Update particles 1 through k jointly against the accumulated frames.
    For every trial, replay the full forward model from its physical start.
    Record accepted updates, rejected trials and all forward/backward work.
Assess the final geometry on observations excluded from fitting.
```

Shared frames enter the cumulative objective once with their declared weights.
The optimizer uses observed misfit, step criteria and a fixed maximum budget;
synthetic true-position errors are evaluated afterwards. A bounded comparison
can allocate five accepted updates to the current block and ten to cumulative
correction at each stage, giving at most 45 updates. This is a testable budget,
not an established optimum. Reset or resize optimizer curvature information
when the active parameter block changes.

The cumulative step gives later evidence an opportunity to correct earlier
estimates. It can help with error propagation, but additional windows cannot
recover a parameter direction to which all of those observations are
insensitive. Compare this schedule with A-D using the same physical model,
initialization, fitting data and accounting of forward work.

### What does freezing a state mean?

Temporarily holding a centre or radius fixed keeps a valid forward calculation
for that trial geometry. Prescribing the earlier crack field instead changes
the inverse problem into a conditional one. A damage image is only part of the
state: displacement, velocity in a dynamic model, history variables and other
internal variables also determine subsequent evolution.

Write a checkpoint as $s_k(\theta)$ and the next evolution as
$s_{k+1}=F_k(s_k(\theta),\theta)$. Its derivative contains two terms:

$$
\frac{d s_{k+1}}{d\theta}
=\frac{\partial F_k}{\partial\theta}
+\frac{\partial F_k}{\partial s_k}\frac{d s_k}{d\theta}.
$$

Detaching a parameter-dependent checkpoint discards the second term. Even a
particle encountered later by the crack can affect earlier elastic fields.
Reuse checkpoints when their dependencies are unchanged, or define and test
the approximation explicitly. A frozen-state calculation can propose an
update; a full replay then checks its actual objective and trajectory.

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

### From a recovered geometry to uncertainty intervals

Begin with a small known-count problem and write an observation model,

$$
y=g(\theta)+b+\varepsilon,\qquad
\varepsilon\sim\mathcal N(0,\Sigma).
$$

Here $y$ contains the measured quantities, $g$ includes registration and the
observation operator, $b$ represents model or discretization discrepancy, and
$\Sigma$ describes measurement error. For a first controlled synthetic test,
one can explicitly assume $b=0$ and generate noise with a known covariance.
That assumption must accompany the resulting uncertainty intervals. In an
experiment, estimate noise and address discrepancy using calibration data or
a stated statistical model. Optimization weights alone do not supply this
calibration.

Bayes' rule combines the likelihood with a physical prior:

$$
p(\theta\mid y)\propto p(y\mid\theta)\,p(\theta).
$$

Priors can encode admissible radii, non-overlap and independently known volume
fraction. A local Gaussian approximation near a recovered mode has covariance

$$
C\approx\left(J^T\Sigma^{-1}J+\Lambda_{\rm prior}\right)^{-1},
$$

where $\Lambda_{\rm prior}$ is the local curvature of the negative log prior.
This Gauss-Newton approximation describes one locally smooth basin. It needs
care near active bounds, switching trajectories, significant residuals or
multiple modes. Strong intervals created mainly by a strong prior should be
identified as such. The linear exercise in this notebook illustrates the
algebra; fracture posterior sampling is a separate computational study.

A sequential probabilistic update carries the uncertainty of earlier particles
forward. Setting their variances to zero because they were optimized earlier
overstates certainty. Each new datum enters a sequential update once, with a
conditional likelihood that respects correlations. Repeated cumulative
optimization is useful for finding a mode, but is not itself posterior sampling.
Likewise, the spread of optimizer endpoints from different starts is not a
calibrated posterior distribution.

### What can one crack tell us about an RVE?

Consider two microstructures that differ mainly away from the observed crack.
If their measured trajectories are indistinguishable at the noise level, the
data cannot choose between them. A useful output is therefore an ensemble of
compatible microstructures with spatial uncertainty, rather than a uniquely
asserted reconstruction of every particle.

Build this programme in stages:

1. Verify a known-count geometry with a declared likelihood, prior and local
   derivative diagnostics at an accepted recovery.
2. Check alternate modes and predictive fields using the actual likelihood.
   Keep particle labels identifiable or use permutation-invariant summaries.
3. Add displacement, reaction or other measurements that constrain weak
   directions; evaluate unused observations for predictive performance.
4. Extend to unknown count or random fields with explicit priors on spatial
   statistics, and report which statistics are informed by the data.
5. Check representative volume size and variability of homogenized responses
   before calling the inferred specimen an RVE.

Independent fracture experiments often require fresh specimens. Combining
them can identify shared material or microstructure-distribution parameters;
it does not mean that every specimen has the same particle arrangement.
Sampling, surrogate construction and validation costs belong in the research
budget. A gradient surrogate used for optimization also needs separate
justification before it is used inside an exact posterior sampler.

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
