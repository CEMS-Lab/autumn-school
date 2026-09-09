# Autumn-school delivery plan

The phase-field day connects fracture modelling, differentiable computation
and learned components. The book provides derivations, executable lessons,
recorded results and worked answers.

## Teaching sequence

Use [TEACHING_SCHEDULE.md](TEACHING_SCHEDULE.md) for the proposed three lecture
hours followed by three exercise hours. Confirm clock times and break allocation
with the organiser. Map the existing three two-hour topic groups in the book
and 44-slide resource onto that agreed timetable.

1. Explain fracture energy, length scale and degradation. Distinguish the model,
   spatial approximation and solution algorithm. Interpret a small PhAST run.
2. Define an observable and scalar loss. Trace reverse accumulation, check a
   derivative and solve a compact inverse problem.
3. Train, save and reload a compatible model. Inspect its proposed field,
   evaluate the residual and apply reference correction.

Each practical ends with a field or checked number, a worked answer and stated
model assumptions. The optional inverse contribution extends the common course
through particle geometry, retained fracture fields and a guided history lesson.

## Computational scope and recorded local runtimes

| Lesson | Model and evidence | Role |
| --- | --- | --- |
| 00 | Algebraic prediction/energy example; 6.381 s | Opening prediction |
| 01 | Public PhAST quasistatic AT2, sparse-direct mechanics; 76.301 s original, 88.351 s package rehearsal | Forward calculation |
| 02 | Public degradation law; analytic/AD/FD check; 4.721 s | Local sensitivity |
| 03 | Elastic-bar inverse model; 5.446 s | Parameter recovery |
| 04 | Scalar-field MLP/RBF, save/reload and held-out comparison; 9.473 s | Learned interface |
| 05 | Scalar-field proposal, assessment and reference correction; 5.179 s | Checked hybrid cycle |
| Diffusion companion | Explicit stencil, reverse recurrence and synthetic recovery; current execution receipt linked below | Optional derivative practical |
| Inverse/history extension | Retained fracture observations, sampled loss landscapes and loading/unloading history | Optional research exhibit |

Sources: [notebook receipt](evidence/notebook_runtime.json),
[teaser receipt](evidence/teaser_runtime.json),
[package rehearsal](evidence/package_rehearsal.json) and
[diffusion receipt](evidence/differentiability_step_by_step.json).
These timings describe the reference local CPU after setup. Rehearse each
complete student calculation below 300 s in the selected environment, timing
setup separately. Fresh Colab verification requires an authenticated session.

The forward notebook provides a quasistatic bridge to the lecture's dynamic
and matrix-free concepts. A classroom dynamic example needs its own complete
under-five-minute rehearsal. The [forward practical audit](source/planning/PRACTICAL_SEQUENCE_AUDIT_20260909.md)
tracks alignment of visible geometry/BC previews with actual solver inputs and
a portable result-reload exercise.

The learning exercises use a scalar field equation. Integrating a learned
component into PhAST requires approved weights, a feature contract, full-field
comparisons, residual checks and matched end-to-end timing. Select an approved
retained example within the allocated exhibit slot when these are available.

## Assets and integration

[CURRENT_DELIVERY.md](CURRENT_DELIVERY.md) links the book, six computational
lessons, 18-slide introduction, 44-slide lecture resource, diffusion companion,
four short Manim animations and optional inverse laboratory. Each animation
includes a poster for static use.

## Classroom completion checklist

- [ ] Confirm organiser clock times and break allocation.
- [ ] Reorder and rehearse the lecture resource against L1/L2/L3.
- [ ] Retain motivation by minute 60 and a clear handover to each practical.
- [ ] Rehearse the full package in a fresh supported environment; time setup
      and each complete notebook separately.
- [ ] Align the forward notebook's preview, actual inputs and result reload.
- [ ] Verify exercise questions, answers, downloads and offline outputs.
- [ ] Test animation playback on the presentation machine.
- [ ] Complete a student-level coherence review and timed six-hour rehearsal.

## Scientific conventions

Quasi-Newton is a solution algorithm; XFEM enriches a spatial approximation;
cohesive and phase-field fracture specify modelling choices. Compare these for
a stated material, geometry, loading and computational objective. Retain the
existing scientific citations when explaining their history.

Distinguish AT1/AT2 crack-density choices from degradation laws. Assess
solution-map regularity and convergence for the complete coupled problem.
Identify constrained minimisation, history approximations and surrogate
backward rules explicitly. Autograd follows supported, connected operations.
DAgger comprises data collection, reference labelling, aggregation and
retraining. A learned warm start and a learned constitutive law have distinct
objectives; report total cost at matched accuracy.

PhAST/PyTorch is the executable platform. JAX is an implementation comparison
in the [teaching notes](DIFFERENTIABLE_SOLVER_TEACHING_NOTES.md). Large architecture
studies, additional solver development and a full DAgger research programme
remain follow-up projects.

## Attribution and continuing work

Present Sathiskumar A. Ponnusami first, with Queen Mary University of London
and CEMS-Lab. Retain Allamaprabhu Ani's creator credit in ordinary metadata,
comments and presenter notes. Metadata supports source attribution and can be
removed through re-export. Preserve third-party notices. Confirm consent and
credits before distributing recordings.

[Issue 1](https://github.com/CEMS-Lab/autumn-school/issues/1) is the main plan;
issues 2–16 retain the wider objectives. Use [BUILD_AGENT_PROMPTS.md](BUILD_AGENT_PROMPTS.md)
for bounded assignments. The edition manifest identifies the published files.
