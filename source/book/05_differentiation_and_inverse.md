# Differentiable Mechanics and Inverse Parameter Discovery

:::{figure} figures/05_autograd_inverse.*
:name: fig-autograd-inverse
:width: 96%
:alt: Parameters enter a supported forward computation and a scalar loss. Reverse sensitivities return a gradient, checked against a directional finite difference. An optional optimizer uses that gradient in a separate parameter update.

In differentiable mechanics, parameters flow through the forward solver graph to produce an observation. Reverse-mode automatic differentiation computes the sensitivity gradient, which guides an optimizer to discover unknown physical properties.
:::

## The Detective Story: Solving Inverse Problems with Differentiable Mechanics

Imagine you are an engineer in a materials testing laboratory. You place a specimen of an unknown advanced alloy into a tensile testing machine, apply incremental stretch, and record the reaction forces and surface displacement fields using digital cameras (digital image correlation).

Now comes the fundamental scientific puzzle:
*What are the true underlying material properties—such as Young's modulus $E$, Poisson's ratio $\nu$, or fracture toughness $G_c$—that gave rise to these experimental measurements?*

In traditional engineering, solving this **inverse problem** required expensive brute-force guessing: pick a trial parameter, run a forward finite element simulation, see how far off the prediction is, and guess again.

With **differentiable mechanics**, the simulation itself calculates the road map!
Because our finite element equations are assembled into a differentiable computational graph in PyTorch, reverse-mode automatic differentiation (`autograd`) uses the chain rule to backpropagate the error between simulation and observation all the way back to the input material parameters:

$$
\frac{\partial J}{\partial p} = \frac{\partial J}{\partial y} \cdot \frac{\partial y}{\partial u} \cdot \frac{\partial u}{\partial p}.
$$

With this exact sensitivity gradient in hand, standard optimization algorithms (`torch.optim.Adam` or L-BFGS) can systematically navigate the parameter landscape and pinpoint the true material properties.

---

## Formulating the Forward and Inverse Maps

Let $p$ denote the physical parameter we wish to discover (for example, Young's modulus $E > 0$). The forward computational graph maps the parameter to a physical state, and then to a measurable observation:

$$
p \longmapsto (u(p), d(p)) \longmapsto y(p).
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
- every mathematical operation from $p$ to $J$; and
- the stopping tolerances and convergence criteria of any iterative solver.

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

## Hands-On Lab: Differentiating Mechanics and Parameter Recovery

In the accompanying computational lesson, you will implement a complete differentiable mechanics problem in PyTorch:
1. **Forward Solution:** Solve deformation in a one-dimensional elastic bar under tensile loading.
2. **Derivative Verification:** Compute sensitivities of an observation with respect to the elastic modulus using analytical formulas, automatic differentiation (`loss.backward()`), and central finite differences.
3. **Inverse Identification:** Use gradient descent to automatically recover the unknown ground-truth stiffness from synthetic displacement measurements.

:::{admonition} Hands-On Tutorial: Lab 2 (Gradients and Parameter Recovery)
:class: tip

**Ready to try this in practice?**  
Explore the interactive tutorial: **{doc}`classroom/02_gradients_and_recovery`**.
You can read through the worked autograd graph and parameter recovery trajectories directly here in the book, or run it interactively in **Google Colab** with one click:

<div class="badge-row">
  <a class="badge-colab" href="https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/02_gradients_and_recovery.ipynb" target="_blank"><img src="_static/colab-badge.svg" alt="Open In Colab"/></a>
  <a class="badge-link" href="../notebooks/study/classroom/02_gradients_and_recovery.ipynb"><i class="fa-solid fa-download"></i> Download Practice Notebook</a>
  <a class="badge-link" href="../notebooks/solutions/classroom/02_gradients_and_recovery.ipynb"><i class="fa-solid fa-check-circle"></i> Download Worked Solutions</a>
</div>
:::

## Directional Derivative Verification

To verify that reverse-mode automatic differentiation yields the true gradient, we compare the directional derivative obtained from autograd with a numerical central difference:

$$
D_hJ(p;q) = \frac{J(p+hq)-J(p-hq)}{2h} \quad\approx\quad g^\mathsf{T}q.
$$

We evaluate this comparison across several perturbation step sizes $h$. A relative error metric measures consistency:

$$
\text{Relative Error} = \frac{|D_hJ - g^\mathsf{T}q|}{\max(1, |D_hJ|, |g^\mathsf{T}q|)}.
$$

When the step size $h$ is in a well-balanced range (typically $10^{-4}$ to $10^{-6}$ for float64), the relative difference is close to machine precision, confirming that autograd correctly traverses every operation in the forward computational graph.

:::{admonition} Interpreting Gradient Verification
:class: note

A close match between autodiff and finite differences confirms that the computational graph correctly implements the intended mathematical derivative. In inverse problems, this verified gradient provides the foundation for stable, efficient optimization.
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
