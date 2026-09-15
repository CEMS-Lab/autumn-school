# Lecture 3: Learned damage updates in PhAST

A trained network can supply a field inside a finite-element calculation.
Identify what the network receives, which operation it affects, and how to
assess the resulting simulation. This practical evaluates a frozen graph
network in a real PhAST fracture calculation.

## Locate the learned operation

Mechanics determines displacement; tensile history supplies the driving field;
the damage update determines the next damage field. The network predicts this
damage update. Mechanics remains in PhAST. Bounds, irreversibility, boundary
values and the damage residual still govern interpretation of an accepted state.

## Define the specimen and constitutive model

{doc}`Lab 3 <../classroom/03_learning_and_hybrid>` builds a 10 mm square
plate with an edge slot and three holes. Quasi-static loading advances through
500 increments to a top displacement of 0.04 mm. Each increment performs one
mechanics–damage pass (`max_stagger=1`); the supplied calculation does not
iterate the coupled fields to staggered convergence at each increment.

The material has $E=210000\,\mathrm{MPa}$, $\nu=0.3$,
$G_c=2.7\,\mathrm{N/mm}$ and $\ell_0=0.4\,\mathrm{mm}$. Its checkpoint-specific
degradation law is

$$g(d)=\frac{(1-d)^2}{(1-d)^2+d}.$$

Damage reduces the full stress, while the tensile part of the elastic energy
drives the history update. This combination does not follow from one common
energy functional; it is a non-variational hybrid constitutive model. The
classical and learned routes in Lab 3 use this same model, mesh and loading.
Lab 1 uses a different constitutive model for the dynamic glass plate.

## Distinguish the three damage routes

| Route | Network role | Accepted damage |
| --- | --- | --- |
| `classical` | No prediction | Classical damage solve |
| `learned_proposal` | Supplies an initial field | Classical solve started from the prediction |
| `learned_replacement` | Supplies a candidate field | Checked prediction, or classical fallback |

Direct replacement is the main application of interest. The proposal route
provides a comparison with numerical correction. Each has its own cost and
accuracy. Retain the fallback and report its use.

## Read the interface and obtain the checkpoint

`DamageStepContext` supplies the mesh, mechanical fields, loading history,
previous damage and material data. The adapter converts these into the inputs
expected by the saved network. Their order, units, boundary description and
scaling must match those used during training. Compare the new specimen and
loading with the training data when assessing transfer to another problem.

The notebook imports the public mesh-graph adapter from the PhAST checkout.
Obtain `mesh_graph_net.pt` from the instructor before starting; public
automated distribution of these weights remains separate from the book.
Printing a checksum identifies a file; verification also requires a trusted
expected hash.

## Compare fields and complete cost

Inspect reference, prediction and difference using common colour scales.
Compare the damage residual and physical constraints alongside nodal field
error. Record complete runtime, including inference, checking, correction and
fallback. The supplied notebook contains this comparison code but no retained
run outputs. A fresh whole-notebook timing, including its three solves and
post-processing, is required before assigning a classroom runtime or speed-up.

The lecture’s damage-stage timing and the optional
{doc}`Radius-GNO case study <../w53_direct_replacement>` concern their own
models, specimens and hardware. Neither provides a measured end-to-end speed-up
for this mesh-graph classroom exercise.

## Extend the exercise

Explore acceptance tolerances, changed holes, predictor interfaces and
per-increment cost. These are additional runs. The network was trained on a
different specimen, so this example tests transfer. Keep the reference
calculation visible when drawing conclusions.

For training fundamentals, the original Helmholtz
{doc}`train/save/reload tutorial <../labs/04_train_save_reload_adapter>`
remains optional. Its simple field equation explains a training loop; the main
Day 2 practical evaluates a supplied trained model within fracture mechanics.
