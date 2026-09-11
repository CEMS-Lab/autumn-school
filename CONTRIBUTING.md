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

The first practical has a dedicated generator,
`source/notebooks/build_forward_practical.py`. The other current notebooks
are authored directly. Shared environment cells come from
`source/notebooks/colab_bootstrap.py`; apply them with
`python source/notebooks/sync_bootstrap.py`, then rerun changed notebooks.
Historical starter templates in `build_day2_notebooks.py` require an explicit
separate export directory. Current prose and exercises belong in canonical
notebooks and solution JSON, so a book rebuild preserves them.

## Curated classroom notebooks

The primary route consists of three notebooks in `notebooks/classroom/`.
`source/notebooks/build_classroom_labs.py` authors them from the retained
examples and inspectable course helpers. `source/book/scripts/build_classroom_pages.py`
creates book-native pages and practice/solution variants after execution.
Do not overwrite the original detailed notebooks or their dated receipts.

After an intentional generator change, run each complete classroom notebook
with `python scripts/run_classroom.py --notebook 1` (then 2 and 3). The runner
retains checked outputs in the tracked canonical classroom files. A clean
checkout can rebuild their HTML from those files; ignored execution caches
provide an optional local source. Generation clears outputs and therefore
requires a new execution before rebuilding the published variants.

Use full classroom notebook names in execution records; the original two-digit
reference IDs are a separate registry. Hash supporting helpers as well as cell
sources. The [placeholder register](source/planning/PLACEHOLDER_REGISTER.md)
tracks future lecture and research assets.

## Rebuild the book

Use Python 3.10–3.12 in an isolated environment. From the repository root:

```bash
python -m pip install -r source/requirements-book.txt
python source/book/scripts/build_lab_pages.py
python source/book/scripts/build_classroom_pages.py
python -m sphinx -b html -E -a source/book book -W --keep-going
```

The build deliberately retains outputs instead of executing notebooks. A
successful Sphinx build is not a numerical test. Re-run any changed computation
in the course environment and record its whole-notebook runtime, environment,
checks and limitations. Preserve failing evidence when reporting an issue.

Inspect the HTML chapters, equations, plots, code and solutions. Test the HTML
on a narrow screen and with the network disconnected. Verify local practice
and solution notebook downloads and keyboard-operated answer panels. Keep
`.nojekyll` so GitHub Pages serves Sphinx's asset folders.

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
