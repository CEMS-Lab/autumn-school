# Delivery checklist — 10 September 2026

## Current decisions

All 18 repository issues and their comments were read against revision `077d43d87c55b4fdea720808fc24f040e957e1ea`. Issues #17–18 govern the current undergraduate teaching style, notebook anatomy and visuals. Preserve numerical assumptions and checks while explaining them constructively.

The route is three lecture hours followed by three practical hours. Organisers must confirm breaks and event clock times. Deliver the web book, executable notebook downloads and editable animated slides. The printable book stays archived. The old timetable graphic has been removed from the book opening; its reusable source assets are retained. The reviewed update is live on GitHub Pages at content revision `3d9739c736fffc104a805c8b74cd9296cab1137c`; live-page and download verification is recorded in the [publication receipt](evidence/publication_20260910.json).

## Batch ownership and acceptance

| Work | Ownership | Acceptance |
| --- | --- | --- |
| Forward practical (#5) | Notebook 01, forward-specific helper/generator and JSON exercises | One actual geometry-to-solver object chain, visible notch/BC/load, result save/reload, one input change, fresh full run under 300 s and inspected fields. |
| Animated slides (#12) | Introduction generator and separate candidate output | Embedded clips, static posters, editable text, notes/pause questions, OOXML and visual checks, native opening/playback. |
| Notebook delivery (#10, #15, #17–18) | Independent review and scoped lab 04/05 prose | Source/download parity, meaningful exercises, accurate model claims and fresh-environment evidence. |
| Integration (#1, #11, #15, #17–18) | Shared setup/generator, landing page, planning and QA | Preserve reviewed prose on regeneration; desktop/mobile math, navigation, solutions and downloads; enforce build design gate. |

The inverse contributor retains ownership of new inverse research work. The classroom bar exercise and optional research reading route remain distinct.

## Complete issue register

| Issue | Next action / disposition |
| --- | --- | --- |
| [#1](https://github.com/CEMS-Lab/autumn-school/issues/1) | The main plan follows the 3+3-hour route and web-first delivery. Keep all 18 issue records and checklists aligned through publication and rehearsal. |
| [#2](https://github.com/CEMS-Lab/autumn-school/issues/2) | Review fracture representations and conceptual exercise with primary sources; preserve formulation/algorithm distinctions. |
| [#3](https://github.com/CEMS-Lab/autumn-school/issues/3) | Audit AT1/AT2 normalisation and degradation plots; use the original profile animation. |
| [#4](https://github.com/CEMS-Lab/autumn-school/issues/4) | Align static/dynamic, load/time/iteration and staggered operator explanations with the actual practical. |
| [#5](https://github.com/CEMS-Lab/autumn-school/issues/5) | The connected input-to-result workflow and changed-load comparison pass locally in 92.00 s. Next, shorten the mesh cells using the [mesh usability plan](source/planning/MESH_USABILITY_REVIEW_20260910.md), preserve the tested case and add a checked Gmsh import activity. Rehearse in Colab; a validated short propagating crack retains its separate acceptance check. |
| [#6](https://github.com/CEMS-Lab/autumn-school/issues/6) | Checked backpropagation material and the reverse-accumulation/history animations are integrated into the candidate. Rehearse their notation and transitions across the full lecture. |
| [#7](https://github.com/CEMS-Lab/autumn-school/issues/7) | The optional extension is integrated. Its contributor owns full fracture recovery with multiple starts, held-out checks and runtime evidence. |
| [#8](https://github.com/CEMS-Lab/autumn-school/issues/8) | Retain MLP/RBF teaching contracts. Genuine learned PhAST damage integration needs approved public weights and matched field/timing evidence. |
| [#9](https://github.com/CEMS-Lab/autumn-school/issues/9) | Explain visited states, reference labels, aggregation, retraining and held-out evaluation; track full executed DAgger separately. |
| [#10](https://github.com/CEMS-Lab/autumn-school/issues/10) | Shared setup and all six fresh local runs pass. Test the deployed revision in fresh authenticated Colab CPU sessions, including setup, computation and downloads; rehearse a slower laptop separately. |
| [#11](https://github.com/CEMS-Lab/autumn-school/issues/11) | Timetable removal and local desktop/mobile, math, download, answer-control and offline checks pass. Live pages, downloads and updated credits are verified. Continue the full student-level review. The printable-book requirement is superseded. |
| [#12](https://github.com/CEMS-Lab/autumn-school/issues/12) | The 23-slide PowerPoint/Keynote candidate contains five clips; local Keynote import and playback pass. Keep the previous deck as a fallback; test PowerPoint, seeking/replay, classroom readability and the full lecture timing. |
| [#13](https://github.com/CEMS-Lab/autumn-school/issues/13) | Keep approved public paper examples optional and within their allocated time; review provenance before adding assets. |
| [#14](https://github.com/CEMS-Lab/autumn-school/issues/14) | Preserve original visual standard; supplied Instagram/PDF repository inventory remains a distinct source-access task. |
| [#15](https://github.com/CEMS-Lab/autumn-school/issues/15) | Local source/output parity, worked answers and browser checks pass. Complete the student-level cross-format review and timed setup → inputs → solve → fields → derivatives → learning rehearsal. |
| [#16](https://github.com/CEMS-Lab/autumn-school/issues/16) | The pushed revision, successful Pages build, credits and downloadable files are verified. Retain original-content licence and final release checks. |
| [#17](https://github.com/CEMS-Lab/autumn-school/issues/17) | Reviewed prose and conceptual exercises are preserved in authoritative sources; the checked notebook variants agree. Continue the complete lecture/book readability review with the current teaching conventions. |
| [#18](https://github.com/CEMS-Lab/autumn-school/issues/18) | Notebook anatomy, plot formatting, source-math balance and the enforced design gate pass locally. Apply these checks to future changes and the final deployed edition. |

## Completion record

The [main course issue](https://github.com/CEMS-Lab/autumn-school/issues/1#issuecomment-5617154602) records this batch and its remaining delivery gates.

The published web edition contains the following completed work:

- [x] Map all 18 open issues and comments; reflect the current 3+3-hour route and authoring directives in the plan.
- [x] Update all 18 GitHub issue bodies with completed/retained work, remaining acceptance checks, next actions and evidence paths; read back every saved body. See [the issue synchronisation receipt](evidence/issue_status_20260910.json).
- [x] Connect the first practical through one configuration, mesh creation/reload, notch, boundary conditions, solver construction, loading, exported fields and post-processing. A second load case shows the effect of changing the imposed separation.
- [x] Execute all six complete notebooks in fresh local processes after setup. Measured whole-process times are 6.20, 92.00, 3.74, 4.12, 5.17 and 4.72 seconds for labs 00–05 respectively.
- [x] Regenerate canonical prose, exercises and computational outputs consistently into the book, practice downloads and worked-solution downloads. Invalid design builds stop automatically.
- [x] Remove the opening timetable graphic. Check desktop/mobile lessons, mathematical rendering, local downloads, keyboard-operated answers, full-size figures and scientific flowcharts.
- [x] Build the 23-slide animated introduction as editable PowerPoint and native Keynote. All five embedded clips played in local Keynote without an import warning; the previous working deck is retained as a fallback.
- [x] Receive authorisation for publication and subsequent live-book verification.
- [x] Credit the book as Prepared by Allamaprabhu Ani and Sathiskumar A. Ponnusami; retain presenter wording on the presentation.

See [today's delivery evidence](evidence/course_delivery_20260910.md) for commands, scope and remaining gates, and the [publication receipt](evidence/publication_20260910.json) for live checks. Local execution, fresh installation and fresh Colab execution remain separate evidence. Whole issues remain open until all their acceptance checks pass.

## Next delivery checks

- [x] Publish the approved revision and verify the Pages deployment, prepared-by book credits, local assets and notebook downloads from the live site.
- [ ] Simplify the first practical's mesh cells and add a tested Gmsh import route following the [mesh usability plan](source/planning/MESH_USABILITY_REVIEW_20260910.md); rerun the revised practical and inspect its fields.
- [ ] Run all six lessons and the optional diffusion companion from public links in fresh authenticated Colab CPU sessions. Record setup and computation separately.
- [ ] Rehearse the three lecture hours and three practical hours using the animated introduction and mapped 44-slide resource. Confirm breaks, transitions, pause questions and the presentation machine.
- [ ] Test PowerPoint playback, native seeking/replay and portability on that machine. Improve first-frame posters and check the history animation at classroom viewing distance.
- [ ] Continue the bounded scientific and research tasks in the register above, with the inverse contributor retaining ownership of new inverse work.

## Classroom decisions still needed

- [ ] Organiser-confirmed break allocation and presentation machine.
- [x] Verified published revision for authenticated Colab rehearsal.
- [ ] Complete three-hour presentation and practical transition rehearsal.
- [ ] Approved research exhibits and original-content licence before final release.
