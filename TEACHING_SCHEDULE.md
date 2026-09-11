# Day two: three lectures and three practicals

Curated from the 10 September voice-memo discussion and the maintainer's
follow-up. This schedule supersedes the earlier six-hour contact-time baseline.
The proposed event window contains **150 minutes of lectures, 150 minutes of
practicals and 60 minutes for breaks, questions, setup support and extension**.
Lunch sits outside this six-hour allocation; organisers confirm clock times.
An earlier finish is appropriate when the learning outcomes have been met.

## Morning: the solver, its gradients and hybrid learning

| Block | Minutes | Sequence |
| --- | ---: | --- |
| L1 — Phase-field fracture and PhAST | 45 | Crack and damage field (6); energy and degradation (12); one numerical increment (13); tensors, matrix-free actions and dynamics (10); practical connection (4). |
| L2 — Differentiability and inverse applications | 55 | Parameter and observation (6); reverse sensitivity (12); derivative scope (10); fracture-energy, single-particle, multi-particle and non-particle exhibit slots (22); practical connection (5). |
| L3 — Hybrid numerical and learned methods | 50 | Training motivation (8); damage-subsolve replacement (10); prediction and physical correction (10); compatible model comparison (10); online learning and DAgger (8); practical connection (4). |

Guides and fill-in slots: `source/book/lectures/`. Research exhibits require
approved public evidence before replacing their outlines. The non-particle
example in the recording remains unnamed until its identity is confirmed.

## Afternoon: three guided notebooks

| Block | Minutes | Sequence and model |
| --- | ---: | --- |
| P1 — Simulate and interpret fracture | 50 | Setup (8); geometry/notch/mesh and BCs (10); load and solve (7); fields, animation, energy curves and archives (15); saved-field exercises (10). Actual PhAST dynamic spectral AT2, explicit momentum and implicit damage. |
| P2 — Gradients and recovery | 50 | Damaged-bar autodiff primer (10); degradation and analytic/AD/FD comparison (10); bar observation and sensitivity (10); parameter recovery (10); exercise and fracture transfer (10). Public degradation law and compact bar teaching models. |
| P3 — Learning and hybrid correction | 50 | Data/feature contract (8); training and inspection (12); save/reload (8); propose, assess and correct (12); exercise and route comparison (10). Teaching Helmholtz field. |

Each block is one notebook with one environment setup and two structured
exercises. Complete computational runs must remain below **120 seconds after setup**;
explanation, prediction and discussion occupy the rest of the slot.
Fresh Colab and presentation-machine rehearsal retain separate delivery checks.

## Flexible time

Allocate the remaining 60 minutes with the organisers: for example, two
15-minute breaks, 15 minutes of setup support and 15 minutes of discussion or
extension. These are proposed allocations. Paper exhibits fit inside L2/L3;
a longer paper discussion replaces an allocated activity.

## Preserved material and next steps

The original individual notebooks remain in `notebooks/` and the book's
**Detailed notebooks and further practice** section. The algebraic teaser is
optional. Existing editable presentations, movies, theory and research readings
are retained. The placeholder register maps them to the curated lecture route.

Use [the placeholder register](source/planning/PLACEHOLDER_REGISTER.md) for
asset ownership and acceptance, [TODAY.md](TODAY.md) for active work and
[COURSE_PLAN.md](COURSE_PLAN.md) for the full curriculum. Rehearse transitions,
code readability, equations, exercises, complete runtime and download parity.
