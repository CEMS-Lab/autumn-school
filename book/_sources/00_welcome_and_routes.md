# From Cracks to Computation: Learn by Doing

## Motivation and Learning Goals

Predicting when, where, and how materials break is one of the foundational challenges of modern solid mechanics. In traditional engineering, we often treat cracks as sharp geometric discontinuities. In modern computational physics and scientific machine learning, however, we represent cracks as continuous damage fields governed by energy minimization.

Interpreting a damage band, a softening reaction curve, or an automatically computed sensitivity gradient requires understanding the interplay between three distinct layers:
1. **The Physical Formulation:** The continuum theory and energy functional describing deformation and fracture.
2. **The Numerical Discretization:** The finite element interpolation, mesh geometry, and quadrature rules that translate continuous fields into discrete tensors.
3. **The Solution and Sensitivity Algorithm:** The nonlinear solver (such as staggered Newton iterations) and differentiation engine (such as reverse-mode automatic differentiation).

By the end of this workshop, you will be able to:
- **Understand Phase-Field Fracture:** Formulate the variational Griffith brittle fracture problem, explain the physical role of regularisation length $\ell$ and fracture toughness $G_c$, and contrast AT1 and AT2 models.
- **Run the PhAST Solver End-to-End:** Set up a two-dimensional domain, generate a triangular mesh, assign boundary conditions, execute the coupled staggered solve, and extract reaction forces and damage fields.
- **Differentiate Mechanics Computations:** Construct a computational graph in PyTorch, verify analytical and autograd derivatives against directional finite differences, and solve an inverse parameter identification problem.
- **Integrate Machine Learning Plug-and-Play:** Train neural operator adapters on field data, evaluate neural predictions against physical equilibrium residuals, and apply hybrid solver-in-the-loop corrections.

---

## Introductory Experiment: Multi-Valued Systems and Energy Objectives

Many non-linear physical systems exhibit multiple stable equilibrium states for a given set of boundary conditions. In our opening tutorial, we explore what happens when we train a learning model on data generated from multiple solution branches.

:::{admonition} Hands-On Tutorial: Lab 00 (Branch Selection & Energy Landscapes)
:class: tip

**Ready to try this in practice?**  
Explore the interactive tutorial: **{doc}`labs/00_why_average_predictions_can_fail`**.  
You can read through the worked derivations and energy plots directly here in the book, or run it interactively in **Google Colab** with one click:

<div class="badge-row">
  <a class="badge-colab" href="https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/00_why_average_predictions_can_fail.ipynb" target="_blank"><img src="_static/colab-badge.svg" alt="Open In Colab"/></a>
  <a class="badge-link" href="../notebooks/study/00_why_average_predictions_can_fail.ipynb"><i class="fa-solid fa-download"></i> Download Practice Notebook</a>
  <a class="badge-link" href="../notebooks/solutions/00_why_average_predictions_can_fail.ipynb"><i class="fa-solid fa-check-circle"></i> Download Worked Solutions</a>
</div>
:::

We compare two fundamental approaches:
- **Supervised Regression (Mean Squared Error):** Which naturally converges to conditional averages.
- **Physics-Informed Energy Minimization:** Which guides the model directly to physical equilibrium branches.

This motivating exercise illustrates a key takeaway: in physical problems, optimizing a physically grounded energy functional is often essential for capturing true physical branches.

---

## Course Workflow: Theory, Code, and Practice

This tutorial series pairs concise mathematical derivations with executable code:

1. **Physical Intuition First:** Every topic begins with the governing physical principles and intuitive sketches.
2. **Mathematical Formulation:** We write out governing equations, weak forms, and tensor operations clearly.
3. **Code Walkthrough:** Step-by-step implementation in PyTorch and PhAST, explaining key data structures and tensor dimensions.
4. **Physical Analysis:** Visualizing the resulting fields and discussing what the plots reveal about material behavior.
5. **Hands-On Exercises:** Each chapter concludes with conceptual questions and code tasks to solidify your understanding.

---

## Documenting Computational Experiments

Whenever you run a simulation or inverse optimization, it is good engineering practice to document four key aspects:

1. **Problem Definition:** Geometry, material properties ($E$, $\nu$, $G_c$), and boundary conditions.
2. **Numerical Discretization:** Mesh type (e.g., T3 triangles), characteristic element size $h$, quadrature order, and phase-field length scale $\ell$.
3. **Physical Observations:** Peak force, displacement at peak, crack nucleation point, and crack trajectory.
4. **Verification & Sensitivity:** Energy balance checks, residual tolerances, and comparisons across mesh refinements.

---

## What to Observe Before We Begin

Before opening the computational lessons, consider a simple intuitive question:
*If a rectangular specimen contains a sharp horizontal notch and is pulled vertically in tension, where should material damage first accumulate?*

As you run the simulations, observe how the high stress concentration at the notch tip naturally drives localized damage accumulation, causing a diffuse crack band to propagate across the specimen.

## Exercise: label the layers

Classify each statement as a fracture formulation, spatial discretisation,
solution/sensitivity method, or observable.

1. “Use a scalar damage field and a gradient penalty.”
2. “Add a discontinuous enrichment near a crack.”
3. “Alternate displacement and damage subproblems.”
4. “Compare reaction force against imposed displacement.”
5. “Differentiate a scalar loss with respect to a material multiplier.”

:::{admonition} Solution
:class: dropdown

1. A phase-field **fracture formulation**. The scalar field and gradient
   penalty define a regularised crack representation.
2. **Spatial discretisation**: this describes the central idea of XFEM.
3. A **solution method**: staggered solution can be applied to a chosen
   formulation and discretisation.
4. An **observable** derived from the computed state and boundary data.
5. A **sensitivity method/task**. Automatic differentiation or an adjoint
   computes a derivative for the chosen formulation and numerical model.
:::

## What to carry into the crack-representation chapter

Keep two questions visible: *what object represents the crack?* and *what
exactly is solved?* The next chapter places phase field, XFEM, and cohesive
models next to one another and identifies the role of each representation.
