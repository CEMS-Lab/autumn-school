# Execution record

All five selected notebooks passed their executable checks under a strict
300-second whole-notebook timeout on 9 September 2026.

These are **local CPU measurements after dependency setup**, not measurements
of a fresh Google Colab session or a guarantee for every laptop.

## Timings

| Notebook | Complete execution | Principal check |
| --- | ---: | --- |
| 01 — PhAST damage evolution | 76.301 s | 60 quasi-static increments, 8,385 nodes / 16,384 T3 elements; strict failure flags enabled; no warnings. |
| 02 — Degradation derivative | 4.721 s | Analytic/autograd difference 0; centred-FD difference 3.51e-12 at the stated point. |
| 03 — Illustrative inverse bar | 5.446 s | Recovered E = 2.40030 from synthetic E = 2.4, with a separate held-out load. |
| 04 — Train, save and reload | 9.473 s | 400-epoch training 1.327 s; reload difference 0; held-out MLP/RBF RMSE 0.05636 / 0.09971. |
| 05 — Assessed model proposal | 5.179 s | Compatible and corrupted cases distinguished; reference-corrected relative residual 2.97e-15. |

The complete execution includes imports, data/configuration preparation,
computation, checking, plotting, output creation and notebook execution overhead.
It does not include installing Python or downloading dependencies. Notebook 01's
actual inner solve took 70.075 seconds; its figure shows the locked precrack,
first load increment and final load increment separately.

A second, independent rehearsal executed all five notebooks from the assembled
distribution with the external source-path environment variable unset. All
passed again: 88.35, 5.04, 4.85, 5.80 and 4.26 seconds, respectively. The
rehearsal used the supplied whole-process runner; its record is
`evidence/package_rehearsal.json`. Runtime variation is expected under changing
system load, but every observed run remained below 90 seconds.

## Reproduction information

- Apple M4 Pro, arm64, 14 logical CPUs; CUDA unavailable.
- macOS 27.0; Python 3.10.18; PyTorch 2.8.0; Matplotlib 3.10.8;
  nbconvert 7.17.0.
- The forward helper uses up to four CPU threads; tiny MLP training uses one.
- Public PhAST version 0.16.2, revision
  `f6324f899f0701769810be117f27f1208f7a582e`.
- The actual imported source was `vendor/PhAST/src`, verified against its
  revision and per-file SHA-256 manifest before import.
- The solver configuration, seeds, tolerances and saved outputs are included.
- Exact machine-readable evidence: `evidence/notebook_runtime.json`.

For the selected forward case, the sum of the positive damage increment outside
the locked precrack was 967.4595 and its maximum was 0.3351. The sum is a
mesh-dependent nodal diagnostic, **not an integrated fracture energy or physical
crack length**.

## Interpret the scope correctly

Notebook 01 is an actual public PhAST quasi-static AT2 calculation with the
SciPy sparse-direct mechanics route. It demonstrates diffuse damage evolution,
not sharp-front propagation, branching or physical-time dynamics. It is not a
matrix-free mechanics speed benchmark.

Notebook 02 checks a smooth constitutive derivative. Notebook 03 is an original
one-dimensional elastic-bar inverse exercise. Notebooks 04–05 use a small
Helmholtz-like teaching field. They are not full-fracture inverse or learned
damage replacement demonstrations.

The example adapter assessment limit in notebook 05 is deliberately loose
(relative residual 0.3) to illustrate an accept/reject decision. It is not a
recommended fracture-equilibrium tolerance. The compatible toy proposal's
relative residual is about 0.194; a corrupted proposal is rejected at about
1.164, and the reference solution brings it to round-off scale.

DAgger is explained in the book and slides. Notebook 05 saves one correction
record; it does **not** perform a complete model-induced rollout, dataset
aggregation and retraining cycle.

Two stronger-load, coarser forward trials stopped at the configured
non-convergence criterion after about 28–30 seconds. They were not selected.
No convergence check was relaxed to make those trials look successful.

## Viewing and portability checks

The book and presentation were rendered and visually reviewed. The HTML
companion's equations and controls have independent checks; book mathematics
is served from included MathJax assets. The package includes executed HTML
notebooks and figures, so teaching can continue without Python execution.

Run `python scripts/run_course.py --notebook 1` (or 2–5) after preparing the
environment to obtain a fresh local timing record. Rehearse all five notebooks
in the actual classroom/Colab environment before the school.
