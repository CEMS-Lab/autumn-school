# Lecture 3: Learned damage updates in PhAST

A trained network can replace one operation inside a finite-element calculation.
The central questions are what it receives, what it predicts, and whether the
resulting fields remain accurate. {doc}`NB3 <../classroom/03_learning_and_hybrid>`
compares conventional FEM with a frozen graph neural network that directly
predicts damage. Mechanics remains in PhAST.

## The same physical problem, two damage updates

The specimen is a 10 mm square plate with a horizontal edge slot and three
holes. The bottom boundary is fixed. The top boundary has zero horizontal
displacement and an increasing vertical displacement, ending at 0.04 mm.
The slot and hole surfaces are traction-free geometric boundaries, not regions
of prescribed damage.

The material has $E=210000\,\mathrm{MPa}$, $\nu=0.3$,
$G_c=2.7\,\mathrm{N/mm}$ and $\ell_0=0.4\,\mathrm{mm}$. Both routes retain
the checkpoint-specific rational degradation law

$$g(d)=\frac{(1-d)^2}{d^2-d+1}, \qquad 0\le d\le1.$$

The retained model degrades the full elastic stress while using tensile energy
to drive the history. This combination is a non-variational constitutive
choice: it should not be presented as the variation of one common split-energy
functional. NB1 uses a different constitutive model for its dynamic glass plate.

## Read one load increment

The calculation is quasi-static: inertia is neglected. At increment $n$,

$$\mathbf d_{n-1}\longrightarrow\mathbf u_n
\longrightarrow\mathbf H_n\longrightarrow\mathbf d_n.$$

1. Solve mechanical equilibrium with the previous damage fixed.
2. Update the maximum-history driving field.
3. Solve the FEM damage equation, or predict damage with the GNN.
4. Project onto the damage bounds, measure the residual and advance the load.

Each increment uses one mechanics–damage pass. It is not an outer staggered
iteration continued to coupled convergence. `QUICK_TEST=True` selects 60
increments; setting it to `False` selects 500 unless `PHAST_DEMO_STEPS`
overrides the count. Changing that count changes the load discretisation, so
compare both routes with the same setting and assess increment sensitivity.

| Route | Damage operation | What follows |
| --- | --- | --- |
| Conventional FEM | FEM damage solve | Projection and residual evaluation |
| Direct learned replacement | GNN damage prediction | Projection and residual evaluation; no FEM damage correction |

Both routes enforce $\mathbf d_n\ge\mathbf d_{n-1}$ and $\mathbf d_n\le1$.
Projection enforces these bounds; it does not solve the damage equation.
The learned residual is measured, not used to trigger an FEM fallback.

## From a mesh to a graph

Every finite-element vertex is a graph node. Triangle edges define connections
in both directions. The network receives an assembled history feature and a
topological boundary indicator at each node, together with edge lengths scaled
by the phase-field length. For the homogeneous linear triangles used here,

$$q_i=\sum_{e\ni i}\frac{A_e H_e}{3G_c\ell_0}.$$

The network transforms this feature as $\log_{10}(1+q_i)$, applies an encoder,
ten message-passing blocks and a decoder, and returns one damage value per
node. The FEM field is reconstructed using the same nodal ordering:

$$d_h(\mathbf x)=\sum_i N_i(\mathbf x)d_i.$$

The notebook downloads `phast_gnn_assets.zip`, which contains the compatible
PhAST source and `moon_pi_dd.pt`. It verifies the supplied hashes before
loading. These weights were trained on an inclined-slot specimen and remain
fixed here: the exercise tests transfer to a different geometry, not training.

## Two comparisons answer different questions

**Independent loading paths.** The FEM and hybrid calculations start from
independent initial states. Each GNN prediction influences its own next
mechanics solve. Compare their damage fields at the same applied displacement,
with common colour scales, and inspect reaction forces and residual histories.

**Identical damage inputs.** Replay stored FEM history and previous-damage
fields through both damage updates. This isolates the replacement operation
from differences that accumulate along the two loading paths.

The relative nodal field error is

$$e_d=\frac{\|\mathbf d_{\mathrm{GNN}}-\mathbf d_{\mathrm{FEM}}\|_2}
{\|\mathbf d_{\mathrm{FEM}}\|_2}.$$

This unweighted nodal norm is not a mesh-independent integral error. A small
field error and a small constrained residual are different checks. Reactions
are evaluated after damage is updated without re-equilibrating displacement
within that increment; interpret them in the context of the one-pass scheme.

## Interpret performance without losing accuracy

The saved notebook includes fields, animations and measured comparisons.
Damage-update timing includes inference or FEM solution, transfers, projection
and residual evaluation. Complete-loop timing also includes mechanics, history,
reactions and storage, but excludes installation, model loading and figures.
Report the device and measurement scope with any ratio. Faster damage updates
do not by themselves establish a faster or equally accurate complete simulation.

The optional {doc}`Radius-GNO case study <../w53_direct_replacement>` uses
a different model and experiment. Its measurements are not results for this
Moon-style graph-network exercise. The optional
{doc}`Helmholtz tutorial <../labs/04_train_save_reload_adapter>` explains
training and reloading a model; it is separate from this fracture application.
