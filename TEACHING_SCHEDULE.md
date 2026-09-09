# Day two: three lecture hours, then three exercise hours

Local next-edition plan. Published v0.1.1 still contains the earlier mixed
2+2+2-hour schedule. Reordering the slide deck/book overview is pending.

The audience knows basic mechanics, calculus and introductory Python but need
not know fracture, phase fields or automatic differentiation. Connect every
block to the same question: how does a damaged body respond, how does its
response depend on an input, and where could a learned component assist?

## Timing

Baseline: 180 lecture minutes followed by 180 exercise minutes. These are
relative contact times, not event clock times. Lunch/breaks need separate
organiser confirmation. If the allocation includes 30 minutes of breaks,
use the six 55-minute blocks described below. Notebook computation is measured
separately but included within the allocated practical slots; each complete
run must stay below 300 seconds after setup.

## L1 — fracture and numerical solvers

| Minutes | Content | Student checkpoint |
| --- | --- | --- |
| 00–05 | Notched-body physical question, damage field and load response. | Name the fields and one observable. |
| 05–13 | Sharp cracks, cohesive models, XFEM and phase fields, with trade-offs. | Distinguish formulation, approximation and solution algorithm. |
| 13–26 | Annotated elastic/fracture energy, damage convention, length scale and degradation; initiation and branching as physical questions. | Identify stored energy, crack cost and regularisation. |
| 26–40 | FEM residuals, staggered versus monolithic coupling; explicit solid dynamics with implicit damage, stability and convergence. | Trace mechanics, driving quantity, damage and checks. |
| 40–50 | Tensor operations and assembled versus matrix-free actions. | Explain an operator action and what need not be stored. |
| 50–60 | PhAST introduction and motivation for sensitivities, inverse calibration and learned proposals. Preview the actual afternoon case. | State the questions for L2 and L3. |

Use one energy visual and one staggered update. Keep more degradation laws,
fracture history and transport derivations in the book. The final ten minutes
must already connect the solver to differentiability and hybrid learning.

## L2 — differentiability and inverse problems

| Minutes | Content | Student checkpoint |
| --- | --- | --- |
| 00–08 | Parameter, state, observation and scalar loss. | State the derivative direction. |
| 08–22 | One explicit update, local derivatives and vector–Jacobian product. | Work one scalar derivative by hand. |
| 22–35 | Several updates, reverse accumulation and shared-parameter contributions. | Explain why contributions must be summed. |
| 35–45 | Implicit damage adjoint, active branches and nonsmooth history operations. | State which derivative a check concerns. |
| 45–55 | Bar inverse example; observations, identifiability and fracture-specific complications. | Identify an ambiguous observation. |
| 55–60 | Calibration parameters versus trainable model weights. | Connect the loss to the selected weights. |

Use the existing derivation and label the bar as a teaching model. The separate
inverse/history extension is reviewed optional detail. Tensor notation does
not alone establish a valid gradient through every implementation operation.

## L3 — hybrid numerical and learned methods

| Minutes | Content | Student checkpoint |
| --- | --- | --- |
| 00–08 | Offline surrogate, in-solver proposal and end-to-end training graphs. | Locate the numerical solve and loss. |
| 08–20 | Inputs/targets, units/locations, data splits, MLP/RBF and graph-model contracts. | Explain why matching output size is insufficient for a model swap. |
| 20–32 | Train, evaluate, save metadata/weights, reload and predict. | Name the held-out and reload checks. |
| 32–45 | Proposed field, admissibility/residual checks, correction, recheck and rejection. | Explain the response to a poor prediction or failed correction. |
| 45–53 | DAgger-style visited states, reference labels, aggregation, retraining and independent evaluation. | Distinguish the loop from one online gradient step. |
| 53–60 | One approved actual hybrid exhibit if ready; otherwise a labelled toy-to-fracture transfer discussion. | Name the evidence needed for a wall-time benefit. |

No new architecture sweep or large-model training is required. A research
exhibit replaces this slot and must have approved provenance and limitations.

## P1 — run and interpret PhAST

Use [notebook 01](notebooks/study/01_phast_tiny_evolving_fracture.ipynb),
with [worked solutions](notebooks/solutions/01_phast_tiny_evolving_fracture.ipynb).
This is actual public PhAST AT2, but its mechanics route is quasistatic and
assembled/sparse-direct. Explicit dynamics and matrix-free mechanics from L1
are not demonstrated by this run.

| Minutes | Activity |
| --- | --- |
| 00–10 | Check setup/source pin; inspect geometry, mesh, material and boundary conditions. If setup stalls, use retained outputs and a running partner. |
| 10–15 | Predict damage concentration; distinguish the locked precrack. |
| 15–20 | Execute the unchanged baseline or inspect the recorded run. |
| 20–40 | Compare initial/final/incremental damage, load response and stagger checks. |
| 40–52 | Complete the existing mesh/precrack-count and evidence-scope exercises. |
| 52–60 | Explain a field, a scalar response and one limitation in a result card. |

Do not make an untested stronger-load case mandatory. Existing attempted variants
stopped at configured nonconvergence. An external mesher import is not part
of the minimum route; the existing prepared mesh uses a tensor/NPZ round-trip.

## P2 — check derivatives and recover a parameter

Use [notebook 02](notebooks/study/02_degradation_autograd.ipynb) and
[notebook 03](notebooks/study/03_tiny_derivative_inverse_toy.ipynb), with
[02 solutions](notebooks/solutions/02_degradation_autograd.ipynb) and
[03 solutions](notebooks/solutions/03_tiny_derivative_inverse_toy.ipynb). The first checks
the exact public degradation law locally; the second is an elastic-bar tensor
inverse teaching model, not full fracture inversion.

| Minutes | Activity |
| --- | --- |
| 00–10 | Derive the degradation slope/curvature and predict their signs. |
| 10–15 | Compare analytic, autograd and centred finite differences. |
| 15–25 | Complete the two derivative exercises and discuss scope. |
| 25–35 | Derive the bar tip response and its modulus sensitivity. |
| 35–40 | Execute the derivative and modulus-recovery baseline. |
| 40–52 | Inspect recovery, positive parameterisation and held-out response; complete exercises. |
| 52–60 | Explain observable, loss, gradient and optional optimiser step. |

## P3 — train, reload and assess a learned proposal

Use [notebook 04](notebooks/study/04_train_save_reload_adapter.ipynb) and
[notebook 05](notebooks/study/05_hybrid_reference_correction.ipynb), with
[04 solutions](notebooks/solutions/04_train_save_reload_adapter.ipynb) and
[05 solutions](notebooks/solutions/05_hybrid_reference_correction.ipynb). These are
ToyHelmholtzProblem MLP/RBF and correction exercises, not trained PhAST damage
models or an executed full DAgger experiment.

| Minutes | Activity |
| --- | --- |
| 00–08 | Inspect whole-case train/validation/test splits and input/output contract. |
| 08–13 | Run bounded MLP training, save and reload. |
| 13–30 | Compare reference/MLP/RBF/error fields, reload equivalence and metadata; complete exercises. |
| 30–35 | Run compatible and corrupted proposals with reference correction. |
| 35–50 | Explain the residual/projection checks, feature-order and nonfinite-input tests. |
| 50–60 | Explain what is missing from one correction record for DAgger, reveal solutions and recap all three result cards. |

Notebook 05 can create its small checkpoint if notebook 04 was not completed.
Use the same approved support files, not an isolated notebook upload.

## Fallback for 330 contact minutes plus 30 minutes of breaks

Use six 55-minute blocks, 165 minutes of lectures and 165 of exercises, with
three separately placed ten-minute breaks. Keep order and all core outcomes.
Cut five minutes per block as follows:

| Block | Reduction |
| --- | --- |
| L1 | Contrast only one degradation law (3 min) and shorten the operator example (2 min); retain ML motivation. |
| L2 | Shorten the hand example (3 min) and inverse discussion (2 min). |
| L3 | Shorten architecture comparison (3 min) and optional exhibit (2 min). |
| P1 | Shorten paired discussion (5 min), preserving baseline interpretation. |
| P2 | Shorten exercise discussion (5 min), preserving both derivative/recovery checks. |
| P3 | Shorten model comparison (3 min) and replay discussion (2 min). |

## Preparation and contingency

Rehearse the exact complete student package in the supported environment before
class. Existing local receipts do not establish fresh Colab performance.
Provide executed HTML, downloadable notebooks and worked answers offline. Retained
outputs support learning during setup failures but are not an execution pass.

The remaining acceptance gates are in [MVP_DELIVERY.md](MVP_DELIVERY.md).
