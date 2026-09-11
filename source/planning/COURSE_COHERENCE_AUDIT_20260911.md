# Course coherence and website audit — 11 September 2026

## Assessment and scope

The local three-lecture/three-practical route has a coherent teaching sequence: interpret a fracture calculation, differentiate a defined observable, then assess a learned field proposal. Its principal delivery gap is publication. Fresh unauthenticated requests on 11 September confirm that the three curated public lab pages and their GitHub-main practice notebooks return HTTP 404. The published homepage still presents the preceding six-notebook, three-plus-three-hour edition.

The requested 90-slide scaffold should expand the explanation within the existing **45/55/50-minute lectures**, followed by **three 50-minute practicals** and **60 minutes of breaks/questions/setup support**. Lunch remains outside the six-hour allocation. Ninety planned slides establish an authoring map; completed figures, exhibits, animation playback and timed teaching require their own reviews.

This audit read the authoring directives, course plan, current delivery record, schedule, all three lecture guides, all classroom notebook Markdown cells, selected authoring/helper code, reference chapters, placeholder register and existing slide storyboards. It inspected the live homepage and local classroom route in a browser, including a rendered expanded worked solution. Notebook execution belongs to the separate execution audit. No solver, notebook calculation, publication, issue update or remote mutation was performed here. The only repository file owned by this audit is this report.

## Priority recommendations

| Priority | Concrete gap and learner consequence | Evidence | Recommended next change | Existing issues |
| --- | --- | --- | --- | --- |
| P1 | Curated Colab badges refer to notebooks absent from public main. Learners following the new local route cannot retrieve those notebooks through Colab. | Fresh HTTP checks below; badge generation in `source/book/scripts/build_classroom_pages.py:70`; local P1/P2/P3 first Markdown cells. | Publish the reviewed notebooks, helpers and generated pages together when authorised. Verify the exact GitHub-main targets and downloaded content, then perform fresh authenticated Colab rehearsal. During local review, identify the curated edition as local and use the complete local course folder. | #10, #11, #20 |
| P1 | The public homepage teaches the previous 180+180-minute allocation and lists six labs. It conflicts with the planned lecture/lab handoffs. | Live `book/index.html`: “3 Hours of Interactive Demonstrations” and “3 Hours of Hands-on Lab Notebooks”; local `TEACHING_SCHEDULE.md:5–7,14–16,26–28`. | Treat the homepage, navigation, notebook downloads and slide/book links as one versioned delivery. Preserve 150 lecture + 150 practical + 60 flexible minutes. | #11, #15, #20 |
| P1 | Reference-chapter introductions overstate the numerical and learning evidence, contradicting their later qualifications and the curated guides. | `source/book/03_staggered_solution.md:22–24`, `05_differentiation_and_inverse.md:18–27`, `06_learning_adapter.md:12–23`; details below. | Prepare a targeted accuracy/tone revision of these passages, preserving the user's current edits and scientific qualifications. Use model-dependent linearity, selected derivative maps and measured complete cost. | #15, #17; mathematical topics #4, #6, #9 |
| P1 | Twenty-two minutes of L2 are reserved for four inverse exhibits whose numerical evidence is still unselected or unreviewed. The non-particle application remains unnamed. | L2 guide “A sequence of fracture inverse applications · 28–50 minutes”; L2-R01–R04 in the register. | Keep their planned layouts and questions. Before rehearsal, either integrate approved evidence or explicitly teach an observation/parameterisation exercise using the available algebraic/bar examples within that same time allocation. A planned result-panel label must not become an asserted recovery result. | #12, #15, #20; inverse evidence #7 |
| P2 | The overview mesh and actual P1 use different lateral restraints. Reusing the overview as the practical setup could change the student's expected deformation. | `source/slides/phast-overview/storyboard.json`, mechanics-slide notes: one horizontal anchor; P1 Markdown cell 9 and `build_classroom_labs.py`: $u_x=0$ on every exterior edge. | Give the P1 handoff its actual boundary sketch and state top/bottom motion, total separation and all lateral restraints visibly. Label the overview mesh as illustrative. Keep the tested configuration unchanged in a prose/slide pass. | #12, #15, #17; practical #5 |
| P2 | “Correction” names both a direct reference fallback and a possible iterative refinement, making the taught algorithm ambiguous. | P3 cells 18–21; `build_classroom_labs.py:557,566,570–579`; helper `course_tools.py:677–681`; local index row for Lab 3. | Name the current branch “direct reference solve/fallback”. Present iterative correction and its recheck as a separate conceptual route. Keep the actual learned-damage PhAST interface and this Helmholtz demonstration distinct. | #12, #15, #20; hybrid #9 |
| P2 | The classroom residual formula and existing slide formula use different denominator conventions. | P3 cell 18 and `course_tools.py:477–480`: $\lVert b\rVert_2+10^{-15}$; curated storyboard S26: $\max(\lVert b\rVert,\epsilon)$. | Use the implemented denominator when displaying the specific classroom residual. A generic alternative may be labelled as such. This is a reproducibility/notation mismatch; no material discrepancy for the present nonzero forcing was established. | #12, #15 |
| P2 | The mechanics chapter predicts a propagating crack and dynamically increased iteration counts for the next practical, whereas P1 explicitly teaches diffuse damage accumulation. | `03_staggered_solution.md:190–194`; P1 cells 2,24,34; P1-R01 remains open. | Describe the actual current fields and reaction response. Put a propagating-front demonstration in its registered extension with its own evidence. | #15, #17, #20; propagation #5/#19 |
| P2 | The new slide map links whole notebooks, with no cell/section anchors. Several preserved decks can otherwise be inserted with duplicated introductions and unbudgeted time. | `CURRENT_DELIVERY.md:27–56`; 32-slide companion, 23-slide introduction, 44-slide resource, separate overview module; all 90 expanded records now link their lecture and notebook. | Refine the existing file-level crosswalk with the precise cell/section handoffs below. State whether a reused module replaces planned slides or is optional. | #12, #15, #20 |
| P2 | One delivery sentence incorrectly calls the current timing superseded. | `TODAY.md:75`: “the curated 150+150-minute core; the active curation above supersedes that timing”. | Clarify that the earlier 180+180 or other historical allocation is superseded. Preserve the current 150+150 core. | #15, #20 |
| P3 | The global damage convention and reused symbols obscure changes of model between lectures and labs. | Local `source/book/index.md:51–52`; P3 defines $d$ as a scalar Helmholtz field; $\lambda$ denotes adjoints in L2 and loading elsewhere; $z$ denotes solver state and later log modulus. | Add a short notation recap at each transition. Say that the same symbol $d$ denotes a dimensionless teaching field in P3. Distinguish adjoint and load labels locally; define log modulus separately. | #12, #15, #17 |
| P3 | P3's worked weight-gradient expression introduces an undefined $\mathbf z_i$, whereas the feature row is described explicitly and the slides use $x_i$. | `source/book/solutions/04.json:14–16`; P3 worked solution 1, visible in the local browser. | Define the normalised feature vector before the formula or use the same feature symbol throughout. Preserve the correct factor $2/M$. | #15, #17 |
| P3 | Classroom image alternative text is generic, which loses the learning point for readers using assistive technology. | Local P3 figure links read “Computed field or curve from Practical 3…”; bootstrap `display_figure` defaults to “Rendered teaching figure”. | Supply concise figure-specific alternative text describing fields, comparison, scale and observed result. Review meaningful figures rather than image counts alone. | #11, #17 |

## Material accuracy passages to resolve

1. **Fixed-damage mechanics and fixed-displacement damage.** The opening of `03_staggered_solution.md` calls mechanics unconditionally well-conditioned and linear, and damage unconditionally strictly convex. The same chapter later states that linearity depends on constitutive choices and boundary conditions. Teach the scoped model first and retain those conditions. The line $g(d)\to0$ at line 15 also needs the stated residual-stiffness convention when referring to this course's $g_\eta(1)=\eta$.
2. **Gradient and inverse recovery.** The opening of `05_differentiation_and_inverse.md` claims earlier inverse methods require brute-force guessing and that an exact gradient allows an optimiser to pinpoint true material properties. These claims omit earlier gradient/adjoint methods, non-identifiability, local minima, model discrepancy and derivative scope. Its later forward-map, implicit/unrolled and identifiability sections give a suitable basis for a restrained replacement.
3. **Hybrid accuracy and speed.** The heading “The Best of Both Worlds: Fast AI Proposals & Physics Truth” and opening of `06_learning_adapter.md` describe FE solvers as exact, claim inference takes a fraction of a millisecond, and promise reduced iterations with guaranteed physical accuracy. None of these universal conclusions follows from the classroom example. State the selected numerical residual, acceptance conditions, field error and measured complete route when available. The current proposal/fallback exercise supplies no acceleration measurement.

These are proposed corrections, not edits made by this audit. The current working tree contains user changes and they must remain intact.

## Proposed 90-slide learning path and lab handoffs

The actual scaffold at `source/slides/course-blueprint-20260911/storyboard.json` was read in three complete batches covering **all 90 records**, including learning points, equations, notation, visual plans, notes and slot mappings. Counts and summed allowances are L1 30 slides/45 minutes, L2 32 slides/55 minutes and L3 28 slides/50 minutes. Each named local lecture, notebook, supporting chapter and reused asset path exists. Its subsection budgets match the current guides. These are source checks; rendered 90-slide readability and equation-width checks belong to the separate build review.

| Block | Learning progression within the fixed time | Lab handoff and evidence to interpret |
| --- | --- | --- |
| L1, 45 min; S01–S30 planned | Notched specimen and diffuse representation (6); energy/degradation/length scale (12); one increment with accepted history (13); element tensors, operator actions and dynamics (10); practical connection (4). | P1: retain actual quasistatic AT2, isotropic degradation, plane strain and assembled sparse-direct mechanics. Revisit actual BCs and predict the half-separation change. Read full displacement/damage fields alongside reaction–separation curves. |
| L2, 55 min; S31–S62 planned | Parameter/observable/loss (6); forward updates and local VJPs, summing every shared-parameter use (12); derivative scope and checks (10); four planned inverse exhibits (22); practical connection (5). | P2: distinguish local $g'(d)$, the bar's $\partial_Eu_{\mathrm{tip}}$, and the optimisation gradient in log modulus. Identify synthetic observations and fixed loads. A held-out positive load tests fitted linear compliance, rather than new nonlinear physics. |
| L3, 50 min; S63–S90 planned | Define/train a small model (8); learned damage subsolve within staggering (10); prediction, assessment and correction/fallback (10); compatible model representations (10); online learning and DAgger-style aggregation (8); practical connection (4). | P3: keep whole load cases in each split; show training and reload; inspect full Helmholtz fields; vary tolerance and interpret the selected branch. DAgger and a learned fracture subsolve remain conceptual extensions. |

Each lab can begin with a two-minute retrieval question inside its existing setup/introduction budget: “Which model and boundary conditions are we using?”, “Which scalar is differentiated with respect to which parameter?”, or “What does this field and residual represent?” This reconnects the afternoon practicals to the morning lectures without changing contact time.

For a readable expanded scaffold, allocate a short slide to introducing symbols before an equation, then use a separate worked step or visual interpretation where needed. Preserve the measured quantity and assumption beside the result. Ninety slides should not become ninety independent topics. Diagram builds can carry several states of one explanation, and review notes should identify them as such.

The existing 32-slide companion correctly includes the complete shared-parameter gradient in notes and visible assumptions for its shortened formula. Carry both into the expansion. For a terminal loss $\ell(z_N,p)$, include its direct parameter derivative, the VJP contribution from every parameter-dependent update, and any parameter dependence of the initial state:

$$
\nabla_p J=\partial_p\ell+\sum_{n=0}^{N-1}B_n^{T}\lambda_{n+1}
+(\partial_p z_0)^{T}\lambda_0,\qquad B_n=\partial_p F_n.
$$

If stage losses are introduced, include their reverse seeds. Conditional history/active-set derivatives need an explicit local path convention. The scalar recurrence, bar, Helmholtz model and full fracture path each have separate scopes.

### Findings from the actual 90-slide source review

The expanded progression is coherent: the bar introduces a scalar derivative before Jacobians/VJPs; the branched scalar example motivates gradient accumulation; the same unrolled graph leads into implicit differentiation and conditional crack-event scope. S41–S42 correctly include the terminal-loss adjoint recurrence, every update's parameter contribution, and direct loss dependence. S46 has the correct adjoint sign for a residual-defined state. S74 matches the classroom residual denominator, resolving that mismatch in the expanded route. S75 and S76 distinguish proposed iterative correction from the implemented direct fallback. The DAgger-style slides retain conceptual status and held-out evaluation.

Concrete source corrections requested during this audit, followed by a fresh source recheck:

- **S30 — corrected in source:** the initial original/increased-loading instruction now uses original/halved separation, matching P1.
- **S42 — corrected in source:** the fixed initial-state assumption is now an explicit equation-panel line; the additional initial-state contribution remains in notes.
- **S64 — corrected in source:** a visible $q\equiv d_{\mathrm{notebook}}$ statement now bridges the slide's Helmholtz symbol to the executable notebook convention.
- **S12 — corrected in source:** visible AT1 and AT2 rows now carry both crack-density laws and their stated normalisation, as the lecture guide requests.
- **S51–S56:** after selecting the inclusion example, state whether geometry parameters act through a smooth fixed-mesh material field or a different geometry/mesh map. The derivative scope must accompany the selected parameterisation.
- **S66 — corrected in source:** the visual instruction and notes now both specify the five training operations.

S12's crack-measure integral and S42's gradient sum are likely wide at the fixed 28 bp equation size; only actual typesetting can establish whether splitting is required. These width candidates are not claims of observed clipping. S17 now specifies the correct horizontal exterior constraints; S29 requests a visible scope descriptor distinguishing the isotropic, quasistatic, assembled classroom mode from other examples.

Suggested precise handoffs use zero-based indices in the current canonical notebooks:

| Lecture slides | Classroom destination | Immediate learner action |
| --- | --- | --- |
| S17, S29–S30 | P1 cells 9–16, then 20–33 | State the actual constraints; predict the smaller-separation response; inspect saved full fields and reaction. |
| S60–S61 | P2 cells 2–9, 10–15, 16–25 | Check degradation, differentiate the bar, then recover modulus and interpret held-out compliance. |
| S64–S67, S88 | P3 cells 2–13 | Identify whole-load splits, feature order and the five training operations; reproduce a saved prediction. |
| S74–S76, S89 | P3 cells 18–27 and exercise 2 at cell 34 | Read the implemented residual/threshold, identify the selected branch, then vary the tolerance. |

Use stable section anchors in published links where possible, since regeneration can change cell indices. For the P1 convergence handoff, retain its actual relative field-change criterion ($10^{-5}$ for both fields), rather than relabelling that trace as a mechanics or constrained-damage residual norm.

### Placeholder preservation

The register contains 15 lecture slots and 6 practical slots, all open. A reused figure or an authored layout does not complete its numerical or animation acceptance requirements.

- L1: L1-A01, L1-W01, L1-A02, L1-W02; P1 handoff: P1-R01 and P1-A01.
- L2: L2-A01, L2-W01, L2-R01, L2-R02, L2-R03, L2-R04; P2 handoff: P2-R01 and P2-A01.
- L3: L3-W01, L3-A01, L3-A02, L3-W02, L3-A03; P3 handoff: P3-R01 and P3-A01.

The 90-slide manifest contains all 21 IDs: L1 slots map to S05, S07/S09/S13, S18–S20/S22 and S23/S26/S27; L2 worked/animation slots map to S35/S43–S45 and S37/S40–S42, and its four research slots to S48–S59; L3 slots map to S64/S66/S67/S88, S68–S72, S73–S77, S78–S82 and S83–S86. Practical slots occur at S29–S30, S34–S35/S61 and S72–S73/S76/S89. The central register currently also retains the 32-slide map. Add the expanded mapping alongside that retained route, preserving every original ID and its open acceptance status.

## Live URL evidence

Read-only checks used unauthenticated HTTP GETs during this audit. GitHub main resolved to `48ae30794de3da1f4242bfbefff124dfd0d9a594`, committed 10 September 2026 at 13:14:52 UTC. The local checked-out HEAD was the same, with substantial uncommitted curation. A shared HEAD identifier therefore does not imply that local classroom files exist in the published tree.

| URL or exact path family | Observed status |
| --- | --- |
| [Published homepage](https://cems-lab.github.io/autumn-school/book/index.html) | 200; previous homepage title and six-lab route; browser inspection confirms the 3+3-hour text. |
| [Public L1 guide](https://cems-lab.github.io/autumn-school/book/lectures/01_fracture_and_phast.html), [L2 guide](https://cems-lab.github.io/autumn-school/book/lectures/02_differentiability_and_inverse.html), [L3 guide](https://cems-lab.github.io/autumn-school/book/lectures/03_hybrid_learning.html) | All 404. |
| [Public P1](https://cems-lab.github.io/autumn-school/book/classroom/01_simulate_fracture.html), [P2](https://cems-lab.github.io/autumn-school/book/classroom/02_gradients_and_recovery.html), [P3](https://cems-lab.github.io/autumn-school/book/classroom/03_learning_and_hybrid.html) | All 404. |
| [Raw curated P1 practice target](https://raw.githubusercontent.com/CEMS-Lab/autumn-school/main/notebooks/study/classroom/01_simulate_fracture.ipynb), [P2](https://raw.githubusercontent.com/CEMS-Lab/autumn-school/main/notebooks/study/classroom/02_gradients_and_recovery.ipynb), [P3](https://raw.githubusercontent.com/CEMS-Lab/autumn-school/main/notebooks/study/classroom/03_learning_and_hybrid.ipynb) | All 404. These are the exact notebook targets encoded by the local Colab badges. |
| [Published curated P1 download](https://cems-lab.github.io/autumn-school/notebooks/study/classroom/01_simulate_fracture.ipynb) | 404. |
| GitHub-main `notebooks/classroom/01_simulate_fracture.ipynb` and `source/book/classroom/01_simulate_fracture.ipynb`, checked through raw content URLs | Both 404. Changing from the practice path to either of these alternatives would not restore P1 availability. |
| [Original P1 page](https://cems-lab.github.io/autumn-school/book/labs/01_phast_tiny_evolving_fracture.html) and [original practice download](https://cems-lab.github.io/autumn-school/notebooks/study/01_phast_tiny_evolving_fracture.ipynb) | Both 200. Original GitHub-main book-native, study and solution notebook targets also returned 200. |
| [Environment setup](https://cems-lab.github.io/autumn-school/SETUP.md) | 200. |
| [Curated P1 Colab URL](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/01_simulate_fracture.ipynb) | 200 Google Colab application shell with sign-in content; its underlying notebook target is 404. An HTTP 200 from Colab is not a notebook retrieval or execution result. |

[Issue #20](https://github.com/CEMS-Lab/autumn-school/issues/20) independently identifies the curation as local, with published-candidate Colab rehearsal and publication still outstanding. The code checker at `scripts/check_classroom_curation.py:40–55` checks local variants, retained receipts and static HTML. It does not verify the remote badge targets. Add that release-stage check rather than treating a local pass as cloud availability.

## Website inspection and practical next steps

The local homepage visibly presents the three lecture guides, three labs and retained references in the intended order. The local P3 page exposes separate Colab, practice, solution and setup links. Its model equation and expanded worked-gradient solution render legibly in the inspected desktop viewport; the answer disclosure works. The live homepage also renders legibly, but presents the earlier route.

The browser inspection covered the live homepage, local curated homepage, local P3 setup/model content and an expanded worked solution. It did not establish every page's layout, mobile/offline behaviour, screen-reader completeness or fresh authenticated Colab execution. Retained receipts describe earlier checks; they should not be relabelled as fresh results of this audit.

Before the classroom handoff:

1. Finish the 90-slide source-to-guide/lab mapping, resolve the priority accuracy passages and retain explicit model scopes.
2. Review the local edition as one teaching route, including actual lab BCs, derivative conventions and direct fallback terminology.
3. Publish only after the requested maintainer review/authority, then verify deployed guide/lab pages and each notebook target against that edition.
4. Rehearse authenticated fresh Colab, presentation-machine playback and the complete 150+150-minute teaching core. Keep the 60-minute flexible allocation available for its stated purposes.

No existing issue should be closed on the basis of this report alone.

## Post-rebuild browser check — 11 September 2026

After the second notebook execution/retention recorded in `evidence/classroom_runs_20260911b/README.md` and the main agent's Sphinx rebuild, this audit fresh-loaded local Practical 2 and Practical 3 through a temporary HTTP server on port 8767. This was a bounded integration check, not another full-site audit or notebook execution.

- **P2 explanation and figure:** the response section now explains that both history curves show displacement RMSE at the same recorded updated modulus. The browser visibly shows `training RMSE (4 loads)`, `validation RMSE (1 load)` and `Displacement RMSE [dimensionless]`. The two-panel figure renders with intact axes, legends and layout. Its served image is `book/_images/5556f458c5317dbfe0d9f84c0c291f27aa091022b6726029be8ec9eccae5f2af.png`.
- **P2 plotting source:** opening the hidden source exposes `training_rmse`, a loop over `history_array[:, 1]`, recomputed bar responses and the square/mean/square-root calculation. It plots that quantity against the validation error at the same recorded states. The corrected labels are present in the served HTML source disclosure.
- **Setup output:** fresh page loads show the updated retained setup receipts, 0.909 seconds for P2 and 0.742 seconds for P3. These are printed results from the separately documented local run, not measurements of a new browser or Colab execution.
- **One practice download:** an unauthenticated GET of the exact P2 practice link returned HTTP 200 and 270,577 bytes of valid notebook JSON. The response matches the served file byte-for-byte, contains the updated RMSE source and accurate worked-solutions links, and preserves canonical code, outputs and execution counts. Download SHA-256: `bea499d09e223b26d96b8a9caf1058dec06337d4b589dcb809458f7e6c03d4a5`. Rechecked canonical P2 SHA-256: `7ec815c4f3e3cf60f051fd81f1666c0149e63ef074891a8a9925f658635b6058`.
- **P3 math and disclosure:** the Helmholtz equation and zero-boundary condition render clearly after a fresh load. Worked solution 1 opens, displays the 325-node/3900-row calculation and the correct mean-squared-error gradient factor, and collapses again. Its previously recorded undefined feature symbol remains a notation follow-up; this check establishes rendering and interaction, not its resolution.

Inspection used a desktop viewport. A narrow/mobile viewport was not established in this bounded pass, so no fresh mobile-layout claim is made. Long code lines use contained horizontal scrolling; the inspected prose, equations and figure do not overlap. The local preview tabs and the audit-owned temporary server were closed afterward. No website files were edited and no public deployment, authenticated Colab run or fresh dependency installation was performed.
