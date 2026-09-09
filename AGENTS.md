# Guidelines for Course Authors and AI Agents

Before making any edits, you **MUST** read:
1. **[DESIGN_DIRECTIVES.md](DESIGN_DIRECTIVES.md):** Authoritative directives on tone, undergraduate accessibility, prohibited negative/contrastive AI phrasing, standardized 6-part notebook anatomy, and Matplotlib plotting parameters.
2. **[PEDAGOGICAL_WALKTHROUGH.md](PEDAGOGICAL_WALKTHROUGH.md):** Complete record of the educational overhaul, implementation plan, and D2L/ADL4P benchmarks across the four workshop pillars.
3. `COURSE_PLAN.md`, `CONTRIBUTING.md`, and the assigned GitHub issue.

### Automated Design Gate
Every `sphinx-build -b html source/book book` automatically executes `scripts/check_design_directives.py` in under 0.1s to enforce zero violations of prohibited negative phrasing, presence of the 4 core pillars, and valid notebook badge layouts. Do not commit or push if this check fails.

### Core Directives
- Write in welcoming, pedagogical, undergraduate-accessible language (D2L / ADL4P style). Never use failure-obsessed framing, contrastive "X not Y" formulations, or raw floating-point quizzes.
- State the files you own; do not modify another contributor's work or the
  vendored solver. Never push without the maintainer's explicit assignment.
- Use original educational prose and figures. Attribute sources and preserve
  bundled licences. Do not import private papers, datasets or model weights.
- Keep the lecture narrative coherent: name prerequisites, connect to the
  preceding lesson, define notation and finish with an interpretable result.
- State whether an example is algebraic, a teaching field model, or actual
  PhAST. Do not upgrade claims when only formatting changes.
- Keep computations below 300 seconds after setup; report complete measured
  time and platform. Test changed calculations rather than recycling receipts.
- Edit source chapters and JSON exercise files, not generated HTML or lesson
  copies. Follow the rebuild instructions and inspect the rendered output.
- Report changed paths, tests, provenance, limitations and the precise next
  action. Do not mark the issue complete while a required check remains open.
