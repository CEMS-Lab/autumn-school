# About the integrated edition

## Interactive history integration, 9 September 2026

The main HTML book now includes the interactive plate/history playground,
the 40-second algorithm walkthrough and eight explanatory stages with offline
equations. The user explicitly authorised merging and publishing this latest
addition. The source payload is teaching/interactive-history at bafb35e.

The plate contains 12 retained frames from a 1600-step forward calculation.
Local energy curves are illustrative; energy/history and active-set snapshots
were not retained. The lesson distinguishes the hard-forward, sigmoid-backward
surrogate from a smooth-forward history model. Seventeen new source/artifact
hashes are checked in addition to the earlier inverse-extension receipts.
The numerical notebook cells, frozen PDF/slides and shared theme are unchanged.
The separately requested Manim animation is subsequent work, not part of this
published payload.

## Optional inverse extension, 9 September 2026

The HTML now includes source-grounded history explanations, an 18-second
animation, seven original HPC-executed teaching examples and a visual
laboratory with three further animations. The latter distinguishes a dense
geometry-image toy from a retained 25-point FEM scan and a recorded inverse
trajectory. Numerical receipts and downloadable inputs accompany the pages.
The user authorised this bounded merge and publication. It does not close
issue #7's fresh actual-fracture notebook requirements or change the six-hour
classroom sequence. No new solver or manuscript changes are included.

The printable PDF and slide release assets remain the earlier classroom
edition; this HTML addition does not imply those frozen files were rebuilt.
See evidence/inverse_publication.json for the content/receipt checks.
The integrated HTML passed a warning-free Sphinx build, 24 inverse and six
classroom page/viewport checks, and eight native-video viewport checks.
Local links, offline equations, downloads, playback and seeking were checked.

## Classroom edition

The book renders six notebooks as native chapter pages, including
their code and recorded outputs. It does not display a separate notebook website
inside an iframe. MyST-NB and Sphinx generate both HTML and PDF.

The original numerical code, outputs and execution counts are checked against
the reviewed notebooks before publication. That comparison is recorded in
**evidence/integrated_notebook_parity.json**. Publication builds do not execute
notebooks. The runtime evidence in **EXECUTION_REPORT.md** remains the earlier
local CPU execution evidence; it is not a new Colab or clean-install test.
The opening teaser has its own new receipt in **evidence/teaser_runtime.json**:
6.381 seconds for the whole notebook process on the reference local CPU after
setup. It is an original algebraic model, not a fracture simulation.

Practice downloads include the computational walkthrough and exercise questions.
Solution downloads add the corresponding hints and worked answers. The exercise
answers explain calculations and interpretation; they do not add an unmeasured
full-fracture inverse, learned-damage coupling or DAgger training cycle.

The first PhAST course package remains a separate edition. The v0.1.1 visual
revision changes seven book diagrams and six corresponding lecture slides,
but does not change numerical examples or their retained execution evidence.
The frozen v0.1.0 release remains available unchanged.

## Visual revision v0.1.1

The course map now explicitly covers three two-hour sessions. Staggered
iteration, assembled/matrix-free alternatives, reverse accumulation and
learned-proposal correction use labelled, spatially separated paths. The
book uses original SVG diagrams for HTML and vector PDF diagrams for print;
the 44-slide deck uses editable LaTeX/TikZ. The printable book has 71 pages.
See [DESIGN_STANDARD.md](DESIGN_STANDARD.md) for inspected Delft, TUM and ETH
references, attribution boundaries and the cross-format review procedure.

This revision is not a new numerical rehearsal. Historical receipts, including
the backpropagation example's original figure hash, describe their original
execution and graphics. The current visual assets are identified by this
edition's manifest. Fresh Colab timing, a full fracture inverse activity,
learned fracture coupling and a complete DAgger training round remain separate
open requirements.

## Authoring and reproducibility

The six canonical notebooks remain under **notebooks/**. The book-specific
copies and answers are generated from those notebooks and the original JSON
exercise sources under **source/book/solutions/**. The generator is
**source/book/scripts/build_lab_pages.py**. Do not hand-edit generated copies.

To rebuild the book, use an authoring environment containing Sphinx, MyST-NB,
sphinx-immaterial and sphinx-copybutton. Regenerate the lesson copies, then run
Sphinx against **source/book/**. PDF compilation additionally needs XeLaTeX.
Dependencies for authoring are separate from those needed to run the course.

## Pedagogical references

- [Dive into Deep Learning](https://d2l.ai/index.html): continuous prose,
  equations, code, computed outputs and exercises, with notebook downloads.
- [D2L contribution guide](https://d2l.ai/chapter_appendix-tools-for-deep-learning/contributing.html):
  notebook-derived publication and source maintenance.
- [Advanced Deep Learning for Physics](https://tum-pbs.github.io/ADL4P/):
  small physical systems, reference comparisons, hand-derived sensitivities
  and learning tasks. The inspected public exercises are longer assignments,
  not evidence of five-minute execution.
- [Physics-based Deep Learning teaser](https://physicsbaseddeeplearning.org/intro-teaser.html):
  a short opening prediction that exposes ambiguity in supervised targets.
- [Differentiable physics](https://physicsbaseddeeplearning.org/diffphys.html):
  the distinction between residual evaluation and gradients through numerical operators.

Our worked solutions and interface design are original. The reference sites
are not represented as suppliers of the answers in this book.
