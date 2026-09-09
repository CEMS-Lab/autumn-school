## 1. Numerical methods and deep learning

Introduce the numerical questions that connect phase-field fracture to differentiable simulation. The course develops the fracture model, computes a small example and uses sensitivities to guide inverse recovery and learning.

User-created Physics Constrained Differentiable Solver Key Points.key, exported 9 September 2026.

## 2. What learning can contribute

A learned relation can approximate a material response, supply a proposal or support repeated queries. Compare the complete cost of data generation, training, prediction and correction for the intended range of loads and geometries.

Course source/book/06_learning_adapter.md; Physics-Based Deep Learning, https://physicsbaseddeeplearning.org/diffphys.html

## 3. What a prediction must satisfy

Separate approximation, discretisation and optimisation errors. A soft physics penalty enters the objective. Exact constraints enforce a relation by construction. Evaluate both approaches in the intended physical setting.

Course source/book/06_learning_adapter.md.

## 4. Coupling a network and a solver

The first diagram shows inference through a compatible model interface. The second shows a training objective evaluated after a differentiable solve. Reverse-mode differentiation propagates the loss sensitivity through each intervening operation to the model weights. The classroom adapter uses a Helmholtz-type teaching equation.

Original diagram; course source/book/06_learning_adapter.md; https://physicsbaseddeeplearning.org/diffphys.html

## 5. The six-hour learning sequence

The live route has 180 minutes of lectures followed by 180 minutes of practical work. Select the diffusion lesson within the second practical. The teaching schedule supplies the detailed allocation.

COURSE_PLAN.md; TEACHING_SCHEDULE.md; MVP_DELIVERY.md.

## 6. A crack represented by a damage field

Define displacement u, small strain, undamaged energy density, toughness Gc, regularisation length ell and external work. Use d=0 for intact material and d=1 for damaged material. AT2 has c0=2. This isotropic energy matches the quick PhAST exercise. Introduce irreversibility as a separate constraint.

Course source/book/02_phase_field_energy.md; Miehe et al. (2010), https://doi.org/10.1002/nme.2861; Bourdin et al. (2000), https://doi.org/10.1016/S0022-5096(99)00028-9.

## 7. How damage changes stiffness

Read the degradation curve and its slope together. Eta supplies residual stiffness. The figure uses eta=1e-6 and the numerical practical uses 1e-7. The quadratic baseline is paired with illustrative cubic and rational functions. Distinguish degradation g from the crack-density function w.

Original course figure build_beamer_figures.py and latex_figures/analytic_plot_data.json; public PhAST quadratic law pinned f6324f899f0701769810be117f27f1208f7a582e.

## 8. The staggered solution

Follow the data dependencies. Mechanics receives the latest damage, and the updated driving or history field enters the damage problem. Enforce prescribed values and irreversibility. A staggered algorithm can combine dynamic mechanics and implicit damage. The classroom PhAST example uses quasistatic mechanics.

Course source/book/03_staggered_solution.md; vendor/PhAST/src/phast/solvers/staggered.py.

## 9. Finite elements as tensor operations

Define each tensor axis and the connectivity-based gather and scatter operations. Tensor notation expresses batched element calculations. Matrix-free evaluation applies the global operator through local operations. The quick forward practical uses assembled SciPy sparse-direct mechanics.

Course source/book/04_fem_to_tensors.md; public PhAST source pin f6324f899f0701769810be117f27f1208f7a582e.

## 10. From an input to a final observation

Define the state vector z, parameter p, observation map C and fixed target. This example uses a fixed initial state and parameter dependence through the updates. Differentiation gives dJ/dp. An optimisation method then uses that gradient to choose a parameter update.

Course source/book/05a_backpropagation_step_by_step.md; https://physicsbaseddeeplearning.org/diffphys.html.

## 11. The backward pass through time steps

Use column adjoints. Seed the terminal adjoint from the loss, propagate with local transposed state Jacobians and accumulate the parameter-Jacobian products at every use of p. Evaluate vector-Jacobian products directly. Direct loss dependence and parameter-dependent initial states contribute additional terms in the general case.

Original course derivation source/book/05a_backpropagation_step_by_step.md; PyTorch autograd documentation; https://physicsbaseddeeplearning.org/diffphys.html.

## 12. Implicit differentiation of a solved equation

Rz and Rp are the residual Jacobians with respect to the state and parameter. Solve the transposed state system against the state loss gradient, then form the total parameter derivative. Unrolling differentiates the executed iterations. Implicit differentiation describes a local converged root with a differentiable residual and nonsingular state Jacobian. Treat active-set changes separately.

Course source/book/05_differentiation_and_inverse.md; Ceyron adjoint_linear_system_example.py, commit a2e50a9df4bb6e938901b33fd957c06ac06b5224, pedagogical reference only.

## 13. Check the derivative before using it

Compare automatic differentiation, an independent analytical or manual derivative and central finite differences at several spacings. Use float64 and a fixed discretisation. Interpret error through truncation and roundoff. For a quadratic, central differences are exact in real arithmetic. Inverse uniqueness depends on observation sensitivity and parameterisation.

Course notebooks/02_degradation_autograd.ipynb; new diffusion draft; https://docs.pytorch.org/docs/stable/notes/autograd.html.

## 14. A small time-stepping notebook

The one-dimensional diffusion lesson makes shared-parameter accumulation explicit. Forward Euler with the central stencil requires alpha*dt/dx^2<=1/2. The bounded parameter interval and fixed time step respect this condition. Students read short update loops, compare derivatives and recover a diffusivity from a synthetic target.

notebooks/drafts/06_differentiability_step_by_step.ipynb; original code. Cell sequencing inspired by Felix Köhler, hybridization-in-jax/first_data_assimilation.ipynb at61ee2629f5800d92fba64492a0f81efe3a6a7c39; no code copied.

## 15. A mesh, a prescribed notch and boundary values

The practical fixes ux=0 on all outer boundaries and splits the total opening between top and bottom. Prescribed damaged nodes represent the initial notch. The load factor runs from .0125 to 1 over 60 increments. Read the effective configuration used by the solve and compare it with the mesh and boundary diagram.

Original BC schematic based on notebooks/day2_helpers/course_tools.py and public symmetric_tension_bcs; no new fracture solve.

## 16. Read the field as well as the response

Compare the prescribed seed, first solution and final field on one damage scale. These figures display the retained course calculation. Read the reaction trace and convergence diagnostics alongside the field. Use the execution receipt for the measured environment and runtime.

source/slides/latex_figures/forward_fields.npz; forward_summary.json; evidence/notebook_runtime.json; evidence/package_rehearsal.json.

## 17. Keep a reproducible numerical experiment

NPZ stores named arrays, JSON stores scalar metadata and histories, and PNG or PDF stores figures. A .pt model checkpoint additionally needs its feature and normalisation contract. The current forward archive contains nodes, elements, prescribed damage and damage snapshots. Explain how those fields support the plotted results.

source/planning/PRACTICAL_SEQUENCE_AUDIT_20260909.md; notebooks/day2_helpers/course_tools.py.

## 18. The practical learning cycle

Ask students to predict, run a small calculation and explain the result. Separate setup from numerical execution. Use the recorded outputs for discussion and the downloadable notebook for experimentation. The course computational budget is 300 seconds per task after setup.

Ceyron notebook references: source/planning/CEYRON_NOTEBOOK_DESIGN.md; D2L and Physics-Based Deep Learning supplied by the user as pedagogical references.
