# Canonical fracture example: source and execution review

Date: 10 September 2026. This is a maintainer-facing diagnostic record for
the first PhAST practical and its alignment with the public solver tutorial.
The current classroom notebook and upstream solver files were preserved.

## Recommendation

Use the **public B3 dynamic single-edge-notched tension (SENT) family** as the
shared candidate for the course and PhAST documentation. Its physical sequence
is simple: load a notched glass plate, observe a tensile crack crossing the
remaining ligament, and inspect damage and energy over physical time.

The strongest executable candidate found here imports the checked-in B3 mesh.
A complete 6,116-step CPU calculation finished in **17.679 seconds**, with
visible propagation across the full 20 mm ligament. A fresh notebook execution,
damage-residual review, mesh/time-step sensitivity check and Colab rehearsal
are the remaining classroom acceptance steps. The case retains the upstream
**qualitative lightweight example** scope during that work.

## Source and competing examples

The reviewed upstream revision is
`CEMS-Lab/PhAST@f6324f899f0701769810be117f27f1208f7a582e`.
Existing documentation edits were left to the release/documentation task.

| Public example | Retained evidence inspected | Recorded original run | Proposed teaching role |
| --- | --- | --- | --- |
| `examples/dynamic/B3_dynamic_sent` | Setup, final damage, animation inventory, crack-tip/energy CSV, metadata and current YAML/fluent source. The final field crosses the remaining ligament. | 1,091 nodes; 1,940 T3 elements; 6,116 steps; 21.25 s on NVIDIA A100. | Canonical candidate, using a checked imported mesh and explicit settings. |
| `examples/quasistatic/miehe_tension` | Final field reaches the far edge; load response and acceptance report accompany it. Current notebook 03 reads retained results. | 2,423 nodes; 4,308 T3 elements; 350 increments; 905.46 s on CPU. | Quasistatic comparison and retained-results study. Full snap-back traversal remains outside its gated comparison. |
| `examples/quasistatic/notched_holed_plate` | Final crack curves into the central hole and emerges on its far side. | 19,129 nodes; 37,666 elements; 200 increments; 37,888.99 s on CPU. | Larger geometry/interaction exhibit with retained results. |
| `examples/dynamic/B7_dynamic_crack_branching_comsol` | Final field visibly branches into two arms; comparison report inspected. | 169,077 nodes; 336,266 elements; 183,941 steps; 2,139.84 s on A100. | Branching exhibit. The retained report's arm-count measurement is unavailable, and its timing uses an energy-based proxy. |

Retained runtimes belong to their recorded hardware and source revisions.
The present review performed two bounded CPU diagnostic runs, both through
the current public solver. A setup validation or a five-step check has a
different learning outcome from a complete propagation calculation.

## B3 model and settings

- Plate: 40 mm × 40 mm, geometric notch from the left edge to `(20, 20)` mm.
- Material: `E = 32000 MPa`, `nu = 0.20`, `Gc = 0.003 N/mm`,
  `l0 = 0.5 mm`, `rho = 2.45e-9` in the solver's mm–N–s unit system.
- Model: plane-strain AT2 with spectral energy split and hard-max history.
- Supports: left and right edges constrained horizontally.
- Loading: top/bottom vertical displacement `+/-0.002 mm`, smooth-step ramp
  over 20 microseconds followed by a hold to 100 microseconds.
- Dynamics: central difference, CFL safety factor 0.8, float64 solver state.
- Environment: macOS 27.0 ARM64; Python 3.10.18; PyTorch 2.8.0;
  `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`; CPU.
- Initial damage: no prescribed damage seed; the crack starts from a geometric
  notch. Threshold extents below exclude the initial 20 mm notch.

## Diagnostic 1: current public YAML

Command: `python -m phast run examples/dynamic/B3_dynamic_sent/config.yaml
--device cpu --output_dir <scratch>/b3_cpu`.
The source YAML and all physical parameters were unchanged.

The current geometry DSL produced 930 nodes and 1,618 T3 elements, with
`h_min = 0.004142136 mm`. Its CFL step was `8.698485e-10 s`, requiring
114,963 steps for the requested 100 microseconds. The process reached the
240-second hard cap and was terminated (whole process 240.031 s, exit -9).
The last complete saved snapshot was step 104,800 at 91.160 microseconds.

The stored damage remained finite and nondecreasing, but its spatial field
remained concentrated around the notch tip. At the last snapshot the forward
extent was 3.127 mm for `d >= 0.5`, and 0.663 mm for both `d >= 0.9` and
`d >= 0.95`. These are partial-run results.

Important reproducibility findings:

1. The checked-in mesh and retained metadata instead describe 1,091 nodes,
   1,940 elements and `h_min = 0.077870592 mm`.
2. In the forward ligament strip `x > 20 mm`, `|y-20 mm| <= 1 mm`, the median
   maximum triangle-edge length is approximately 2.000 mm for the generated
   mesh and 0.420 mm for the retained mesh. A tiny minimum element size alone
   does not describe resolution along the propagation path.
3. Current YAML/lockfile residual stiffness is `1e-7`; retained result metadata
   records `1e-6`.
4. The default `damage_every=3` triggers the runner's subcycling warning
   against its estimated bound of 2.
5. Retained `history.csv` contains its header only. Energy and crack-tip CSV
   contain data; teaching should select the actual available histories.

The changed mesh is consistent with the increased step count and reduced
propagation. Several settings differ from the retained run, so this review
does not isolate a unique cause for every difference in its field.

## Diagnostic 2: imported retained mesh

This second run used the supported `geometry.mesh_path` entry in a scratch
configuration. Physical dimensions, material values, supports, displacement
amplitude, ramp duration and total time were preserved. Explicit differences
from current B3 YAML were:

| Setting | Current public B3 YAML | Imported-mesh diagnostic |
| --- | --- | --- |
| Geometry | Compile inline DSL | Import checked-in `mesh.msh` |
| Residual stiffness | `1e-7` | `1e-6`, matching retained metadata |
| Damage cadence | Default `damage_every=3` | Explicit `damage_every=1` |
| Device/precision | Automatic device/default double precision | CPU/float64 |
| Plane strain/compilation | Default settings | Explicit `plane_stress=false`, `compile=false` |

The conservative cadence performs one damage update per explicit step and
satisfies the runner's subcycling estimate.

The run completed with exit 0: **17.6787 s solver subprocess**, including importing
the package, loading the mesh and writing result files; the solver's internal
timing is 15.76 s. Raw-field extraction and the five-panel diagnostic figure
completed in a separate measured command of 0.573 s. Installation and a whole
teaching notebook were outside this timing. There was no authenticated Colab run.

The imported mesh SHA256 exactly matches the public mesh. All 6,116 steps
completed, with `dt = 1.635282424e-8 s`. The final solver step is 6,115;
the final saved field is step 6,100 because snapshots are written every 20
steps. All 306 saved damage fields are finite and nondecreasing. The stored
trajectory damage precision is float32, while the solver uses float64.

The inspected field panels show initiation near the geometric notch, forward
growth, and a connected horizontal high-damage band to the opposite edge.
For the strip `x > 20 mm`, `|y-20 mm| <= 1 mm`, the table reports the maximum
qualifying nodal x-coordinate minus 20 mm. This is a threshold-dependent
extent diagnostic, with nodal resolution; it is not an independently
converged crack-length measurement.

| Saved time [microseconds] | Extension at `d >= 0.5` [mm] | At `d >= 0.9` [mm] | At `d >= 0.95` [mm] |
| --- | ---: | ---: | ---: |
| 0.000 | 0.000 | 0.000 | 0.000 |
| 15.045 | 1.024 | 0.148 | 0.148 |
| 19.950 | 6.192 | 5.128 | 5.128 |
| 30.089 | 18.929 | 17.599 | 17.337 |
| 99.752 | 20.000 | 20.000 | 20.000 |

### Numerical acceptance still needed

The 6,116 telemetry rows record 3–29 phase-field PCG iterations per step;
none reaches the requested 5,000-iteration limit. The generic explicit-route
residual columns are all NaN and omit a dedicated damage convergence flag.
The solver also emits its existing warning that the inner adjoint/active-set
PCG hard cap is 1,000. That warning concerns an alternate inner path; the
present forward iteration counts stay below it. Iteration counts and exit 0
alone do not certify the constrained damage residual.

Before promoting this candidate, retain final linear/projected damage
residuals and per-update convergence outcomes, inspect energy evolution,
and compare mesh/time-step resolution and damage cadence. The forward-ligament
maximum-edge range of the retained mesh is 0.148–1.233 mm for `l0=0.5 mm`,
so the existing qualitative resolution scope remains relevant. No statement
of mesh convergence, benchmark-level crack speed or fracture-path gradient
validation follows from this fast run.

### Portable reproduction recipe

From a checkout of the pinned public PhAST revision, copy
`examples/dynamic/B3_dynamic_sent/config.yaml` into a new scratch directory.
Replace its entire `geometry` block with:

```yaml
geometry:
  units: mm
  mesh_path: mesh.msh
```

Place a byte-identical copy of
`examples/dynamic/B3_dynamic_sent/mesh.msh` beside that scratch YAML. Apply the
settings in the table above, including `material.eta_residual: 1e-6`,
`solver.damage_every: 1` and explicit CPU selection. Keep the original
material, supports, ramp, time horizon and output cadence. Run the same
public CLI from that checkout:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python -m phast run \
  runs/b3_classroom_input/config.yaml --device cpu \
  --output_dir runs/b3_classroom_result
```

The two paths are suggested scratch locations. Resolve `mesh_path` relative
to the copied YAML and verify the mesh SHA256 below before running. This
relative-path recipe describes the tested input changes; the actual diagnostic
used absolute resolved scratch paths recorded in its receipt. A production
classroom configuration remains subject to the acceptance checks above.

## Precise next implementation action

The release/documentation task should define a public, immutable **B3 classroom
configuration** beside the canonical example, beginning with the checked mesh
and all settings above. Review its residual/cadence/resolution evidence before
assigning it a tutorial-ready execution status. The course then consumes that
same configuration and public setup/result interfaces, with a pinned source
revision and a pre-generated mesh fallback. Avoid maintaining a second
independent geometry/material/loading definition in the course.

Teaching cells can follow: import/create geometry → inspect mesh and named
boundaries → inspect supports and loading → run → plot field snapshots and
energy → interpret → change one parameter. Keep the current tested course
calculation until this new route has a complete notebook/runtime receipt,
worked exercise, downloadable variants and visual review.

## Local diagnostic artifacts and source hashes

Ignored scratch directory: `.build/propagation-review/`. It contains
`run_bounded.py`, `analyse_b3.py`, `b3_imported.yaml`, both `*_receipt.json`,
both `*_field_review.json`, both `*_diagnostic_fields.png`, logs and raw
trajectory directories. The timeout trajectory is about 1.1 GB and the
completed candidate is about 78 MB; these are local evidence, excluded from
the public package. The field-review JSON records hashes of the relevant
configuration resolver, geometry compiler, runner and solver source files.

| Artifact | SHA256 |
| --- | --- |
| Public B3 `config.yaml` | `abebef68a514c58a9fcf9bdb71cd2ec9fa7467930ac6137eabdd2926be39411c` |
| Public B3 `mesh.msh` | `59c3a41dff41a03fdef93bdd91f974e2d1a263a01aaa96094c125b08cb5e14be` |
| Scratch imported-mesh configuration | `03755468fe97819e3f882e858c2eabd4e37083564d5e194c90385614795d3899` |
| Generated diagnostic-1 mesh | `e7ad9f0e05ace45a19a3922087f35d0d33b70820959dd5acc92739df7577fc5c` |

After both runs, `git diff --quiet -- examples src configs` passed in the
upstream checkout. The public B3 configuration, mesh, metadata and final
image also matched their HEAD bytes. The initial documentation changes were
preserved, and there were no solver edits, notebook replacements, commits or
pushes from this review.
