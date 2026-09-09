# Academic diagrams for the PhAST course

This standard supports the complete six-hour lecture, book and notebook route.
Figures should help a student answer a scientific question before they inspect
implementation details. A diagram is an explanation, not decoration.

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
- Export SVG for sharp HTML, PDF for print and PNG for simple previews.
  Preserve live SVG text and embedded PDF fonts. Supply meaningful alternative
  text and a prose interpretation beside each diagram.

## Course-wide invariants

The overview has three 120-minute blocks, each including a ten-minute break.
It must show the fundamentals and model-learning activities, not only inverse
problems. Notebook numbers refer to the canonical six notebooks. Lecture time
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
python -m sphinx -b latex -E -a source/book .build/latex -W --keep-going
latexmk -cd -xelatex -interaction=nonstopmode -halt-on-error .build/latex/phast-ukacm-course.tex
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
