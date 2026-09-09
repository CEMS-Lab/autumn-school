# Fracture mechanics and differentiable solvers

These notes address the three lecture questions. The mathematics is largely
framework-independent. The course computations use PhAST/PyTorch. The JAX
discussion explains corresponding implementation concepts and API contracts.

## 1. Energy, explicit mechanics and implicit damage

For small-strain brittle fracture, let \(d=0\) denote intact material and
\(d=1\) fully damaged material. One representative energy is

\[
\mathcal E(u,d)=\int_\Omega
\left[
g(d)\psi_0^+(\varepsilon(u))+\psi_0^-(\varepsilon(u))
+\frac{G_c}{c_w}\left(\frac{w(d)}{\ell}
+\ell|\nabla d|^2\right)
\right]\,{\rm d}V,
\qquad
c_w=4\int_0^1\sqrt{w(s)}\,{\rm d}s .
\]

Here \(G_c\) sets the fracture-energy scale, \(\ell\) regularises the crack
surface, \(w\) controls crack density, and \(g\) degrades selected elastic
energy. Stress and damage driving force must follow the same stated energy.
The tension/compression split is part of this representative model. The quick
PhAST notebook selects isotropic degradation in its effective configuration.
[Miehe, Welschinger and Hofacker (2010)](https://doi.org/10.1002/nme.2861).

At fixed displacement, a rate-independent damage update may be posed as

\[
d_{n+1}\in\arg\min_{d_n\leq d\leq1}\mathcal E(u_{n+1},d).
\]

The constrained first-order condition is a variational inequality. Active
constraints contribute multipliers to the stationarity equation. Replacing
current tensile energy with a history field introduces a modelling or
algorithmic approximation whose relation to the constrained problem requires
separate analysis.

### A partitioned time step

With lumped mass \(M_L\), an illustrative explicit mechanics update is

\[
a_n=M_L^{-1}\!\left[f_n^{\rm ext}-f^{\rm int}(u_n,d_n)\right],
\quad
v_{n+\frac12}=v_{n-\frac12}+\Delta t\,a_n,
\quad
u_{n+1}=u_n+\Delta t\,v_{n+\frac12}.
\]

Then solve the constrained damage problem at fixed \(u_{n+1}\). Mass
inversion is diagonal and mechanics uses accepted, lagged damage. This
partitioned update differs from a quasistatic alternating solve. Any added
coupling corrector must reference the same accepted time level throughout
its nonlinear iterations.
[Borden et al. (2012)](https://doi.org/10.1016/j.cma.2012.01.008).

For fixed linear undamped mechanics, central difference has the familiar
limit \(\Delta t\leq2/\omega_{\max}\). For coupled nonlinear fracture,
assess timestep refinement, convergence,
irreversibility and kinetic + elastic + fracture energy against external
work and any specified additional dissipation. Continuum thermodynamic
consistency is distinct from discrete stability and energy accuracy.

### Matrix-free implementation in JAX

Gather element degrees of freedom, evaluate strains/damage at quadrature
points, integrate and accumulate nodal contributions. Evaluate a tangent
action \(v\mapsto R_zv\) and transpose action \(q\mapsto R_z^Tq\) directly
through local operations. Matrix-free describes this operator implementation.
Time integration and thermodynamic consistency require their own choices and checks.

The conceptual JAX ingredients are pure state/parameter functions, batched
element operations, gather/scatter, jax.jvp / jax.vjp and a fixed-length
jax.lax.scan rollout. Define the whole state, including relevant history,
and preserve its shapes and dtypes across steps.
[Official scan documentation](https://docs.jax.dev/en/latest/_autosummary/jax.lax.scan.html).

For a linear damage subproblem, jax.lax.custom_linear_solve supports
matrix-free actions and implicit gradients. Its contract assumes the supplied
solver actually satisfies the equation; verify that invariant in the calling
code. Nonsymmetric operators require a transpose solve.
[Official linear-solve documentation](https://docs.jax.dev/en/latest/_autosummary/jax.lax.custom_linear_solve.html).

A nonlinear/constrained damage problem needs its appropriate
free-variable/active-branch residual and tangent solve. JAX
[custom_root](https://docs.jax.dev/en/latest/_autosummary/jax.lax.custom_root.html)
and [custom_vjp](https://docs.jax.dev/en/latest/_autosummary/jax.custom_vjp.html)
provide mechanisms for defining these derivatives. Scientific assessment
requires checks of the chosen model and numerical solution. Select the
derivative primitive according to the actual linear, nonlinear or constrained
problem being solved.

## 2. Degradation, convergence and crack-event sensitivities

Convergence and crack-event sensitivities depend on the coupled formulation,
its solution branch and the numerical algorithm. A transparent teaching baseline is

\[
g(d)=(1-\eta_{\rm res})(1-d)^2+\eta_{\rm res},\quad
g'(d)=-2(1-\eta_{\rm res})(1-d),\quad
g''(d)=2(1-\eta_{\rm res}),
\]

with \(0<\eta_{\rm res}\ll1\). Residual stiffness helps avoid a fully singular
damaged stiffness but also changes the response and needs a sensitivity check.

| Model | Crack density \(w(d)\) | \(c_w\) here | Distinction |
| --- | --- | --- | --- |
| Standard AT1 | \(d\) | \(8/3\) | A homogeneous elastic threshold under its stated assumptions. |
| Standard AT2 | \(d^2\) | \(2\) | Homogeneous damage may begin at arbitrarily small positive loading; localisation is separate. |
| Cohesive phase field | Calibrated model-specific choice | Model-specific | Strength and softening require a consistent calibrated formulation. |

AT1 and AT2 commonly share quadratic degradation \(g\); their crack-density
laws distinguish the models. Higher-order/rational alternatives can change
strength, softening, conditioning and sensitivity. Compare the complete model,
including the smoothness of its constitutive functions.
[Vicentini et al. (2024)](https://link.springer.com/article/10.1007/s10704-024-00763-w);
[Geelen et al. (2019)](https://arxiv.org/abs/1809.09691).

For fixed nonnegative driving field \(H\), unconstrained quadratic AT2 gives

\[
\left[2(1-\eta_{\rm res})H+\frac{G_c}{\ell}\right]d
-G_c\ell\,\Delta d=2(1-\eta_{\rm res})H.
\]

The positive reaction term and gradient stiffness give an instructive linear
subproblem for positive \(G_c,\ell\). Bounds still require constrained
treatment, and the coupled energy can be nonconvex. A staggered solution
requires convergence criteria, appropriate preconditioning and globalisation,
bounded increments and explicit failure handling.

### A derivative belongs to a specified solution branch

For a fixed smooth branch,

\[
R(z^\star,p)=0,\qquad
R_z\,\frac{{\rm d}z^\star}{{\rm d}p}=-R_p.
\]

For scalar \(J(z^\star,p)\), solve

\[
R_z^T\lambda=J_z^T,\qquad
\frac{{\rm d}J}{{\rm d}p}=J_p-\lambda^T R_p .
\]

This implicit-function argument requires a suitable nonsingular linearisation
and consistent history/previous-state dependence. Changing active sets, hard
maxima, clamps, spectral switches and crack-path bifurcations can produce
kinks or ill-conditioned sensitivities. The solution map can be nonsmooth
even with smooth constitutive degradation.

Distinguish stable-branch derivatives, smooth-forward regularisation that
changes the model, and hard-forward/smooth-backward surrogate derivatives.
A surrogate backward rule defines a chosen approximation to the derivative
of the hard forward operation. Report directional AD/finite-difference checks with perturbation
size, solve tolerances and branch status. A cross-event finite difference
may probe another branch. Each check assesses the stated parameter, direction
and solution branch.

## 3. Radius-GNO/GNN integration and acceleration

Define the component's role and its interface. One possible
damage-proposal interface is

\[
\widehat d_{n+1}=\mathcal G_\theta(
\text{mesh},u_{n+1},d_n,H_n,\text{material fields},\text{boundary data}).
\]

Specify node/quadrature location, feature order, units, normalisation,
graph construction, batch layout and output meaning. Changing radius
neighbourhoods with trainable geometry creates another derivative boundary.

Check bounds/irreversibility and the appropriate discrete residual or KKT
measure. Accept a qualified proposal, or use a reference corrector and
recheck before acceptance. Active inequality constraints require the
corresponding stationarity and complementarity checks. Models used as constitutive laws, state
predictors and preconditioners have different validation requirements.

### A warm start needs an appropriate objective

If model weights enter only the initial guess, the corrector converges to the
same isolated root, and the residual is independent of the model weights,

\[
R(z^\star,p)=0,\qquad R_\theta=0
\quad\Longrightarrow\quad
\frac{\partial z^\star}{\partial\theta}=0.
\]

This follows from the implicit derivative above. The exact converged-state
gradient vanishes on that branch. To train a pure warm-start predictor, use
supervised/reference targets, a proposal residual/energy
before correction, or an explicitly defined finite-iteration unrolled
objective. A model that changes the residual/constitutive law is a different
formulation requiring physical validation. Initial-guess-dependent branch
selection introduces an additional derivative boundary.

DAgger-style training collects states visited by the current model, obtains
reference labels, aggregates data, retrains and evaluates on independent
cases. Correction records supply examples for this full training and evaluation cycle.
[Ross, Gordon and Bagnell (2011)](https://proceedings.mlr.press/v15/ross11a.html).

For an acceleration claim, measure at matched quality

\[
T_{\rm hybrid}=T_{\rm mechanics}+T_{\rm graph}
+T_{\rm prediction}+T_{\rm checks}+T_{\rm correction}.
\]

Include model/graph overhead and fallback frequency. Compare end-to-end
runtime at matched field quality and account for the work in each stage.

## Connection to the practicals

P1 uses actual public quasistatic PhAST. P2 checks a local public degradation
law and a bar inverse toy. P3 trains/assesses MLP/RBF models on a toy field
equation. The new animations explain the general concepts with explicit
analytic/schematic captions. Use the displayed equations and contracts to
connect the small exercises to questions of coupled fracture sensitivity,
model compatibility and complete computational cost.
