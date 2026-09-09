# Improve the course

Begin with an issue describing the learner-facing problem and a small proposed
change. Good contributions include corrections, clearer explanations,
accessibility improvements, reproducible runtime reports and short exercises.
Please discuss new numerical examples with the maintainers before building them.

## Which files should change?

| Change | Source |
| --- | --- |
| Theory or chapter navigation | `source/book/*.md` |
| Exercise, hint or worked answer | `source/book/solutions/*.json` |
| Computation and its recorded outputs | `notebooks/<lesson>.ipynb` |
| Book-native lessons and downloadable variants | Regenerate; do not hand-edit |
| Styling and answer controls | `source/book/_static/` |
| Solver implementation | Propose separately in CEMS-Lab/PhAST |

## Rebuild the book

Use Python 3.10–3.12 in an isolated environment. From the repository root:

```bash
python -m pip install -r source/requirements-book.txt
python source/book/scripts/build_lab_pages.py
python -m sphinx -b html -E -a source/book book -W --keep-going
```

The build deliberately retains outputs instead of executing notebooks. A
successful Sphinx build is not a numerical test. Re-run any changed computation
in the course environment and record its whole-notebook runtime, environment,
checks and limitations. Preserve failing evidence when reporting an issue.

For a PDF, install XeLaTeX and latexmk separately, then run:

```bash
python -m sphinx -b latex -E -a source/book .build/latex -W --keep-going
latexmk -cd -xelatex -interaction=nonstopmode -halt-on-error .build/latex/phast-ukacm-course.tex
```

Inspect rendered pages, equations, plots, code and solutions before replacing
`ebooks/phast-ukacm-course.pdf`. Test the HTML on a narrow screen and with the
network disconnected. Verify local notebook downloads and keyboard-operated
answer panels. Keep `.nojekyll` so GitHub Pages serves Sphinx's asset folders.

## Acceptance criteria for a computational change

1. A stated physical or algebraic problem and explicit toy/solver scope.
2. Deterministic inputs, documented precision and public source provenance.
3. A whole-notebook runtime below 300 seconds after setup, measured separately
   from installation; a hard-cap runner is supplied in `scripts/run_course.py`.
4. An interpretable figure and relevant residual, derivative or reload check.
5. A prediction question, exercise, hint and independently checked solution.
6. No private data, machine-specific paths, credentials or unapproved material.

Do not replace rigorous checks with assertions chosen merely to pass. A fast,
visually attractive calculation is not by itself a converged physical result.

## Publication and reuse

Maintainers review content and publish updated Pages files and release assets.
Before opening a pull request, ensure you are entitled to share the contribution.
Third-party code keeps its existing licence. A blanket licence for original
course material has not yet been assigned; see `ATTRIBUTION.md`. Opening a
public repository does not relicense third-party or unpublished material.
