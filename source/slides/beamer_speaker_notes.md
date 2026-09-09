# Instructor notes — PhAST six-hour course

Primary source: `phast_autumn_school_2026.tex`. These are the same notes embedded in the Beamer source.

Three 120-minute sections; each contains 110 minutes of instruction/activity and one 10-minute break. Relative teaching timings are not event-timetable claims or compute-runtime measurements.

## 1. From cracks to computation

Timing: Opening

Introduce the 2+2+2-hour design. Each section includes a ten-minute break. The event allocation is separate and must be agreed with the organiser. The title illustration is an original analytic-distance schematic, not a computed fracture field.

## 2. One specimen. Three learning questions.

Timing: Orientation

Introduce the companion book and notebook routes. Notebook 01 is a real PhAST damage-evolution solve; notebooks 02--05 teach local differentiation, an elastic-bar inverse toy and a Helmholtz-like field model/adapter. The distinctions remain visible throughout. Discussion prompt: Take away one executed notebook and one comparison sheet.

## 3. Understand the crack

Timing: Session A / 00--10

Ten-minute opening prediction activity. Ask where a centreline precrack in tension will localise damage. Damage is not displacement jump or crack opening. A schematic can support a hypothesis; an actual field and its loading history are needed to test it.

## 4. Three descriptions of an evolving crack

Timing: A 10--22 / 12 minutes

Compare the same conceptual specimen. XFEM is an enrichment strategy and CZM a constitutive traction--separation law, not mutually exclusive rival generations. A phase-field-CZM exists. Discuss interface knowledge, path complexity, calibration and computational cost without claiming universal superiority. Discussion prompt: An adhesive interface? An unknown branching path?

## 5. A model is not a solution algorithm

Timing: A 22--25 / 3 minutes

Use the question for retrieval. Classify each term before describing advantages. Distinguish an FE enrichment from the physical constitutive relation and the nonlinear algorithm. Discussion prompt: Can quasi-Newton solve a phase-field system?

## 6. Fracture balances storage and crack cost

Timing: A 25--37 / 12 minutes

Build the two lines term by term. Define displacement u, small strain, damage d, toughness Gc and length ell. The normalisation is c0=4 integral from 0 to 1 of sqrt(w(s)) ds. This representative tension/compression split is not the unique phase-field model. Ask learners to identify storage reduction and crack cost. Discussion prompt: Which term favours damage? Which term resists it?

## 7. AT1 and AT2 choose the crack-density term

Timing: A 37--45 / 8 minutes

Compute c0 for w=d and w=d squared. Note that onset also depends on degradation, split, loading, flaw, length and calibration. The statement about an elastic stage describes the standard idealisations, not every calibrated extension. Maintain the d=0 intact convention consistently.

## 8. How quickly should stiffness be lost?

Timing: A 45--53 / 8 minutes

Predict before explaining. Quadratic law exactly matches the selected PhAST baseline. Cubic illustration: (1-eta)(1-3d squared+2d cubed)+eta. Rational illustration: (1-eta)(1-d) squared/[(1-d) squared+a d(1+d)]+eta, a=2. For a>0 its denominator is positive on [0,1]. These illustrations are not calibrated PF-CZM.

## 9. A derivative measures the local energy response

Timing: A 53--60 / 7 minutes, then break 60--70

Predict g prime at d=0.25. The illustrative plot uses eta=1e-6, giving -1.4999985. Notebook 02 uses eta=1e-7, giving -1.49999985. Explain local AD and later revisit the full computational path. Take the ten-minute comfort break. Discussion prompt: Why is $g'$ negative?

## 10. A diffuse crack has a spatial profile

Timing: A 70--78 / 8 minutes

Read the horizontal axis as x/ell. Explain exponential tail versus compact support and how ell scales both. These are crack-density minimisers, not measured crack openings, stress fields or full fracture solutions. Discussion prompt: Tail or compact support?

## 11. The mesh must resolve the chosen length

Timing: A 78--85 / 7 minutes

Ask whether one element across a band can describe it. Hold ell and physical parameters fixed while refining h. Compare full damage fields, load response and energies. Changing ell can alter nucleation/strength and requires separate calibration. Mesh visibility is not convergence. Discussion prompt: Refine $h$ at fixed $\ell$. What should you compare?

## 12. Initiation is not propagation or branching

Timing: A 85--90 / 5 minutes

The initiation sketch is a shorter precrack; the other two are different conceptual states, not results from one run. Discuss flaw, strength, loading and regularisation. Dynamic branching requires a physical time history and a converged path-instability calculation. Notebook 01 demonstrates quasi-static damage evolution, not branching.

## 13. A staggered step alternates coupled problems

Timing: A 90--100 / 10 minutes

Trace an outer load increment and inner staggered iterations. Mechanics uses current damage; the driving/history field depends on tensile energy; damage uses updated driving. Keep prescribed damage and irreversibility. Advance only under the chosen convergence checks. Analogy: a gradient term resembles a diffusion operator, but damage is not mass-conserving transport. Discussion prompt: Which field is held fixed in each subproblem?

## 14. Time integration and nonlinear iteration are different

Timing: A 100--108 / 8 minutes

Separate physical modelling, time discretisation, nonlinear solve and staggered coupling. Static means no inertia in the balance; quasi-static follows equilibrium along a loading history. Explain acceleration in dynamic mechanics and the distinction between algorithmic iteration k and time n.

## 15. Matrix-free means applying an operator

Timing: A 108--114 / 6 minutes

Explain the action of gather/scatter operators A_e. Assembly, local kernels and boundary handling differ by route. Preconditioning and convergence remain important. Notebook 01 actually uses an assembled SciPy mechanics backend; it does not benchmark matrix-free acceleration. No speed claim is made here. Discussion prompt: What is avoided? What work remains?

## 16. Tensors still have physical locations

Timing: A 114--120 / 6 minutes

Retrieval: trace one element from connectivity through quadrature to global accumulation. Shapes alone do not identify units or location. Ask why a smooth damage band still needs spatial resolution and numerical convergence. Preview notebook 01. Discussion prompt: Which axes must agree before two tensors can interact?

## 17. Build, run and differentiate

Timing: Session B / 00--04

Four-minute orientation. Notebook 01 runs PhAST; notebook 02 checks its local degradation law; notebook 03 is a separate original elastic-bar inverse toy. This deliberate scope reduction makes the derivative chain inspectable.

## 18. Start from the same computational state

Timing: B 04--10 / 6 minutes

Run the source/version check. The helper gives the vendored manifest precedence and verifies every public source hash, or checks the external public Git revision. Record dtype/device and source version. Setup/download and kernel execution times are different. Saved outputs provide a fallback if setup fails. Discussion prompt: Can you identify the source that was actually imported?

## 19. Geometry, mesh and precrack are separate inputs

Timing: B 10--19 / 9 minutes

Display the actual notebook mesh and node counts. It is a 4 by 2 rectangle, nx=128, ny=64, 8385 nodes and 16384 T3 elements. The precrack is damage Dirichlet data to x=0.8, not a cut-out geometric notch. The sketch illustrates a coarser T3 mesh with the same symmetric-opening convention as symmetric_tension_bcs. Geometry generation/import is an extension and must not be claimed as executed if not run.

## 20. A named boundary is not yet a boundary condition

Timing: B 19--25 / 6 minutes

Ask learners to print the count and extent of each boundary set. Check support against rigid-body motion, load direction, corner overlap and prescribed damage. Explain that a physical group carries a name/selection; applying mechanics requires a component and value. Discussion prompt: What happens if the group is empty or the wrong component is fixed?

## 21. A reproducible calculation has a complete specification

Timing: B 25--33 / 8 minutes

Read the configuration instead of copying slide values. The representative split energy in Session A is not the exact isotropic choice in this quick example. Point out ell=0.15, eta=1e-7 and stagger tolerance=1e-5. Solver tolerances and failure flags are part of provenance, not proof of discretisation convergence. Discussion prompt: Which of these choices changes physics? Which changes accuracy?

## 22. Distinguish the seeded crack from new damage

Timing: B 33--45 / 12 minutes

Run the selected notebook or use saved output. These fields were replotted from the frozen NPZ result. First distinguish the locked seed from diffuse regularisation after the first solve, then compare first and final increments. The change beyond the seeded region is not merely initialisation, but the example does not demonstrate a long propagating or branched crack. Use the incremental field in the notebook for a more sensitive view. Compute target 60--120 seconds is a teaching target; receipts describe actual local timings. Discussion prompt: What changed after the first increment?

## 23. Read response and numerical checks together

Timing: B 45--55 / 10 minutes

Read the reaction and recorded outer residual alongside the whole damage field. Inspect bounds, irreversibility and configured failure flags. Discuss why reaction, energy, mesh/load-step sensitivity and a relevant reference answer different questions. The record has no measured energy history; do not invent one from residuals. Discussion prompt: Does a small residual establish mesh convergence?

## 24. Change one input, then explain the difference

Timing: B 55--60 / 5 minutes, then break 60--70

Assign one supported material/load or resolution/tolerance change. Predict direction first. Save both configuration and outputs and compare the same scales. If the second solve is still running, record the state and continue after the break; never imply a result already exists. Take ten minutes. Discussion prompt: Keep the other settings fixed and save both results.

## 25. Tensor code can mirror the finite-element calculation

Timing: B 70--78 / 8 minutes

Trace connectivity, local basis gradients, material state, quadrature weights and global degrees of freedom. Ask the class to name the element and quadrature axes. Explain that tensors expose familiar numerical operations without making all solver operations automatically differentiable. Discussion prompt: Where do shape, units and boundary treatment enter?

## 26. A gradient follows a specific computational path

Timing: B 78--85 / 7 minutes

Explain backpropagation as chain-rule accumulation through a supported graph. PyTorch and JAX are frameworks; PhAST and JAX-FEM are solver projects. Both ecosystems can support differentiable FEM. Framework choice alone is not a gradient or performance guarantee. Discussion prompt: What could break or change this path?

## 27. Check a local derivative three ways

Timing: B 85--97 / 12 minutes

Execute notebook 02 and compare analytic, AD and central FD. For a quadratic, central FD is exact in real arithmetic; small-step cancellation remains. A nonquadratic smooth extension can demonstrate truncation error. Do not claim the usual U-shaped error must appear for this exact quadratic. Discussion prompt: Try several $\epsilon$ values. Report precision and error.

## 28. Choose an informative inverse observation

Timing: B 97--105 / 8 minutes

Run the bar exercise, check du_tip/dE against the analytic expression -FL/(AE squared), then recover E. Fix geometry and units. Explain that the scalar toy exposes the parameter-to-loss chain without history maxima, damage constraints or crack-path changes. Full fracture inversion requires its own checks. Discussion prompt: What is known? Which parameter does the observation constrain?

## 29. A small loss is only one part of recovery evidence

Timing: B 105--110 / 5 minutes

Inspect actual observations, recovered response, held-out point and optimisation history. Ask for another initial guess where time permits. A locally valid gradient does not establish uniqueness or global recovery. The plotted training loss and validation absolute error have different meanings/scales. Discussion prompt: Check the parameter, the fit and an unused load case.

## 30. Keep an experiment someone else can reproduce

Timing: B 110--120 / 10 minutes

Use the final lab block to finish the inverse exercise and hand-in. Record exact inputs, output figures and derivative check. Distinguish the real PhAST forward activity from the elastic-bar inverse toy. Do not report a fresh Colab pass without executing it. Discussion prompt: What did your experiment establish --- and what did it not?

## 31. Train, save and assess a model

Timing: Session C / 00--04

Four-minute orientation to notebooks 04 and 05. These use an original Helmholtz-like finite-difference field problem, not PhAST fracture data or an existing public learned-damage checkpoint. One complete small model is the core learning exercise.

## 32. The data card defines what learning means

Timing: C 04--10 / 6 minutes

Read the dataset card before architecture. Explain interpolation and extrapolation and why samples within a case are correlated. The toy supplies a real discrete residual for later assessment, but it is not an AT2 fracture equation. Fit normalisation using training data only. Discussion prompt: Why not split adjacent frames or individual nodes at random?

## 33. An MLP maps named features to a named target

Timing: C 10--18 / 8 minutes

Trace one node through normalisation, hidden layers and output. Identify trainable weights, activation functions and the explicit target. Ask which material, history or boundary information would be needed for a broader fracture problem. Keep the network small enough to inspect in class. Discussion prompt: What physical information is absent from this input?

## 34. A fitted model can still miss the local field

Timing: C 18--30 / 12 minutes

Run short training, then read actual training/validation logs and the held-out image. The two slide panels show the same held-out reference and reloaded MLP on identical 0--1 scales. Here L_h denotes the positive discrete negative-Laplacian on interior nodes, with boundary rows replaced by Dirichlet conditions; the model map includes the saved feature normalisation. A scalar loss can hide localisation and boundary error. Use the notebook's additional RBF/error panels for diagnosis. Reference generation and training are separate costs. Discussion prompt: Where is the error concentrated? What does the baseline reveal?

## 35. A checkpoint is more than weights

Timing: C 30--45 / 15 minutes

Execute the actual checkpoint routine. Reconstruct a fresh instance, load weights and metadata, set evaluation mode and compare the same held-out input numerically. Record feature order, normalisation, mesh signature, seed and source. Do not load an unknown arbitrary checkpoint as trusted code. Discussion prompt: Same input. Fresh model. Same prediction.

## 36. A model swap requires compatible inputs

Timing: C 45--60 / 15 minutes, then break 60--70

Compare the MLP with the compatible RBF and their held-out fields. Check feature ordering, shape, dtype and mesh signature. Explain why a graph or grid model cannot be substituted without constructing its inputs. Deliberately run the notebook incompatibility check. Take the ten-minute break. Discussion prompt: Try the compatible swap. Deliberately reject an incompatible input.

## 37. A learned model supplies a proposal

Timing: C 70--78 / 8 minutes

Read the adapter contract: feature order, mesh signature, bounds, output location, precision and scope. The actual public learned-damage hook also uses detached/no-gradient inference; do not confuse access to PyTorch with a fully connected training graph. The teaching adapter demonstrates assessment logic on its own equation. Discussion prompt: What exactly does the adapter promise?

## 38. Bounds are necessary but not equilibrium

Timing: C 78--85 / 7 minutes

Explain the nested min/max operation and consistent boundary treatment. This algebraic projection can enforce simple bounds and irreversibility but not balance. A fracture active-set problem needs a suitable projected/KKT check; the toy has its own explicitly defined residual. Discussion prompt: Can a bounded field still be mechanically wrong?

## 39. Acceptance needs an explicit correction route

Timing: C 85--90 / 5 minutes

Run notebook 05 and read its useful/rejected proposal comparison and correction record. The deliberately corrupted input should trigger reference fallback. Include proposal, audit and correction in any timing comparison; do not compare inference time alone with a complete classical solve. Discussion prompt: Inspect one useful proposal and one rejected proposal.

## 40. DAgger learns from states the model visits

Timing: C 90--105 / 15 minutes

Explain Dataset Aggregation: roll out the learner, obtain expert/reference labels on learner-induced states, append training data, retrain and evaluate on unchanged held-out cases. Inspect the saved correction/replay record. The current notebook does not execute a full DAgger loop. Optional activity: design one controlled offline round and its cost/evaluation gates. Discussion prompt: How do visited states differ from teacher-provided states?

## 41. Architectures encode different assumptions

Timing: C 105--110 / 5 minutes

Compare input construction and inductive assumptions. Moving from the small toy to fracture needs material/history/boundary representation and an appropriate data split. Neither a model name nor one good field proves transfer to new topology or crack paths. Discussion prompt: Which new load, material, mesh or topology has actually been tested?

## 42. Read a research example through the same evidence

Timing: C 110--115 / 5 minutes

Use a course-lead-supplied permitted paper example if available. This preparation does not include an unpublished large inverse/hybrid result. Compare like accuracy, hardware and precision; include data/reference generation, training, prediction, audit and correction when relevant. No speedup is claimed by the deck. Discussion prompt: What has this example demonstrated, specifically?

## 43. A useful contribution starts with reproducibility

Timing: C 115--118 / 3 minutes

Suggest a documentation correction, exercise extension or minimal reproducible issue. Include environment/source, configuration, expected/actual behaviour and relevant output. This course creates no public issue, message or publication automatically. Discussion prompt: What is the smallest example another person could run?

## 44. Keep the chain from assumptions to evidence visible

Timing: C 118--120 / 2 minutes

Close with retrieval, not a new topic. The PDF is the teaching copy and the TeX/Matplotlib files are the editable source. Point to the companion book and all five notebooks. CWI inspired physical example-to-equation-to-code, a small complete training loop and model-induced-state assessment, not copied visual assets. Discussion prompt: Name one physical assumption, one check and one limitation.
