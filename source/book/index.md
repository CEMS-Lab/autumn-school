# PhAST: A Learn-by-Doing Introduction to Phase-Field Fracture

```{figure} figures/00_course_map.*
:name: fig-course-map
:width: 100%
:alt: Overview of the 6-hour workshop: 3 hours of interactive theory and demonstrations paired with 3 hours of hands-on computational lab exercises.

The workshop combines interactive lecture demonstrations with hands-on notebook activities across four core pillars of computational mechanics and scientific machine learning.
```

Welcome to this interactive tutorial guide on **phase-field fracture modeling and differentiable finite elements**. 

This guide connects continuum solid mechanics, numerical algorithms, and machine learning into a clear, hands-on learning route. Designed for students, researchers, and engineers with an undergraduate background in mechanics or computing, this course demystifies how cracks nucleate and evolve, how finite element equations are assembled in modern tensor frameworks like PyTorch, and how automatic differentiation enables inverse parameter discovery.

---

## Four Core Workshop Pillars

This course is organized into four key computational and physical milestones:

1. **What Phase-Field Fracture Is (Fundamentals):**  
   We begin with the physics of fracture, contrasting sharp cracks with smooth diffuse approximations. We study the Griffith energy balance, regularisation length scales ($\ell$), crack density functionals $\Gamma_\ell(d)$, and degradation laws $g(d)$ in AT1 and AT2 models.
2. **Hands-on with the PhAST Solver (Simulation Pipeline):**  
   We walk through an end-to-end simulation: creating a two-dimensional specimen geometry, generating a triangular (T3) mesh, prescribing displacement and precrack boundary conditions, running the staggered Newton/direct solver, and post-processing the resulting stress and diffuse damage fields.
3. **Differentiability and Inverse Problems (Sensitivities & Discovery):**  
   We explore how automatic differentiation operates on numerical mechanics solvers. We verify gradients by comparing PyTorch autograd with directional finite differences, backpropagate sensitivities through coupled equilibrium steps, and solve an inverse problem to recover unknown material properties (such as Young's modulus $E$).
4. **Deep Learning Integration (Plug-and-Play Surrogates):**  
   We examine how neural networks and operator learning interface with physics solvers. We train a neural adapter on simulation data, save and reload model checkpoints, evaluate neural field proposals against physical equilibrium residuals, and apply hybrid solver-in-the-loop corrections.

---

## Course Schedule & Hands-On Labs

The workshop is designed for a **six-hour curriculum**, divided into two complementary streams:
- **3 Hours of Interactive Demonstrations:** Concepts, mathematical derivations, numerical algorithms, and visual field walkthroughs.
- **3 Hours of Hands-on Lab Notebooks:** Interactive Jupyter tutorials where you run code, inspect fields, modify physical parameters, and solve guided exercises.

```{admonition} How to Use This Tutorial Guide
:class: tip

- **Read and Follow:** Each chapter introduces the physical intuition before deriving the governing equations and presenting the code.
- **Run the Notebooks:** Computational lessons can be read inline or executed interactively in Jupyter or Google Colab.
- **Explore and Modify:** Use the practice notebooks to test your understanding. Try varying the material parameters (such as fracture toughness $G_c$ or length scale $\ell$) to see how the physical crack pattern responds.
- **Notation Convention:** Throughout this guide, $d=0$ denotes completely intact material, while $d=1$ denotes fully damaged material. A small numerical residual stiffness $\eta_{\mathrm{res}} \ll 1$ is retained in computation to keep the linear elasticity operator well-conditioned.
```

For visual experiments alongside the text, explore the [interactive visual explorations](../explorations.html) or follow the [environment setup guide](../SETUP.md). Practice and solution notebooks are provided for each computational chapter.

```{toctree}
:maxdepth: 2
:numbered:

00_welcome_and_routes
01_crack_representations
02_phase_field_energy
03_staggered_solution
04_fem_to_tensors
05_differentiation_and_inverse
06_learning_adapter
07_practice_references
```

## Optional inverse experiments

The {doc}`inverse visual laboratory <research/08_visual_lab>` connects particle
geometry, sampled loss landscapes and retained fracture fields. Begin with
the {doc}`animated history lesson <research/03_history_visual>` to see how loading
and unloading change a derivative route. Select these readings to extend a
classroom topic or explore the subject after the course. The interactive panels
and animations accompany the downloadable notebooks and figures.

```{toctree}
:maxdepth: 1
:caption: Optional inverse experiments

research/index
```
