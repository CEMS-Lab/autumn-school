# Crack representations: sharp, cohesive, and diffuse

:::{figure} figures/01_methods_map.*
:name: fig-methods-map
:width: 96%
:alt: Three separate choices: fracture formulation, spatial discretisation and nonlinear solution algorithm. Phase field, XFEM and quasi-Newton answer different questions.

Three different questions are often compressed into one phrase such as
“the fracture method.” Keeping them separate prevents misleading comparisons.
:::

## The starting point: a sharp crack

In classical brittle fracture, a crack is a lower-dimensional set
$\Gamma$ inside a body $\Omega$. A Griffith-type idealisation balances bulk
elastic energy, external work, and an energy proportional to newly created
crack surface:

$$
\mathcal{E}(u,\Gamma)
  = \int_{\Omega\setminus\Gamma}\psi(\varepsilon(u))\,\mathrm{d}x
    +G_c\,\mathcal{H}^{d-1}(\Gamma)
    -\mathcal{W}_{\mathrm{ext}}(u).
$$

Here $u$ is displacement, $\psi$ is elastic energy density, $G_c$ is fracture
toughness, and $\mathcal{H}^{d-1}(\Gamma)$ measures crack length in two
dimensions or area in three. The attractive feature is conceptual clarity:
the model makes a literal discontinuity. The difficult feature is that the
unknown crack geometry may advance, branch, or meet another crack during the
calculation.

The energy criterion is associated with
[Griffith (1921)](https://doi.org/10.1098/rsta.1921.0006) and the
variational treatment of evolving cracks by
[Francfort and Marigo (1998)](https://doi.org/10.1016/S0022-5096(98)00034-9).

## Cohesive-zone models: separation on an interface

A cohesive-zone model (CZM) places a constitutive traction--separation law on
an interface. If $\delta$ denotes displacement jump, a simple scalar picture
is

$$
T = T(\delta), \qquad
\Phi(\delta)=\int_0^\delta T(s)\,\mathrm{d}s.
$$

The area below $T(\delta)$ supplies an interface fracture energy. A CZM is
especially natural when an interface is known in advance: an adhesive layer,
a ply interface, or a prescribed material boundary. Its parameters can
express a peak traction and a separation scale in addition to an energy.

The interface still needs to be represented numerically. It may coincide with
element faces, embedded interface elements, or a tracked surface. A cohesive
law is therefore a **fracture formulation or constitutive law** whose numerical
representation is chosen separately. The classical computational formulation of
[Xu and Needleman (1994)](https://doi.org/10.1016/0022-5096(94)90003-5) is a
standard reference.

:::{admonition} Formulation and discretisation
:class: note

A cohesive law can be coupled to several discretisations; it has a different
physical idealisation from a diffuse crack-density regularisation.
:::

## XFEM: enrich an approximation space

The extended finite-element method (XFEM) represents a discontinuity or a
near-tip feature by enriching a conventional finite-element approximation. A
schematic displacement approximation is

$$
u_h(x)
 = \sum_{i\in I}N_i(x)u_i
 + \sum_{j\in J}N_j(x)H(x)a_j
 + \sum_{k\in K}N_k(x)\sum_{\alpha}F_\alpha(x)b_{k\alpha}.
$$

$N_i$ are ordinary shape functions; $H$ may encode a jump across a crack; and
$F_\alpha$ can encode near-tip asymptotic behaviour. The index sets $J$ and
$K$ select enriched nodes. XFEM changes the **spatial approximation**, allowing a crack to
cut through elements independently of the element-edge alignment.

XFEM can reduce repeated remeshing for propagating cracks, but brings its own
implementation questions: enrichment support, integration of cut cells,
conditioning, branch handling, and the geometry used to describe the crack.
The foundational paper is
[Moes, Dolbow, and Belytschko (1999)](https://doi.org/10.1002/(SICI)1097-0207(19990910)46:1%3C131::AID-NME726%3E3.0.CO;2-J).

## Phase field: replace a surface by a narrow band

In a phase-field formulation, a scalar field $d(x)$ spreads the crack over a
band of width governed by a length $\ell$. With the convention used here,
$d=0$ is intact and $d=1$ is broken. A typical crack-density functional is

$$
\Gamma_\ell(d)
 = \frac{1}{c_0}\int_\Omega
 \left(\frac{w(d)}{\ell}+\ell|\nabla d|^2\right)\,\mathrm{d}x,
\qquad
c_0=4\int_0^1\sqrt{w(s)}\,\mathrm{d}s.
$$

As $\ell$ becomes small under appropriate refinement and modelling
assumptions, this regularised functional approximates a sharp fracture
surface. Crack propagation is represented by the evolution of a continuous
field $d$, whose diffuse band must be resolved on the mesh.

This is a **regularised fracture formulation**. It is commonly discretised
with ordinary continuous finite elements, but the formulation and the
discretisation are conceptually separate. The diffuse approach was developed
for brittle fracture by
[Bourdin, Francfort, and Marigo (2000)](https://doi.org/10.1016/S0022-5096(99)00028-9).

## Comparing Crack Representations

Each representation offers distinct advantages depending on the engineering application:

| Method | Geometric Representation | Mesh Requirements | Crack Branching & Merging | Primary Engineering Applications |
| :--- | :--- | :--- | :--- | :--- |
| **Sharp Crack (LEFM)** | Exact lower-dimensional surface $\Gamma$ | Conforming mesh with tip singularity elements | Requires remeshing at every crack extension step | Standard fatigue crack propagation along known paths |
| **Cohesive Zone (CZM)** | Traction–separation interface law | Interface elements along predefined element boundaries | Predefined along mesh interfaces | Delamination in composites, adhesive joints, masonry |
| **XFEM** | Enriched continuous displacement field | Fixed background mesh with Heaviside and tip enrichments | Requires level-set tracking for multiple crack fronts | Crack growth without global remeshing on structured grids |
| **Phase Field (PFM)** | Continuous scalar damage field $d(x) \in [0, 1]$ | Standard finite elements (element size $h < \ell$) | Handled naturally via energy minimization without tracking | Complex crack topologies, branching, coalescence in 2D/3D |

### When to Choose Phase-Field Fracture

Phase-field methods have become widely adopted in modern computational mechanics because they transform a complex geometric interface tracking problem into the solution of coupled partial differential equations on a fixed mesh. The crack trajectory, initiation, branching, and coalescence emerge naturally from energy minimization without requiring *ad hoc* geometric tracking criteria.

---

## Separating Formulation, Discretization, and Solver

To reason clearly about any computational mechanics calculation, we maintain a clean separation between three levels:

1. **Continuum Formulation:**  
   The governing energy functional or constitutive equations (e.g., linear elasticity coupled to an AT1 or AT2 phase-field damage model).
2. **Spatial Discretization:**  
   The mathematical approximation space and mesh topology used to discretize continuous fields (e.g., standard continuous linear triangular T3 elements).
3. **Nonlinear Solution Strategy:**  
   The iterative numerical algorithm used to solve the coupled nonlinear system of equations (e.g., staggered alternating minimization, or monolithic Newton–Raphson).

This separation is modular: a phase-field formulation can be discretized using standard continuous Galerkin finite elements, and the resulting equations can be solved using either a staggered alternating loop or a monolithic Newton–Raphson solver.

---

## Exercise: Identifying the Computational Layers

Consider the following statement from a research paper:
> *"We simulate crack branching using an AT2 phase-field model on triangular finite elements solved with a staggered alternating minimization scheme."*

Break this down by identifying:
1. The fracture formulation.
2. The spatial discretization.
3. The nonlinear solver.

:::{admonition} Solution
:class: dropdown

1. **Fracture Formulation:** The AT2 phase-field regularisation, which specifies the quadratic local dissipation function $w(d) = d^2$ and degradation law $g(d) = (1-d)^2$.
2. **Spatial Discretization:** Standard continuous triangular (T3) finite elements with piecewise linear shape functions.
3. **Nonlinear Solver:** A staggered (alternating minimization) algorithm that decouples the mechanical equilibrium and damage updates within each load increment.
:::

---

## Summary of Key Concepts

- **Sharp vs. Diffuse:** Sharp crack models treat cracks as surfaces of discontinuity; phase-field models diffuse the crack over a narrow zone of characteristic width governed by the length scale $\ell$.
- **Energy Balance:** In a phase-field model, the total energy consists of bulk elastic strain energy and surface fracture dissipation.
- **Modularity:** Distinguishing formulation, discretization, and solver ensures clarity when comparing numerical results and computational costs.
