# Handoff issued 9 September — progress updated 10 September 2026

This is the original handoff checklist. The [10 September execution record](TODAY.md)
records completed items, current files and the remaining delivery checks.

## Progress against the original handoff

- [x] Build a 23-slide editable animated introduction with five embedded clips,
  static fallbacks and presenter questions. Local Keynote import/playback pass.
- [x] Complete the connected first PhAST practical, portable result reload and
  changed-load comparison; fresh local whole-notebook time is 92.00 seconds.
- [x] Preserve canonical notebook prose, code, outputs and worked answers across
  the web and download editions. All six fresh local runs finish within 300 seconds.
- [x] Check local desktop/mobile pages, equations, answer controls, downloads,
  offline assets and scientific flowcharts; remove the opening timetable graphic.
- [x] Receive publication authorisation for the reviewed update.
- [x] Verify the pushed revision and live Pages deployment, including credits
  and downloads; record the deployed revision for fresh Colab rehearsal.
- [x] Shorten the visible mesh cell and verify the full local practical in
  92.2464 seconds; retain exact physical arrays and result fields.
- [ ] Add a tested Gmsh import activity following the
  [mesh usability plan](source/planning/MESH_USABILITY_REVIEW_20260910.md).
- [ ] Assess B3 dynamic SENT as a canonical propagation example and align the
  course with upstream tutorials under [issue #19](https://github.com/CEMS-Lab/autumn-school/issues/19).
- [ ] Run the six lessons and optional diffusion companion in fresh authenticated
  Colab CPU sessions, recording setup and computation separately.
- [ ] Test PowerPoint and presentation-machine playback, seeking/replay and
  portability; refine opening movie frames and classroom readability.
- [ ] Confirm organiser times and rehearse the full three-lecture/three-practical
  route. Continue the separately tracked scientific extensions.

The requirements below preserve the original handoff. Use [TODAY.md](TODAY.md)
for current acceptance status and ownership.

## Delivery priorities

The web textbook and notebook downloads are the current student edition.
Preserve the editable PowerPoint and Keynote files, LaTeX sources, equation
sources, animation clips and static posters. The printable book is archived.

### 1. Build the presentation with animations

- Continue the latest 18-slide introduction and draw from the 44-slide lecture
  resource. Map the combined material to the agreed six-hour lecture/practical
  sequence before adding slides.
- Keep Sathiskumar A. Ponnusami first, with Queen Mary University of London and
  CEMS-Lab. Retain creator attribution in ordinary metadata and presenter notes.
- Use one learning point per slide, generous spacing, consistent orange/blue
  accents, and large correctly rendered equations with defined symbols.
- Insert the existing AT2-profile, staggered-update, reverse-accumulation and
  learned-proposal clips at the relevant explanations. Use the history-cycle
  animation in the derivative section.
- Add a pause prompt and static fallback for each animation. Preserve editable
  slide text and connectors alongside the media.
- Test the actual PowerPoint and Keynote decks from local disk: opening,
  slideshow playback, seeking/replay, fonts, equations, video embedding and
  offline portability. Capture the exact message if an import warning recurs.

**Completion check:** one current editable presentation in each required format,
with functioning embedded media and a documented local presentation-machine test.

### 2. Complete the first PhAST practical sequence

- Use one explicit configuration through geometry, notch, mesh, materials,
  selected boundary sets, prescribed values, load increments and solve.
- Connect the visible preview objects to the actual solver inputs, or make the
  configuration-driven construction visible in consecutive notebook cells.
- Show the initial notch separately from loading-induced damage.
- Save and reload mesh, fields, response history and configuration through
  portable relative paths. Explain NPZ/JSON/figure exports and interpret the
  reloaded results.
- Change one physical input, rerun, and verify the expected change in the field
  or response. Keep the complete computation under five minutes after setup.

**Starting evidence:** [forward-practical audit](source/planning/PRACTICAL_SEQUENCE_AUDIT_20260909.md).

### 3. Rehearse every classroom notebook in fresh Colab

- Provide a clear Colab launch/bootstrap route that fetches the complete pinned
  public course folder, including helpers, solver and configurations.
- Start from the public notebook/download route in a fresh authenticated CPU
  runtime. Record dependency setup separately from complete execution time.
- Run the six classroom lessons and the optional diffusion companion with a
  300-second per-calculation limit. Check downloadable results and worked answers.
- Pin or record dependency versions, seed and runtime details. Keep retained
  HTML outputs available for classroom discussion during installation.
- Check that practice and solution notebooks contain the same computational
  walkthrough and that every exercise refers to variables actually defined.

**Completion check:** reproducible fresh-Colab receipts, working downloads and
clear restart/run-all instructions. Record research/HPC examples separately.

### 4. Connect differentiation and learning into one teaching story

- Reuse the same input → state → observation → loss notation across book,
  slides and notebooks. Derive one explicit update, then unroll several steps
  and accumulate every shared-parameter contribution.
- Explain the transpose solve for a converged implicit problem, with its
  regularity assumptions. Compare local AD and finite differences at several
  spacings, and explain history and active-set effects.
- Select the elastic-bar or diffusion recovery as the short hands-on inverse
  task. Use the retained fracture/particle history laboratory as an optional
  research exhibit within the allocated time.
- Explain the existing train/save/reload and residual-correction interface.
  For an actual learned PhAST damage component, select an approved example
  with weights, feature contract, held-out fields and matched timing evidence.
- Present DAgger through collection, reference labelling, aggregation and
  retraining, linked to the model's intended role.

### 5. Final coherence and delivery rehearsal

- Confirm the organiser's teaching times and break allocation.
- Walk the whole course as a student: prerequisites, explanation, prediction,
  equation, code, plot, question, worked answer and next lesson.
- Recheck mobile/desktop layout, mathematical rendering, navigation, search,
  notebook links and animation controls on the live site.
- Rehearse transitions and demonstrations against the timetable. Record what
  students should produce at the end of each hour.
- Update the main course issue and its existing sub-issues with completed
  evidence and the remaining bounded assignments.

## Parallel work assignments

1. **Presentation agent:** own the editable slide source and media integration;
   use the existing clips and preserve the latest working deck as a fallback.
2. **Notebook agent:** own the forward-practical input/export fixes and fresh
   Colab rehearsal; preserve numerical receipts and enforce the runtime budget.
3. **Review agent:** inspect the resulting website and decks as a student;
   report concrete missing definitions, broken transitions and rendering faults.

Agree file ownership before work. Rebuild derived files from the edited source,
then review the rendered result before publishing the next update.
