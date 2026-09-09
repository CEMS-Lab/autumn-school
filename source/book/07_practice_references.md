# Practice, Solutions, Glossary, and References

## Workshop Synthesis: The Four Core Milestones

Throughout this tutorial course, we navigated the bridge connecting continuum fracture mechanics to modern differentiable scientific computing and machine learning. As a review, ensure you can comfortably explain the four foundational milestones:

1. **Pillar 1: What Phase-Field Fracture Is**  
   Explain how Griffith's surface energy is approximated by a volume integral over a continuous scalar damage field $d(x)$, governed by the regularisation length $\ell$, the crack-density function $w(d)$, and the stiffness degradation law $g(d)$.
2. **Pillar 2: The Computational Simulation Pipeline (PhAST)**  
   Trace an end-to-end simulation: defining domain coordinates and connectivity, assembling finite element tensors, applying boundary conditions and precracks, and executing the staggered alternating minimization loop until equilibrium residuals converge.
3. **Pillar 3: Differentiability and Inverse Discovery**  
   Explain how reverse-mode automatic differentiation computes exact sensitivities through numerical mechanics graphs, verify autograd gradients against directional numerical finite differences, and formulate gradient-based inverse optimization to recover unknown physical parameters.
4. **Pillar 4: Deep Learning Surrogates and Hybrid Correction**  
   Formulate how neural networks can serve as fast surrogate proposal models, evaluate neural predictions against physical PDE residuals, and use trusted numerical solvers in a hybrid loop to correct out-of-distribution predictions.

---

## Best Practices for Computational Exploration

When experimenting with computational mechanics models in Jupyter or Colab:

- **Vary One Parameter at a Time:** For example, decrease $\ell$ to observe crack bandwidth narrowing, or increase $G_c$ to observe higher fracture toughness and peak load.
- **Examine Both Fields and Curves:** Do not rely solely on scalar metrics. Always inspect the full spatial damage and stress fields alongside global load-displacement curves.
- **Verify Gradients Early:** When writing custom differentiable loss functions, verify gradients against finite differences before launching long optimization runs.
- **Check Physical Bounds:** Ensure the damage field respects $0 \le d \le 1$ and non-decreasing history $d_n \ge d_{n-1}$.

---

## Complete Notebook Index & Google Colab Links

Use the quick-reference table below to open any course notebook directly in **Google Colab**, or download the practice and solution notebooks for offline study:

| Lab Tutorial | Topic & Pillar | Launch in Colab | Practice Notebook | Worked Solutions | Relevant Theory |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **{doc}`Lab 00 <labs/00_why_average_predictions_can_fail>`** | **Branch Selection & Energy Objectives** | [![Open In Colab](_static/colab-badge.svg)](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/00_why_average_predictions_can_fail.ipynb) | [Practice .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/study/00_why_average_predictions_can_fail.ipynb) | [Solutions .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/solutions/00_why_average_predictions_can_fail.ipynb) | {doc}`00_welcome_and_routes` |
| **{doc}`Lab 01 <labs/01_phast_tiny_evolving_fracture>`** | **End-to-End PhAST Simulation** | [![Open In Colab](_static/colab-badge.svg)](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/01_phast_tiny_evolving_fracture.ipynb) | [Practice .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/study/01_phast_tiny_evolving_fracture.ipynb) | [Solutions .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/solutions/01_phast_tiny_evolving_fracture.ipynb) | {doc}`04_fem_to_tensors` |
| **{doc}`Lab 02 <labs/02_degradation_autograd>`** | **Autograd vs. Finite Differences** | [![Open In Colab](_static/colab-badge.svg)](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/02_degradation_autograd.ipynb) | [Practice .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/study/02_degradation_autograd.ipynb) | [Solutions .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/solutions/02_degradation_autograd.ipynb) | {doc}`02_phase_field_energy` |
| **{doc}`Lab 03 <labs/03_tiny_derivative_inverse_toy>`** | **Inverse Parameter Discovery** | [![Open In Colab](_static/colab-badge.svg)](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/03_tiny_derivative_inverse_toy.ipynb) | [Practice .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/study/03_tiny_derivative_inverse_toy.ipynb) | [Solutions .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/solutions/03_tiny_derivative_inverse_toy.ipynb) | {doc}`05_differentiation_and_inverse` |
| **{doc}`Lab 04 <labs/04_train_save_reload_adapter>`** | **Neural Field Adapter** | [![Open In Colab](_static/colab-badge.svg)](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/04_train_save_reload_adapter.ipynb) | [Practice .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/study/04_train_save_reload_adapter.ipynb) | [Solutions .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/solutions/04_train_save_reload_adapter.ipynb) | {doc}`06_learning_adapter` |
| **{doc}`Lab 05 <labs/05_hybrid_reference_correction>`** | **Residual Evaluation & Hybrid Correction** | [![Open In Colab](_static/colab-badge.svg)](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/05_hybrid_reference_correction.ipynb) | [Practice .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/study/05_hybrid_reference_correction.ipynb) | [Solutions .ipynb](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/solutions/05_hybrid_reference_correction.ipynb) | {doc}`06_learning_adapter` |

---

## Worked consolidation exercise

Consider a two-dimensional notched specimen represented by displacement $u$
and damage $d$. The calculation uses a length scale $\ell$, a residual
stiffness $\eta_{\mathrm{res}}$, and a displacement-controlled load increment.

1. Give the three terms in the fracture density that regularise a sharp crack.
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
4. labelled figures or data products with original provenance;
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
