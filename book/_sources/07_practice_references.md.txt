# Practice, solutions, glossary, references, and contributing

## A six-part learn-by-doing sequence

The book can be read in order or used as a companion to six teaching blocks.
Each block should leave a visible artefact: a written prediction, a derived
equation, a labelled field, a result card, or a checked derivative. Where a
computational lesson appears in the table of contents beneath its chapter,
read the prompt and retained output before downloading code to execute.

1. **Represent a crack.** Separate sharp cracks, cohesive interfaces, phase
   fields, XFEM enrichment, and nonlinear solvers.
2. **Read the energy.** Identify $G_c$, $\ell$, $w(d)$, $g(d)$, the
   tension--compression split, and the damage convention.
3. **Follow an update.** Sketch a staggered mechanics/damage loop and locate
   the irreversibility rule.
4. **Trace data.** Start with geometry and boundary conditions; end with
   fields and observables; write tensor shapes at the interface.
5. **Check a derivative.** Define a scalar loss, select a direction, and
   compare automatic differentiation with a finite difference.
6. **Audit a learned proposal.** Save state, reload it, define the adapter,
   and separate a proposal from a corrected mechanics result.

The computational exercises are intentionally small. Their code, retained
outputs, hints, and worked solutions belong to the same reading route as the
theory. Use the timing record in the lesson rather than transferring a runtime
result to a different device or software version.

## Quickstart checklist

Before an activity:

- read the problem definition and prediction prompt;
- record the phase-field convention, mesh/array dimensions, and parameters;
- identify the quantity that will be checked; and
- read the corresponding integrated computational lesson; download its
  notebook only if you intend to execute cells in a suitable environment.

During an activity:

- change one named input at a time;
- retain the original result card when making a comparison;
- inspect a field, an observable, and a numerical check; and
- stop and diagnose if bounds, residuals, or tensor shapes are unexpected.

After an activity:

- state what was observed;
- state which assumption or numerical choice could change that observation;
- link the output to its lesson and case definition; and
- write one limitation rather than promoting a small illustration to a
  general material claim.

## Worked consolidation exercise

Consider a two-dimensional notched specimen represented by displacement $u$
and damage $d$. The calculation uses a length scale $\ell$, a residual
stiffness $\eta_{\mathrm{res}}$, and a displacement-controlled load increment.

1. Give the three terms in the fracture density that regularise a sharp crack.
2. Write the qualitative order of a staggered update.
3. Name two visual outputs and one scalar output you would retain.
4. A learned model proposes $d$. Name two checks required before using it as a
   starting point for a mechanics update.
5. State one conclusion that the exercise could support and one conclusion it
   could not support.

:::{admonition} Solution
:class: dropdown

1. The fracture part uses a local crack-density term $w(d)/\ell$, a gradient
   term $\ell|\nabla d|^2$, and the fracture energy scale $G_c/c_0$.
2. Start from accepted prior damage; solve mechanics with damage fixed; update
   the stated tensile driving quantity; solve damage subject to
   irreversibility; then check and accept or repeat.
3. Retain the geometry/mesh with loading direction, a damage field with a
   colour scale, and a displacement/deformed-field view. A suitable scalar is
   reaction force, an energy contribution, or a stated residual.
4. Check the damage bounds/irreversibility and a stated mechanics residual or
   correction step. The precise checks depend on the proposal's intended use.
5. The result can support a statement about this defined discretisation and
   load path. It cannot alone establish a calibrated material law, a
   mesh-independent crack path, or a general acceleration claim.
:::

## Glossary

**Adapter**
: A declared map that changes a data representation, for example node order,
  units, or tensor layout. It does not automatically preserve physical
  meaning.

**Automatic differentiation (AD)**
: A method for evaluating derivatives of a program by applying the chain rule
  to its recorded operations. Its result concerns the executed computation.

**Cohesive-zone model (CZM)**
: A fracture/interface formulation based on a traction--separation law.

**Crack-density function $w(d)$**
: The local part of a phase-field fracture regularisation. AT1 and AT2 use
  different choices.

**Damage field $d$**
: A scalar field used here with $d=0$ intact and $d=1$ fully broken.

**DAgger-style aggregation**
: Iterative collection of reference labels at states visited by the current
  proposal/policy, followed by retraining on the aggregate data.

**Degradation function $g(d)$**
: A function that reduces selected elastic energy as damage grows.

**Finite difference**
: A derivative approximation from nearby function evaluations; useful as an
  independent local check.

**Irreversibility**
: The condition that brittle damage does not decrease over the stated loading
  history.

**Matrix-free action**
: An implementation of $v\mapsto Kv$ or a Jacobian action without explicitly
  storing every global matrix entry.

**Phase-field fracture**
: A regularised fracture formulation in which a diffuse scalar field
  approximates a sharp crack surface.

**Quadrature**
: Numerical integration on an element using selected points and weights.

**Quasi-Newton method**
: A nonlinear optimisation/solution strategy that updates an approximate
  Jacobian or inverse Jacobian. It is not a fracture model.

**Residual**
: The imbalance in a stated discrete equation. A residual norm is meaningful
  only with its definition, scaling, tolerance, and field context.

**XFEM**
: Extended finite elements: an enriched finite-element approximation for
  discontinuities or near-tip features.

## Contributing a new course activity

An activity is easier for others to reuse when it has a narrow learning
objective and an inspectable result. Include:

1. a one-sentence question and the prerequisite chapter;
2. a complete case definition: geometry, parameter choices, boundary
   conditions, and initial state;
3. a short prediction prompt before code is executed;
4. labelled figures or data products with original provenance;
5. a numerical or physical check appropriate to the task;
6. a solution or interpretation note; and
7. a limitation that prevents an over-broad claim.

Place the explanation, code, retained output, learner exercise, hint, and
worked solution in that order. A standalone code download is useful for
execution, but it should not become the only place where a reader can see the
case definition or interpret the result.

Do not reuse a paper figure, dataset panel, or code fragment merely because it
is publicly reachable. Check its licence and attribution requirements. The
schematic figures in this book were authored for the course; cited papers and
documentation are linked for reading rather than reproduced.

## Reference trail

### Further interactive study

[Dive into Deep Learning](https://d2l.ai/index.html) combines exposition,
mathematics, computational examples and exercises in one reading sequence.
For a physics-oriented progression, [Advanced Deep Learning for
Physics](https://tum-pbs.github.io/ADL4P/) connects numerical simulation,
sensitivity analysis and learning through longer assignments. These resources
informed the teaching format; the exercises and worked answers in this book
were written specifically for the PhAST course.

### Scientific references

The following sources support the formulation boundaries and teaching
conventions used here.

- A. A. Griffith, “The phenomena of rupture and flow in solids,”
  *Philosophical Transactions of the Royal Society A* 221 (1921),
  [DOI: 10.1098/rsta.1921.0006](https://doi.org/10.1098/rsta.1921.0006).
- G. A. Francfort and J.-J. Marigo, “Revisiting brittle fracture as an
  energy minimization problem,” *Journal of the Mechanics and Physics of
  Solids* 46 (1998),
  [DOI: 10.1016/S0022-5096(98)00034-9](https://doi.org/10.1016/S0022-5096(98)00034-9).
- B. Bourdin, G. A. Francfort, and J.-J. Marigo, “Numerical experiments in
  revisited brittle fracture,” *Journal of the Mechanics and Physics of
  Solids* 48 (2000),
  [DOI: 10.1016/S0022-5096(99)00028-9](https://doi.org/10.1016/S0022-5096(99)00028-9).
- C. Miehe, F. Welschinger, and M. Hofacker, “Thermodynamically consistent
  phase-field models of fracture: Variational principles and multi-field FE
  implementations,” *International Journal for Numerical Methods in
  Engineering* 83 (2010),
  [DOI: 10.1002/nme.2861](https://doi.org/10.1002/nme.2861).
- K. Pham, H. Amor, J.-J. Marigo, and C. Maurini, “Gradient damage models
  and their use to approximate brittle fracture,” *International Journal of
  Damage Mechanics* 20 (2011),
  [DOI: 10.1177/1056789510386852](https://doi.org/10.1177/1056789510386852).
- N. Moes, J. Dolbow, and T. Belytschko, “A finite element method for crack
  growth without remeshing,” *International Journal for Numerical Methods in
  Engineering* 46 (1999),
  [DOI: 10.1002/(SICI)1097-0207(19990910)46:1%3C131::AID-NME726%3E3.0.CO;2-J](https://doi.org/10.1002/(SICI)1097-0207(19990910)46:1%3C131::AID-NME726%3E3.0.CO;2-J).
- X.-P. Xu and A. Needleman, “Numerical simulations of fast crack growth in
  brittle solids,” *Journal of the Mechanics and Physics of Solids* 42
  (1994), [DOI: 10.1016/0022-5096(94)90003-5](https://doi.org/10.1016/0022-5096(94)90003-5).
- P. K. Kristensen, C. F. Niordson, and E. Martínez-Pañeda, “An assessment
  of phase field fracture: crack initiation and growth,” *Philosophical
  Transactions of the Royal Society A* 379 (2021),
  [DOI: 10.1098/rsta.2021.0021](https://doi.org/10.1098/rsta.2021.0021).
- PyTorch contributors, [Autograd documentation](https://docs.pytorch.org/docs/stable/autograd.html).
- JAX contributors, [Automatic differentiation guide](https://docs.jax.dev/en/latest/automatic-differentiation.html).
- JAX-FEM contributors, [Quickstart and examples](https://deepmodeling.github.io/jax-fem/guide/Quickstart.html).

## Final checklist

Before sharing an educational fracture result, make the reader able to answer:

- What is the crack representation?
- Which energy, convention, and constraint are used?
- Which mesh, boundary conditions, and fields are solved?
- Which quantity was observed and which check was applied?
- What is the scope of the conclusion?

If these answers are visible, the result is useful even when it is small.
