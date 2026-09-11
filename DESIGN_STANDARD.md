# Academic diagrams for the PhAST course

This standard supports the complete six-hour lecture, book and notebook route.
Figures should help a student answer a scientific question before they inspect
implementation details. A diagram is an explanation, not decoration.

## Curated Keynote lecture companion

The [Keynote presentation standard](source/slides/curated-keynote/DESIGN_STANDARD.md)
specifies fixed typography, half-slide equations, Matplotlib scaling, restrained
builds and native Keynote review for the three-lecture narrative. Its source
notes distinguish teaching guidance from our numerical layout choices.

## Inspected design references

The following publicly accessible sources were visually reviewed on
9 September 2026. They inform original layouts; no university figure, logo,
slide template or screenshot is redistributed, and no endorsement is implied.

| Source and inspected location | Principle applied here |
| --- | --- |
| [TU Delft: Finite Elements in Civil Engineering and Geosciences, §8.3, Fig. 8.9](https://teachbooks.tudelft.nl/computational-modelling/advanced_topics/multiscale/surrogate.html) | Connect the physical calculation, dataset and surrogate; label exchanged quantities at the interface. |
| [TUM: ADL4P, Differentiable Physics II, PDF pages 5 and 14](https://tum-pbs.github.io/ADL4P/slides/ADL4P%203%20-%20Differentiable%20Physics%20II.pdf) | Align forward states and backward sensitivities; use consistent notation and separate comparison rows. |
| [ETH Zurich SPCL: DaCeML presentation, PDF pages 8–9](https://spcl.inf.ethz.ch/Publications/.pdf/daceml-slides.pdf) | Establish an input–process–output overview before expanding one stage. This is a research presentation, not a course lecture. |

D2L and Physics-based Deep Learning remain references for the continuous
explanation–code–exercise–solution format. The three sources above supplement
that teaching structure with specific visual-design observations. This is not
a claim to have reviewed every university course or the outstanding supplied
Instagram/PDF repository inventory.

## Visual grammar

### HTML reading theme

The HTML book uses **Sphinx Book Theme 1.1.4 / PyData Sphinx Theme 0.15.4**,
matching the theme stack served by
[Physics-based Deep Learning](https://physicsbaseddeeplearning.org/intro.html).
Reference HTML, stylesheets and local package source were inspected on
9 September 2026; this is not a claim of a new side-by-side browser review.

Retain the upstream defaults: dark background `#121212`, primary/link blue
`#528fe4`, secondary/hover orange `#e89217`, system sans-serif text, and 1.65
body line height. The wide layout caps the page at 88 rem, uses a 20% primary
sidebar from 992 px, a 17 rem page-contents column from 1200 px, and 2 rem
article padding (1 rem at narrow widths). Let the theme collapse navigation
at its native breakpoints; do not force three columns onto a small screen.

Dark is the initial mode; the reader may choose light or system mode with
the standard toolbar control. Course CSS only adapts notebook cells, solution
panels, equation overflow and print. Quantitative figures must not be inverted,
darkened or recoloured: preserve white canvases and original colour bars.
Lecture slides and scientific figure exports keep their existing white design.
The theme does not alter notebook computation, output or runtime claims.

#### PhAST accents and optional discoveries

The subsequent user-approved accent pass keeps the same dark surfaces and
column geometry but replaces the stock blue/orange accents with PhAST-derived
colours. Public [PhAST documentation CSS](https://github.com/CEMS-Lab/PhAST/blob/f6324f899f0701769810be117f27f1208f7a582e/docs/_static/phast.css)
declares orange `#e95420`. Pixel (600, 406) of the
[public gradient banner](https://github.com/CEMS-Lab/PhAST/blob/f6324f899f0701769810be117f27f1208f7a582e/assets/phast-banner.png)
is blue `#0261e0`; this is a sampled colour, not a formally declared palette.
Reading accents are adapted to `#79b8ff` / `#ff9966` in dark mode and
`#005bc4` / `#b83e13` in light mode. Keep headings predominantly neutral:
only the short heading rule, current navigation, links and answer-panel edges
carry the two colours. Do not replace semantic warning/error colours.

Two tiny, closed-by-default footer disclosures offer a gradient observation
and a scalar chain-rule puzzle. They work without JavaScript, collect no data,
play no sound, trigger no animation and are omitted from print. They are
optional extras, never prerequisites or a gate on reading a solution.

The footer credits Allamaprabhu Ani and Sathiskumar A. Ponnusami as creators,
identifies CEMS-Lab and states “Prepared for the UKACM Autumn School 2026”.
Keep those two lines readable but secondary to the lesson, without academic
titles, promotional claims or an implication that UKACM owns the course content.

Rebuild with the pinned requirements and the existing Sphinx command below.
The local MathJax distribution is retained in `book/_static/mathjax/`; do not
delete it when rebuilding the tracked HTML output. The Sphinx build hook copies
that retained distribution into other HTML output directories. Keep upstream theme
licences in `source/book/_static/licenses/` so Sphinx includes them in HTML.

### Diagram conventions

- Use white space and a clear left-aligned heading. One figure answers one
  principal question; remove unnecessary panels, shadows and branded ribbons.
- Blue (`#245A81`) denotes forward evaluation. Orange (`#B85C20`) denotes
  reverse sensitivity or a labelled retry/correction route. Teal (`#087F82`)
  denotes parameters, learned components or an explicitly labelled acceptance.
  Dark grey is explanatory context. Text and arrow direction carry the meaning
  independently of colour.
- Use circles for states in a computational graph, plain rectangles for
  operations and a diamond only for an actual decision. Course-overview rows
  need no surrounding boxes. Label every decision branch.
- Prefer aligned, orthogonal paths. A feedback arrow must connect the output
  that changes to the operation that consumes it; do not add a loop merely to
  suggest iteration. A dashed path denotes the named conceptual extension.
- Put the mathematical quantity near its operation. Define symbols in the
  adjacent prose. Never confuse a state, scalar objective, gradient and
  optimisation update.
- Use Matplotlib with mathematical text for original book schematics, with
  14–18 pt principal annotations on an approximately nine-inch source canvas.
  Use editable LaTeX/TikZ for lecture diagrams. Recompose for each aspect ratio
  rather than shrinking the whole textbook figure onto a slide.
- Export SVG for sharp HTML, PDF for vector figure reuse and PNG for simple previews.
  Preserve live SVG text and embedded PDF fonts. Supply meaningful alternative
  text and a prose interpretation beside each diagram.

## Course-wide invariants

The curated edition follows three lectures of 45, 55 and 50 minutes, then three
50-minute practicals. The six-hour event window includes 60 flexible minutes;
TEACHING_SCHEDULE.md defines that allocation. The frozen v0.1.1 overview
depicts the previous three mixed 120-minute blocks.
It must show the fundamentals and model-learning activities, not only inverse
problems. Classroom notebooks are numbered 1–3; the original six notebooks retain their
separate detailed-reference identifiers. Lecture time
includes explanation and discussion; it is not a computational runtime.

The staggered diagram orders mechanics, driving field, damage and convergence;
failure returns to mechanics within the same increment. The matrix-free
comparison shares its physical inputs and required output checks. Reverse mode
accumulates every use of a shared parameter. A learned proposal reaches a
stated gate before acceptance; correction must itself be checked. A conceptual
DAgger round is not labelled as an executed notebook result.

## Rebuild and review

The tested diagram-authoring packages are recorded in
`source/requirements-figures.txt`; the book build uses
`source/requirements-book.txt`. Diagram exports embed subset fonts so that
offline browser rendering does not depend on locally installed font families.

```bash
python source/book/scripts/build_figures.py --flowcharts-only
python source/book/scripts/build_backprop_example.py --figure-only
python -m sphinx -b html -E -a source/book book -W --keep-going
cd source/slides
latexmk -pdf -outdir=../../.build/slides -interaction=nonstopmode -halt-on-error phast_autumn_school_2026.tex
```

Read the actual exported diagrams, changed slide pages and affected book pages.
Check small-screen HTML, zoomed vector labels, print contrast, captions,
branches, equations and links. Re-run changed calculations, but do not launch
solver jobs for a purely graphical change. Preserve historical numerical
receipts; an old figure hash describes the old visual artifact. A visual
revision needs its own manifest, not a fabricated new execution record.

Track design work under issue #14, slide changes under #12 and final
cross-format coherence under #15. These checks do not close unrelated content
or fresh-Colab requirements.
