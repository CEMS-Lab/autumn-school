# PhAST Autumn School

A short, learn-by-doing course on phase-field fracture, finite elements,
differentiation and learning around numerical solvers.

**[Read the interactive book](https://cems-lab.github.io/autumn-school/)** ·
**[Download an edition](https://github.com/CEMS-Lab/autumn-school/releases)** ·
**[Report an issue](https://github.com/CEMS-Lab/autumn-school/issues)**

The book places explanations, equations, code, recorded outputs, exercises,
hints and worked solutions in one reading sequence. Download practice notebooks
or notebooks with solutions when you want to run or modify a calculation.

## What is included?

- An opening experiment on ambiguous predictions and energy-based training.
- Phase-field fracture fundamentals, degradation laws and solution methods.
- A small public PhAST quasistatic calculation with generated geometry and mesh.
- Derivative checks and a small elastic-bar inverse problem.
- An optional inverse extension with an animated history lesson, a complete
  teaching notebook, particle loss landscapes and retained FEM recovery films.
- Train/save/reload and checked model proposals on a labelled toy field problem.
- A printable e-book, 44-slide lecture deck and three two-hour teaching schedule.

Start with [the setup guide](SETUP.md) for execution, or open `index.html` in
the complete downloaded folder to read offline. The book is static HTML:
it shows recorded Python outputs; it does not run Python inside the browser.
The supplementary `explorations.html` page has browser-only visual controls.

## Runtime and scientific scope

All six unmodified notebooks completed in less than 90 seconds each on the
reference Apple M4 Pro CPU after setup. Installation time is separate. See
[the execution report](EXECUTION_REPORT.md),
[the teaser receipt](evidence/teaser_runtime.json), and the per-file receipts.
Fresh Colab and clean-environment timings remain to be measured; the local
measurements are not a guarantee for another machine or edited problem.

The real PhAST example demonstrates a small quasistatic damage calculation,
not a validated branching demonstration. The inverse and learning activities
are original teaching models, not full fracture inversion, a trained fracture
accelerator or a completed DAgger cycle. These are explicit course development
directions, not capabilities established by the included notebooks.

The [optional inverse extension](https://cems-lab.github.io/autumn-school/book/research/index.html)
adds seven small HPC-executed teaching examples and separately identified
retained FEM visualizations. Its recorded fracture fields are not a new
under-five-minute fracture-inverse notebook or a historical solver replay.
The existing downloadable PDF and slides remain the earlier classroom edition;
the new extension is currently in HTML and its downloadable notebooks/figures.

## Source and maintenance

The solver snapshot is the public [CEMS-Lab/PhAST](https://github.com/CEMS-Lab/PhAST)
revision `f6324f899f0701769810be117f27f1208f7a582e` (v0.16.2), with its
licence and file hashes in `vendor/PhAST/`. This repository has its own clean
history and does not include the research-authoring worktree.

Editable book sources live in `source/book/`; canonical executed notebooks
live in `notebooks/`; original exercise sources live in
`source/book/solutions/`. See [contributor guidance](CONTRIBUTING.md) and
[edition notes](INTEGRATED_EDITION.md) before editing generated pages.
The [academic diagram standard](DESIGN_STANDARD.md) records the inspected
Delft, TUM and ETH references and the original course-wide visual grammar.

The reading design is informed by [D2L](https://d2l.ai/),
[ADL4P](https://tum-pbs.github.io/ADL4P/) and
[Physics-based Deep Learning](https://physicsbaseddeeplearning.org/intro-teaser.html).
Our teaching text, examples and solutions are original.
See [attribution and content reuse](ATTRIBUTION.md) and
[bundled component notices](THIRD_PARTY_NOTICES.md).

This first edition is a course prerelease. Issues and reviewed improvements
will guide its development before and after the school.

The [course plan](COURSE_PLAN.md) and
[main planning issue](https://github.com/CEMS-Lab/autumn-school/issues/1)
track the complete curriculum and its 15 linked workstreams. The
[coherence review](https://github.com/CEMS-Lab/autumn-school/issues/15)
is a required teaching-release gate.
