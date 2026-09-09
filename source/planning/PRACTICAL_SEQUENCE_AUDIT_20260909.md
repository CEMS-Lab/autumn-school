# Practical 1 sequence audit and repair plan

Date: 9 September 2026. Workstream: [C04 / issue #5](https://github.com/CEMS-Lab/autumn-school/issues/5), open when checked. This is a source and retained-evidence audit, with a proposed repair sequence. It does not implement a notebook change or record a new calculation, installation, Colab rehearsal or publication.

The current practical runs an actual public PhAST calculation, but its visible preparation objects do not feed that calculation. The main repair is to connect the displayed geometry, mesh, constraints and material to the solver, then teach saving, reopening and plotting the resulting fields. The retained calculation can support the practical once this sequence is made explicit and checked.

## Verified current state

The inspected worktree is `course/mvp-delivery`, with HEAD `6444831e56b2faaba0aa72f9fa832764c2f60caf` and existing local changes. The operational source is [notebook 01](../../notebooks/01_phast_tiny_evolving_fracture.ipynb); cell numbers below are zero-based JSON cell indices. Study, solution and book copies are generated delivery surfaces, not additional operational sources to patch independently.

Notebook cell 4 creates `mesh_preview`, `bcs_preview` and `material_preview`, saves a prepared tensor mesh, reloads its arrays, and checks connectivity equality. Cell 6 calls `run_notched_tension(config)`. That helper accepts configuration and artifact options, rebuilds nodes, connectivity, mesh, constraints and material internally, and constructs its own solver. It has no input for any preview object. Editing a preview object therefore does not change the solve. Reloaded prepared-mesh arrays are also not used to construct the mesh passed to the solver. This is a visible-setup/actual-execution gap, even though both paths currently use matching configuration values. Evidence: notebook cells 4 and 6; [helper](../../notebooks/day2_helpers/course_tools.py), lines 218-298.

The selected routine is public PhAST `StaggeredSolver.step_full()` using `solver_type="quasi_static"`, mechanics `backend="scipy"`, AT2 and the `isotropic` energy split, CPU float64. It uses assembled sparse-direct mechanics and staggered mechanics/history/damage updates. Sixty load increments do not constitute physical-time dynamics. This exercise provides evidence of diffuse damage evolution outside an initially locked precrack; it does not establish a sharp propagating/branching crack, matrix-free mechanics performance or a full fracture derivative. Evidence: [configuration](../../configs/day2_forward/tiny_notched_tension.json), lines 22-50; helper lines 276-322; [public staggered solver](../../vendor/PhAST/src/phast/solvers/staggered_solver.py), lines 614-629 and 1165 onward.

## Stage-by-stage teaching sequence

| Stage | What exists now | Minimum repair or explicit teaching outcome |
| --- | --- | --- |
| Install and verify | [SETUP](../../SETUP.md) describes local and Colab preparation. Notebook cells 1-2 locate the course, load configuration and verify the public source pin. | Present setup as a separate stage. Print environment, imported source and revision; retain the complete bundle. Measure fresh installation separately from computation. |
| Geometry | A rectangle of width 4 and height 2 is built from configuration. No geometric notch is removed. | Plot the outline with dimensions and loading direction before meshing. State the coordinate/unit convention; do not invent physical units absent from the case. |
| Mesh | A 128 by 64 structured grid is split into T3 elements: 8,385 nodes and 16,384 elements. Preview arrays are saved/reopened, but the solve regenerates its own mesh. | Construct one actual `FEMMesh`, show its edges and node labels, and use that same mesh in the solve. If demonstrating reload, reconstruct that actual mesh from the reopened arrays. Call this a prepared tensor-mesh route; external meshes with physical groups remain separate work. |
| Initial notch | Centreline nodes with `y=1` and `x<=0.8` receive phase-field Dirichlet `d=1`; the solver damage state is seeded to 1 there. Connectivity is unchanged. | Show and label the nodal damaged set before loading. Explain that this is a locked initial damage condition, not a geometric cut or disconnected crack-face mesh. |
| Boundary conditions | `symmetric_tension_bcs` fixes `u_x=0` on all four exterior edges and applies symmetric top/bottom `u_y`. Phase-field constraints lock the precrack. | Display the actual constrained node sets and components. State the lateral restraint explicitly: the public helper comments that it is more restrictive than the standard Miehe setup. Preserve it for the existing reference case; a physical BC change needs a new result. |
| Load ramp | Helper creates 60 factors from 0.0125 to 1.0 and assigns `bcs.load_factor` before each `step_full()`. Total prescribed separation is 0.04. | Show the actual load array and top/bottom values: `u_y(top)=+0.02*lambda`, `u_y(bottom)=-0.02*lambda`. Label the horizontal axis load factor or load increment, with physical time absent. |
| Actual solver | Hidden helper rebuilds all inputs and loops through the load factors. Strict mechanics and stagger nonconvergence flags are enabled. | Expose solver construction from the preceding objects and a short readable load loop, or pass those constructed objects into a thin course helper. Preserve the public source pin and existing failure settings. |
| Results schema | The in-memory result contains mesh/solver objects, damage snapshots and traces. NPZ saves coordinates, connectivity, precrack and damage arrays. JSON saves source metadata, summary and 60 scalar trace rows. | Define a portable schema for numerical arrays plus a JSON case/receipt record. Add final displacement, explicit units/conventions, configuration and schema version. Document step IDs for every saved snapshot. |
| Save and reload | Only the prepared mesh is reopened. Postprocessing reads the in-memory `result`; the saved solution is not reopened. | Save, close and reopen NPZ/JSON, validate keys/shapes/metadata, then use only reopened data for the classroom postprocessing stage. This is result portability, not a solver restart checkpoint. |
| Postprocess | Notebook cells 8-9 plot seeded/first/final damage, incremental damage, top internal-force sum, outside-precrack damage sum and stagger iterations. | Add geometry/BC and displacement/deformation views with a stated deformation scale. Reproduce damage and response views from saved data with visible boundaries, colourbars and load labels. Explain the observable and its limitations. |

Stage evidence: notebook cells 0-10; helper lines 250-340 and 345-398; [boundary-condition implementation](../../vendor/PhAST/src/phast/physics/boundary_conditions.py), lines 635-659. The required displacement/deformation view already appears in the [book lesson](../book/04_fem_to_tensors.md), lines 166-174, but is absent from notebook 01's current plotted sequence.

## One authoritative object chain

The proposed operational notebook should implement this dependency chain:

```text
verified public source + one case configuration
  -> geometry and nodal coordinates/connectivity
  -> actual FEMMesh + named boundary/precrack sets
  -> actual boundary conditions + material + load factors
  -> StaggeredSolver using those same objects
  -> step_full() load loop + numerical checks
  -> copied displacement/damage arrays + scalar traces + case metadata
  -> saved NPZ/JSON
  -> reopened NPZ/JSON + schema/equality checks
  -> geometry, displacement, damage and response figures
```

If mesh import is the chosen classroom path, the chain passes through `save mesh -> reopen arrays -> construct actual FEMMesh` before constraints are attached. Do not retain an independent preview path that students can modify without affecting the solver. A geometry or mesh change requires rebuilding downstream objects; changing a title or figure must not silently alter case inputs.

The lecture bridge should name the route students will execute: the lecture can explain matrix-free actions and explicit mechanics, while this retained practical solves quasistatic mechanics with a sparse-direct backend. A dynamic or matrix-free replacement is a distinct numerical deliverable with its own acceptance evidence.

## Current saved contract and required additions

Direct inspection of `tiny_notched_tension_fields.npz` confirms exactly these seven arrays: `nodes`, `elements`, `precrack`, `seeded_damage`, `first_damage`, `final_damage`, `incremental_damage`. Displacement is available through the live `result["solver"].u`, but the NPZ contains no `u` or other displacement field. Scalar `max_displacement` in the JSON trace cannot reconstruct the spatial displacement field.

The saved summary JSON has 60 trace rows with `step`, `load_factor`, `reaction_top_y`, `damage_outside_sum`, `damage_outside_max`, `max_displacement`, `stagger_iterations`, `stagger_residual` and `step_seconds`. It includes PhAST revision metadata, but lacks the full case configuration, units/conventions and a result-schema version. The live `result` includes configuration; the JSON writer saves only summary, PhAST information and trace. Evidence: helper lines 345-398 and direct archive/JSON-key inspection.

The minimum proposed portable contract is:

- NPZ: retain the seven arrays and add `final_displacement` with shape `(N_nodes, 2)`. Save selected displacement snapshots only if the lesson plots them; pair all snapshots with explicit load-step identifiers. Document coordinate `(N_nodes, 2)`, connectivity `(N_elements, 3)` and nodal scalar `(N_nodes,)` ordering.
- JSON: schema version; full case configuration; public revision and verification route; units or an explicit dimensionless convention; damage convention; BC components and selected sets; load factors; trace definitions; environment; source/configuration hashes; setup and complete-notebook timings; warnings and checks. Preserve the current summary quantities.
- Reload: use numeric arrays without pickled solver objects, check finite values and expected shapes, and verify reopened displacement/damage/connectivity against the values written. A portable results archive need not contain all internal state required for restarting the nonlinear solver; do not label it a restart checkpoint.

The top response is a sum of internal-force components at prescribed top nodes. It is a diagnostic with the case's units/conventions, not a calibrated experimental force. The nodal sum of damage outside the precrack is mesh dependent; it is neither integrated fracture energy nor physical crack length.

## Retained timing evidence and its boundary

| Evidence | Reported result | What it supports |
| --- | --- | --- |
| [Original notebook receipt](../../evidence/notebook_runtime.json), lines 11-20 and 31-68 | 76.301 s whole notebook; 70.07502 s solve; Apple M4 Pro, macOS, Python 3.10.18, PyTorch 2.8.0; no recorded warnings | The retained notebook completed in the recorded, already provisioned local environment and passed the stated evolving-damage checks. |
| [Packaged rehearsal](../../evidence/package_rehearsal.json), lines 1-7 | 88.351077 s, exit code 0, assembled course directory with `PHAST_PUBLIC_SRC` unset | A second local execution from the packaged directory; not an independent fresh-installation or Colab measurement. |
| [Setup limits](../../SETUP.md), lines 25-28 and 57-77 | Fresh installation across supported systems and fresh Colab rehearsal remain open | No measured classroom/Colab promise follows from the local timings. |

These receipts were read, not rerun during this audit. They belong to the recorded notebook and cannot certify a repaired implementation. The selected evidence reports a maximum positive damage increment outside the locked set of about 0.3351, and a nodal increment sum of about 967.4595. Existing assertions and enabled failure flags are useful bounded checks; they are not a mesh-convergence study or fresh verification of the physical case.

## Minimum repair acceptance checks

1. Execute the revised operational notebook from a fresh kernel, top to bottom. Confirm that the mesh/material/BC objects visibly built in the notebook are the ones held by the solver, and that the displayed load schedule is the schedule executed. Any prepared-mesh import must feed this same chain. Confirm this connection directly before solving.
2. Confirm the unchanged reference case: 8,385 nodes, 16,384 T3 elements, valid indices and finite arrays; explicit exterior component constraints; locked `d=1` nodes on the stated centreline; 60 increasing load factors with the stated endpoint displacements. Verify the actual constrained values at the first and final load factors. Do not silently change the restrictive lateral restraint.
3. Preserve source verification and nonconvergence flags, and inspect the relevant returned mechanics/stagger diagnostics. Retain the existing positive-damage-increment and warning checks; check damage bounds and irreversibility at recorded steps with a stated tolerance. A failed check remains visible evidence and must not be relaxed simply to obtain a plot.
4. Verify the saved schema, array shapes and reload equality, including displacement. Generate geometry/BC, displacement/deformation, full damage and scalar-response views from reopened results. Inspect complete rendered figures; document colour ranges, load labels and deformation scale.
5. Record a new complete-notebook receipt, including imports, case preparation, solving, assertions, saving, reopening and plotting. Record installation separately, plus environment and revised notebook/helper/configuration hashes. Use the existing bounded runner, `python scripts/run_course.py --notebook 1`, and require completion below 300 seconds after setup. Its runtime JSON should be accompanied by the richer case/check receipt above. Preserve previous receipts under their original provenance.
6. Regenerate study/solution/book notebook copies through the documented course build workflow, then check code/output parity, plots, links and stated scope. Before making a Colab claim, separately rehearse the full bundle and installation in a fresh Colab runtime and save that receipt. Until then, retain the executed HTML/figures as the classroom fallback and keep the portability gate open.

The next implementation assignment should own notebook 01, its course helper/configuration as needed, and the adjacent source lesson, with generated copies rebuilt afterwards. This audit owns only this planning file; no operational notebook, vendored solver or published artifact was changed for it. A short sharp-crack example and an external mesh with physical groups remain separate C04 acceptance work.

## Reference slide review for the lecture/practical handoff

Rendered and visually inspected PDF pages 3-5 in each supplied reference, rather than relying on extracted text. Both are 16:9 presentations. These observations guide original slide design; source images were not copied into the course.

| Reference and pages | Observed pattern | Application to the PhAST continuation |
| --- | --- | --- |
| Rackauckas, `DifferentiableSimulation_TheRealBits_Rackauckas.pdf`, p. 3 | One large section question, generous empty space and a simple frame | Use a short transition question before the practical; keep detailed setup instructions in the notebook. |
| Rackauckas, p. 4 | One large equation-to-model graphic beneath a fixed title band | Show one principal dependency or operation per slide, with a clear reading direction and large labels. |
| Rackauckas, p. 5 | A dense multipanel result combines traces and a modelling workflow | Split a comparable PhAST result into successive views or use progressive reveals; do not shrink a complete paper figure to fill a teaching slide. |
| Hesthaven, `Hesthaven_CWIWorkshop2023.pdf`, p. 3 | Left-aligned title/prose, one relation, a central explanatory sketch and a closing question | Couple the actual specimen/mesh image with one question about its constraints or output. Reserve a stable title margin and generous space around the image. |
| Hesthaven, pp. 4-5 | Equations occupy distinct vertical bands; red labels/arrows attach directly to individual terms | Introduce a dependency or derivative in stages. Label the term being discussed beside the term, with a restrained accent colour; move dense derivation steps to later slides or notes. |

For the continuation, use the existing deck's typography and colours while adopting these spacing patterns: stable title/content margins, one principal relation or field per slide, direct annotations and deliberate vertical spacing. Use successive slides/reveals for setup, solve and interpretation; the complete end-to-end sequence belongs in the practical notebook.
