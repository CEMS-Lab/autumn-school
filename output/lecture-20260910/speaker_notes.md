# Animated lecture speaker notes

## 1. Numerical methods
and deep learning

Delivery placement: L1.

Introduce the numerical questions that connect phase-field fracture to differentiable simulation. The course develops the fracture model, computes a small example and uses sensitivities to guide inverse recovery and learning.

Sources and provenance:
User-created Physics Constrained Differentiable Solver Key Points.key, exported 9 September 2026.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 2. The six-hour learning sequence

Delivery placement: L1.

The live route has 180 minutes of lectures followed by 180 minutes of practical work. Select the diffusion lesson within the second practical. The teaching schedule supplies the detailed allocation.

Sources and provenance:
COURSE_PLAN.md; TEACHING_SCHEDULE.md; MVP_DELIVERY.md.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 3. A crack represented by a damage field

Delivery placement: L1.

Define displacement u, small strain, undamaged energy density, toughness Gc, regularisation length ell and external work. Use d=0 for intact material and d=1 for damaged material. AT2 has c0=2. This isotropic energy matches the quick PhAST exercise. Introduce irreversibility as a separate constraint.

Sources and provenance:
Course source/book/02_phase_field_energy.md; Miehe et al. (2010), https://doi.org/10.1002/nme.2861; Bourdin et al. (2000), https://doi.org/10.1016/S0022-5096(99)00028-9.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 4. The length scale controls the crack band

L1 · 13–26 min. Analytic isolated AT2 profile. Lengths use one arbitrary unit.

Play the 24.8-second clip. Pause around 15 seconds.
Ask: How should the mesh change when the regularisation length is halved?

Discussion: Keep the mesh-to-length-scale ratio comparable: halving the length scale suggests halving the local mesh spacing, followed by a resolution study.

Static fallback: media/phase_field_band_poster.png. Describe the same sequence from its poster.
Replay from the beginning after discussion. The clip is embedded in this deck and needs no network connection.

Original source: source/animations/mechanics_scenes.py: PhaseFieldBand

Created by Allamaprabhu Ani, CEMS-Lab, for the UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 5. How damage changes stiffness

Delivery placement: L1.

Read the degradation curve and its slope together. Eta supplies residual stiffness. The figure uses eta=1e-6 and the numerical practical uses 1e-7. The quadratic baseline is paired with illustrative cubic and rational functions. Distinguish degradation g from the crack-density function w.

Sources and provenance:
Original course figure build_beamer_figures.py and latex_figures/analytic_plot_data.json; public PhAST quadratic law pinned f6324f899f0701769810be117f27f1208f7a582e.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 6. The staggered solution

Delivery placement: L1.

Follow the data dependencies. Mechanics receives the latest damage, and the updated driving or history field enters the damage problem. Enforce prescribed values and irreversibility. A staggered algorithm can combine dynamic mechanics and implicit damage. The classroom PhAST example uses quasistatic mechanics.

Sources and provenance:
Course source/book/03_staggered_solution.md; vendor/PhAST/src/phast/solvers/staggered.py.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 7. Follow one partitioned dynamic update

L1 · 26–40 min. Partitioned dynamic schematic. The PhAST practical uses quasistatic mechanics.

Play the 26.5-second clip. Pause around 11 seconds.
Ask: Which fields are held fixed during the mechanics and damage updates?

Discussion: The explicit mechanics update uses the accepted damage. Its updated tensile energy and stored history drive the implicit damage problem. Describe the time-step stability and acceptance checks before advancing.

Static fallback: media/explicit_implicit_step_poster.png. Describe the same sequence from its poster.
Replay from the beginning after discussion. The clip is embedded in this deck and needs no network connection.

Original source: source/animations/mechanics_scenes.py: ExplicitImplicitStep

Created by Allamaprabhu Ani, CEMS-Lab, for the UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 8. Finite elements as tensor operations

Delivery placement: L1.

Define each tensor axis and the connectivity-based gather and scatter operations. Tensor notation expresses batched element calculations. Matrix-free evaluation applies the global operator through local operations. The quick forward practical uses assembled SciPy sparse-direct mechanics.

Sources and provenance:
Course source/book/04_fem_to_tensors.md; public PhAST source pin f6324f899f0701769810be117f27f1208f7a582e.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 9. A mesh, a prescribed notch and boundary values

Delivery placement: L1.

The practical fixes ux=0 on all outer boundaries and splits the total opening between top and bottom. Prescribed damaged nodes represent the initial notch. The load factor runs from .0125 to 1 over 60 increments. Read the effective configuration used by the solve and compare it with the mesh and boundary diagram.

Sources and provenance:
Original BC schematic based on notebooks/day2_helpers/course_tools.py and public symmetric_tension_bcs; no new fracture solve.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 10. Read the field as well as the response

Delivery placement: L1.

Compare the prescribed seed, first solution and final field on one damage scale. These figures display the retained course calculation. Read the reaction trace and convergence diagnostics alongside the field. Use the execution receipt for the measured environment and runtime.

Sources and provenance:
source/slides/latex_figures/forward_fields.npz; forward_summary.json; evidence/notebook_runtime.json; evidence/package_rehearsal.json.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 11. From an input to a final observation

Delivery placement: L2.

Define the state vector z, parameter p, observation map C and fixed target. This example uses a fixed initial state and parameter dependence through the updates. Differentiation gives dJ/dp. An optimisation method then uses that gradient to choose a parameter update.

Sources and provenance:
Course source/book/05a_backpropagation_step_by_step.md; https://physicsbaseddeeplearning.org/diffphys.html.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 12. The backward pass through time steps

Delivery placement: L2.

Use column adjoints. Seed the terminal adjoint from the loss, propagate with local transposed state Jacobians and accumulate the parameter-Jacobian products at every use of p. Evaluate vector-Jacobian products directly. Direct loss dependence and parameter-dependent initial states contribute additional terms in the general case.

Sources and provenance:
Original course derivation source/book/05a_backpropagation_step_by_step.md; PyTorch autograd documentation; https://physicsbaseddeeplearning.org/diffphys.html.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 13. Every use of a parameter contributes

L2 · 22–35 min. Two differentiable updates; fixed initial state; terminal scalar loss.

Play the 27.7-second clip. Pause around 15 seconds.
Ask: Why does the final derivative contain one contribution from each update?

Discussion: The shared parameter enters both update maps. Reverse accumulation propagates the terminal loss sensitivity through the state path and adds the local parameter-Jacobian products at both uses. The clip uses x, theta and L for the state, parameter and loss denoted z, p and J in the preceding slides.

Static fallback: media/reverse_accumulation_poster.png. Describe the same sequence from its poster.
Replay from the beginning after discussion. The clip is embedded in this deck and needs no network connection.

Original source: source/animations/learning_scenes.py: ReverseAccumulation

Created by Allamaprabhu Ani, CEMS-Lab, for the UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 14. Implicit differentiation of a solved equation

Delivery placement: L2.

Rz and Rp are the residual Jacobians with respect to the state and parameter. Solve the transposed state system against the state loss gradient, then form the total parameter derivative. Unrolling differentiates the executed iterations. Implicit differentiation describes a local converged root with a differentiable residual and nonsingular state Jacobian. Treat active-set changes separately.

Sources and provenance:
Course source/book/05_differentiation_and_inverse.md; Ceyron adjoint_linear_system_example.py, commit a2e50a9df4bb6e938901b33fd957c06ac06b5224, pedagogical reference only.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 15. Stored history selects the active sensitivity

L2 · 35–45 min. Dimensionless material-point teaching example. Green: surrogate reverse weights.

Play the 18-second clip. Pause around 10 seconds.
Ask: During unloading below the previous peak, which input receives the hard-history sensitivity?

Discussion: For H_new=max(H_old, psi), the old history receives the derivative when psi<H_old; the current energy receives it when psi>H_old. At equality the maximum is nonsmooth. The displayed 0.5 marker is a selected tie convention. The green sigmoid weights define a surrogate backward rule; they describe a different derivative rule from the hard maximum away from the branch transition as well.

Static fallback: media/history_switch_poster.png. Describe the same sequence from its poster.
Replay from the beginning after discussion. The clip is embedded in this deck and needs no network connection.

Original source: source/book/research/code/history_animation.py; history_lesson.py

Created by Allamaprabhu Ani, CEMS-Lab, for the UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 16. Check the derivative before using it

Delivery placement: L2.

Compare automatic differentiation, an independent analytical or manual derivative and central finite differences at several spacings. Use float64 and a fixed discretisation. Interpret error through truncation and roundoff. For a quadratic, central differences are exact in real arithmetic. Inverse uniqueness depends on observation sensitivity and parameterisation.

Sources and provenance:
Course notebooks/02_degradation_autograd.ipynb; new diffusion draft; https://docs.pytorch.org/docs/stable/notes/autograd.html.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 17. A small time-stepping notebook

Delivery placement: L2.

The one-dimensional diffusion lesson makes shared-parameter accumulation explicit. Forward Euler with the central stencil requires alpha*dt/dx^2<=1/2. The bounded parameter interval and fixed time step respect this condition. Students read short update loops, compare derivatives and recover a diffusivity from a synthetic target.

Sources and provenance:
notebooks/drafts/06_differentiability_step_by_step.ipynb; original code. Cell sequencing inspired by Felix Köhler, hybridization-in-jax/first_data_assimilation.ipynb at61ee2629f5800d92fba64492a0f81efe3a6a7c39; no code copied.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 18. What learning can contribute

Delivery placement: L3 / practical bridge.

A learned relation can approximate a material response, supply a proposal or support repeated queries. Compare the complete cost of data generation, training, prediction and correction for the intended range of loads and geometries.

Sources and provenance:
Course source/book/06_learning_adapter.md; Physics-Based Deep Learning, https://physicsbaseddeeplearning.org/diffphys.html

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 19. What a prediction must satisfy

Delivery placement: L3 / practical bridge.

Separate approximation, discretisation and optimisation errors. A soft physics penalty enters the objective. Exact constraints enforce a relation by construction. Evaluate both approaches in the intended physical setting.

Sources and provenance:
Course source/book/06_learning_adapter.md.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 20. Coupling a network and a solver

Delivery placement: L3 / practical bridge.

The first diagram shows inference through a compatible model interface. The second shows a training objective evaluated after a differentiable solve. Reverse-mode differentiation propagates the loss sensitivity through each intervening operation to the model weights. The classroom adapter uses a Helmholtz-type teaching equation.

Sources and provenance:
Original diagram; course source/book/06_learning_adapter.md; https://physicsbaseddeeplearning.org/diffphys.html

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 21. A learned field enters a checked interface

L3 · 32–45 min. Interface schematic. Practical models: MLP/RBF on a Helmholtz-type teaching field.

Play the 26.5-second clip. Pause around 15 seconds.
Ask: Which checks should a proposed damage field satisfy before the simulation accepts it?

Discussion: Check the declared node/graph ordering, units, normalisation and output location first. Check prescribed values, bounds, irreversibility and the declared residual tolerance. A corrected state is checked again. The graphic names Radius GNO/GNN as possible architecture contracts; the practical trains MLP/RBF models for a Helmholtz-type field problem. Total cost includes graph construction, prediction, conversion, checks and correction.

Static fallback: media/checked_learned_proposal_poster.png. Describe the same sequence from its poster.
Replay from the beginning after discussion. The clip is embedded in this deck and needs no network connection.

Original source: source/animations/learning_scenes.py: CheckedLearnedProposal

Created by Allamaprabhu Ani, CEMS-Lab, for the UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 22. Keep a reproducible numerical experiment

Delivery placement: L3 / practical bridge.

NPZ stores named arrays, JSON stores scalar metadata and histories, and PNG or PDF stores figures. A .pt model checkpoint additionally needs its feature and normalisation contract. The current forward archive contains nodes, elements, prescribed damage and damage snapshots. Explain how those fields support the plotted results.

Sources and provenance:
source/planning/PRACTICAL_SEQUENCE_AUDIT_20260909.md; notebooks/day2_helpers/course_tools.py.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.

## 23. The practical learning cycle

Delivery placement: L3 / practical bridge.

Ask students to predict, run a small calculation and explain the result. Separate setup from numerical execution. Use the recorded outputs for discussion and the downloadable notebook for experimentation. The course computational budget is 300 seconds per task after setup.

Sources and provenance:
Ceyron notebook references: source/planning/CEYRON_NOTEBOOK_DESIGN.md; D2L and Physics-Based Deep Learning supplied by the user as pedagogical references.

Course material created by Allamaprabhu Ani, CEMS-Lab, UKACM Autumn School 2026. Presented by Sathiskumar A. Ponnusami, Queen Mary University of London.
