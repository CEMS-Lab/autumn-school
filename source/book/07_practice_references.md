# Practice, Solutions, Glossary, and References

## Workshop Synthesis: The Four Core Milestones

The course connects fracture modelling, numerical solution, differentiation and learning. Use the following topics to review those connections.

1. **Pillar 1: What Phase-Field Fracture Is**  
   Explain how Griffith's surface energy is approximated by a volume integral over a continuous scalar damage field $d(x)$, governed by the regularisation length $\ell$, the crack-density function $w(d)$, and the stiffness degradation law $g(d)$.
2. **Pillar 2: Simulation with PhAST**
   Trace the geometry, mesh, boundary conditions, mechanical update and damage solve, and explain the resulting fields and energy histories.
3. **Pillar 3: Differentiation and Recovery**
   Explain how the chain rule produces a parameter gradient, compare it with a finite-difference check, and use it to estimate an unknown parameter.
4. **Pillar 4: Learning and Hybrid Correction**
   Explain the role of a learned prediction, assess its residuals and constraints, and compare the complete hybrid calculation with its numerical reference.

---

## Best Practices for Computational Exploration

When experimenting with computational mechanics models in Jupyter or Colab:

- **Vary One Parameter at a Time:** For example, change $\ell$ and examine the damage-band width, or change $G_c$ and compare the resulting peak load. Keep the other model inputs fixed and check that the mesh resolves each case.
- **Examine Both Fields and Curves:** Inspect the full spatial damage and stress fields alongside global load-displacement curves.
- **Verify Gradients Early:** When writing custom differentiable loss functions, verify gradients against finite differences before launching long optimization runs.
- **Check Physical Bounds:** Ensure the damage field respects $0 \le d \le 1$ and non-decreasing history $d_n \ge d_{n-1}$.

---

## Three classroom notebooks

| Practical | Focus |
| --- | --- |
| {doc}`Lab 1 — Simulate fracture <classroom/01_simulate_fracture>` | Geometry, supports, loading, PhAST results and their interpretation. |
| {doc}`Lab 2 — Gradients and recovery <classroom/02_gradients_and_recovery>` | One force, one tip observation and Young’s-modulus recovery through PhAST. |
| {doc}`Lab 3 — Learned damage updates <classroom/03_learning_and_hybrid>` | Frozen graph-network predictions, classical correction and checked direct replacement on a three-hole plate. |

Each page includes Google Colab, notebook downloads and a conceptual answer.
The learned lab needs the instructor-supplied checkpoint. Visit
{doc}`further_practice` for the original individual notebooks and longer
implementation walkthroughs.

## Continue with the PhAST documentation

The [PhAST tutorial sequence](https://cems-lab.github.io/PhAST/tutorial/index.html)
extends the same workflow used here: define a specimen, inspect mesh regions,
apply supports and loading, solve, and interpret the saved fields.

| Activity | Physical question | Next reading |
| --- | --- | --- |
| Course Lab 01 | How do a graded mesh and imposed separation affect dynamic crack growth? | Inspect displacement, strain, stress and damage animations in the square-plate notebook. |
| PhAST SENT setup | How do a Gmsh geometry and named regions become a configured problem? | [Step-by-step problem setup](https://cems-lab.github.io/PhAST/tutorial/notebook_setup.html) |
| B3 dynamic SENT results | How does a damaged band extend across a tensile specimen during a dynamic calculation? | [Public B3 example and retained animation](https://github.com/CEMS-Lab/PhAST/tree/f6324f899f0701769810be117f27f1208f7a582e/examples/dynamic/B3_dynamic_sent) |

B3 uses a 40 mm square with a 20 mm notch and explicit dynamics. Its retained
animation provides a qualitative crack-growth example. When comparing it with
Lab 01, identify the geometry, units, loading history and inertial terms in each
model. For a fresh B3 calculation, review its configuration and mesh resolution
and measure the complete runtime in your environment.

## Worked consolidation exercise

Consider a two-dimensional notched specimen represented by displacement $u$
and damage $d$. The calculation uses a length scale $\ell$, a residual
stiffness $\eta_{\mathrm{res}}$, and a displacement-controlled load increment.

1. Identify the local damage term, the gradient term and the energy prefactor in the fracture contribution.
2. Write the qualitative order of a staggered update.
3. Name two visual outputs and one scalar output you would retain.
4. A learned model proposes $d$. Name two checks required before using it as a
   starting point for a mechanics update.
5. State a conclusion supported by the exercise and identify an additional
   study needed to apply it more broadly.

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
5. The result describes the defined discretisation and load path. Material
   calibration requires experimental comparison, mesh independence requires
   refinement, and acceleration requires matched measurements of the full
   computational cost.
:::

## Glossary

**Adapter**
: A declared map that changes a data representation, for example node order,
  units, or tensor layout, with physical meaning checked across the mapping.

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
: The condition that brittle damage is nondecreasing over the stated loading
  history.

**Matrix-free action**
: An implementation of $v\mapsto Kv$ or a Jacobian action using local operator
  evaluations and accumulation into global degrees of freedom.

**Phase-field fracture**
: A regularised fracture formulation in which a diffuse scalar field
  approximates a sharp crack surface.

**Quadrature**
: Numerical integration on an element using selected points and weights.

**Quasi-Newton method**
: A nonlinear optimisation/solution strategy that updates an approximate
  Jacobian or inverse Jacobian for a chosen system of equations.

**Residual**
: The imbalance in a stated discrete equation. Interpret a residual norm
  using its definition, scaling, tolerance, and field context.

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
4. labelled figures or datasets with their sources and processing steps;
5. a numerical or physical check appropriate to the task;
6. a solution or interpretation note; and
7. the assumptions and scope of the result.

Place the explanation, code, retained output, learner exercise, hint, and
worked solution in that order. Include the case definition and interpretation
in the chapter as well as in the downloadable code.

Check the licence and attribution requirements before reusing a paper figure,
dataset panel, or code fragment. The schematic figures in this book were
authored for the course; cited papers and documentation provide further reading.

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

The original diagrams also draw visual-design inspiration from the
[TU Delft surrogate-model explanation](https://teachbooks.tudelft.nl/computational-modelling/advanced_topics/multiscale/surrogate.html),
[TUM's differentiable-physics lecture](https://tum-pbs.github.io/ADL4P/slides/ADL4P%203%20-%20Differentiable%20Physics%20II.pdf)
and the [ETH Zurich SPCL DaCeML research presentation](https://spcl.inf.ethz.ch/Publications/.pdf/daceml-slides.pdf).
These sources illustrate labelled physical interfaces, aligned forward and
reverse paths, and overview-to-detail explanations. The original course
diagrams adapt these design principles to the notation and models used here.

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
