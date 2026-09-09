# Fracture energy: AT1, AT2, degradation, and width

:::{figure} figures/02_energy_profiles.png
:name: fig-energy-profiles
:width: 96%

The crack-density choice and the degradation law are separate functions. The
curves shown are mathematical profiles, not measured material data.
:::

## A common energy template

For small-strain brittle fracture, a frequently used phase-field energy is

$$
\mathcal{E}_\ell(u,d)
= \int_\Omega \left[
g_\eta(d)\,\psi^+(\varepsilon(u))
+\psi^-(\varepsilon(u))
+\frac{G_c}{c_0}\left(
\frac{w(d)}{\ell}+\ell|\nabla d|^2
\right)\right]\mathrm{d}x
-\mathcal{W}_{\mathrm{ext}}(u).
$$

The ingredients have different jobs:

- $\psi^+$ is the part of elastic energy selected to drive fracture, often a
  tensile contribution;
- $\psi^-$ is retained rather than degraded in a tension--compression split;
- $g_\eta(d)$ reduces tensile stiffness as damage grows;
- $G_c$ sets the energy scale of fracture;
- $w(d)$ selects a crack-density family; and
- $\ell$ controls the regularised width of the damage band.

This notation does not identify a unique model. Different spectral,
volumetric--deviatoric, or other decompositions define $\psi^+$ and $\psi^-$
differently. State the split before interpreting compression, crack closure,
or mixed-mode behaviour.

## The damage convention and degradation derivative

This book uses $d=0$ for intact material and $d=1$ for fully broken material.
A standard residual-stiffness degradation law is

$$
g_\eta(d) = (1-\eta_{\mathrm{res}})(1-d)^2+\eta_{\mathrm{res}},
\qquad 0<\eta_{\mathrm{res}}\ll1.
$$

It satisfies $g_\eta(0)=1$ and $g_\eta(1)=\eta_{\mathrm{res}}$. The residual
term helps prevent the elastic operator from becoming singular in a damaged
zone. It should be reported because it affects the numerical problem and the
post-peak response.

For a hand calculation or a tensor implementation, differentiate explicitly:

$$
g_\eta'(d)=-2(1-\eta_{\mathrm{res}})(1-d),
\qquad
g_\eta''(d)=2(1-\eta_{\mathrm{res}}).
$$

The negative first derivative is meaningful: increasing $d$ lowers the
degraded tensile energy. It does *not* mean that damage is free to grow
everywhere, because fracture density, gradients, boundary data, and
irreversibility all enter the total variation.

## Computational lesson: inspect a degradation derivative

Continue directly to the lesson below. Predict the sign of $g_\eta'(d)$ at an
interior damage value, then compare the analytic derivative with automatic
differentiation and a central finite difference. The code calls the pinned
public PhAST material law for this *local, smooth* check. It does not
differentiate a full coupled fracture history, active constraint, or nonlinear
solve.

```{toctree}
:maxdepth: 1

labs/02_degradation_autograd
```

## AT2 and AT1 are normalised choices

The crack-density contribution is often written

$$
\Gamma_\ell(d)
=\frac{1}{c_0}\int_\Omega
\left(\frac{w(d)}{\ell}+\ell|\nabla d|^2\right)\mathrm{d}x,
\qquad
c_0=4\int_0^1\sqrt{w(s)}\,\mathrm{d}s.
$$

With this convention:

$$
\begin{aligned}
\text{AT2:}\quad & w(d)=d^2,\qquad c_0=2,\\
\text{AT1:}\quad & w(d)=d,\qquad c_0=\frac{8}{3}.
\end{aligned}
$$

The labels AT1 and AT2 are widely used, but coefficients in papers can look
different because authors absorb factors into $G_c$, $c_0$, or the gradient
term. Compare complete functionals, not a label alone.

### Why the profiles look different

At a fully developed straight crack in an idealised one-dimensional setting,
the AT2 profile has exponential tails,

$$
d_{\mathrm{AT2}}(x)=\exp(-|x|/\ell),
$$

whereas the corresponding AT1 profile is compactly supported,

$$
d_{\mathrm{AT1}}(x)
=\left(1-\frac{|x|}{2\ell}\right)_+^2,
\qquad (a)_+=\max(a,0).
$$

These ideal profiles explain the left panel of the preceding figure. They do
not remove the need for a mesh-convergence study in a finite domain with
boundary conditions and a particular loading path.

In common one-dimensional analyses, AT1 exhibits a finite damage-initiation
threshold, whereas AT2 can begin to reduce stiffness without a strictly
elastic phase. That statement depends on the surrounding energy, loading, and
history construction. It should not be shortened to “AT1 is always delayed”
or “AT2 is always more brittle.”

## Deriving the strong-form damage residual

Hold $u$ fixed momentarily and take a virtual change $\delta d$. The
damage-dependent part of the first variation is

$$
\delta_d\mathcal{E}_\ell
=\int_\Omega\left[
g_\eta'(d)\psi^+\,\delta d
+\frac{G_c}{c_0}\left(
\frac{w'(d)}{\ell}\delta d
+2\ell\nabla d\cdot\nabla(\delta d)
\right)\right]\mathrm{d}x.
$$

Integrating the gradient term by parts gives, away from active constraints,

$$
r_d
=g_\eta'(d)\psi^+
+\frac{G_c}{c_0}\left(
\frac{w'(d)}{\ell}-2\ell\Delta d
\right)=0.
$$

A natural boundary condition for an unconstrained boundary is
$\nabla d\cdot n=0$. The equation has three visible influences:

1. $g_\eta'(d)\psi^+$ drives damage where the selected elastic energy is high;
2. $w'(d)/\ell$ penalises local damage; and
3. $-2\ell\Delta d$ penalises abrupt spatial variation.

The derivation also shows why a diffusion analogy is helpful but incomplete:
the gradient term is diffusion-like, yet the mechanical driving energy and
one-way damage history are essential.

## Irreversibility is a constraint, not a plot style

For brittle damage, a common admissible set at load step $n$ is

$$
d_n(x)\geq d_{n-1}(x), \qquad 0\leq d_n(x)\leq1.
$$

At a point where the lower bound is active, the unconstrained equation
$r_d=0$ need not hold. If only the lower bound is displayed, a local
complementarity form is

$$
r_d-\lambda=0,\qquad
\lambda\geq0,\qquad
d-d_{n-1}\geq0,\qquad
\lambda(d-d_{n-1})=0.
$$

The upper bound introduces a second multiplier. Implementations may instead
use a history field, a constrained solver, or another equivalent strategy
under stated assumptions. A colour map that happens to look monotone is not
evidence that irreversibility was imposed correctly; check the stored
constraint or history data.

## Width, mesh, and what must be checked

The parameter $\ell$ is a modelling and numerical length. It spreads the
regularised crack and therefore interacts with mesh spacing $h$, geometry, and
material calibration. A credible study reports $\ell$, the mesh, and a
convergence or sensitivity check. There is no universal element-count slogan
that replaces this check.

Changing $\ell$ can change:

- the apparent width of the damaged band;
- the peak load and softening response in a finite discretisation;
- the required mesh density and nonlinear conditioning; and
- the meaning of a comparison with an observed fracture process zone.

The phase-field regularisation should not be described as a physical crack
width unless that calibration has actually been established for the material
and model.

## Exercise: one derivative and one scale argument

1. Evaluate $g_\eta(0)$, $g_\eta(1)$, and $g_\eta'(1)$ for the law above.
2. In the damage residual, which term becomes large when $\ell$ is made small
   at fixed $d$ and $\nabla d$?
3. Why is it incomplete to infer mesh independence from an unchanged
   full-domain average of $d$?

:::{admonition} Solution
:class: dropdown

1. $g_\eta(0)=1$, $g_\eta(1)=\eta_{\mathrm{res}}$, and
   $g_\eta'(1)=0$. The derivative vanishes at the fully degraded endpoint for
   this quadratic law.
2. The local crack-density contribution $w'(d)/\ell$ scales inversely with
   $\ell$. The gradient and solution fields may also change, so this is a
   scale observation rather than a full solution argument.
3. A spatial average can remain similar while the crack band moves, changes
   width, or is under-resolved. Compare fields, energies, and observables at
   stated refinements.

In the computational lesson, the first result is a narrower check: it compares
the analytic, automatic-differentiation, and finite-difference derivatives of
the selected degradation law at one stated damage value. It is evidence about
that scalar operation, not about the entire coupled fracture route.
:::

## Sources for this chapter

The Ambrosio--Tortorelli regularisation idea underlies the AT terminology.
For phase-field fracture derivations and comparisons, see
[Miehe, Welschinger, and Hofacker (2010)](https://doi.org/10.1002/nme.2861),
[Pham et al. (2011)](https://doi.org/10.1177/1056789510386852), and the
review by [Kristensen, Niordson, and Martínez-Pañeda
(2021)](https://doi.org/10.1098/rsta.2021.0021).
