# Animated lecture spine — 10 September 2026

The course has three lecture hours followed by three practical hours. Use
`TEACHING_SCHEDULE.md` for the 60-minute teaching blocks. The present 23-slide
candidate provides a coherent editable spine with selected animations; the
44-slide LaTeX resource supplies the longer worked explanations. Select and
rehearse those explanations inside each allocated hour.

Presenter: Sathiskumar A. Ponnusami, Queen Mary University of London · CEMS-Lab.
Course creator attribution remains in ordinary document metadata and notes.

## Teaching map

| Block | Candidate slides | Use in the lecture | Additional resource to integrate |
| --- | --- | --- | --- |
| L1, 0–13 min | 1–2; preview 9–10 | Establish the damaged-body question, fields and response; introduce the day's learning route. | `Three descriptions of an evolving crack`; `Fracture models and solution algorithms`. |
| L1, 13–26 min | 3–5 | Define the damage convention, energy terms and degradation; use the AT2 profile to explain the length scale. | `AT1 and AT2 choose the crack-density term`; `The mesh must resolve the chosen length`; `Crack initiation, propagation and branching`. |
| L1, 26–40 min | 6–7 | Trace coupled-field updates; separate a fixed-load staggered iteration from a partitioned dynamic time step. | `A staggered step alternates coupled problems`; `Time integration and nonlinear iteration are different`. |
| L1, 40–50 min | 8 | Gather, element kernels, quadrature and scatter expose the finite-element structure. | `Matrix-free means applying an operator`; `Tensors still have physical locations`. |
| L1, 50–60 min | 9–10; preview 11 and 20 | Preview the actual PhAST practical and motivate sensitivities and learned assistance. | `Boundary sets and prescribed values`; `Read response and numerical checks together`. |
| L2, 0–35 min | 11–13 | Define input, state, observation and loss; derive reverse accumulation; sum every shared-parameter contribution. | Book `05a_backpropagation_step_by_step`; the explicit scalar example and its manual derivative. |
| L2, 35–45 min | 14–15 | Explain the transposed implicit solve and history branch sensitivity. | Book `05_differentiation_and_inverse`; optional `research/history`. |
| L2, 45–60 min | 16–17 | Check derivatives at several spacings and connect to a small parameter-recovery problem. | `Choose an informative inverse observation`; elastic-bar Lab 03. The diffusion notebook is an alternative within this allocation. |
| L3, 0–32 min | 18–20 | Establish the learned model's role, physical checks and training graph. | `The data card defines what learning means`; `An MLP maps named features to a named target`; `A checkpoint is more than weights`; `A model swap requires compatible inputs`. |
| L3, 32–45 min | 21 | Assess, correct and recheck a proposed field. | `Admissibility and equilibrium`; `Acceptance needs an explicit correction route`. |
| L3, 45–60 min | 22–23 | Connect reproducibility and the practical learning cycle to model improvement. | `DAgger learns from states the model visits`; one approved research example inside the remaining slot. |
| P1 / P2 / P3 | 9–10 / 11–17 / 18–23 as reference | Run PhAST / check derivatives and recovery / train, reload and assess proposals. | Labs 01 / 02–03 / 04–05 with worked solutions. |

The resource titles above refer to
`source/slides/phast_autumn_school_2026.tex`. Its older A/B/C timing notes
require alignment with the current three-lecture/three-practical allocation
when individual resource slides are integrated. The resource remains intact.

## Animation cues and static fallbacks

| Slide | Concept and original clip | Length | Pause cue | Question |
| --- | --- | --- | --- | --- |
| 4 | Analytic AT2 profile, `phase_field_band.mp4` | 24.8 s | About 15 s, while the band widens | How should the mesh change when the regularisation length is halved? |
| 7 | Partitioned update, `explicit_implicit_step.mp4` | 26.5 s | About 11 s, once the damage stage appears | Which fields are held fixed during the mechanics and damage updates? |
| 13 | Shared parameter, `reverse_accumulation.mp4` | 27.7 s | About 15 s, after the backward state path | Why does the final derivative contain one contribution from each update? |
| 15 | Material-point history, `history_switch.mp4` | 18.0 s | About 10 s, at the tie state | During unloading, which input receives the hard-history sensitivity? |
| 21 | Checked proposal, `checked_learned_proposal.mp4` | 26.5 s | About 15 s, on the correction route | Which checks should a proposed damage field satisfy before acceptance? |

Each movie is inside the PowerPoint package. The `media/` folder also contains
the same movie and a static PNG poster for independent playback or discussion.
Presenter notes contain the pause question, suggested answer, notation bridge,
original source and teaching scope. The reverse clip uses x, θ and L for the
state, parameter and loss represented by z, p and J in the preceding equations.

## Scientific scope

- The AT2 animation evaluates an isolated analytic profile.
- The dynamic update illustrates a partitioned algorithm. The forward practical
  uses the public quasistatic PhAST route and its own verified configuration.
- Reverse accumulation assumes a fixed initial state, differentiable update
  maps and a terminal scalar loss. Direct parameter terms and initial-state
  sensitivity enter the more general formula in the book.
- The history clip is a dimensionless material-point primitive. The green
  sigmoid curve specifies a surrogate backward rule. A hard maximum has a
  branch-dependent derivative and requires a convention at a tie.
- The model graphic explains an interface contract. The practical MLP/RBF
  calculations use the stated Helmholtz-type teaching model.

## Presentation-machine rehearsal

Open the candidate from a fully downloaded local directory. Test slides 4, 7,
13, 15 and 21 in Keynote and PowerPoint: click to play, pause at the cue, seek,
replay, then advance. Confirm that the media and equations remain visible with
the network disconnected. Inspect the history-panel labels from the back of
the teaching room; the companion book provides a larger view for close study.
Record any exact import warning before replacing the validated v7 fallback.
