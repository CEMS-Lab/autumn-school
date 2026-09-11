# Lecture and example placeholder register

These 21 content slots are textual outlines in the three lecture guides and
the three classroom notebooks.
Every slot below is **open: content preparation and acceptance pending**.
Existing reuse sources are starting points; they do not establish completion
of the proposed animation, result exhibit or worked-example adaptation.

The placements below retain their original lecture-storyboard IDs. The new
32-slide [Keynote storyboard](../slides/curated-keynote/storyboard.json) maps
each slot through its `placeholder_ids` field to the current S01–S32 slides.
The [delivery map](../../output/curated-keynote-20260910/slide_map.json) records
that mapping. All 21 slots retain their acceptance checks. Earlier editable
decks and media remain preserved.
Owner labels are workstream roles; the course integration lead coordinates
assignments. Reuse paths below are relative to the repository root.

The 11 September [90-slide authoring storyboard](../slides/course-blueprint-20260911/STORYBOARD.md)
adds a finer-grained teaching sequence. Its `slots` fields map all 21 entries
without closing them. The 32-slide source and this register remain preserved;
the [four-deliverable plan](FOUR_PILLAR_DELIVERY_20260911.md) coordinates final
visuals, practicals, publication and teaching acceptance.

## L1-A01 · Diffuse crack representation

- **Placement:** lecture 1, “From a crack to a damage field”; slide storyboard `L1-S02`.
- **Learning question:** Which quantity changes when the diffuse band widens?
- **Content:** specimen, damage band and idealised line-profile reveal; change $\ell$ while keeping the damage convention fixed.
- **Reuse source:** `source/book/01_crack_representations.md`, `source/book/02_phase_field_energy.md`, `source/book/figures/02_energy_profiles.png`.
- **Owner:** course integration lead, with fundamentals review.
- **Acceptance:** label schematic versus numerical fields; define $d$ and $\ell$; preserve AT1/AT2 normalisation; provide static frames, alternative text and readable controls; review the rendered asset.

## L1-W01 · Energy, degradation and length scale

- **Placement:** lecture 1, “Energy and stiffness degradation”; slide storyboard `L1-S04`.
- **Learning question:** How do fracture energy, degradation and band width enter the model?
- **Content:** three points on the existing degradation curve, followed by a qualitative $G_c$/$\ell$ comparison and mesh-resolution discussion.
- **Reuse source:** `source/book/02_phase_field_energy.md`, `notebooks/02_degradation_autograd.ipynb`.
- **Owner:** course integration lead, with fundamentals review.
- **Acceptance:** retain residual-stiffness convention; define units and fixed quantities; check any displayed arithmetic independently; distinguish profile reasoning from a computed propagation result; include an interpretable worked answer.

## L1-A02 · One staggered increment

- **Placement:** lecture 1, “One numerical increment”; slide storyboard `L1-S06`.
- **Learning question:** Which loop repeats at fixed load and which step advances loading?
- **Content:** animate mechanics, driving field, constrained damage, convergence and final increment acceptance; retain the previous accepted damage as history reference.
- **Reuse source:** `source/book/03_staggered_solution.md`, `source/book/figures/03_staggered_loop.svg`.
- **Owner:** course integration lead, with numerical-method review.
- **Acceptance:** inner loop returns to mechanics at the same load; load advancement follows acceptance; describe the actual history/constraint convention; keep controls and static frame sequence readable.

## L1-W02 · A triangle, an operator and a dynamic state

- **Placement:** lecture 1, “Tensors, matrix-free actions and dynamics”; slide storyboard `L1-S08`.
- **Learning question:** Which arrays represent geometry, fields and physical-time evolution?
- **Content:** one-element gather, strain and residual example; matrix-free action on a vector; an additional state row for velocity and acceleration.
- **Reuse source:** `source/book/04_fem_to_tensors.md`, `source/book/figures/04_fem_pipeline.svg`.
- **Owner:** course integration lead, with numerical-method review.
- **Acceptance:** define shapes and local/global ordering; check the element arithmetic; distinguish physical time, load increment and nonlinear iteration; retain the assembled quasistatic description of the selected practical; make no unmeasured speed claim.

## L2-A01 · Forward states and reverse sensitivity

- **Placement:** lecture 2, “Follow the sensitivity backwards”; slide storyboard `L2-S03`.
- **Learning question:** Why does an early update contribute to the final loss gradient?
- **Content:** reveal three forward updates, observation and loss; trace VJPs backwards; accumulate shared-parameter contributions; show the optimisation step last.
- **Reuse source:** `source/book/05a_backpropagation_step_by_step.md`, `source/book/figures/05a_backpropagation.svg`.
- **Owner:** course integration lead, with differentiation review.
- **Acceptance:** keep states, loss, cotangents and parameter gradient distinct; include all dependencies present in the chosen graph; match the checked algebraic example; label scope; supply static frames and inspect playback.

## L2-W01 · Derivative evidence and derivative scope

- **Placement:** lecture 2, “Specify the derivative being computed”; slide storyboard `L2-S05`.
- **Learning question:** What evidence supports the gradient of the selected computational map?
- **Content:** analytical/autograd/finite-difference comparison in the elastic bar; adjacent fixed-iteration and converged-residual graph outlines.
- **Reuse source:** `source/book/05_differentiation_and_inverse.md`, `notebooks/03_tiny_derivative_inverse_toy.ipynb`.
- **Owner:** course integration lead, with differentiation review.
- **Acceptance:** state the elastic-bar scope; define parameter, observable and loss; inspect a finite-difference step-size range; identify unrolling and implicit assumptions; preserve constraint/history caveats for the fracture transfer; verify any new calculation.

## L2-R01 · Fracture-energy recovery

- **Placement:** lecture 2, first inverse exhibit; slide storyboard `L2-S07`.
- **Learning question:** Which feature of the observation contains information about $G_c$?
- **Content:** textual positions for target/initial/recovered observation, parameter trajectory, derivative comparison and one physical interpretation.
- **Reuse source:** `source/book/05_differentiation_and_inverse.md` for the workflow; approved public fracture-recovery source and numerical receipt to be supplied under issue #7.
- **Owner:** inverse-extension contributor supplies evidence; course integration lead places the reviewed exhibit.
- **Acceptance:** fix the source/configuration; define synthetic or measured target, observation operator and derivative convention; provide initial/recovered fields and scalar response, gradient check, full timing and limitations; establish sharing authority; retain textual outline until reviewed data exists.

## L2-R02 · Single-particle recovery

- **Placement:** lecture 2, second inverse exhibit; slide storyboard `L2-S08`.
- **Learning question:** Can the selected observations distinguish the chosen inclusion parameters?
- **Content:** target/initial/recovered inclusion and field panels with common scales; explicit unknown geometry/material parameters and observation definition.
- **Reuse source:** approved contributor material under issue #7; `source/book/research/01_geometry.md` and `source/book/research/04_recovery.md` are candidate reading references subject to scope review.
- **Owner:** inverse-extension contributor supplies evidence; course integration lead integrates it.
- **Acceptance:** identify geometry parameterisation and derivative scope, source version, fixed loading/mesh assumptions and starting point; inspect full fields and observation agreement; provide numerical and provenance checks for this example; import no private paper or result without approval.

## L2-R03 · Multiple-particle recovery

- **Placement:** lecture 2, third inverse exhibit; slide storyboard `L2-S09`.
- **Learning question:** How does the number of unknowns change the information needed for recovery?
- **Content:** textual geometry/field comparisons, parameter-correlation explanation, selected initialisations and observations held out from fitting.
- **Reuse source:** approved public contributor material under issue #7; source selection pending.
- **Owner:** inverse-extension contributor supplies evidence; course integration lead integrates it.
- **Acceptance:** define every unknown and observation; retain starting-point and ambiguity information; report whether held-out evidence exists; provide checked fields and retained receipts; tie each statement to the actual selected experiment and keep broader generalisation claims bounded.

## L2-R04 · Non-particle inverse application

- **Placement:** lecture 2, fourth inverse exhibit; slide storyboard `L2-S10`.
- **Learning question:** Which parts of the inverse workflow transfer to another physical setting?
- **Content:** application description, parameter/state/observation/loss map, and textual result-panel outline after selection.
- **Reuse source:** voice-memo request only; the term recognised as “DAC” at 01:32–01:38 and 02:14–02:20 is unresolved. No expansion or application identity is assigned.
- **Owner:** inverse-extension contributor and maintainer confirm selection; course integration lead integrates the approved material.
- **Acceptance:** confirm the intended term and physical problem; establish public provenance and sharing authority; define observables and assumptions; review evidence and field interpretation before filling numerical panels.

## L3-W01 · Train, save and reuse

- **Placement:** lecture 3, “Define and train a small model”; slide storyboard `L3-S02`.
- **Learning question:** What information is needed to reuse a trained model?
- **Content:** short supervised training step and saved/reloaded prediction on the same Helmholtz input, including preprocessing and feature ordering.
- **Reuse source:** `notebooks/04_train_save_reload_adapter.ipynb`, `source/book/06_learning_adapter.md`.
- **Owner:** course integration lead, with learning-interface review.
- **Acceptance:** retain scalar Helmholtz scope; name input/target channels and split; make the weight-gradient call visible; save preprocessing/configuration with weights; check reloaded predictions using an independently instantiated model; record execution of the final curated notebook.

## L3-A01 · Learned damage-subsolve replacement

- **Placement:** lecture 3, “Route A”; slide storyboard `L3-S04`.
- **Learning question:** Which operation is learned and what governs the accepted state?
- **Content:** replace the damage operation inside the staggered diagram; label driving field, material/geometry/history inputs, predicted damage and subsequent mechanics update.
- **Reuse source:** `source/book/figures/03_staggered_loop.svg`, `source/book/06_learning_adapter.md`; implementation extensions tracked in issues #8 and #9.
- **Owner:** course integration lead owns the conceptual asset; learned-damage contributor owns future implementation evidence.
- **Acceptance:** mark the workflow as conceptual until an implementation is checked; specify field location/order, damage bounds, history and coupled checks; retain mechanics in the loop; keep this route visually distinct from external proposal correction; inspect static frames and playback.

## L3-A02 · Prediction, physical correction and fallback

- **Placement:** lecture 3, “Route B”; slide storyboard `L3-S06`.
- **Learning question:** Does the complete hybrid route improve the reference calculation?
- **Content:** separate proposal, residual gate, numerical correction, corrected-state check and reference fallback; a qualitative strip lists the complete cost components.
- **Reuse source:** `source/book/figures/06_learning_cycle.svg`, `notebooks/05_hybrid_reference_correction.ipynb`.
- **Owner:** course integration lead, with hybrid-method review.
- **Acceptance:** label the current Helmholtz implementation and any fracture extension; distinguish correction from reference fallback accurately; re-check any corrected output; add measured timings only for matched full routes with field-quality evidence; review both animation and static alternatives.

## L3-W02 · Compatible model comparison

- **Placement:** lecture 3, “Compare models through a common interface”; slide storyboard `L3-S08`.
- **Learning question:** Which parts of the interface must agree for a meaningful comparison?
- **Content:** existing MLP/RBF inputs, outputs and saved metadata; qualitative grid/graph representation rows for possible extensions.
- **Reuse source:** `notebooks/04_train_save_reload_adapter.ipynb`, `source/book/06_learning_adapter.md`.
- **Owner:** course integration lead, with learning-interface review.
- **Acceptance:** use common physical targets and explicit channel/order/normalisation conventions; label any grid/graph extension conceptual; retain matched splits for quantitative comparison; claim neither arbitrary interchangeability nor unmeasured performance.

## L3-A03 · Model-visited data and a DAgger-style round

- **Placement:** lecture 3, “Learning from states encountered during use”; slide storyboard `L3-S10`.
- **Learning question:** Why can model-visited states add information to the original dataset?
- **Content:** current-model rollout, reference labels at visited states, aggregation and retraining, with separate held-out evaluation.
- **Reuse source:** `source/book/06_learning_adapter.md`, `source/book/figures/06_learning_cycle.svg`; complete implementation remains under issue #9.
- **Owner:** course integration lead owns the conceptual asset; hybrid-learning contributor owns the complete experiment.
- **Acceptance:** distinguish online inference, online updating, active selection and DAgger-style aggregation; show a model-induced trajectory and reference-labelling step; label conceptual status; require recorded rollout, labels, retraining and held-out evaluation before representing the loop as executed.

## P1-R01 · Short propagating-crack practical

- **Placement:** classroom practical 1, after the changed-load comparison.
- **Learning question:** How does a resolved crack front advance under loading?
- **Content:** public dynamic fracture case with full-domain fields and response history.
- **Reuse source:** the shared B3 work in issues #5/#19 and PhAST #5.
- **Owner:** course integration lead and upstream PhAST documentation contributor.
- **Acceptance:** checked configuration/provenance, visible front advance, convergence and resolution evidence, complete notebook below 300 seconds after setup and fresh Colab rehearsal.

## P1-A01 · Geometry-to-damage sequence

- **Placement:** classroom practical 1, after the numerical plots.
- **Learning question:** How are the specimen, mesh, loading and computed field connected?
- **Content:** show the geometry, mesh, prescribed motion and three saved damage states.
- **Reuse source:** the executed `01_simulate_fracture` arrays and existing static figures.
- **Owner:** course integration lead.
- **Acceptance:** actual field data, shared damage scales, labelled load factors, complete specimen views, static alternatives and playback review.

## P2-R01 · Small fracture inverse practical

- **Placement:** classroom practical 2, after elastic-bar recovery.
- **Learning question:** Which fracture parameters can the selected observations identify?
- **Content:** stated parameters/loss, checked gradients, recovery histories and held-out observations.
- **Reuse source:** approved inverse contribution under issue #7; connect with lecture slots L2-R01–R04.
- **Owner:** inverse-extension contributor, with course integration review.
- **Acceptance:** public-source approval, source/configuration lock, interpretable fields, multiple-start evidence and complete runtime below 300 seconds after setup.

## P2-A01 · Bar forward and reverse sequence

- **Placement:** classroom practical 2, alongside its computational graph.
- **Learning question:** How does the loss return a gradient to the modulus?
- **Content:** modulus, stiffness, displacement and loss forwards; derivatives backwards; optimisation update last.
- **Reuse source:** executed bar equations and L2-A01's original graph assets.
- **Owner:** course integration lead, with differentiation review.
- **Acceptance:** state/observable/loss/gradient labels, correct derivative direction and static frames matched to the actual calculation.

## P3-R01 · Fracture-compatible hybrid practical

- **Placement:** classroom practical 3, after the Helmholtz correction example.
- **Learning question:** When does a proposed damage state require a coupled correction?
- **Content:** declared history/features, predicted damage, physical checks and corrected fields.
- **Reuse source:** approved PhAST model-interface work in issues #8/#9; lecture slots L3-A01/A02.
- **Owner:** model-interface contributor, with course integration review.
- **Acceptance:** sharing authority, feature/location/history contract, checked full fields, matched complete proposal/check/correction timing and execution below 300 seconds after setup.

## P3-A01 · Proposal and correction sequence

- **Placement:** classroom practical 3, after the accepted and perturbed proposals.
- **Learning question:** How does the residual determine the selected field?
- **Content:** proposal, assessment and accepted/reference-corrected field; link to the conceptual data-aggregation loop.
- **Reuse source:** executed `03_learning_and_hybrid` fields and L3-A02/A03 storyboards.
- **Owner:** course integration lead, with hybrid-method review.
- **Acceptance:** algorithmically correct branches, labelled toy scope, matched residual values and static alternatives; keep full DAgger execution under its separate slot.

## Register-wide closure rule

Closing a slot requires its final source path, review evidence and relevant
execution or rendering receipt to be recorded here. New plots require actual
data and labelled units; animations require readable controls and static
alternatives. Research assets require approval and source/evidence review from
their contributor. Reuse of an existing figure or numerical receipt should
identify exactly what was reused and what the new adaptation adds. Issue #20
and the relevant content issue remain open for any unmet acceptance criteria.
