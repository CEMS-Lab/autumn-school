# Autumn-school delivery plan

The phase-field day connects fracture modelling, differentiable computation
and learned components. The book provides derivations, executable lessons,
recorded results and worked answers.

## Teaching sequence

Use [TEACHING_SCHEDULE.md](TEACHING_SCHEDULE.md) for the proposed three lecture
hours followed by three exercise hours. Confirm clock times and break allocation
with the organiser. The current book follows this 3+3-hour route. The animated
introduction maps the retained 44-slide resource onto L1/L2/L3; the complete
lecture and practical sequence needs its timed rehearsal.

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
| 00 | Algebraic prediction/energy example; 6.20 s | Opening prediction |
| 01 | PhAST plane-strain quasistatic AT2, assembled sparse-direct mechanics; connected workflow and changed-load comparison; 92.00 s | Forward calculation |
| 02 | Public degradation law; analytic/AD/FD check; 3.74 s | Local sensitivity |
| 03 | Elastic-bar inverse model; 4.12 s | Parameter recovery |
| 04 | Teaching Helmholtz field MLP/RBF, save/reload and held-out comparison; 5.17 s | Learned interface |
| 05 | Teaching Helmholtz field proposal, assessment and independent direct-reference fallback; 4.72 s | Checked hybrid cycle |
| Diffusion companion | Explicit stencil, reverse recurrence and synthetic recovery; current execution receipt linked below | Optional derivative practical |
| Inverse/history extension | Retained fracture observations, sampled loss landscapes and loading/unloading history | Optional research exhibit |

The [current notebook receipt](evidence/notebook_runtime_current.json) records
the 10 September whole-process runs, source hashes and platform. Earlier
evidence is retained in the [original notebook receipt](evidence/notebook_runtime.json),
[teaser receipt](evidence/teaser_runtime.json),
[package rehearsal](evidence/package_rehearsal.json) and
[diffusion receipt](evidence/differentiability_step_by_step.json).
The optional diffusion companion retains its 9 September receipt. Today's six
timings describe fresh local processes on macOS ARM/Python 3.10.18 after setup.
Rehearse each
complete student calculation below 300 s in the selected environment, timing
setup separately. Fresh Colab verification requires an authenticated session.

The forward notebook provides a quasistatic bridge to the lecture's dynamic
and matrix-free concepts. A classroom dynamic example needs its own complete
under-five-minute rehearsal. The [current forward-practical evidence](evidence/forward_practical_20260910.md)
records the connected geometry/BC/solver objects, portable mesh and result
reloads, inspected fields and changed-load exercise. The
[9 September audit](source/planning/PRACTICAL_SEQUENCE_AUDIT_20260909.md)
preserves the starting assessment.

The learning exercises use a scalar field equation. Integrating a learned
component into PhAST requires approved weights, a feature contract, full-field
comparisons, residual checks and matched end-to-end timing. Select an approved
retained example within the allocated exhibit slot when these are available.

## Assets and integration

[CURRENT_DELIVERY.md](CURRENT_DELIVERY.md) links the book, six computational
lessons, 23-slide editable animated introduction, retained 44-slide lecture
resource, diffusion companion and optional inverse laboratory. The animated
introduction embeds five original clips with static fallbacks and presenter
pause questions. The previous working introduction is retained as a fallback.

## Classroom completion checklist

- [ ] Confirm organiser clock times and break allocation.
- [x] Map the animated introduction and retained lecture resource to L1/L2/L3.
- [ ] Rehearse the combined lecture, its motivation by minute 60 and the handover
      to each practical.
- [x] Execute all six complete classroom notebooks in fresh local processes;
      record their whole-process times after setup and exact source hashes.
- [ ] Install and rehearse the full package in fresh supported environments,
      including authenticated Colab CPU sessions and a slower laptop; measure
      setup and complete computation separately.
- [x] Align the forward notebook's preview, actual inputs and result reload;
      inspect the physical effect of a changed load.
- [ ] Simplify the visible mesh workflow and add a checked Gmsh import activity
      using the [mesh usability plan](source/planning/MESH_USABILITY_REVIEW_20260910.md).
- [x] Verify local exercise questions, answers, notebook downloads, offline
      outputs, mobile/desktop rendering and mathematical notation.
- [x] Test all five animation clips in local Keynote; preserve their embedded
      movies in the native Keynote file.
- [ ] Test PowerPoint and presentation-machine playback, seeking/replay,
      portability and classroom readability.
- [x] Check local source/output parity and notebook-level coherence.
- [ ] Complete the student-level cross-format review and timed six-hour rehearsal.
- [x] Receive authorisation to publish the reviewed update.
- [x] Verify the pushed revision, live book, credits and downloadable files;
      record the checks in the [publication receipt](evidence/publication_20260910.json).

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

Use Presented by Sathiskumar A. Ponnusami only in the presentation, with
Queen Mary University of London and CEMS-Lab. Credit the book as Prepared by
Allamaprabhu Ani and Sathiskumar A. Ponnusami, CEMS-Lab. Retain creator credit in ordinary metadata,
comments and presenter notes. Metadata supports source attribution and can be
removed through re-export. Preserve third-party notices. Confirm consent and
credits before distributing recordings.

[Issue 1](https://github.com/CEMS-Lab/autumn-school/issues/1) is the main plan;
issues 2–16 retain the wider objectives, and issues 17–18 govern course-wide
pedagogy and authoring standards. Use [BUILD_AGENT_PROMPTS.md](BUILD_AGENT_PROMPTS.md)
for bounded assignments. The current manifest identifies the published web edition;
the publication receipt records its content revision and live checks. Complete
fresh Colab checks and the timed rehearsal before classroom delivery. The inverse
contributor retains ownership of new inverse research work.
