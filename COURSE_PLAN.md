# PhAST Autumn School: course plan and completion record

This is the versioned plan for a coherent six-hour lecture series, supported
by one interactive book, executable notebooks, worked solutions and slides.
The main planning issue links the topic issues; this file preserves the
curriculum when issues are closed or reorganised.

## Purpose and audience

Students should move from understanding the fracture model to running a small
calculation, interpreting it, differentiating a defined computational graph,
and evaluating the role of a learned component. Assume basic calculus, linear
algebra and introductory Python; introduce the FEM and autograd notation used
in the activities. Do not assume experience with phase-field fracture.

The intended event is the UKACM Autumn School, 14–17 September 2026, with the
organiser-led sessions on 15–16 September. Confirm room-level scheduling,
speaker credits and programme wording with the organisers. This plan concerns
the three two-hour phase-field/differentiable-computing sessions, not the
entire event programme.

## Learning sequence

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

## Three two-hour sessions

| Session | Principal question | Student outcome |
| --- | --- | --- |
| A: model and numerical method | What represents a crack, and what do we solve? | Explain the energy, degradation and length scale; distinguish a formulation from a discretisation or nonlinear algorithm. |
| B: computation and derivatives | How does an input affect the final result? | Run and interpret a small public PhAST case; trace a chain rule; compare analytic, autograd and finite-difference sensitivities. |
| C: learning and model interfaces | What can a learned component replace or propose safely? | Train/save/reload a small model; inspect a model contract; accept, correct or reject a proposal using explicit checks. |

The minute-by-minute allocation is in [TEACHING_SCHEDULE.md](TEACHING_SCHEDULE.md).
The opening teaser fits inside the opening ten minutes, not on top of them.
Larger paper studies are optional extensions or explicitly replace an allocated
slot. A 45-minute paper discussion is not silently added to a full six-hour day.

## Coverage and remaining work

| ID | Workstream | First-edition position and next gate |
| --- | --- | --- |
| C01 | Phase-field foundations and comparisons | Explanations and figures exist. Review XFEM/cohesive trade-offs; do not call quasi-Newton a competing fracture formulation or claim universal phase-field superiority. |
| C02 | Energy, degradation and damage morphology | Equations, derivative notebook and browser controls exist. Audit AT1/AT2 normalisation, profiles, continuity, mesh/length-scale effects and initiation/branching explanations. |
| C03 | Solution algorithms and coupled physics | Staggering, static/dynamic and matrix-free concepts exist. Complete the transport/solid/damage operator narrative and distinguish physical time, load stepping and nonlinear iteration. |
| C04 | First PhAST simulation | Public source, generated mesh, loads/BCs, fields and reaction checks run locally. Add a clear imported-mesh route and a better short propagating-crack example without weakening checks. |
| C05 | Backpropagation explained step by step | Add explicit local derivatives, adjoint propagation, shared-parameter sums, numerical checks and a clean diagram; distinguish observable, gradient and optimisation update. |
| C06 | Inverse recovery | The elastic-bar toy runs. A small actual fracture-parameter/inclusion recovery remains a separate implementation and validation task using approved public material. |
| C07 | Train, save, reload and interchangeable models | MLP/RBF toy field examples run. Define and validate fracture-compatible damage inputs/outputs and saved-model contracts; do not imply arbitrary architectures are interchangeable automatically. |
| C08 | Hybrid correction and DAgger | Toy accept/reject/fallback runs; DAgger is explained. A complete model-induced rollout, reference labelling, aggregation, retraining and held-out evaluation remains to be built. |
| C09 | Laptop/Colab execution | All six notebooks have local receipts below 90 seconds after setup. Fresh installation, fresh Colab and slower-laptop rehearsal remain open; all activities must stay below 300 seconds. |
| C10 | Integrated book and accessibility | Native code/output chapters, practice/solution downloads, HTML/PDF and visual explorations exist. Review offline/mobile/keyboard/print behaviour and all links after every edition change. |
| C11 | Coherent lecture slides and animations | A clean 44-slide LaTeX deck exists. Align the new teaser and explicit backpropagation sequence; review pacing, readable equations and original animations against the final book. |
| C12 | Paper-based extension studies | Select approved public papers and reproducible retained results, with one question and one limitation per study. Do not publish private worktrees or unapproved checkpoints. |
| C13 | Teaching references and design standard | D2L, PBDL, ADL4P and programme materials inform the design. Complete the source inventory for any remaining supplied Instagram/PDF repository lists; do not imply inaccessible material was inspected. |
| C14 | Final coherence and completeness | Perform a learning-objective, notation, prerequisite, example, cross-format and timing audit; map every requested topic to a deliverable or an explicit open issue. |
| C15 | Release, credits and community | Public repository, Pages and downloadable editions are the delivery route. Confirm credits/content licence, contributor guidance, follow-up exercises and a public showcase before claiming a finished course release. |

## Evidence required before marking an issue complete

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
The teaching-ready release requires the final coherence issue, public-content
audit, fresh-environment rehearsal and rendered cross-format checks to pass.

Maintain the plan and main issue together. New requests enter the coverage
table and a linked issue before implementation. Do not delete unfinished
requirements simply because they do not fit the first edition.
