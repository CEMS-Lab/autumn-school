# Shared PhAST documentation and autumn-school example

Tracking: [course #19](https://github.com/CEMS-Lab/autumn-school/issues/19),
[forward practical #5](https://github.com/CEMS-Lab/autumn-school/issues/5),
and [PhAST documentation #4](https://github.com/CEMS-Lab/PhAST/issues/4).
The upstream reproduction discrepancy is tracked in
[PhAST B3 provenance #5](https://github.com/CEMS-Lab/PhAST/issues/5).
Date: 10 September 2026. Course starting revision: `6254c050f1af34efd10ddf1df7c5e80aa8302d40`.
Inspected public PhAST source: `f6324f899f0701769810be117f27f1208f7a582e`.

## Learning problem

Students should be able to move from the autumn-school notebook to the main PhAST documentation and recognise the same geometry, mesh regions, loads, solution route and result files. The current course mesh cell exposes too much implementation detail, and its diffuse-damage calculation shows limited crack extension.

## Scope and ownership

- Course integration owns the six-hour narrative, Lab 01/helper readability, candidate timing, book links and course issues #1/#5/#10/#15.
- The existing PhAST release/documentation task owns public PhAST tutorial and gallery changes and its existing documentation issue.
- Preserve current solver kernels, public scientific boundaries, original-content attribution and tested fallback calculations.
- Upstream tracking: [PhAST documentation #4](https://github.com/CEMS-Lab/PhAST/issues/4).

## Shared example selection

Assess public `examples/dynamic/B3_dynamic_sent/` first: a small single-edge-notched tensile geometry with retained damage fields, energy/crack-tip records and an animation. Its current evidence supports a qualitative demonstration; its retained `history.csv` is header-only. Keep model-specific units, energy split, loading and solver route visible. The two-step upstream setup activity and the course quasistatic diffuse-damage example each retain their stated learning role.

## Acceptance checklist

- [ ] Record canonical public example/configuration paths and exact source revision in both repositories.
- [x] Shorten course mesh cells while preserving exact tested mesh/physical inputs and checks. Local full-notebook run: 92.2464 seconds; exact result NPZ and PNG artifacts retained.
- [ ] Provide a coherent standard Gmsh -> named physical regions -> import -> BC/load -> solve -> result inspection route.
- [ ] Distinguish the setup check, student-run propagation calculation and retained research results through clear positive descriptions.
- [ ] Assess a bounded existing propagation run, preserve diagnostics and inspect full fields and response curves. Quantify extension beyond the initial notch at stated damage thresholds; describe mesh and load-step sensitivity.
- [ ] Promote a student-run case only after complete computation is measured below 300 seconds after setup, including result extraction; record fresh Colab separately in #10.
- [ ] Provide an attributed retained animation and interpretable static frames as a teaching fallback.
- [ ] Align notebook terminology and links with upstream tutorials, including dynamic versus quasistatic assumptions.
- [x] Execute the changed course notebook, regenerate study/solution/HTML variants, and review rendered math, figures, downloads and navigation. Upstream notebook checks are recorded by their owner.
- [ ] Reply to actionable issue comments with evidence and update the main plan/checklist; close only completed acceptance items.

## Current local findings

- Course mesh refactor: complete notebook **92.2464 s**, exact previous mesh and
  field archives, passing contract/source/build/browser checks. See
  [readability evidence](../../evidence/mesh_readability_20260910.md).
- The exact current public B3 YAML reached the 240 s diagnostic cap after
  remeshing, with limited extension. Its propagation-path refinement and
  minimum element size differ from the checked-in evidence mesh.
- The checked-in B3 mesh with explicit residual stiffness `1e-6` and damage
  update every step completed 6,116 CPU steps in **17.6787 s**, plus **0.573 s**
  for field inspection/figure generation. The high-damage band crosses the
  remaining 20 mm ligament. This is a qualitative candidate calculation.
- Promotion requires damage residual/convergence evidence, mesh/time-step
  sensitivity, one complete teaching notebook and fresh Colab verification.
  Read the [canonical-example review](CANONICAL_FRACTURE_REVIEW_20260910.md) for
  both runs, source hashes, explicit adjustments and the reproduction recipe.
- Define the eventual classroom configuration once beside the upstream example,
  then consume that exact version from the course. Keep examples, tutorial prose,
  figures and acceptance records aligned through the linked issues.
- The release/documentation task completed its local tutorial changes and
  synchronized setup-notebook repairs. It reports successful execution of the
  B3 retained-reading notebook (3.17 s), setup (9.47 s), mesh diagnostic (1.13 s)
  and retained-results activity (1.09 s), followed by a warning-free Sphinx build.
  These times concern documentation activities; the B3 reading notebook's
  default executes schema preflight and inspects retained results. Upstream
  publication was authorised after joint review. Published source revisions
  and live checks are recorded in the linked repository issues.

## Brainstorm-to-delivery workflow

Record each new decision in the existing issue that owns it. Create a new issue for a distinct deliverable, link dependencies, assign file ownership, implement a bounded change, and post command/runtime/visual evidence. Preserve discussion history and scientific caveats. Main issue #1 remains the curriculum record; #5 remains the forward numerical workstream and #15 the final coherence gate.

This issue coordinates a shared teaching route within the existing solver capabilities.
The reviewed documentation and course changes are authorised for publication;
the numerical propagation candidate retains its separate acceptance checks.
