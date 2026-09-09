# Differentiation and an illustrative inverse problem

The {doc}`animated history lesson <research/03_history_visual>` follows the
history variable through loading and unloading and connects the forward
trajectory to its derivative route.

:::{figure} figures/05_autograd_inverse.*
:name: fig-autograd-inverse
:width: 96%
:alt: Parameters enter a supported forward computation and a scalar loss. Reverse sensitivities return a gradient, checked against a directional finite difference. An optional optimizer uses that gradient in a separate parameter update.

Automatic differentiation follows the stated computational graph. A derivative
check asks whether that graph implements the derivative you intended.
:::

## Define the forward map before differentiating it

Let $p$ denote one scalar parameter, such as a bounded multiplier of a
material field. A forward computation maps it to a state and an observable:

$$
p \longmapsto (u(p),d(p)) \longmapsto y(p).
$$

With a target observation $y^\star$, an illustrative least-squares objective
is

$$
J(p)=\frac12\|y(p)-y^\star\|_2^2.
$$

This objective introduces the chain rule, tensor shapes, and optimisation
bookkeeping. Parameter identifiability depends on the observations, loading
conditions, and chosen parameterisation.

Before calling a gradient routine, write down:

- the parameter and its units or nondimensionalisation;
- the geometry, loads, and boundary conditions held fixed;
- the observable $y$ and the target $y^\star$;
- every operation from $p$ to $J$; and
- what happens when a nonlinear solver fails, reaches a tolerance, clips a
  field, or changes its iteration count.

These choices define the mathematical map being differentiated.

## Three ways to obtain a sensitivity

### Finite differences

A directional central difference uses a chosen direction $q$ and step $h$:

$$
D_hJ(p;q)
=\frac{J(p+hq)-J(p-hq)}{2h}.
$$

It is simple and independent of the autodiff implementation, which makes it
valuable as a check. It also has a step-size trade-off: a large $h$ includes
nonlinear curvature, while a very small $h$ can suffer cancellation and solver
tolerance effects.

### Unrolled automatic differentiation

If a program executes a fixed differentiable sequence of operations, reverse
mode can differentiate the sequence actually run. For example, unrolling $K$
iterations gives

$$
x_0 \rightarrow x_1 \rightarrow \cdots \rightarrow x_K \rightarrow J.
$$

The derivative is of that truncated algorithm. If $K$ changes by parameter
value or a non-differentiable branch is taken, the interpretation must mention
it. Memory cost can also increase when many states are retained for a reverse
pass.

### Implicit differentiation

Suppose a converged state is defined by a residual

$$
R(x,p)=0.
$$

Under appropriate differentiability and nonsingularity assumptions,

$$
\frac{\mathrm{d}x}{\mathrm{d}p}
=-\left(\frac{\partial R}{\partial x}\right)^{-1}
\frac{\partial R}{\partial p}.
$$

In practice, an adjoint formulation often avoids forming this inverse
explicitly. This method differentiates a local equation for a converged state.
Differentiating the iterations gives the derivative of the executed
algorithm. Inequality constraints,
active-set changes, damage irreversibility, and non-smooth constitutive
choices require particular care.

## Follow the gradient one update at a time

The worked section below expands the chain rule into local derivatives,
backward-propagated sensitivities and the sum of all uses of a shared
parameter. Work through the three scalar updates before interpreting an
autograd call as a derivative of a fracture calculation.

```{toctree}
:maxdepth: 1

05a_backpropagation_step_by_step
```

## A bounded parameterisation

An unconstrained update can turn a positive material multiplier negative. One
simple way to enforce a scalar interval is to optimise an unconstrained
variable $\theta$ and map it to

$$
p(\theta)
=p_{\min}+(p_{\max}-p_{\min})\,s(\theta),
\qquad
s(\theta)=\frac{1}{1+\exp(-\theta)}.
$$

The chain rule gives

$$
\frac{\mathrm{d}J}{\mathrm{d}\theta}
=\frac{\mathrm{d}J}{\mathrm{d}p}
(p_{\max}-p_{\min})s(\theta)(1-s(\theta)).
$$

This construction enforces bounds but introduces saturation near the limits:
the sigmoid derivative becomes small. The choice of transform therefore
affects the conditioning of the optimisation problem.

## A minimal inverse experiment

For a first experiment, choose one parameter, one geometry, one loading
protocol, and one stated observable. For example:

1. define a reference parameter $p_{\mathrm{ref}}$ within a known interval;
2. compute a synthetic observation $y^\star=y(p_{\mathrm{ref}})$ using a
   documented forward map;
3. start from a different $\theta$ and map it to $p(\theta)$;
4. compute $J(\theta)$ and a gradient;
5. take a bounded update; and
6. report the parameter trajectory, loss, observable mismatch, and a
   derivative check.

This controlled recovery uses synthetic observations from the same forward
model and specified noise assumptions. Experimental recovery additionally
requires assessment of measurement noise and model discrepancy.

## Computational lesson: check a derivative and recover a positive modulus

The lesson below is an original one-dimensional elastic-bar toy. It first
compares automatic differentiation, a central finite difference, and the known
analytic sensitivity; it then recovers a synthetic modulus and checks a
held-out load case. Its implementation uses a positive log-modulus map,
$E=\exp(\theta)$. The preceding section's sigmoid map supplies a finite
interval. Positivity is enforced in the lesson, while finite lower
and upper bounds remain a separate parameterisation choice to assess for a
particular inverse problem.

The elastic-bar example has a smooth constitutive response and fixed boundary
conditions. A fracture inverse additionally involves damage history,
irreversibility, active sets, and nonlinear solve behaviour.

```{toctree}
:maxdepth: 1

labs/03_tiny_derivative_inverse_toy
```

## A directional derivative check

Let $g$ be a gradient returned by automatic differentiation. Compare

$$
D_hJ(p;q)\quad\text{with}\quad g^\mathsf{T}q
$$

over a short sweep of reasonable $h$ values. A useful result card shows the
direction $q$, the $h$ values, the two numbers, and an error measure such as

$$
\frac{|D_hJ-g^\mathsf{T}q|}
{\max(1,|D_hJ|,|g^\mathsf{T}q|)}.
$$

Compare several spacings. If the check fails, investigate tensor broadcasting,
parameter detachment, in-place
updates, inconsistent normalisation, solver tolerances, and non-smooth
branches before interpreting an optimisation trajectory.

:::{admonition} What a passed check means
:class: note

A small discrepancy at one $(p,q,h)$ supports the local derivative of the
implemented scalar computation. Smoothness over a wider parameter range,
nonlinear convergence, physical calibration, and uniqueness of an inverse
solution each require their own assessment.
:::

## Why inverse recovery can be difficult

Several different parameter fields can produce similar limited observations.
This non-uniqueness can arise from insufficient loading diversity, a coarse
observable, parameter correlation, regularisation choices, or weak sensitivity
of the forward response. A decreasing loss should therefore be reported with
the parameter path, held-out or alternative observables where available, and
the stated prior/bounds.

For a spatial parameter field $p(x)$, an additional smoothness term might be

$$
J_{\mathrm{reg}}(p)
=J_{\mathrm{data}}(p)
+\frac{\beta}{2}\int_\Omega |\nabla p|^2\,\mathrm{d}x.
$$

This selects smoother solutions and changes the inverse problem. The
coefficient $\beta$ controls the balance between fitting observations and
penalising spatial variation.

## Exercise: interpret a gradient result

An implementation reports a small central-difference discrepancy for one
direction $q$ at a parameter $p$. Which conclusions below are supported?

1. The local scalar derivative is consistent with this finite-difference
   check.
2. The inverse problem has a unique solution.
3. The phase-field model is calibrated to a real specimen.
4. The automatic-differentiation graph likely connects the chosen parameter
   to the stated loss along this tested path.

:::{admonition} Solution
:class: dropdown

Conclusions 1 and 4 follow for the tested step, direction, parameter and
forward solve. Conclusions 2 and 3 require additional studies:
identifiability requires a study of observations,
parameters, and priors; calibration requires suitable experimental comparison
and uncertainty treatment.

The computational lesson applies this reasoning to a one-dimensional elastic
bar with a positive log-modulus parameterisation and the displayed scalar
observable.
:::

## Sources for this chapter

The [PyTorch autograd documentation](https://docs.pytorch.org/docs/stable/autograd.html)
and [JAX automatic-differentiation guide](https://docs.jax.dev/en/latest/automatic-differentiation.html)
describe their respective differentiation systems. For a finite-element
example of implicit gradient computation, see the
[JAX-FEM gradient example](https://deepmodeling.github.io/jax-fem/learn/compute_gradients/example.html).
