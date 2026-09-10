# PhAST Autumn School

A short, learn-by-doing course on phase-field fracture, finite elements,
differentiation and learning around numerical solvers.

Prepared by **Allamaprabhu Ani and Sathiskumar A. Ponnusami**, CEMS-Lab,
for the UKACM Autumn School 2026.

The [delivery guide](MVP_DELIVERY.md) describes the three-hour lecture /
three-hour exercise route. The book's topics follow three connected groups.
See [current materials](CURRENT_DELIVERY.md) and [the delivery checklist](TODAY.md).

**[Read the interactive book](https://cems-lab.github.io/autumn-school/)** ·
**[Download the current course](https://github.com/CEMS-Lab/autumn-school/archive/refs/heads/main.zip)** ·
**[Report an issue](https://github.com/CEMS-Lab/autumn-school/issues)**

The book places explanations, equations, code, recorded outputs, exercises,
hints and worked solutions in one reading sequence. Download practice notebooks
or notebooks with solutions when you want to run or modify a calculation.

## What is included?

- An opening experiment on ambiguous predictions and energy-based training.
- Phase-field fracture fundamentals, degradation laws and solution methods.
- A small public PhAST quasistatic calculation with generated geometry and mesh.
- Derivative checks and a small elastic-bar inverse problem.
- Train/save/reload and checked model proposals on a labelled toy field problem.
- An HTML learning book with notebook downloads, a 23-slide animated introduction
  and a 44-slide lecture resource, organised into three lecture hours followed
  by three practical hours.

Start with [the setup guide](SETUP.md) for execution, or open `index.html` in
the complete downloaded folder to read offline. The book is static HTML:
it shows recorded Python outputs. Download a notebook to execute its Python cells.
The supplementary `explorations.html` page has browser-only visual controls.

## Runtime and scientific scope

All six current notebooks completed in 3.74–92.00 seconds each in fresh local
processes on the reference macOS ARM machine after setup. Installation time is
separate. See [the current runtime receipt](evidence/notebook_runtime_current.json)
and [the delivery evidence](evidence/course_delivery_20260910.md).
These measurements describe the reference environment. Repeat setup and timing
on your chosen machine or Colab runtime before class.

The PhAST example follows quasistatic damage around a seeded notch. The
elastic-bar inverse problem isolates parameter recovery, while the scalar
Helmholtz example isolates training, reload and proposal assessment. The course
connects these examples to questions of fracture-parameter identifiability,
learned solver coupling and data aggregation.

## Source and maintenance

The solver snapshot is the public [CEMS-Lab/PhAST](https://github.com/CEMS-Lab/PhAST)
revision `f6324f899f0701769810be117f27f1208f7a582e` (v0.16.2), with its
licence and file hashes in `vendor/PhAST/`. This repository uses a dedicated
course history and a bundled public solver snapshot.

Editable book sources live in `source/book/`; canonical executed notebooks
live in `notebooks/`; original exercise sources live in
`source/book/solutions/`. See [contributor guidance](CONTRIBUTING.md) and
[edition notes](INTEGRATED_EDITION.md) before editing generated pages.
The [Design Directives](DESIGN_DIRECTIVES.md) and [Pedagogical Walkthrough](PEDAGOGICAL_WALKTHROUGH.md)
record the D2L/ADL4P pedagogical standards, notebook anatomy, and Matplotlib plotting rules,
enforced automatically on every Sphinx build.
The [academic diagram standard](DESIGN_STANDARD.md) records the inspected
Delft, TUM and ETH references and visual grammar.

The reading design is informed by [D2L](https://d2l.ai/),
[ADL4P](https://tum-pbs.github.io/ADL4P/) and
[Physics-based Deep Learning](https://physicsbaseddeeplearning.org/intro-teaser.html).
Our teaching text, examples and solutions are original.
See [attribution and content reuse](ATTRIBUTION.md) and
[bundled component notices](THIRD_PARTY_NOTICES.md).

Issues and reviewed improvements guide course development before and after
the school.

The [course plan](COURSE_PLAN.md) and
[main planning issue](https://github.com/CEMS-Lab/autumn-school/issues/1)
track the complete curriculum and its 15 linked workstreams. The
[coherence review](https://github.com/CEMS-Lab/autumn-school/issues/15)
is a required teaching-release gate.
