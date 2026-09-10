# Course delivery review — 10 September 2026

## Scope and provenance

All 18 open issues and their comments were reviewed. [TODAY.md](../TODAY.md)
maps their directives, ownership and remaining acceptance checks. The course
follows three lecture hours and three practical hours, with the web textbook,
executable notebooks and editable slides as the delivery formats.

A [progress comment on the main course issue](https://github.com/CEMS-Lab/autumn-school/issues/1#issuecomment-5617154602)
records this local batch and the remaining gates. All 18 issues remain open.
Every issue body has now been synchronised with a dated completed/remaining
checklist and verified by reading it back from GitHub. The
[issue update receipt](issue_status_20260910.json) records each body hash,
evidence path and next action.

This is a reviewed local candidate based on repository revision
`077d43d87c55b4fdea720808fc24f040e957e1ea`. The base revision identifies the
starting checkout; the current manifest and notebook hashes identify the local
changes. The maintainer authorised publication on 10 September. Deployment and
live checks are recorded separately in the publication receipt. The separate inverse
contributor's source and the vendored PhAST solver were preserved.

## Completed work

- Connected Notebook 01's geometry, prepared mesh, initial notch, materials,
  boundary sets, prescribed loading and actual solver objects. Portable mesh
  and result reloads feed the displayed post-processing. A second load case
  changes the separation from 0.04 to 0.02.
- Added validation for exported fields, displacement, boundary arrays,
  increasing snapshot indices and consistency between named and time-indexed
  states. The checker exercises 48 malformed archive cases.
- Moved reviewed prose into authoritative notebook/JSON sources. One generator
  produces the book, practice and solution editions with preserved numerical
  outputs. A code-hash check rejects stale execution records.
- Added shared setup that retrieves the complete course folder in Colab,
  records the resolved revision and environment, and separates setup timing
  from computation. Local authoring uses the existing checked-out folder.
- Replaced raw-output questions with physical interpretation and parameter
  exploration. Corrected the reference-fallback explanation and the distinction
  between decision metadata and stored training field pairs.
- Corrected inherited missing math variables/delimiters in Lab 00 and aligned
  Lab 03's written loss with the mean squared error used by its code. An
  independent reread covered all 22 canonical markdown cells and 90 solution
  prose fields. The authoring tests now check delimiter balance as well.
- Removed the timetable graphic and its caption from the book opening while
  retaining the reusable figure assets. Scientific flowcharts remain available
  as keyboard-enlargeable vectors; notebook output figures now enlarge too.
- Built a 23-slide animated introduction with five embedded movies, editable
  text, pause questions and a native Keynote copy. Previous working slides and
  the 44-slide lecture resource remain available.
- Updated the web credit to Prepared by Allamaprabhu Ani and Sathiskumar A.
  Ponnusami. Presenter wording remains in the presentation. The book's shared
  footer and metadata now identify both preparers.

## Measured notebook execution

Fresh local whole-notebook processes, after environment setup, on macOS ARM
with Python 3.10.18. Each calculation uses a 300-second whole-process budget.
These measurements establish local execution; authenticated fresh Colab and
dependency installation are separate delivery checks.

| Lab | Computation | Whole-process time |
| --- | --- | ---: |
| 00 | Branch selection and energy-based objectives | 6.20 s |
| 01 | Connected PhAST forward practical and changed-load comparison | 92.00 s |
| 02 | Degradation-law derivatives | 3.74 s |
| 03 | Elastic-bar derivative and inverse exercise | 4.12 s |
| 04 | Train, save and reload a teaching field model | 5.17 s |
| 05 | Check a proposal and select the reference fallback | 4.72 s |

Exact times and source hashes are in
[notebook_runtime_current.json](notebook_runtime_current.json).
Notebook 01's reference and half-load cases each use 60 increments; its actual
model is plane-strain quasistatic AT2 with an assembled sparse-direct solve.
Its convergence tolerance measures relative iterate changes. The demonstrated
field is diffuse damage. [Forward-practical evidence](forward_practical_20260910.md)
records fields, checks and the source fingerprint.

Labs 04–05 use the named teaching Helmholtz field model and its MLP/RBF
interface. The fallback independently computes the direct reference solution.
Genuine learned PhAST damage integration and full DAgger execution retain their
own issue requirements, including approved weights and matched field/timing
evidence. The optional diffusion and research notebooks retain their existing
evidence and were outside today's six-notebook rerun.

## Build, browser and native-slide checks

Reproducible commands from the repository root:

```bash
python scripts/run_course.py --notebook 0  # repeat for indices 1 through 5
python scripts/retain_course_runs.py
python source/book/scripts/build_lab_pages.py
python scripts/test_course_authoring.py
python scripts/check_forward_practical.py
python -m sphinx -q -b html -E -a source/book book -W --keep-going
python scripts/check_book_theme.py
node scripts/check_classroom_pages.cjs
node scripts/check_flowcharts.cjs book reviews/flowcharts-20260910
python source/slides/intro-lecture/verify_animated_deck.py
python scripts/test_package_public_edition.py
python scripts/package_public_edition.py --manifest-only
python scripts/package_public_edition.py --check-only
```

The browser scripts use the locally served `book/` folder, installed Playwright
and a configured Chromium executable. External asset requests are blocked.
`COURSE_BASE_URL` identifies the local book URL; `BROWSER_EXECUTABLE` and
`NODE_PATH` select the installed browser and runtime modules.

- Six authoring regression tests pass. They cover calculation parity, source
  math delimiters, stable cell IDs, missing pages and a failing design gate.
- Eight isolated packaging tests pass. The manifest-only route preserves
  artifacts and published-version provenance, rejects unsafe paths, and
  verifies the current public inventory and every SHA-256 hash.
- The full warning-as-error HTML build and static checks pass: 33 HTML pages,
  six notebook lessons and 968 local asset references.
- Browser checks pass at 1440- and 390-pixel widths for the opening and all
  six lessons. They exercise keyboard-accessible answers, notebook downloads,
  MathJax, horizontally scrollable equations and full-size PNG links.
- Fourteen page/viewport checks cover the opening and six scientific
  flowcharts; SVG text, fonts, alt text and keyboard enlargement pass.
- The notebook review includes rendered plots and open worked answers.
  See [browser receipts](classroom_browser_20260910.json) and the
  [independent visual and prose review](notebook_delivery_review_20260910.md).
- All 23 slides were rendered and visually inspected. The PowerPoint package
  has five internal H.264 movies and passes its OOXML/package checks.
- Keynote imported the local PowerPoint without a media warning. All five
  movies played and showed advancing scientific content. The native Keynote
  file retains the same five movie hashes. See
  [slide compatibility evidence](slides_20260910.md).

## Remaining delivery work

1. Publish the approved candidate and execute the six lessons plus optional
   diffusion companion from public links in fresh authenticated Colab CPU
   sessions. Record setup, complete execution and result downloads separately.
2. Rehearse the complete three-hour lecture and three-hour practical route,
   including organiser-confirmed breaks and transitions. The 23-slide file is
   the animated introductory spine; the mapped lecture resource supplies the
   broader explanations.
3. Test native PowerPoint playback, seeking/replay and portability on the
   presentation machine. Improve video opening frames and inspect the history
   animation at classroom viewing distance.
4. Continue the source/formulation audits and optional scientific extensions
   listed in the issue register. Close each issue when its own acceptance
   checks and required evidence are complete.

The printable book remains archived. Original presentation and animation
sources, earlier delivery evidence, and the pre-existing executable-mode change
to `scripts/check_book_theme.py` were preserved.
