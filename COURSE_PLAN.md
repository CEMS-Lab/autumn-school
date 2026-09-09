# PhAST Autumn School: course plan and completion record

This is the versioned plan for a coherent six-hour course, supported
by one interactive book, executable notebooks, worked solutions and slides.
The main planning issue links the topic issues; this file preserves the
curriculum when issues are closed or reorganised.

## Latest delivery decision: a minimum viable course

The latest autumn-school discussion sets **three hours of lectures followed
by three hours of interactive exercises**. Lecture 1 covers fracture,
staggered solution and matrix-free operators and must already motivate
differentiability and hybrid learning. Lecture 2 develops differentiability;
lecture 3 develops hybrid approaches. The exercises revisit those questions
in the same order.

This is a local next-edition plan. Published v0.1.1 still has the earlier
mixed two-hour sessions. The book, slide timings and overview must be rebuilt
and reviewed before publishing this change. See [MVP_DELIVERY.md](MVP_DELIVERY.md)
for the selected scope and [BUILD_AGENT_PROMPTS.md](BUILD_AGENT_PROMPTS.md)
for bounded build assignments. Preserve the complete issue inventory below.

Timing assumption: 360 minutes of contact time, with lunch and breaks outside
that allocation. The previous edition had 330 contact minutes and 30 minutes
of breaks. The schedule supplies a 330-minute fallback pending organiser
confirmation; these allocations are not interchangeable.

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

The new live route is L1 fracture/numerics → L2 derivatives → L3 hybrid
methods, followed by P1 PhAST → P2 derivative/recovery exercises → P3
training/proposal assessment. The current graphical overview belongs to the
previous edition until rebuilt. The longer sequence below preserves the
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

## Three lecture hours and three exercise hours

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

These are the full course ambitions. The MVP checklist in MVP_DELIVERY.md
selects the classroom subset without closing or deleting unfinished extensions.

| ID | Workstream | First-edition position and next gate |
| --- | --- | --- |
| C01 | Phase-field foundations and comparisons | Explanations and figures exist. Review XFEM/cohesive trade-offs; do not call quasi-Newton a competing fracture formulation or claim universal phase-field superiority. |
| C02 | Energy, degradation and damage morphology | Equations, derivative notebook and browser controls exist. Audit AT1/AT2 normalisation, profiles, continuity, mesh/length-scale effects and initiation/branching explanations. |
| C03 | Solution algorithms and coupled physics | Staggering, static/dynamic and matrix-free concepts exist. Complete the transport/solid/damage operator narrative and distinguish physical time, load stepping and nonlinear iteration. |
| C04 | First PhAST simulation | The existing public run is quasistatic with SciPy sparse-direct mechanics. The requested explicit-mechanics/implicit-damage, matrix-free demonstration needs a validated replacement or an explicit lecture-to-quasistatic-exercise bridge. Imported external meshes and short propagating-crack examples remain extensions. |
| C05 | Backpropagation explained step by step | Explicit local derivatives, adjoint propagation, shared-parameter sums and a checked three-step algebraic example exist. Revised book/lecture diagrams distinguish observable, gradient and optimisation update; a toy derivative check is not a full fracture-path validation. |
| C06 | Inverse recovery | The elastic-bar toy is the minimum classroom route. The separate inverse/history handoff remains unmerged pending source, timing and coherence review. Primitive/history checks do not establish full fracture recovery. A small actual fracture-parameter/inclusion recovery remains a separate task. |
| C07 | Train, save, reload and interchangeable models | MLP/RBF toy field examples run. Define and validate fracture-compatible damage inputs/outputs and saved-model contracts; do not imply arbitrary architectures are interchangeable automatically. |
| C08 | Hybrid correction and DAgger | Toy accept/reject/fallback runs; DAgger is explained. A complete model-induced rollout, reference labelling, aggregation, retraining and held-out evaluation remains to be built. |
| C09 | Laptop/Colab execution | All six notebooks have local receipts below 90 seconds after setup. Fresh installation, fresh Colab and slower-laptop rehearsal remain open; all activities must stay below 300 seconds. |
| C10 | Integrated book and accessibility | Native code/output chapters, practice/solution downloads, HTML/PDF and visual explorations exist. Review offline/mobile/keyboard/print behaviour and all links after every edition change. |
| C11 | Coherent lecture slides and animations | A clean 44-slide LaTeX deck exists. Align the new teaser and explicit backpropagation sequence; review pacing, readable equations and original animations against the final book. |
| C12 | Paper-based extension studies | Select approved public papers and reproducible retained results, with one question and one limitation per study. Do not publish private worktrees or unapproved checkpoints. |
| C13 | Teaching references and design standard | D2L/PBDL inform the book. The design standard records inspected Delft textbook, TUM lecture and ETH research-presentation visuals; original flowcharts apply those patterns. Remaining supplied Instagram/PDF repository lists still need a complete inventory; do not imply inaccessible material was inspected. |
| C14 | Final coherence and completeness | Perform a learning-objective, notation, prerequisite, example, cross-format and timing audit; map every requested topic to a deliverable or an explicit open issue. |
| C15 | Release, credits and community | Public repository, Pages and downloadable editions are the delivery route. Confirm credits/content licence, contributor guidance, follow-up exercises and a public showcase before claiming a finished course release. |

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
Footer credit: created by Allamaprabhu Ani and Sathiskumar A. Ponnusami,
CEMS-Lab; prepared for the UKACM Autumn School 2026. Preserve third-party credits.

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
