# Visual revision v0.1.1 — review record

Date: 9 September 2026. Baseline: public course revision
`d424f3a0eae791f04d42e6af513a54244f2881c6`.

## Scope

Seven original book flowcharts were recomposed; corresponding lecture pages
2, 13, 15, 26, 39 and 40 were updated in editable LaTeX/TikZ. The course plan
retains three 120-minute blocks and distinguishes full-course integration
from the separately reviewed inverse extension. The design reference trail
is in `DESIGN_STANDARD.md`.

Canonical notebooks, book-native notebook cells and outputs, existing
numerical receipts, data, model files, the solver vendor snapshot and
`TEACHING_SCHEDULE.md` have no tracked changes relative to the baseline.
No solver, training or inverse calculation was executed for this revision.
The historical backpropagation receipt's figure hash belongs to its earlier
drawing, not the new SVG/PNG/PDF. Current asset hashes are in `MANIFEST.json`.

## Build and visual checks

- Sphinx HTML and LaTeX builds completed with warnings treated as errors.
- XeLaTeX produced the 71-page e-book. All pages were rendered; all twelve
  contact sheets and the seven affected figure pages were inspected. The
  four code-block pages associated with small internal vertical-box warnings
  (maximum 2.70 pt) were inspected at full page size: no visible clipping,
  missing final lines or footer collisions. The FontAwesome icon font emits
  a ToUnicode-map warning; this does not certify fully tagged PDF accessibility.
- The Beamer PDF has 44 rendered slides and 44 sets of instructor notes.
  The six revised pages were individually inspected and corrected after the
  first render. No overfull boxes, missing glyph warnings or missing expected
  figure resources remain in the deck.
- An independent source-figure review checked all seven diagrams against
  the adjacent equations, curriculum and schedule. Arrow direction,
  shared-parameter sums, model/algorithm distinctions and scope labels passed.
- Offline native-notebook checks passed for all six lesson pages at 1440 px
  and 390 px. Code/output figures, local downloads, previous/next links,
  keyboard answer controls, no-JavaScript answer fallback and MathJax rendering
  passed. This is a reading-interface test, not notebook execution.
- `scripts/check_flowcharts.cjs` passed fourteen page/viewport cases. Each
  primary diagram has descriptive alternative text and a keyboard-accessible
  full-size SVG link; pages have no document overflow or failed resources.
  The standalone SVGs retain text and embed subset fonts, avoiding the browser
  font substitution discovered and corrected during review.

## Reproduction

Use `DESIGN_STANDARD.md` for figure and book build commands. Render the slide
build with:

```bash
python source/slides/render_beamer.py --build-dir .build/slides --output reviews/slides
python scripts/review_book_pdf.py .build/latex/phast-ukacm-course.pdf --output reviews/book_pdf
node scripts/check_flowcharts.cjs book reviews/flowcharts
```

The browser checker needs Playwright and an installed Chromium browser;
`BROWSER_EXECUTABLE` can select it. Review output is intentionally excluded
from the public payload. The publication build retains notebook outputs.

## Remaining gates

The original v0.1.0 release remains frozen. This visual prerelease does not
claim a fresh Colab run, a complete fracture inverse activity, arbitrary model
interchangeability, learned fracture acceleration or a complete DAgger cycle.
The main issue and topic issues remain open until their full acceptance
criteria are met. Mobile users should enlarge a diagram to read dense
equations; inline fit alone is not proof of lecture-scale readability.
