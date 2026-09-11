# Full-ligament propagation and branching

The maintainer requests a visible crack crossing the plate and a separate
branching example after inspecting the 60-increment classroom animation.
Owning workstreams: course issues #5 and #19; upstream PhAST #5.

## Teaching decision

The current classroom example supplies a small quasistatic damage calculation.
Its final opening is 0.04 in dimensionless units. Increasing the number of
increments at that final opening refines the load path. A through-ligament
crack requires an appropriate physical configuration and a converged solution.

Assess the public B3 dynamic SENT configuration with its checked-in mesh for
the short propagation activity. Use the public B7 AT1/Amor branching result
as a clearly attributed recorded lecture exhibit. Keep the three-practical
structure and concise code cells. Preserve the original notebooks and receipts
until a replacement completes the numerical, teaching and execution checks.

## Ownership and checks

- Integration: `scripts/probe_crack_propagation.py`, gallery/package generator,
  selected media and this plan. No solver-kernel or vendored-source changes.
- Dynamic diagnostic: `scripts/probe_dynamic_sent.py` and separate `b3_*`
  evidence folders. Observe every damage update, retain history and assess
  finite fields, irreversibility, boundary values and constrained residuals.
- Branching review: public source, material/model, timestamps, media identity,
  domain-wide final field and original runtime.
- Assess connected high-damage extension at stated thresholds; distinguish
  recorded physical time from movie playback speed.
- Preserve bounded trial failures. Whole-notebook timing, fresh Colab and
  mesh/time-step refinement remain explicit acceptance items.

## Load-extension trials

Two local trials used the unchanged pinned public solver, a 96 by 48 T3 grid,
and final opening 0.08 with the existing material and boundary conditions.
The 60-increment trial reached the 200-stagger limit (53.44 s); the
100-increment trial reached the 1,000-stagger limit (160.74 s). Neither is
accepted as a classroom result. Exact configurations and receipts are in
`evidence/propagation_20260911/`.

## Accepted local dynamic candidate

The public B3 mesh has 1,091 nodes and 1,940 T3 elements. The plane-strain
spectral AT2 model uses E = 32,000 MPa, nu = 0.2, Gc = 0.003 N/mm and
length scale 0.5 mm. Opposite boundary displacements ramp to +/-0.002 mm
over 20 microseconds, then hold until 100 microseconds. The 20 mm geometric
notch is distinct from a prescribed initial damage field.

Projected CG with Jacobi preconditioning passed all 6,116 independently
checked constrained damage residuals (maximum 9.994e-6 at tolerance 1e-5),
finite-field, irreversibility and displacement-BC checks. The complete
diagnostic run took 26.686 seconds. The connected path crosses the remaining
20 mm ligament at damage thresholds 0.5, 0.9 and 0.95.

Halving the time step completed in 49.20 seconds. Final area-weighted damage
relative L2 difference is 1.60%; the maximum total-energy difference relative
to peak energy is 0.856%. This assesses temporal sensitivity. Mesh convergence
remains a separate study. The external-work column is a solver placeholder;
plot the individual energy components without presenting a verified work balance.

The portable notebook candidate took 27.624 seconds including local setup,
three PNG plots, a results table and a 40-frame GIF. It is being promoted to
Classroom 1 with the older quasistatic notebook preserved. Every future
student run is gated at 120 seconds; a fresh Colab receipt is still required.

## Branching and autodiff teaching additions

Public B7 provides a genuine two-arm branching movie with source provenance.
Its original 169,077-node A100 calculation took 2,139.84 seconds, so the lesson
uses the recorded movie. Material, loading and fracture formulation differ
from B3 and are stated alongside the exhibit.

Classroom 2 starts with F=(EA/L_b)(1-d)^2 u and a squared force mismatch.
At u=0.1, d=0.5, E=2, A=L_b=1 and target force 0.04, the loss is 5e-5 and
its input gradient is [0.005, -0.002]. Analytic, PyTorch and central-difference
checks agree. Original inverse calculations and exercises are preserved.
