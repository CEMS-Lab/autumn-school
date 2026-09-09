# Backpropagation through a stepped update

This original, small example makes the bookkeeping behind reverse-mode
automatic differentiation visible. It is deliberately an algebraic recurrence,
not a fracture calculation. For a complementary visual introduction to
reverse-mode differentiation in physics, see the [Physics-Based Deep Learning
discussion of differentiable physics](https://physicsbaseddeeplearning.org/diffphys.html).
That link is a pedagogical reference only: no external code, figure, or
derivation is reproduced here.

:::{figure} figures/05a_backpropagation.png
:name: fig-backpropagation-step-by-step
:width: 100%

One parameter can influence a final loss at every update. Reverse mode passes
a cotangent backwards and adds one parameter contribution per use of that
parameter.
:::

## Start from a sequence of update maps

Let a state evolve through $N$ discrete updates,

$$
z_{n+1}=S_n(z_n,p),\qquad n=0,\ldots,N-1,
$$

where the same parameter vector $p$ may appear in every $S_n$. A final field
or state is observed by $y=Cz_N$, and a scalar loss is formed as

$$
J=\ell(y,p)=\ell(Cz_N,p).
$$

Here $C$ is assumed fixed with respect to $p$. If an observation operator also
depends on $p$, its derivative belongs in the direct parameter dependence of
the final observable/loss.

Define the local state and parameter derivatives

$$
A_n=\frac{\partial S_n}{\partial z_n},
\qquad
B_n=\frac{\partial S_n}{\partial p}.
$$

For a scalar loss, the terminal adjoint is the vector

$$
\lambda_N=C^\mathsf{T}\nabla_y\ell,
$$

and reverse accumulation is

$$
\lambda_n=A_n^\mathsf{T}\lambda_{n+1}
\qquad (n=N-1,\ldots,0).
$$

The resulting **total derivative** is

$$
\frac{dJ}{dp}
=\frac{\partial\ell}{\partial p}
+\sum_{n=0}^{N-1}B_n^\mathsf{T}\lambda_{n+1}
+\left(\frac{\partial z_0}{\partial p}\right)^\mathsf{T}\lambda_0.
$$

This is $dJ/dp$, the gradient of the final scalar observable/loss with
respect to the input parameter $p$. An optimisation algorithm uses that
gradient in a *separate* choice such as

$$
p_{\mathrm{new}}=p-\alpha\,\frac{dJ}{dp},
$$

where the learning rate $\alpha$ and any line search, regularisation, or
constraint handling belong to the optimisation method rather than to reverse
accumulation itself.

If $z_N$ is a field, $\lambda_N$ has one entry per field degree of freedom.
For a scalar loss, the loss fixes the seed. For a vector-valued output, choose
a seed $v$ to obtain a vector--Jacobian product $A_n^\mathsf{T}v$. Neither
case requires forming a full Jacobian matrix. This is why a scalar
`loss.backward()` can be economical even when the state is large.

## A three-step scalar calculation that can be checked by hand

Use the explicit recurrence

$$
x_{n+1}=(1-\Delta t\,p)x_n+\Delta t\,f,
\qquad
J=\frac12(x_3-y_\star)^2.
$$

It is a relaxation/load **analogue only**, not PhAST, phase-field fracture, or
a claim about a finite-element time integrator. The parameter $p$ appears at
every step, so it provides a clean miniature of the shared-parameter sum.
For this scalar homogeneous relaxation, choosing $p>0$ and
$0<\Delta t\,p<1$ makes $0<1-\Delta t\,p<1$. That is a property of this one
recurrence, not a universal CFL or solver-stability rule.

Take

$$
\Delta t=0.2,\quad p=0.8,\quad f=1.5,\quad x_0=0.4,
\quad y_\star=0.9.
$$

Then $A_n=\partial x_{n+1}/\partial x_n=1-\Delta t p=0.84$ and
$B_n=\partial x_{n+1}/\partial p=-\Delta t x_n$. The forward states and
local parameter derivatives are:

| step $n$ | $x_n$ | $x_{n+1}$ | $B_n=-\Delta t x_n$ |
| ---: | ---: | ---: | ---: |
| 0 | 0.400000 | 0.636000 | -0.0800000 |
| 1 | 0.636000 | 0.834240 | -0.1272000 |
| 2 | 0.834240 | 1.000762 | -0.1668480 |

The terminal seed is $\lambda_3=x_3-y_\star=0.1007616$. Therefore

$$
\lambda_2=0.084639744,
\qquad
\lambda_1=0.07109738496,
\qquad
\lambda_0=0.0597218033664.
$$

The corresponding reverse contributions are:

| step $n$ | $\lambda_{n+1}$ | $B_n\lambda_{n+1}$ |
| ---: | ---: | ---: |
| 0 | 0.07109738 | -0.005687791 |
| 1 | 0.08463974 | -0.010766175 |
| 2 | 0.10076160 | -0.016811871 |

The displayed loss has no direct $p$ dependence and $x_0$ is fixed, so its
two non-sum terms are zero. Adding the three entries in the last column gives

$$
\frac{dJ}{dp}=-0.0332658376704.
$$

Those zero terms are a feature of this chosen calculation, not a general
rule: a parameter-dependent observation/loss or parameter-dependent initial
state contributes through the first or last term of the total-derivative
formula.

The accompanying script independently evaluates the same recurrence with
PyTorch and a central finite difference. Its retained receipt records

$$
\begin{aligned}
\text{reverse accumulation} &= -0.0332658376704,\\
\text{PyTorch autograd} &= -0.0332658376704,\\
\text{central difference }(h=10^{-6}) &= -0.0332658376618.
\end{aligned}
$$

The small finite-difference discrepancy is truncation and floating-point
roundoff, not a new model effect. The complete check takes under five seconds
on the recorded CPU and is reproducible with:

```bash
python source/book/scripts/build_backprop_example.py
```

Run this command from the extracted public edition's root. It updates the
figure under `source/book/figures/` and writes a new validation receipt under
`reviews/`, leaving the published evidence receipt unchanged.

The [machine-readable validation receipt](../evidence/backprop_example.json)
retains the measured runtime, all forward/reverse values, and the analytic,
automatic-differentiation, and central-difference assertions used here.

The check confirms this scalar recurrence and its stated arithmetic. It does
not validate a fracture derivative or a complete optimisation workflow.

## A restricted fixed-history AT2 connection

The packaged public PhAST source documents an AT2 damage weak form and an
adjoint CG backward for selected damage-solve inputs in
`vendor/PhAST/src/phast/solvers/damage_solver.py`. For an **unconstrained
interior solve** (or a residual restricted to free damage degrees of freedom),
with spatially constant $G_c$ and no mesh-dependent $\gamma$ correction, a
useful **fixed-history, fixed-mechanics reduced** notation for that damage
subproblem is

$$
R_d(d;G_c,H)
=\left[\frac{G_c}{\ell}M+G_c\ell K+2M_H\right]d-2b_H=0,
$$

where $M$ and $K$ are mass and stiffness assemblies, while $M_H$ and $b_H$
collect the history-weighted assembly. With $H$, mechanics, and $\ell$ held
fixed, let

$$
A=\frac{\partial R_d}{\partial d},
\qquad
A^\mathsf{T}\lambda=\frac{\partial J}{\partial d}.
$$

Implicit differentiation of this *reduced* residual gives

$$
\frac{dJ}{dG_c}
=\frac{\partial J}{\partial G_c}
-\lambda^\mathsf{T}
\left[\left(\frac{M}{\ell}+\ell K\right)d\right].
$$

The direct term remains only when the chosen loss explicitly depends on
$G_c$. The minus sign follows from differentiating $R_d=0$ and solving for
$dd/dG_c$.

This is intentionally narrower than an end-to-end fracture claim. In a full
load history, mechanics can change $H$; an irreversibility update may use a
non-smooth maximum; damage bounds can activate; and nonlinear/staggered
iterations and stopping criteria matter. Active-set changes, history changes,
and convergence failures must be accounted for by the selected differentiation
rule. A discrete model change is not automatically differentiable merely
because it is written in tensor operations.

## Check your understanding

1. In the scalar example, why are there three $B_n\lambda_{n+1}$ terms even
   though there is only one scalar parameter $p$?
2. Suppose $x_0=x_0(p)$ instead of being fixed. Which term in the total
   derivative changes, and why is it propagated by $\lambda_0$ rather than
   $\lambda_3$?
3. Which assumptions must remain fixed before the displayed AT2 $G_c$
   identity can be treated as a reduced-subproblem calculation?

:::{admonition} Short answers
:class: dropdown

1. The single parameter is used once in each of the three update maps. Each
   local use affects the final loss through the remaining steps, so reverse
   mode adds one local parameter contribution for each use.
2. The initial-state term
   $(\partial z_0/\partial p)^\mathsf{T}\lambda_0$ becomes nonzero. The
   adjoint at step zero contains the sensitivity of the final loss to a
   perturbation of the initial state after every later update has been
   traversed backwards.
3. The mechanics-dependent history field $H$, the mechanics state, and
   $\ell$ are held fixed. The identity is not by itself a statement about
   history maxima, bounds/active sets, staggered convergence, or a total
   derivative through a full fracture load path.
:::
