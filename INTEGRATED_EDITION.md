# About the integrated edition

The HTML book renders six notebooks as native chapter pages, including their
code and recorded outputs. MyST-NB and Sphinx generate the HTML reading route;
each computational lesson provides downloadable practice and solution notebooks.

The original numerical code, outputs and execution counts are checked against
the reviewed notebooks before publication. That comparison is recorded in
**evidence/integrated_notebook_parity.json**. Publication builds reuse the retained
outputs. The runtime evidence in **EXECUTION_REPORT.md** describes execution on
the reference local CPU. Measure setup and execution on your target environment
when preparing a class. The opening teaser has its own receipt in
**evidence/teaser_runtime.json**:
6.381 seconds for the whole notebook process on the reference local CPU after
setup. It is an original algebraic model.

Practice downloads include the computational walkthrough and exercise questions.
Solution downloads add the corresponding hints and worked answers. The exercise
answers work through the included algebraic, elastic-bar and scalar-field
examples and their interpretation.

The first PhAST course package remains a separate edition. The v0.1.1 visual
revision changes seven book diagrams and six corresponding lecture slides;
the numerical examples retain their recorded code and results.
The frozen v0.1.0 release remains available unchanged.

## Visual revision v0.1.1

The course map now explicitly covers three two-hour sessions. Staggered
iteration, assembled/matrix-free alternatives, reverse accumulation and
learned-proposal correction use labelled, spatially separated paths. The
book uses original SVG diagrams for HTML, with vector PDF figure assets for
reuse. The 44-slide deck uses editable LaTeX/TikZ.
See [DESIGN_STANDARD.md](DESIGN_STANDARD.md) for inspected Delft, TUM and ETH
references, attribution boundaries and the cross-format review procedure.

Historical receipts, including the backpropagation example's original figure
hash, describe the corresponding execution and graphics. This edition's manifest
identifies the current visual assets. The course plan tracks extensions in
fracture inversion, learned coupling and data aggregation.

## Authoring and reproducibility

The six canonical notebooks remain under **notebooks/**. The book-specific
copies and answers are generated from those notebooks and the original JSON
exercise sources under **source/book/solutions/**. The generator is
**source/book/scripts/build_lab_pages.py**. Edit the canonical notebooks and
exercise sources, then regenerate the book copies.

To rebuild the book, use an authoring environment containing Sphinx, MyST-NB,
sphinx-book-theme and sphinx-copybutton. Regenerate the lesson copies, then run
the Sphinx HTML builder against **source/book/**.
Dependencies for authoring are separate from those needed to run the course.

## Pedagogical references

- [Dive into Deep Learning](https://d2l.ai/index.html): continuous prose,
  equations, code, computed outputs and exercises, with notebook downloads.
- [D2L contribution guide](https://d2l.ai/chapter_appendix-tools-for-deep-learning/contributing.html):
  notebook-derived publication and source maintenance.
- [Advanced Deep Learning for Physics](https://tum-pbs.github.io/ADL4P/):
  small physical systems, reference comparisons, hand-derived sensitivities
  and learning tasks. The inspected public exercises use longer assignment
  formats; measure runtime independently for each adapted example.
- [Physics-based Deep Learning teaser](https://physicsbaseddeeplearning.org/intro-teaser.html):
  a short opening prediction that exposes ambiguity in supervised targets.
- [Differentiable physics](https://physicsbaseddeeplearning.org/diffphys.html):
  the distinction between residual evaluation and gradients through numerical operators.

Our worked solutions and interface design are original. The reference sites
inform the pedagogical structure.
