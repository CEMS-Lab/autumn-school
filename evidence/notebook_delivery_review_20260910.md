# Notebook delivery review — 10 September 2026

## Scope and evidence boundary

Independent review of issues #10, #15, #17 and #18 against repository revision
`077d43d87c55b4fdea720808fc24f040e957e1ea`. All four issue bodies and comments,
AGENTS.md, DESIGN_DIRECTIVES.md, PEDAGOGICAL_WALKTHROUGH.md, COURSE_PLAN.md and
CONTRIBUTING.md were read. The review covers the six canonical notebooks,
their book/study/solution variants, the source generator, setup instructions
and the model-adapter helper. Paths and line references below describe this
baseline, before today's parallel corrections.

No shared generated outputs were rebuilt for the audit. A baseline copy was
created with `git archive HEAD` under
`.build/notebook-review-20260910.Z28J3n`; the original
`source/book/scripts/build_lab_pages.py` was executed only in that copy using
the provisioned Python 3.10 environment. This authoring check executes no
notebook computations. No Google Colab runtime was launched.

## Computational parity

Code source, execution counts and retained outputs match exactly between each
canonical notebook and all three delivered variants at the reviewed revision.
The comparison excludes markdown and presentation metadata.

| Lab | Code cells | Book parity | Practice parity | Solution parity | Book markdown cells changed by baseline regeneration |
| --- | ---: | --- | --- | --- | ---: |
| 00 | 6 | Pass | Pass | Pass | 5 |
| 01 | 7 | Pass | Pass | Pass | 4 |
| 02 | 4 | Pass | Pass | Pass | 3 |
| 03 | 4 | Pass | Pass | Pass | 1 |
| 04 | 5 | Pass | Pass | Pass | 1 |
| 05 | 6 | Pass | Pass | Pass | 1 |

The generator's parity report proves preservation of recorded computations.
It does not establish that changed setup code or a fresh cloud environment
has been executed successfully.

## Priority findings

1. **Generated pedagogical changes are not reproducible from authoring inputs.**
   The baseline generator reconstructs titles, objectives and exercises from
   JSON and canonical prose (`source/book/scripts/build_lab_pages.py:104`,
   `:119`, `:127`, `:145`). Rebuilding changes at least one markdown cell in
   every book lesson and loses parts of the new badge/header/interpretation
   treatment. Lab 00's practice and solution downloads still contain the
   previous “stationary trap” exercise title, while the book uses a revised
   title. Migrate reviewed book-only prose into canonical notebooks, migrate
   exercises into JSON, and generate every delivery format from those inputs.

2. **Cloud launch setup is incomplete and tracks a moving source revision.**
   Every opening code cell clones the default branch with `--depth 1`, then
   imports scientific packages. It does not install the package dependencies
   or reject unsupported Python before imports. The full clone contains the
   vendored solver, helpers and configuration, and the helper verifies the
   vendored source manifest, but the course checkout itself is unpinned.
   `vendor/PhAST/pyproject.toml:14` requires Python >=3.10,<3.13.
   `SETUP.md:55` still describes manual ZIP upload/extraction. Provide one
   documented, revision-checked bootstrap with dependency installation and
   explicit setup-versus-computation timing; rehearse it on fresh Colab.

3. **The new Lab 05 header overstates the implemented correction.**
   `source/book/labs/05_hybrid_reference_correction.ipynb:22` says the proposal
   becomes an initial guess and accelerates convergence. In the actual helper,
   `course_tools.py:469` calls `torch.linalg.solve(matrix, source)` and
   `:677` calls that independent reference solve. No proposal is passed into
   an iterative solve. Teach a proposal/residual/direct-reference replacement
   and preserve the course-owned ToyHelmholtz scope. Speed benefit requires
   separate matched end-to-end measurements.

4. **The new Lab 02 finite-difference answer applies a generic error model
   incorrectly to the selected quadratic law.** Its second exercise's worked
   answer (`source/book/labs/02_degradation_autograd.ipynb:364`) discusses a
   nonzero leading truncation term and a generic cube-root-epsilon optimum.
   Here g is quadratic, so g'''=0 and the centred derivative is exact in real
   arithmetic. Explain that special case and floating-point cancellation;
   use a nonquadratic comparison if teaching truncation-versus-roundoff.
   Reverse-mode cost depends on the graph, primitive backward operations and
   storage/recomputation; the quoted universal “2 to 3 forward evaluations”
   should become a qualified qualitative comparison.

5. **Lab 01's new introduction disagrees with its configuration.** Its first
   markdown cell describes a 1.0 by 2.0 domain, whereas the selected case and
   mesh exercise use 4.0 by 2.0. The independent forward contributor owns the
   correction and the stronger end-to-end input-flow review.

6. **Several required teaching components are missing from the baseline.**
   No lab has the specified 3–4-item key-takeaways section. Source exercises
   00/2, 01/2, 03/2, 04/2 and 05/1 remain partly quizzes about many-digit log
   values. Replace them with conceptual questions and small parameter/code
   experiments, using numerical tolerances for code verification. The lab04
   training loop is hidden inside `make_toy_checkpoint`; explain the visible
   call through normalisation, prediction, loss, `backward` and optimizer step.

7. **The replay artifact contains a decision record, rather than field labels.**
   The final code cell of canonical Lab 05 writes scope, load, feature order,
   assessments and correction description to JSON. It stores no coordinate,
   proposal or reference arrays. Its closing prose and JSON worked solution
   should identify it as a decision record and explain which fields to add
   before using it as supervised retraining data. A complete DAgger rollout
   and retraining experiment remains issue #9.

## Additional notebook findings

- Lab 03's book header writes a half-squared Euclidean tracking loss, whereas
  its optimizer uses `torch.mean((predicted-observed_train)**2)`. Both have
  the same minimizer for this fixed dataset, but their gradient magnitudes
  differ. Use the exact mean-squared expression when tracing the code.
- The Lab 04 helper uses 12 whole training load cases, two validation cases
  and two test cases; normalisation statistics are computed from training
  features. Reloading reconstructs the architecture and loads a state dict
  using `weights_only=True`. These are useful concrete teaching contracts.
- The model interface is nodewise `(N,3)` features to `(N,1)` output. The
  RBF baseline is a Gaussian kernel weighted average on that feature space.
  GNN/GNO connectivity and CNN grid mappings require their own contracts.
- Lab 05 enforces boundary values after bounds/history projection. For the
  shipped monotone loads and admissible previous field, its reference
  correction meets the tested residual. Arbitrary nonzero previous boundary
  values or unloading require a separately defined constrained field model;
  the example should not imply full fracture irreversibility validation.
- Plot layouts use constrained layout and readable field colormaps, but
  lab04/05 colorbars currently omit field labels, and the requested global
  Matplotlib defaults are absent. These are useful next visual refinements;
  changed plot-producing code should receive a fresh execution receipt.
- Downloaded notebooks containing raw book-relative HTML badges can resolve
  images incorrectly in Jupyter/Colab. Generate notebook-appropriate Markdown
  badges and absolute published links; retain local badge assets in the book.

## Fresh Colab acceptance

The existing receipt `evidence/core_notebook_rehearsal_20260909.json` records
sequential local runs of six prior source snapshots (slowest about 70 s), using
an already provisioned scientific environment. It records a Colab sign-in
barrier and no started runtime. It is historical local evidence, not a fresh
installation or current-revision cloud receipt.

Issue #10 therefore needs an authenticated fresh CPU runtime, complete pinned
bootstrap installation, supported Python/package versions, source verification,
and whole-notebook executions of the final six notebooks with setup measured
separately. Record current source hashes and keep the 300-second task cap.
The source clone/setup and notebook code should also be rehearsed without
pre-existing model artifacts, especially Lab 05's independent training path.

## Follow-up ownership

The root contributor owns generator/bootstrap integration and corrections to
Labs 00/02/03. The forward contributor owns Lab 01. This reviewer was then
assigned a bounded prose/exercise patch for canonical Labs 04/05 and their
solution JSON files. It preserves all computational cells and outputs, adds
four takeaways each, corrects the direct-fallback/replay description, and uses
conceptual plus executable numerical exercises. Final regenerated HTML and
fresh runtime checks belong to the integration pass.

## Bounded corrections and validation completed

Updated canonical notebook 04's opening/closing markdown to define the linear
field problem, feature shapes, mean-squared objective, training-only
normalisation, visible optimizer-loop excerpt, and field interpretation.
Updated canonical notebook 05's opening/closing markdown to explain input
compatibility, projection, the relative residual, direct reference correction,
and the exact content of the saved decision record. Computational cell count
and numerical code bodies were preserved by this reviewer. The integration
lead subsequently changed the shared opening setup cell and cleared outputs
for the final fresh execution; those changes are separate from this patch.

Replaced the two source-owned exercises in each of `04.json` and `05.json`,
including their hints and worked answers, and added four takeaways per lesson.
Lab 04 now derives the loss gradient and compares error fields at three loads.
Lab 05 relates residual to field error and evaluates three acceptance
tolerances using the actual notebook variables.

Private validation used `nbformat` to load each archived canonical notebook,
appended the Python code extracted from its new JSON worked answer, and ran
`nbclient.NotebookClient(..., timeout=90, allow_errors=False)` with the private
notebook directory as kernel working directory. Existing assertions and the
additional worked code passed:

| Private check | Local elapsed time | Observed result |
| --- | ---: | --- |
| Lab 04 plus three-load error plots | 4.065 s | RMSE approximately 0.0240, 0.0424, 0.0564 at loads 0.82, 0.94, 1.00 |
| Lab 05 plus tolerance sweep | 2.168 s | Tolerances 0.05 and 0.15 select reference correction; 0.30 accepts the model proposal |

These checks use the provisioned Python environment, archived setup, and
unchanged numerical body. They validate the worked-answer snippets; the
integration lead's new bootstrap and final full notebooks require their own
receipts. The course design checker also passed after the prose patch.

The privately regenerated Lab 04 reference/MLP/RBF/error image was inspected.
Its layout is readable. The existing fixed error scale of +/-0.15 clips an
observed maximum absolute error of approximately 0.258 without an extension
marker. This was reported to the integration lead for a plot-code follow-up.
The new worked-answer plot derives a shared symmetric scale from all three
error fields and supplies a dimensionless field label.

## Independent review of the new forward practical

Read-only review of `notebooks/day2_helpers/forward_workflow.py`,
`source/notebooks/build_forward_practical.py`, its result checker, configuration,
and the relevant pinned PhAST boundary-condition/staggered-solver implementation.
No full solve was launched by this reviewer. Line references describe the
files inspected before any subsequent integration amendments.

### Verified implementation relationships

- The imported NPZ coordinate/connectivity arrays create the actual `FEMMesh`
  (`build_forward_practical.py:128`), and `construct_solver` attaches the actual
  boundary conditions and material to that mesh (`:153`). Object-identity
  assertions confirm the same objects pass into the solver and execution.
  `solve_prepared_case` advances the supplied solver, with no hidden mesh or
  configuration reconstruction (`forward_workflow.py:35`).
- The prescribed conditions agree with the vendored
  `symmetric_tension_bcs`: horizontal displacement is zero on every exterior
  edge and top/bottom vertical displacements are plus/minus half the total
  separation. The notch uses both a persistent phase-field Dirichlet condition
  and seeded nodal damage. Its centreline and mesh-dependent endpoint are
  explained accurately.
- Every load step checks finite states, damage bounds, nodal irreversibility,
  the locked notch, prescribed displacement error, and the selected staggered
  convergence value. The mechanics and staggered exceptions remain enabled.
  Tolerances are retained in the output metadata.
- Exported arrays are copied away from live solver tensors. NPZ/JSON round-trip
  equality is checked before post-processing, and the figures use the reloaded
  arrays and trace. The archive is correctly described as a post-processing
  result, with restart-state requirements explained separately.
- The half-separation experiment deep-copies the configuration and constructs
  a fresh solver, boundary-condition object and material on the same imported
  mesh. Both cases begin with the same seeded notch and execute the same 60
  load factors. Only the separation amplitude is halved. The full and half
  result arrays are independently saved and reloaded. The comparison is
  between two complete loading histories; the prose correctly restricts the
  quarter-energy scaling argument to fixed damage.
- The dimensions, displacement signs, damage convention, and reaction
  definition are consistent. The figures and metadata use dimensionless
  teaching scales, and the mesh-dependent nodal damage sum is labelled as such.

### Bounded follow-ups reported to integration

1. **Name the convergence measure precisely.** At the pinned public default,
   `stagger_criterion='relative'` and `stagger_norm='l2'`. Therefore the value
   saved as `stagger_residual` at `forward_workflow.py:93` is the maximum
   relative change of displacement and damage iterates, rather than a PDE
   residual norm. Record the actual criterion/norm and describe this iterate
   convergence measure in the lecture text. The supplied strict mechanics
   check remains a separate safeguard.
2. **Record the two-dimensional constitutive assumption.**
   `Material.plane_stress` defaults to `False`, so this case uses plane strain.
   Include that in the material explanation and resolved metadata. The public
   source pin makes the implicit default traceable; an explicit learner-facing
   statement makes the mechanical model easier to reproduce and interpret.
3. **Complete the portable-file contract for plotting.** `load_results`
   (`forward_workflow.py:150`) validates the core arrays, dimensions, finite
   values and hashes, but does not require or range-check the four boundary
   index arrays used by the outline plot. A correctly hashed archive missing
   `boundary_top` can therefore pass the loader and encounter a later key
   error during post-processing. Require all boundary arrays and integer,
   one-dimensional, in-range node indices. Likewise validate snapshot IDs as
   ordered integer step indices within the trace and check their endpoint
   consistency with the separately named initial/first/final arrays.

No new defect was identified in the actual-object chain, state isolation, or
half-load comparison. The follow-ups above concern terminology and the
standalone result contract. Current-run timing, source hashes, final numerical
receipts and rendered full-course integration remain the root contributor's
validation responsibility.

## Final classroom browser review

The final integrated local book at `http://127.0.0.1:8767/book/` was checked
with headless Brave/Playwright at 1440 × 1000 and 390 × 1000 pixels. The
independent checker is `scripts/check_classroom_pages.cjs`; its machine-readable
receipt is `evidence/classroom_browser_20260910.json`. The run passed all 14
page/viewport combinations: the index and each of the six labs at both widths.

The browser context allowed only the local HTTP origin. Every required runtime
asset loaded locally; there were no page exceptions, failed local requests,
HTTP errors, broken images, MathJax error nodes or unrendered math regions.
There were 490 rendered mathematical expressions across the tested pages and
viewports. No page extended horizontally beyond the viewport.

For each lab at both widths, the checker verified one action group, downloadable
practice and solution files that parse as notebook version 4, an available
environment setup file, the correct Colab launch target, one Key takeaways
heading, and four expandable answers. Enter and Space operated all 48 tested
answer panels, and the collective Show all control worked from the keyboard.
The 11 wide displayed equations could be focused and scrolled using the arrow
key. Figure enlargement was tested by pressing Enter on the first computational
figure link on all 12 lab/viewport combinations, opening its local full-size
image, and returning to the lab.

### Visual inspection and a repaired regression

Fifty screenshots are retained in `reviews/classroom-20260910/`. The inspection
covered both index openings and, for all six labs, the opening on mobile plus
the first equation, first computational figure and an opened worked solution
at useful desktop/mobile scales. The final Lab 00 mobile solution, Lab 03
equation, Lab 01 geometry and Lab 05 figure were inspected again after the last
integration changes. The dark background, orange current-page and answer
accents, blue actions, body spacing and mathematical typography are consistent.
The mobile action groups wrap into readable rows; the desktop navigation leaves
the notebook content in a clear central column.

The first complete browser run found a genuine Lab 00 regression: unmatched
inline-math delimiters in the physical-interpretation paragraph caused ordinary
prose to be typeset as a long equation and widened the mobile page to 643
pixels. MathJax accepted that malformed prose as valid mathematics, so a
MathJax-error-only test would have missed it. The integration owner repaired the
canonical paragraph, regenerated the book, and the full 14-check rerun passed.

The retained figures have readable axes and consistent scientific labels.
Lab 01's geometry view clearly identifies the initial damaged centreline, the
4-by-2 dimensionless specimen, symmetric separation and constrained horizontal
displacements. Lab 04's revised error limits include the measured error range;
Lab 05 now labels its colour bars. The field-model figures use four horizontal
panels, which are compact at book-column width. The new keyboard-accessible
full-size image links provide an effective inspection route. A future
two-by-two layout would make these comparisons easier to read directly in a
narrow notebook column. Similarly, breaking the longest equations over two
lines would reduce the need for mobile horizontal scrolling; the full
expressions are currently reachable by touch or keyboard.

### Additional bounded Lab 03 exercise check

The new second worked exercise was executed against the canonical Lab 03
mechanics and inverse-training cells in memory, without running its bootstrap,
changing output files, or rebuilding the book. Python 3.10.18 and PyTorch 2.8.0
completed the computation and plot draw in 0.733 seconds. The snippet produced
12 finite load responses and a maximum recovered/reference displacement
difference of `7.874e-5`. Its variables and callable contract are valid.

The Lab 03 introductory half-squared Euclidean loss still differed from the
implemented mean-squared error over four tip-load observations at the moment
of this visual check. This small mathematical wording mismatch was reported
to the integration owner separately; the worked exercise itself passes.

This review establishes local rendered delivery and a bounded additional
exercise execution. Colab links were inspected as targets only. An authenticated
fresh Colab run remains necessary for a cloud execution receipt, including
installation and runtime timing; local browser checks and provisioned Python
execution do not establish that cloud result.
