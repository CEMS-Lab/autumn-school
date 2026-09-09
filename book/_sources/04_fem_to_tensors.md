# Geometry, FEM, tensors, and matrix-free operators

:::{figure} figures/04_fem_pipeline.*
:name: fig-fem-pipeline
:width: 97%
:alt: Geometry, mesh, fields and boundary data define finite-element operators. Assemble a global matrix or evaluate element-local actions; both routes include a solution and numerical checks.

Tensor representations of finite-element data specify geometry, interpolation,
quadrature, loads, and checks explicitly.
:::

## Start with a boundary-value problem

A computational fracture result begins with a boundary-value problem. State:

- the domain $\Omega$, notch or initial damaged region, and material regions;
- the displacement boundary $\Gamma_u$ and traction boundary $\Gamma_t$;
- prescribed displacement $\bar u$, traction $\bar t$, and body force $b$;
- the phase-field convention and initial value $d_0$;
- the mesh, finite-element interpolation, quadrature, and load increments;
  and
- the scalar quantities and fields that will be plotted.

In standard notation,

$$
u=\bar u \text{ on }\Gamma_u,\qquad
\sigma n=\bar t \text{ on }\Gamma_t.
$$

State how the notch is represented: a prescribed initial damage field or a
geometric cut. These choices encode different computational objects and can
produce visually similar pictures.

## From cells to fields

For a two-dimensional mesh, common arrays are:

- coordinates $X\in\mathbb{R}^{N_{\mathrm{node}}\times2}$;
- cell connectivity
  $C\in\{0,\ldots,N_{\mathrm{node}}-1\}^{N_{\mathrm{cell}}\times n_e}$;
- nodal displacement
  $U\in\mathbb{R}^{N_{\mathrm{node}}\times2}$; and
- nodal damage $D\in\mathbb{R}^{N_{\mathrm{node}}}$.

The cell connectivity identifies which rows of $X$, $U$, and $D$ belong to
each element; the field arrays store the corresponding values. For an element $e$ with
local nodes $a$, finite-element interpolation takes the form

$$
u_h(x)=\sum_{a=1}^{n_e}N_a(x)u_a,\qquad
d_h(x)=\sum_{a=1}^{n_e}N_a(x)d_a.
$$

Differentiating the shape functions maps nodal displacement to strain. In
matrix notation at one quadrature point,

$$
\varepsilon_h=B_e u_e.
$$

The element residual is computed by integrating the weak form. A schematic
mechanical contribution is

$$
r_e(u,d)=\int_{\Omega_e}B_e^\mathsf{T}\sigma(u_h,d_h)\,\mathrm{d}x
-f^{\mathrm{ext}}_e.
$$

Assembly scatters each local residual into the appropriate entries of the
global residual. The same operation can be expressed with index operations,
scatter-adds, or framework-specific sparse primitives.

## Tensor shapes are part of the model contract

Write expected shapes next to a tensor operation. For example, with batched
cells and quadrature points, an implementation might use:

- cell coordinates: $(N_{\mathrm{cell}}, n_e, 2)$;
- shape-function gradients:
  $(N_{\mathrm{cell}}, N_q, n_e, 2)$;
- gathered displacement:
  $(N_{\mathrm{cell}}, n_e, 2)$;
- strain or stress:
  $(N_{\mathrm{cell}}, N_q, n_{\varepsilon})$; and
- quadrature weights: $(N_{\mathrm{cell}}, N_q)$.

The exact ordering is a convention. A transpose that preserves the total
number of entries can still mix components, cells, and quadrature points. Use
small assertions and one element-level hand calculation before relying on a
large field plot.

:::{admonition} Indexing check
:class: tip

Select one cell and one quadrature point. Write the gathered nodal values,
shape gradients, strain, stress, and residual contribution on paper. If those
five objects agree with the tensor code, then vectorising over cells has a
clear reference calculation.
:::

## Assembled and matrix-free routes

For a linearised subproblem, an assembled finite-element method forms a global
matrix

$$
K=\sum_e A_e^\mathsf{T}K_eA_e
$$

and solves $Kx=b$ or a linearised residual equation. $A_e$ symbolically
represents the local-to-global map.

A matrix-free method implements the action

$$
v\longmapsto K v
$$

by gathering $v$ to elements, applying local operations, and scattering
contributions back. An iterative Krylov solver can use this implicit
representation of $K$.

Matrix-free evaluation uses local operator actions and associated element data.
Its cost depends on residual/Jacobian actions,
preconditioning, data movement, and stopping criteria. Compare memory use and
runtime at matched physics, mesh, tolerance, and reported observable.

## Static and dynamic arrays

In a quasistatic calculation, the state often consists primarily of $U$ and
$D$. A dynamic calculation adds at least velocity and acceleration or their
time-integration equivalents. A schematic time step must then track

$$
(U_n,V_n,A_n,D_n)\longrightarrow
(U_{n+1},V_{n+1},A_{n+1},D_{n+1}).
$$

The update rules for these arrays express inertia and affect the computed
path. A sequence of prescribed displacement increments represents load
stepping; a dynamic calculation also evolves the inertial state.

## Where automatic differentiation fits

PyTorch provides tensors and a reverse-mode automatic-differentiation system.
The user or a library defines mesh data, interpolation, constitutive response,
residuals, boundary conditions, and solver behaviour.

JAX likewise provides array transformations such as differentiation,
compilation, and vectorisation. JAX-FEM is an additional finite-element
library built on that ecosystem and includes worked mechanics examples. A suitable choice depends
on the existing solver, device support, reproducibility needs, and whether the
relevant operations are differentiable in the intended computation.

See the official [PyTorch autograd
documentation](https://docs.pytorch.org/docs/stable/autograd.html), the
[JAX automatic-differentiation
guide](https://docs.jax.dev/en/latest/automatic-differentiation.html), and
the [JAX-FEM quickstart](https://deepmodeling.github.io/jax-fem/guide/Quickstart.html).

## Inspecting results: four views, one interpretation

For a tiny evolving-fracture run, inspect at least:

1. the geometry, mesh, and loading direction;
2. displacement or deformed configuration with a stated scale factor;
3. damage field with a labelled colour range and the $d=0$/$d=1$ convention;
   and
4. a scalar observation such as reaction force, energy term, or residual.

## Hands-On Lab: Running an End-to-End PhAST Fracture Simulation

In the accompanying computational notebook, you will execute a complete phase-field fracture calculation using the PhAST solver:

1. **Geometry & Meshing:** Generate a two-dimensional rectangular specimen and discretize it with structured triangular (T3) finite elements.
2. **Boundary Conditions & Precrack:** Identify boundary node sets (`left`, `right`, `top`, `bottom`) and define an initial center-notch precrack.
3. **Solver Execution:** Run the staggered displacement-damage solver over 60 incremental load steps.
4. **Post-Processing & Field Visualization:** Extract the global load-displacement curve, observe peak softening, and render the localized diffuse damage field.

```{toctree}
:maxdepth: 1

labs/01_phast_tiny_evolving_fracture
```

This notebook serves as our reference simulation pipeline throughout the course. You will see how tensor representations map directly to physical finite element fields.

## Exercise: identify a silent shape error

A tensor containing displacement at cell nodes has shape
$(N_{\mathrm{cell}},n_e,2)$. A tensor of shape-function gradients has shape
$(N_{\mathrm{cell}},N_q,n_e,2)$. Which new axes must be aligned or introduced
before forming a displacement gradient at every quadrature point, and what
physical quantity should you recover for an affine displacement field?

:::{admonition} Solution
:class: dropdown

The nodal displacement needs a quadrature axis, for example by treating it as
$(N_{\mathrm{cell}},1,n_e,2)$, so that it aligns with the $N_q$ axis of the
shape gradients. Contract the local-node axis and preserve the displacement
component and spatial-derivative axes according to the chosen convention. For
an affine displacement field, the displacement gradient and its symmetric
strain should be constant across all elements and quadrature points (up to
round-off). This is an excellent first unit test. The PhAST lesson makes the
mesh, nodal fields, and boundary labels visible; this one-element affine test
remains the right additional check before treating a vectorised tensor route
as trustworthy.
:::

## Take-away

Tensors make data movement and differentiation explicit. The finite-element
description specifies what is interpolated, where it is integrated,
how boundary conditions are enforced, and how the resulting field is checked.
