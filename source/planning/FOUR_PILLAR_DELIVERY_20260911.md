# PhAST autumn school: four coordinated deliverables

Prepared by Allamaprabhu Ani and Sathiskumar A. Ponnusami, CEMS-Lab.
Course integration plan, 11 September 2026.

## Outcome

Students should explain a damage field, run and interpret a small PhAST case,
differentiate a defined observation, and train and assess a compatible learned
component. The slides, executable notebooks and web book should teach these
same outcomes in the same order. Pedagogy is the acceptance criterion shared
by the three formats.

The [90-slide storyboard](../slides/course-blueprint-20260911/STORYBOARD.md)
provides a precise authoring scaffold, including titles, learning points,
equations, figure placements, questions, reveal directions, sources and
notebook/book mappings. All 21 existing example/animation slots remain mapped.
Its equation and placement objects are editable through the supplied source;
LaTeX is also retained in presenter notes for Keynote's equation editor.
The earlier editable Keynote and animated overview remain preserved.
The [presentation reuse map](PRESENTATION_REUSE_MAP_20260911.md) traces the
WCCM/ECCOMAS PowerPoint, the earlier 32-slide lecture and the eight-slide
animated module into the 90-slide sequence. It distinguishes embedded assets
from the existing movies and research fields reserved for later insertion.

## One learning route

```text
Physical question → model and notation → numerical update → observable result
                                                               ↓
           train and assess a model ← checked gradient ← defined loss

                 SAME IDEAS IN THREE COMPLEMENTARY FORMATS
  Slides: physical picture + equation + question + presenter-controlled reveal
  Jupyter: prediction → short code → inspect output → exercise → worked solution
  Website: connected explanation + rendered mathematics + notebook/solution links

  Shared review: terminology · assumptions · pace · scope · reproducibility
```

The three practicals follow the three lecture themes. The main lecture block
contains 150 minutes (45/55/50). The three practicals contain 50 minutes each.
The six-hour event window retains 60 minutes for breaks, questions and setup
support. Ninety slides are small explanatory steps inside the existing budget,
including questions and handoffs. They are not ninety new topics.

| Deliverable | Current local material | Acceptance before student delivery | Issue owners |
|---|---|---|---|
| Presentation | 90-slide authoring scaffold; 45 fixed-scale LaTeX panels; original visual reuse; preserved 32-slide Keynote and eight-slide animated module | Lecturer selects final exhibits; every equation and notation is legible; source/assumption on results; native Keynote opening, animation playback and timed rehearsal | #12, #14, #20 |
| Jupyter notebooks | Three concise canonical labs, practice and worked-solution editions; fresh local CPU runs; targeted audit fixes | All cells run sequentially from a fresh kernel; code/output/solution parity; full computation under 300 seconds after setup; fresh Colab CPU rehearsal; downloads survive | #5–#10, #17–#18 |
| Website | Local three-lecture/three-practical Sphinx edition, retained chapters and optional readings | One coherent navigation path; correct math/figures; working deployed Colab and downloads; current credits; local/live content parity; desktop/mobile review | #11, #16, #20 |
| Pedagogy | [Independent cross-format audit](COURSE_COHERENCE_AUDIT_20260911.md), mapped learning questions and all registered slots | Same symbols and model scopes at each handoff; no hidden prerequisite; examples answer their stated question; beginner rehearsal within budget | #1, #15, #17, #20 |

## Reference layout and whitespace

The reference photographs suggest a geometric sans-serif font. Futura is the
closest locally available candidate, but exact identification requires the
original presentation metadata. Retain Arial and NewTX for the current build
and use the reference's composition: stable notation, aligned equations,
large physical pictures and deliberate open space.

- Canvas: 1280 × 720 CSS px, equivalent to 960 × 540 pt.
- Margins: 72 px; two 544 px content lanes separated by 48 px.
- Typography: title 34 pt, body 24 pt, caption 18 pt, page number 14 pt.
- Equation panels: fixed 28 bp NewTX; keep their physical scale when inserting.
- Equations receive up to half the content width. Long derivations split into
  successive steps. A short glossary sits with the relevant equation.
- Three-field comparisons use equal panels and common spatial/colour scales.
- The reference-based 35–45% open-area aim is a design target, not a measured
  claim for every slide. Check rendered content envelopes and visual balance.

See [reference typography review](REFERENCE_TYPOGRAPHY_20260911.md) for
photograph-specific estimates and their uncertainty. The authoring scaffold
uses visible reserved regions deliberately; replace their guidance when
filling final visuals. Conference photographs remain local design references.

## Scientific continuity at the three handoffs

1. **Practical 1:** quasistatic AT2, plane strain, isotropic degradation,
   assembled sparse-direct mechanics and the exact classroom constraints.
   Horizontal displacement is constrained on every exterior edge. Compare
   original and halved imposed separation. The current output teaches diffuse
   damage evolution. Dynamic branching and advancing-crack demonstrations
   keep their own source/configuration and runtime evidence.
2. **Practical 2:** degradation derivative, elastic-bar sensitivity and
   positive-modulus recovery. Define whether the parameter is modulus or log
   modulus. Distinguish a state derivative from a loss gradient. Preserve the
   observation operator and finite-difference check.
3. **Practical 3:** scalar Helmholtz field learning, reload and residual gate.
   Slides use `q` for this field and explicitly identify the notebook's `d`.
   Failed proposals invoke the current direct reference solve. Iterative
   refinement, learned fracture subsolves and DAgger remain separately scoped
   conceptual/research routes until their implementations pass review.

Research slides S48–S59 reserve 22 minutes for four inverse exhibits. The
inverse contributor supplies their approved data, parameters, observations,
derivative convention and provenance. If those exhibits are deferred, use the
same 22 minutes for worked bar recovery, observation-design exercises and
questions. Retain the authoring slots for later completion.

## Checks and next actions

- [x] Independently review typography/whitespace in five selected conference photographs.
- [x] Map all 90 slides to the current guides and notebooks, preserving all 21 slots.
- [x] Verify 45/55/50-minute source budgets and fixed-size equation bounds.
- [x] Execute all three pre-fix notebooks in fresh local processes and inspect every output figure.
- [x] Identify notebook readability and timing-reporting fixes with exact source locations.
- [x] Check live publication targets; curated pages/notebooks currently return 404.
- [x] Complete targeted notebook fixes, regeneration, final-source execution and parity review.
- [x] Rebuild local Sphinx with warnings treated as errors; pass classroom/theme checks and targeted desktop browser QA.
- [x] Complete final deck rendering and all 90 native-page visual checks; correct comparison-caption padding; verify native Keynote save/reopen and cleaned PowerPoint import.
- [ ] Select final inverse exhibits and assemble lecturer-approved media into the scaffold.
- [ ] Resolve the accuracy passages in reference chapters described below.
- [ ] Review and authorise one publication containing the curated notebooks, dependencies, pages and links.
- [ ] Verify every deployed notebook target and downloadable variant against the published revision.
- [ ] Run the deployed edition in fresh authenticated Colab CPU sessions.
- [ ] Rehearse lecture timing, three practical transitions and playback on the presentation machine.

Final local complete-process times were **93.176, 4.614 and 5.118 seconds**.
The [final correction receipt](../../evidence/classroom_runs_20260911b/README.md)
records source hashes, setup and post-setup timings, environment and variant
parity. Practical 2 now compares matching training and validation displacement
RMSE. Practice introductions point to worked solutions, setup timing includes
imports, and the setup guide uses the current runner. Numerical settings and
recovery outputs are preserved. These runs used already installed local
dependencies; fresh installation and authenticated Colab remain separate gates.

The final local HTML build passed `sphinx -b html -E -a source/book book -W
--keep-going`, `check_classroom_curation.py` and `check_book_theme.py`.
The [desktop browser postfix](COURSE_COHERENCE_AUDIT_20260911.md) verifies the
updated RMSE explanation/plot, download parity, setup receipt and solution
disclosures. Mobile-width review remains open.

The live publication remains the older six-notebook edition. The new Colab
buttons cannot yet retrieve their target files from GitHub main. Changing
only the homepage or checking Colab's HTTP-200 app shell will not resolve
this. Publish the complete reviewed candidate when authorised, then run the
public path as a student would.

## Accuracy passages for the next editorial decision

The working tree includes existing edits. The audit records these passages
for targeted review rather than silently replacing them during slide work:

| Existing wording/claim | Suggested factual replacement | Source |
|---|---|---|
| Fixed-field subproblems described as unconditionally linear/well-conditioned/strictly convex | “For the selected material model and boundary conditions, fixing one field produces a smaller subproblem. Its linearity and conditioning depend on the formulation.” | `source/book/03_staggered_solution.md` opening |
| Inverse solvers described as brute-force guessing, with exact gradients pinpointing true properties | “A derivative describes how the chosen observation or loss changes locally. Recovery also depends on the information in the observations, initialisation and model assumptions.” | `source/book/05_differentiation_and_inverse.md` opening |
| FE called exact; universal sub-millisecond inference and guaranteed hybrid accuracy | “A learned model proposes a field. The numerical residual and stated constraints assess that proposal. Evaluate field error and complete computation time for the selected case.” | `source/book/06_learning_adapter.md` opening |

## Clear prompts for the next build contributors

### Presentation contributor — issue #12

Read AGENTS.md and its required documents, this plan, the typography review,
the 90-slide storyboard and the placeholder register. Work only in an assigned
copy of the authoring scaffold. Fill slides S01–S30 first, using verified
PhAST visuals with source/configuration labels. Use the fixed font roles and
equation scale. Preserve the same specimen and numerical scope across the
Practical 1 handoff; retain the actual exterior horizontal constraints and
half-separation comparison. Put each new animation in MP4 with a static PNG
alternative and explicit presenter controls. Record which prior slide/module
each filled slide replaces. Render and inspect every affected slide at full
size, then test the native Keynote file. Deliver editable slides, original
sources, a changed-slide map and QA evidence. Leave unapproved research slots
labelled in the authoring source. Do not publish or alter notebooks.

### Notebook contributor — issues #10/#17/#18

Read AGENTS.md, CONTRIBUTING.md, the final notebook correction receipt and
the coherence audit. Use only the three classroom notebooks and their
authoritative generators. Preserve numerical settings unless a separately
approved task changes them. Review one objective and prediction, short visible
code, interpretable outputs, two exercises and matched worked solutions in
each notebook. Test from fresh kernels in an isolated snapshot; report setup,
computation and whole-process timings with environment and code hashes. After
publication, ask the user to open the exact deployed Colab targets in fresh
CPU runtimes and record those results separately. Do not infer cloud success
from local execution or a Colab application-shell response. Deliver patched
authoring source, regenerated variants, outputs and dated receipts.

### Website contributor — issues #11/#16/#20

Read AGENTS.md, this plan, the live-target audit and the current publication
receipt. Integrate the three guides and three labs as the primary student
path, retaining detailed material under further practice. Use Prepared by
Allamaprabhu Ani and Sathiskumar A. Ponnusami for book credits; keep Presented
by wording on the presentation. Generate from source, build with warnings
treated as errors, and check equations, layout, figure descriptions, worked
solutions and downloads. Test desktop and narrow mobile widths. Produce an
exact publication manifest including helpers and notebook variants. Request
publication authority if the current task does not grant it. After an
authorised push, compare deployed files with the manifest and check every
Colab GitHub target. Do not close issues on a local-build pass alone.

### Pedagogical reviewer — issues #15/#17

Read all three lecture guides, the final slide notes and all notebook cells.
Trace one novice learner through each physical question, equation, code cell,
figure and exercise. Record concrete undefined symbols, hidden prerequisites,
inconsistent constraints, observation/loss mismatches and claims exceeding the
example's evidence. Review each final slide and plot visually. Check the
150-minute lecture and 150-minute practical budget using a timed rehearsal.
Keep essential physical and derivative assumptions concise and visible.
Return a prioritised list with exact source locations, suggested corrections
and which acceptance gates remain open. Make no numerical or publication
changes during an independent review.

## Issue synchronisation packet

Use this plan for a main-issue update under #1 and the active curation issue
#20. Link the storyboard and audits; describe the presentation as an authoring
scaffold. Record targeted notebook fixes and their final receipts when ready.
Keep #10/#11 open for publication and authenticated Colab; keep #12 open for
final visuals, animation assembly and timed playback. Keep #7/#8/#9 open for
their separately owned research/implementation evidence. No remote issue was
closed or updated by this local preparation pass.
