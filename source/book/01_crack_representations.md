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
law is therefore a **fracture formulation or constitutive law**, not a
particular mesh technology. The classical computational formulation of
[Xu and Needleman (1994)](https://doi.org/10.1016/0022-5096(94)90003-5) is a
standard reference.

:::{admonition} Useful boundary
:class: warning

It is misleading to say that a CZM “is XFEM” or that it “is phase field.”
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
$K$ select enriched nodes. The important point is not this exact notation but
its role: XFEM changes the **spatial approximation**, allowing a crack to
cut through elements without forcing every element edge to align with the
crack.

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
surface. The method avoids explicitly tracking a discontinuity during
propagation. It instead solves for a continuous field $d$ and must resolve its
diffuse band on the mesh.

This is a **regularised fracture formulation**. It is commonly discretised
with ordinary continuous finite elements, but the formulation and the
discretisation are conceptually separate. The diffuse approach was developed
for brittle fracture by
[Bourdin, Francfort, and Marigo (2000)](https://doi.org/10.1016/S0022-5096(99)00028-9).

## A fair comparison

Choose a method by first stating the question.

**If the crack path and interface are known.** An interface model with a
cohesive law may make the physical parameters particularly direct. The price
is that a new path outside that interface is not automatically represented.

**If a sharp discontinuity is needed on a fixed background mesh.** XFEM gives
a route to enrich the approximation. It does not by itself choose a fracture
criterion or resolve a crack evolution law.

**If evolving, branching, or merging cracks make explicit tracking awkward.**
A phase field can be convenient because the crack is an evolving field.
Resolution and regularisation sensitivity then become central scientific
questions rather than implementation details.

These statements compare *useful roles*, not universal winners. Cost depends
on mesh, dimension, nonlinear solver, loading path, conditioning, and the
question being asked.

## Method and algorithm are not synonyms

The following labels belong at different levels:

- **phase field, Griffith, cohesive zone:** fracture energy or interface-law
  choices;
- **standard FEM, XFEM, mesh refinement:** spatial representations;
- **staggered iteration, Newton, quasi-Newton:** nonlinear solution methods;
- **finite difference, unrolled automatic differentiation, implicit adjoint:**
  sensitivity strategies.

For example, a phase-field calculation can use standard finite elements and a
staggered solver; another may use Newton-type iterations. A quasi-Newton
update is not a third crack representation.

## Exercise: separate the layers before reading code

Rewrite the sentence below as two technically accurate sentences.

> “We use XFEM phase field with a quasi-Newton fracture method.”

:::{admonition} Solution
:class: dropdown

One possible rewrite is: “We represent brittle fracture with a
phase-field regularisation and approximate its displacement and damage fields
with a stated finite-element space. We solve the resulting nonlinear problem
with a quasi-Newton method; XFEM would be relevant only if the approximation
space is explicitly enriched for a discontinuity or crack-tip feature.”

The original sentence may describe a legitimate hybrid method, but it does not
say which component provides the fracture energy, which provides enrichment,
or which equation the optimisation method solves.
:::

## Take-away

Before comparing curves, mesh sizes, or runtimes, identify the crack
representation, the finite-element approximation, and the nonlinear solver.
That separation makes the phase-field energy in the next chapter much easier
to read. It also gives a useful template for the later computational lessons:
the case card states the formulation, mesh and solver route before any output
is interpreted.
