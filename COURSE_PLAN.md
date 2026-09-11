# PhAST Autumn School: course plan and completion record

This is the versioned plan for a coherent six-hour course, supported
by one interactive book, executable notebooks, worked solutions and slides.
The main planning issue links the topic issues; this file preserves the
curriculum when issues are closed or reorganised.

## Latest delivery decision: three curated lectures and three labs

**11 September runtime update.** Every complete student calculation, including
plots and exports, must finish in less than **120 seconds**. The development
target is at most 60 seconds locally to leave headroom for Colab CPUs. Time
one-time dependency installation separately and rehearse each published
notebook in a fresh Colab runtime. This decision supersedes earlier 300-second
budgets recorded below. See [runtime policy](source/planning/RUNTIME_POLICY_20260911.md).

Classroom 1 now uses the public B3 dynamic plate with its imported 1,091-node
mesh, projected CG and Jacobi preconditioning. It demonstrates a crack crossing
the remaining 20 mm ligament. The original quasistatic practical remains a
detailed reference. Classroom 2 begins with a local damaged-bar force law,
manual chain rule, PyTorch backward pass and finite-difference check before
the existing parameter-recovery exercise. A four-slide insertion module follows
that same example. B7 branching remains a recorded lecture exhibit.

The 10 September voice memo and maintainer follow-up set the current route:
**45 minutes of fracture/PhAST, 55 minutes of differentiability/inverse
applications, and 50 minutes of hybrid learning**, followed by **three
50-minute practicals**. The remaining 60 minutes in a six-hour event window
support breaks, questions, setup and optional exploration; organisers confirm
clock times. This replaces the previous six-hour contact-time assumption.

The three classroom notebooks are `01_simulate_fracture`,
`02_gradients_and_recovery` and `03_learning_and_hybrid`, stored in
`notebooks/classroom/`. The original six notebooks remain detailed references.
Existing editable decks and animations are preserved. The three lecture guides
reserve clearly labelled example and animation slots for later completion.

[Issue #20](https://github.com/CEMS-Lab/autumn-school/issues/20), the
[curation plan](source/planning/VOICE_MEMO_CURATION_20260910.md) and
[placeholder register](source/planning/PLACEHOLDER_REGISTER.md) govern this
local curation. The latest published edition remains identified by its dated
publication receipt until this candidate is reviewed and published.

## Previous delivery baseline

The 11 September [four-deliverable integration plan](source/planning/FOUR_PILLAR_DELIVERY_20260911.md)
adds a [90-slide editable authoring scaffold](source/slides/course-blueprint-20260911/STORYBOARD.md),
fresh notebook execution and independent layout/coherence audits. The scaffold
preserves the 45/55/50-minute lectures, three practicals and all 21 content
slots. It is a candidate expansion of the preserved 32-slide companion.
Publication and fresh authenticated Colab remain separate acceptance gates.

The preceding baseline allocated **three hours of lectures followed
by three hours of interactive exercises**. Lecture 1 covers fracture,
staggered solution and matrix-free operators and must already motivate
differentiability and hybrid learning. Lecture 2 develops differentiability;
lecture 3 develops hybrid approaches. The exercises revisit those questions
in the same order.

The current book source uses the curated three-lecture/three-practical route above.
Frozen v0.1.1 artifacts retain the earlier mixed two-hour sessions.
The editable animated deck and classroom rehearsal are tracked in
[TODAY.md](TODAY.md). See [MVP_DELIVERY.md](MVP_DELIVERY.md)
for the selected scope and [BUILD_AGENT_PROMPTS.md](BUILD_AGENT_PROMPTS.md)
for bounded build assignments. Preserve the complete issue inventory below.

The preceding editions used 360 contact minutes or 330 contact minutes plus
30 minutes of breaks. These historical allocations are retained here for
traceability; TEACHING_SCHEDULE.md defines the current 300-minute teaching core.

## Purpose and audience

Students should move from understanding the fracture model to running a small
calculation, interpreting it, differentiating a defined computational graph,
and evaluating the role of a learned component. Assume basic calculus, linear
algebra and introductory Python; introduce the FEM and autograd notation used
in the activities. Do not assume experience with phase-field fracture.

The intended event is the UKACM Autumn School, 14–17 September 2026, with the
organiser-led sessions on 15–16 September. Confirm room-level scheduling,
speaker credits and programme wording with the organisers. This plan concerns
the phase-field/differentiable-computing day, not the entire event programme.
The organiser leads the other day's preparation. Support for it is a separate
bounded assignment, not another full course inside this allocation.

## Learning sequence

The current local route is L1 fracture/numerics → L2 derivatives → L3 hybrid
methods, followed by P1 PhAST → P2 derivative/recovery exercises → P3
training/proposal assessment. The opening timetable graphic has been removed
from the book; its reusable figure sources are retained. The longer sequence preserves the
full book inventory. Figures follow the [academic design standard](DESIGN_STANDARD.md).

```text
Opening prediction: can a learned average be inadmissible?
        ↓
Cracks and their representations: phase field, XFEM, cohesive models
        ↓
Energy → degradation → regularisation → damage initiation/evolution
        ↓
FEM discretisation → staggered solution → static/dynamic algorithms
        ↓
Geometry → mesh → boundary conditions → first PhAST run → interpretation
        ↓
Tensor operations → chain rule → reverse accumulation → derivative check
        ↓
Inverse recovery → train/save/reload → compatible model proposals
        ↓
Residual checks/correction → data aggregation → larger paper examples
        ↓
Independent practice, reproducible extensions and contributions
```

The book supplies the continuous explanation; the slides guide the live
conversation; the notebooks provide inspectable computations. Each activity
follows **predict → explain → compute → inspect → exercise → worked solution**.
Use a toy problem only after explicitly stating what it isolates and how the
concept transfers to, or differs from, a fracture calculation.

## Three lectures and three practical notebooks

| Session | Principal question | Student outcome |
| --- | --- | --- |
| L1 then P1: model and numerical method | What represents a crack, what do we solve, and why make it differentiable or hybrid? | Explain the physical/numerical model and interpret one small public PhAST calculation. |
| L2 then P2: derivatives and recovery | How does an input affect a stated observable or loss? | Trace a chain rule; check derivatives and parameter recovery in labelled teaching examples. |
| L3 then P3: learning and model interfaces | What can a learned component propose safely? | Train/save/reload a small model; assess a compatible proposal and its correction. |

The minute-by-minute allocation is in [TEACHING_SCHEDULE.md](TEACHING_SCHEDULE.md).
The opening uses one physical question within five minutes. A complete run of
notebook 00 is optional preparation, not another required practical.
Larger paper studies are optional extensions or explicitly replace an allocated
slot. A 45-minute paper discussion is not silently added to a full six-hour day.

## Coverage and remaining work

### Coordination and ownership

The course integration lead owns the full six-hour curriculum, lecture deck,
notebook sequence, common visual language, book integration and publication.
The inverse-extension contributor owns only the separately reviewed inverse
teaching material. That extension must not replace the fundamentals, forward
simulation or model-learning blocks, change their shared styles, or silently
expand the six-hour allocation. Integration requires its source, full-run
receipt, figures, solutions and scientific-scope review; draft status is not
publication readiness. The existing inverse toy remains the classroom route
until a replacement passes the relevant gates.

### Workstream record

The [shared PhAST/course example issue #19](https://github.com/CEMS-Lab/autumn-school/issues/19)
coordinates C04 and C14 with [PhAST documentation #4](https://github.com/CEMS-Lab/PhAST/issues/4).
The [alignment plan](source/planning/PHAST_COURSE_ALIGNMENT_20260910.md) records
example selection, source versions, short mesh cells, propagation evidence and
cross-links. Course integration owns the classroom lesson; the PhAST release
task owns upstream documentation. B3 dynamic SENT is being assessed as the
shared crack-propagation example. The tested quasistatic lesson remains the
current numerical baseline during that assessment.

These are the full course ambitions. The MVP checklist in MVP_DELIVERY.md
selects the classroom subset without closing or deleting unfinished extensions.

| ID | Workstream | First-edition position and next gate |
| --- | --- | --- |
| C01 | Phase-field foundations and comparisons | Explanations and figures exist. Review XFEM/cohesive trade-offs; do not call quasi-Newton a competing fracture formulation or claim universal phase-field superiority. |
| C02 | Energy, degradation and damage morphology | Equations, derivative notebook and browser controls exist. Audit AT1/AT2 normalisation, profiles, continuity, mesh/length-scale effects and initiation/branching explanations. |
| C03 | Solution algorithms and coupled physics | Staggering, static/dynamic and matrix-free concepts exist. Complete the transport/solid/damage operator narrative and distinguish physical time, load stepping and nonlinear iteration. |
| C04 | First PhAST simulation | The published practical connects one configuration through geometry, mesh/notch, actual boundary conditions and solver objects, loading, exports and reloaded post-processing. Its reference and changed-load cases pass locally in 92.00 s. The model is plane-strain quasistatic AT2 with assembled sparse-direct mechanics and diffuse damage. Follow the [mesh usability plan](source/planning/MESH_USABILITY_REVIEW_20260910.md) to shorten the mesh cells and add checked Gmsh import, then rehearse in Colab. Explicit/matrix-free execution and short propagating-crack examples retain their own acceptance checks. |
| C05 | Backpropagation explained step by step | Explicit local derivatives, adjoint propagation, shared-parameter sums and a checked three-step algebraic example exist. Revised book/lecture diagrams distinguish observable, gradient and optimisation update; a toy derivative check is not a full fracture-path validation. |
| C06 | Inverse recovery | The elastic-bar toy is the classroom route. The optional inverse/history reading extension is integrated. Its contributor owns the remaining actual fracture recovery, multiple-start, held-out and under-300-second acceptance checks in issue #7. |
| C07 | Train, save, reload and interchangeable models | MLP/RBF toy field examples run. Define and validate fracture-compatible damage inputs/outputs and saved-model contracts; do not imply arbitrary architectures are interchangeable automatically. |
| C08 | Hybrid correction and DAgger | Toy accept/reject/fallback runs; DAgger is explained. A complete model-induced rollout, reference labelling, aggregation, retraining and held-out evaluation remains to be built. |
| C09 | Laptop/Colab execution | All six notebooks have fresh local whole-process receipts of 3.74–92.00 seconds after setup, recorded in evidence/notebook_runtime_current.json. Shared cloud setup is implemented. Fresh installation, authenticated Colab and slower-laptop rehearsal retain separate checks; all activities must stay below 300 seconds. |
| C10 | Integrated book and accessibility | The web textbook, native code/output chapters, practice/solution downloads and visual explorations form the student edition. The printable book is archived. Review offline/mobile/keyboard behaviour and links after every edition change. |
| C11 | Coherent lecture slides and animations | A new 32-slide native Keynote outline follows the curated 45/55/50-minute lectures and maps all 21 registered content slots. Its fixed font roles, 24 LaTeX panels and five Matplotlib figures have native rendered reviews. The prior 23-slide animated introduction and 44-slide LaTeX resource are retained. Approve the style, fill selected exhibits, adapt presenter-controlled builds and rehearse the complete lecture/practical route. |
| C12 | Paper-based extension studies | Select approved public papers and reproducible retained results, with one question and one limitation per study. Do not publish private worktrees or unapproved checkpoints. |
| C13 | Teaching references and design standard | D2L/PBDL inform the book. The design standard records inspected Delft textbook, TUM lecture and ETH research-presentation visuals; original flowcharts apply those patterns. Remaining supplied Instagram/PDF repository lists still need a complete inventory; do not imply inaccessible material was inspected. |
| C14 | Final coherence and completeness | Local source/code/output parity, exercise, mathematical rendering and desktop/mobile checks pass. All 18 issues are mapped. Complete the whole-course learning-objective, notation, prerequisite and cross-format review, plus the timed three-lecture/three-practical rehearsal. |
| C15 | Release, credits and community | The reviewed update is published; pushed revision, Pages deployment, credits and downloadable editions are verified in the [publication receipt](evidence/publication_20260910.json). Original-content licence, approved research exhibits, contributor pathway and final release acceptance remain tracked. |

## Evidence required before marking an issue complete

### C10 theme update, 9 September 2026

Use the same open-source Sphinx Book Theme as Physics-based Deep Learning,
with dark mode initially selected, its original desktop column proportions,
and the existing light/system switch. Preserve lessons, recorded outputs,
notebook downloads and white-background scientific figures. This is a local
HTML styling update, not a change to the six-hour schedule, numerical evidence
or the white lecture/PDF design. Theme source and rebuild details are recorded
in DESIGN_STANDARD.md; issue #11 remains the governing accessibility workstream.

The requested PhAST orange/blue accent follow-up preserves those columns and
dark surfaces. Use readable tints of the public logo/documentation colours for
navigation, links and answer edges; never alter quantitative figure colours.
Two optional footer discoveries are native, keyboard-operable details, with no
automatic animation, sound, tracking or impact on lesson completion.
Book footer credit: prepared by Allamaprabhu Ani and Sathiskumar A. Ponnusami,
CEMS-Lab; prepared for the UKACM Autumn School 2026. Preserve third-party credits.
Reserve presenter wording for the slides, with Sathiskumar A. Ponnusami first
and Queen Mary University of London · CEMS-Lab as his affiliation.

The [main planning issue #1](https://github.com/CEMS-Lab/autumn-school/issues/1)
tracks these linked workstreams. They remain open until their full acceptance
criteria are met, even where a first-edition artifact already exists.

| Workstream | GitHub issue |
| --- | --- |
| C01 | [#2: Phase-field foundations and method comparisons](https://github.com/CEMS-Lab/autumn-school/issues/2) |
| C02 | [#3: Energy, degradation laws and damage visual explanations](https://github.com/CEMS-Lab/autumn-school/issues/3) |
| C03 | [#4: FEM, staggered solution, dynamics and tensor operators](https://github.com/CEMS-Lab/autumn-school/issues/4) |
| C04 | [#5: Geometry-to-results PhAST tutorial and short crack propagation](https://github.com/CEMS-Lab/autumn-school/issues/5) |
| C05 | [#6: Step-by-step backpropagation equations and gradient checks](https://github.com/CEMS-Lab/autumn-school/issues/6) |
| C06 | [#7: Small actual fracture inverse-recovery activity](https://github.com/CEMS-Lab/autumn-school/issues/7) |
| C07 | [#8: Damage-model interfaces and train-save-reload model swaps](https://github.com/CEMS-Lab/autumn-school/issues/8) |
| C08 | [#9: Checked hybrid learning and complete DAgger-style loop](https://github.com/CEMS-Lab/autumn-school/issues/9) |
| C09 | [#10: Fresh Colab and laptop rehearsal under five minutes](https://github.com/CEMS-Lab/autumn-school/issues/10) |
| C10 | [#11: Integrated textbook, notebook solutions and accessibility](https://github.com/CEMS-Lab/autumn-school/issues/11) |
| C11 | [#12: Clean lecture slides, animations and pacing](https://github.com/CEMS-Lab/autumn-school/issues/12) |
| C12 | [#13: Approved paper studies and advanced teaching extensions](https://github.com/CEMS-Lab/autumn-school/issues/13) |
| C13 | [#14: Reference inventory and reusable academic design standard](https://github.com/CEMS-Lab/autumn-school/issues/14) |
| C14 | [#15: Final lecture-series coherence and requirement-completeness audit](https://github.com/CEMS-Lab/autumn-school/issues/15) |
| C15 | [#16: Public releases, credits, contributor pathway and course showcase](https://github.com/CEMS-Lab/autumn-school/issues/16) |
| Curated three-lab classroom edition | [#20: Voice-memo curation and concise notebooks](https://github.com/CEMS-Lab/autumn-school/issues/20) |
| Course-wide pedagogy | [#17: Undergraduate tutorial style and coherent learning activities](https://github.com/CEMS-Lab/autumn-school/issues/17) |
| Authoring standards | [#18: Editorial, notebook and visual directives](https://github.com/CEMS-Lab/autumn-school/issues/18) |
| Shared upstream/course example | [#19: Mesh-to-propagation learning route](https://github.com/CEMS-Lab/autumn-school/issues/19) |

## Completion evidence

- A learner-facing artifact linked at a specific repository revision.
- The exact build/test command and its result; measured timing when executable.
- Visual inspection of the actual figure, page or slide, not only a successful build.
- Source attribution, explicit assumptions and limitations.
- A check that the change matches the notation and prerequisites in adjacent lessons.
- Updated links, downloadable files and relevant issue cross-references.

For every run, separate setup from complete notebook execution. A hard timeout
is a safety cap, not proof that every user will finish. Use retained outputs
as the classroom fallback. No fresh Colab performance claim is made until a
fresh-runtime receipt exists.

## Release gates

The reviewed 10 September update is live. The [publication receipt](evidence/publication_20260910.json)
records the successful Pages build, content revision, live HTML and notebook
hashes, credits and browser checks. Use this edition for authenticated
fresh-Colab rehearsal.

The first publication is an evolving **prerelease**. Publishing it does not
close the full-fracture inverse, learned damage or DAgger implementation issues.
An MVP teaching release requires the scoped checklist in MVP_DELIVERY.md,
public-content audit, fresh-environment rehearsal and rendered cross-format
checks to pass. Retained outputs support participation when execution fails;
they do not establish fresh Colab performance. Full curriculum completion also
requires the outstanding extensions and final coherence issue. Keep the main
and child issues open while their full acceptance criteria remain unmet.

Maintain the plan and main issue together. New requests enter the coverage
table and a linked issue before implementation. Do not delete unfinished
requirements simply because they do not fit the first edition.

After each brainstorming discussion, update the owning issue with the decision,
file ownership, dependencies and acceptance checks. Create an additional issue
for a distinct deliverable, then cross-link it here. Reply to actionable comments
with the change and its evidence, preserving the discussion history. Review
runtime, scientific interpretation and rendered output before closing a task.
