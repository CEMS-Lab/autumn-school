# Authoring and integration notes

This directory is an isolated book-only extension. The main course task owns
publication, the primary toctree, themes and release packaging. The extension
is intentionally excluded from that build until its handoff is reviewed.

## Contents

The one-stop notebook is assembled by code/build_notebook.py from the same
chapter sources and full experiment/plotting functions. Its code cells have
no external course-helper or data-file dependency. The unexecuted source is
excluded from the HTML build; only a verified HPC-executed copy is added to
the reading route.

- index.md and 01--06 including 03_history: foundations, derivations, 20 exercises with worked
  answers and four application protocols.
- 07_results.md: generated teaching result card.
- code/lab.py: six original analytic/linear-algebra experiments, run on HPC.
- code/history_lesson.py: one history-rule example, with 11 additional checks.
- data/notebook_execution_receipt.json: complete HPC notebook execution,
  16 code cells, eight plots and 26 passing checks; 8.56 seconds including
  kernel startup, excluding queue wait, installation and HTML rendering.
- data/teaching_results.json: unchanged retained HPC output, 15 passing checks.
- code/render.py: render the retained arrays; no numerical experiment rerun.
- figures/: seven original Matplotlib figures as PNG/PDF, the workflow PNG,
  and history_rules.png extracted directly from the executed notebook.
- tex/inverse_workflow.tex and .pdf: editable original TikZ workflow.
- conf.py, _static/ and code/check_preview.cjs: isolated preview/QA support.

## Render and build

From this directory, in the existing course-authoring environment:

    python code/render.py
    sphinx-build -b html -W --keep-going . _build/html
    node code/check_preview.cjs _build/html _build/qa

The browser checker uses Playwright and the local Brave executable. NumPy,
Matplotlib and Sphinx are authoring dependencies. PyTorch is only needed to
execute lab.py; research execution for this project belongs on HPC.

Rebuild the workflow using pdflatex in tex/, then rasterise the PDF for the
HTML image. The recorded renderer requires the source hash of lab.py to match
the retained JSON. Changing lab.py requires a new recorded HPC execution.

The offline preview vendors MathJax 3.2.2 with its license. The publication
owner can reuse the main course's single MathJax copy and shared theme.
Exclude _build/, author-only README.md, TeX intermediate .aux/.log files and
preview-specific configuration when packaging for the main course.

## Scope

All teaching prose, computations and scientific figures here are original.
ADL4P is credited for pedagogical inspiration and linked for further study.
No private fracture source or numerical result is in this directory.
Public distribution and integration still require the publication owner's
review. This extension does not complete the actual-fracture inverse notebook
requested in issue #7 or the advanced research programme in issue #13.
