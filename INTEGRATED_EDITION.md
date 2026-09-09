# About the integrated edition

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

The first PhAST course package remains a separate edition. This revision does
not change its numerical examples or the lecture-slide design.

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
