# Geometry, FEM, tensors, and matrix-free operators

:::{figure} figures/04_fem_pipeline.png
:name: fig-fem-pipeline
:width: 97%

Finite-element data can be expressed as tensors without changing the need to
define geometry, interpolation, quadrature, loads, and checks.
:::

## Start with a boundary-value problem

A computational fracture result should be traceable to a boundary-value
problem, not merely a tensor shape. State:

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

If a notch is represented through a prescribed initial damage field rather
than a literal geometric cut, say so. These choices can produce visually
similar pictures but encode different computational objects.

## From cells to fields

For a two-dimensional mesh, common arrays are:

- coordinates $X\in\mathbb{R}^{N_{\mathrm{node}}\times2}$;
- cell connectivity
  $C\in\{0,\ldots,N_{\mathrm{node}}-1\}^{N_{\mathrm{cell}}\times n_e}$;
- nodal displacement
  $U\in\mathbb{R}^{N_{\mathrm{node}}\times2}$; and
- nodal damage $D\in\mathbb{R}^{N_{\mathrm{node}}}$.

The cell connectivity does not contain the field values. It tells the program
which rows of $X$, $U$, and $D$ belong to each element. For an element $e$ with
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

A matrix-free method instead implements the action

$$
v\longmapsto K v
$$

by gathering $v$ to elements, applying local operations, and scattering
contributions back. An iterative Krylov solver can use this action without
storing every entry of $K$.

Matrix-free does **not** mean “no matrix mathematics,” “no memory cost,” or
“automatically faster.” It moves attention to the correctness and efficiency
of residual/Jacobian actions, preconditioning, data movement, and stopping
criteria. Compare methods at matched physics, mesh, tolerance, and reported
observable.

## Static and dynamic arrays

In a quasistatic calculation, the state often consists primarily of $U$ and
$D$. A dynamic calculation adds at least velocity and acceleration or their
time-integration equivalents. A schematic time step must then track

$$
(U_n,V_n,A_n,D_n)\longrightarrow
(U_{n+1},V_{n+1},A_{n+1},D_{n+1}).
$$

The extra arrays are not bookkeeping only: their update rule expresses
inertia and affects the computed path. Do not label a code dynamic merely
because it loops over a sequence of prescribed displacements.

## Where automatic differentiation fits

PyTorch provides tensors and a reverse-mode automatic-differentiation system;
it is not, by itself, a fracture finite-element formulation. The user or a
library still defines mesh data, interpolation, constitutive response,
residuals, boundary conditions, and solver behaviour.

JAX likewise provides array transformations such as differentiation,
compilation, and vectorisation. JAX-FEM is an additional finite-element
library built on that ecosystem and includes worked mechanics examples. Neither
ecosystem is universally superior for this course: a suitable choice depends
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

## Computational lesson: follow a public PhAST calculation

The lesson below is the book's small public PhAST example. It defines a
rectangular T3 mesh, labelled boundaries, a locked centreline precrack, and
symmetric displacement loading before showing the damage fields, response
trace, and stagger-iteration trace. Read the case card before interpreting the
plots. The route is quasistatic and uses an assembled sparse-direct mechanics
solve; it is neither a dynamic calculation nor a demonstration that no
matrices are constructed.

```{toctree}
:maxdepth: 1

labs/01_phast_tiny_evolving_fracture
```

Interpret each image using the case definition; do not crop away a boundary,
notch, colourbar, or load increment that makes the result intelligible. The
lesson's retained result card belongs to its recorded environment. If you
download it for execution, record a new result card for your own environment.

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

Tensors make data movement and differentiation explicit. They do not replace
the finite-element questions: what is interpolated, where it is integrated,
how boundary conditions are enforced, and how the resulting field is checked.
