# Practical 1: connected geometry-to-results workflow

Date: 10 September 2026. Workstream: [C04 / issue #5](https://github.com/CEMS-Lab/autumn-school/issues/5), with the [issue #18 design directives](https://github.com/CEMS-Lab/autumn-school/issues/18). Authoring base: `077d43d87c55b4fdea720808fc24f040e957e1ea`; this record describes local changes on that base.

## Delivered teaching sequence

The revised [operational notebook](../notebooks/01_phast_tiny_evolving_fracture.ipynb) uses one configuration throughout: geometry → generated arrays → saved/imported tensor mesh → actual `FEMMesh` → actual boundary conditions/material → actual `StaggeredSolver` → checked load loop → portable results → reopened fields/response → one controlled input change. Object-identity assertions connect the displayed setup to the executed solver.

The geometry, symmetric loading and initial damage are shown before solving. The first mesh import constructs the mesh used in both calculations. The notch consists of 26 centreline nodes with locked damage `d=1`; the nominal threshold `x<=0.8` selects a last grid coordinate of `0.78125`. The original `4×2` rectangle, 8,385 nodes, 16,384 T3 elements, material values and reference load schedule are preserved. Horizontal displacement remains constrained on all four exterior edges; vertical displacement is prescribed symmetrically on top and bottom.

The configuration file and vendored public solver are unchanged. The older `run_notched_tension` helper and all inverse/learning helper calculations are also unchanged. The new forward-only load loop lives in [forward_workflow.py](../notebooks/day2_helpers/forward_workflow.py). The narrow authoring generator is [build_forward_practical.py](../source/notebooks/build_forward_practical.py), which inlines the shared Colab setup template and preserves forward-specific imports. Rebuilding the older multi-notebook generator must retain this new Practical 1 source.

## Portable result contract

`phast-course-forward-v1` consists of numeric NPZ arrays and a JSON companion. Arrays include coordinates, connectivity, four boundary node sets, initial/first/final/incremental damage, final displacement with shape `(8385,2)`, and damage/displacement snapshots identified by steps `[0,1,30,60]`. The JSON contains the complete configuration and its hash, public-source verification, dimensionless conventions, the actual material's `plane_stress` flag and resolved kinematics, the actual relative-L2 stagger settings, environment, all 60 scalar trace rows, checks and an archive hash.

The notebook reopens both calculation archives with `allow_pickle=False`, validates schema/shapes/hashes/finite values, and checks equality against every saved array. All four boundary arrays are required and checked for one-dimensional integer, nonempty, unique, in-range indices. Snapshot IDs must strictly increase from zero through step one to the final load step; initial, first and final damage snapshots and the final displacement snapshot must equal their named arrays. Direct ordering comparisons also cover unsigned integer IDs. All result figures use reopened arrays and metadata. These files support portable post-processing; complete simulation restart additionally needs the internal solver/history state.

The second complete 60-step calculation changes only `loading.total_symmetric_vertical_displacement` from `0.04` to `0.02`. It uses a fresh solver state on the same imported mesh. The final nodal damage sum outside the locked precrack decreases from `1213.4936485` to `519.6831787`, agreeing with the exercise's qualitative prediction. The full fields and reaction–separation curves are shown together. This nodal sum is a mesh-dependent diagnostic.

## Execution and checks

Commands, run from the repository root in an already provisioned Python environment:

```bash
python source/notebooks/build_forward_practical.py
python scripts/run_course.py --notebook 1
python scripts/check_forward_practical.py
python -m py_compile notebooks/day2_helpers/forward_workflow.py source/notebooks/build_forward_practical.py scripts/check_forward_practical.py
```

The interpreter was Python 3.10.18 from the local scientific environment. Platform: macOS 27.0, arm64, CPU float64, four PyTorch threads; PyTorch 2.8.0, NumPy 2.2.6, SciPy 1.14.1, Matplotlib 3.10.8. The final source was executed from a fresh notebook kernel by the bounded runner.

| Measurement | Final measured time |
| --- | ---: |
| Complete notebook subprocess, including kernel/import overhead and both full calculations | **91.9964 s** |
| Notebook computation timer after shared environment/plot setup, including preparation, two solves, checks, saving/reopening and plotting | 88.2160 s |
| Reference 60-step solve | 60.0903 s |
| Half-separation 60-step solve | 25.2908 s |

Setup used an existing local environment; no installation timing was measured. The process-level 300 s requirement passed. Earlier complete rehearsals took 90.8087 s, 91.6270 s and 88.4413 s. The final execution above includes the corrected geometry-legend position, explicit resolved model/convergence metadata, robust boundary/snapshot validation and stable notebook-source provenance.

Both calculations retain strict mechanics and staggered nonconvergence flags. Every step checks finite displacement/damage, damage bounds and irreversibility within `1e-10`, the locked precrack, actual prescribed boundary values, and the configured staggered tolerance. The saved `stagger_residual` is the maximum of the displacement and damage relative L2 iterate changes, each divided by its current-iterate L2 norm plus `1e-30`. It describes stabilization of successive coupled iterates; it is distinct from a force-balance or PDE residual norm. The actual settings are recorded as `stagger_criterion="relative"`, `stagger_norm="l2"` and tolerance `1e-5`, with adaptive tolerance disabled. Both returned zero warnings, maximum boundary error zero and minimum damage increment zero. Positive damage increment assertions for the reference case passed. The final reference increment sum and maximum remain approximately `967.4594748` and `0.3350812850`, matching the retained reference case.

The independent result-contract check validates both 60-step archives, exact snapshot IDs, mesh/precrack counts, resolved plane-strain state and convergence settings, source hashes and the single-input-change comparison. It checks 24 malformed cases per archive, including altered configuration, displacement shape, missing or invalid boundary indices, invalid/unsorted snapshot IDs (including unsigned integers), and inconsistent endpoint fields. Array mutations are tested with matching archive checksums so structural checks are exercised independently of hash rejection. A stable notebook fingerprint hashes only cell types and source text; retained outputs/execution metadata leave that fingerprint unchanged, and a source edit changes it. The raw authored notebook hash is also retained as provenance. The final result-contract check passed all 48 malformed-file cases and the stable-source tests; syntax compilation passed.

The notebook-cell receipt is [tiny_notched_tension_notebook_receipt.json](../assets/day2_forward/tiny_notched_tension_notebook_receipt.json). The bounded runner also wrote `runs/01_phast_tiny_evolving_fracture/runtime.json` and the executed notebook in the same run directory. The integration lead should retain that executed notebook under the standard `notebooks/executed/` route before regenerating lesson/download copies.

Final source hashes (the raw notebook hash records the authoring artifact at execution; the stable cell-source hash validates both authored and retained-output copies):

| Source | SHA-256 |
| --- | --- |
| Operational notebook 01, raw authored file | `1e15c38391713a4c27ce2bf5ad10fea50f5d1973f43576a6f5e89862ca420732` |
| Operational notebook 01, stable cell types/source | `ceb102d2b2b48770403edfe40444a7f9f9dd3b57c0d28d48ffd716b7ac9f7571` |
| `notebooks/day2_helpers/forward_workflow.py` | `c60efa3d98ea2a830c860262be1df56581d29ca10fe9c329b5eee39631d68437` |
| Unchanged reference configuration | `31f808405a43c6d9aa88b54041ca8b51fde8f6991c3c149a3d03d23473627aa2` |

## Visual inspection

All seven complete figures were rendered and visually inspected: geometry/loading; actual mesh with initial notch; final displacement and a labelled 5× deformed outline; initial/first/final damage; damage increment; reaction/damage/iteration traces; and half/full-separation comparison. The geometry legend was moved away from the top displacement label and the corrected full figure was inspected again. Axes, mathematical subscripts, dimensionless conventions and colourbars are readable. The damage comparison uses one common `[0,1]` colour range. The displacement map uses a symmetric colour range; the deformation magnification is explicitly stated. The reaction comparison uses distinct line styles.

## Scientific scope and remaining gates

This is an actual pinned public PhAST AT2 calculation, with isotropic degradation, the material's plane-strain default, quasistatic sparse-direct mechanics, history-based damage and the retained restrictive exterior lateral constraints. The fields illustrate diffuse damage evolution. The reaction increases throughout the selected loading range. This evidence does not establish a sharp propagating or branching crack, peak-load softening, mesh convergence, matrix-free performance, dynamic time integration or a fracture-path derivative.

Issue #5 remains open for an external-mesh/physical-group route and a separately checked short propagating-crack example. Prepared NPZ mesh import is complete. Fresh Colab installation/execution and slower-laptop timing remain open in issue #10; the shared bootstrap is implemented but this receipt is local. Book/download regeneration, rendered cross-format checks and publication are integration tasks. No commit, push, issue closure or publication was performed by this bounded forward-practical assignment.
