# Voice-memo curation: three lectures and three practicals

## Decision and provenance

The user-directed curation on 10 September 2026 is tracked by
[issue #20](https://github.com/CEMS-Lab/autumn-school/issues/20). It follows the
5 minute 15 second user-provided recording and its locally reviewed
discussion summary. The recording establishes the requested learning sequence
and priorities; it supplies no numerical or implementation evidence. The
private recording and raw transcript stay outside the public course checkout.

This curation adds short lecture guides, three concise classroom notebooks
and an explicit register of content still to prepare. It retains the existing
chapters, six detailed notebooks, research extension, figures and editable
decks. Existing derivations remain available as reference reading. Each core
practical follows physical question → short explained calculation → field or
curve interpretation → exercise with hint and worked solution.

## Timing and learning sequence

The 360-minute event window contains a 300-minute teaching core and 60 minutes
for breaks, questions, setup support and optional exploration. Lunch sits
outside this window. The 45/55/50-minute lecture allocation consolidates the
recorded ranges and is a planning choice. Event clock times remain subject to
organiser scheduling. Historical 180+180-minute contact-time allocations
describe earlier plans and should remain identifiable as such.

| Block | Minutes | Central question | Principal source |
| --- | ---: | --- | --- |
| L1: fracture and PhAST | 45 | How does a crack model become a numerical calculation? | `source/book/lectures/01_fracture_and_phast.md` |
| L2: derivatives and recovery | 55 | How does a parameter affect an observation and a scalar loss? | `source/book/lectures/02_differentiability_and_inverse.md` |
| L3: learning and hybrid methods | 50 | What role does the learned operation play in the numerical workflow? | `source/book/lectures/03_hybrid_learning.md` |
| P1: simulate fracture | 50 | What do the fields and reaction curve reveal? | `classroom/01_simulate_fracture` |
| P2: gradients and recovery | 50 | How can a checked gradient guide recovery? | `classroom/02_gradients_and_recovery` |
| P3: learning and hybrid | 50 | How are a model prediction and its numerical assessment connected? | `classroom/03_learning_and_hybrid` |
| Flexible time | 60 | Breaks, questions, setup support and optional exploration | `TEACHING_SCHEDULE.md` |
| **Total** | **360** | Lunch outside the allocation | |

The lecture block precedes the practical block, with practicals repeating the
same sequence. Preparation and explanation occupy most practical time;
complete notebook computation remains below 300 seconds after setup, measured
on the actual executed notebook. The recording's possible 5–10-minute small
inverse calculation does not relax that existing execution requirement.

## Curation and preserved sources

| Core practical | Selected content | Preserved detailed references |
| --- | --- | --- |
| P1 | Configuration, short geometry/mesh setup, visible PhAST solve call, damage and reaction interpretation, one controlled change | `01_phast_tiny_evolving_fracture.ipynb` |
| P2 | Degradation derivative, visible autograd and finite-difference calls, elastic-bar modulus recovery and parameter/loss interpretation | `02_degradation_autograd.ipynb`, `03_tiny_derivative_inverse_toy.ipynb` |
| P3 | Small model training, save/reload, prediction, residual assessment and reference correction/fallback | `04_train_save_reload_adapter.ipynb`, `05_hybrid_reference_correction.ipynb` |
| Optional opening or further study | Branch-selection algebra and the full implementations of all six existing notebooks | `00_why_average_predictions_can_fail.ipynb` and the five references above |

The preserved notebooks remain canonical detailed resources. Classroom
notebooks provide the selected route; generated book pages and practice/solution
downloads must be regenerated from their appropriate sources. Implementation
detail can be expandable or delegated to short inspectable course helpers.
The key solver, gradient, training and assessment calls remain visible in the
student's notebook. A helper's prose should name the inputs, outputs and
scientific operation it performs.

## Scientific scope and ownership

The actual PhAST classroom baseline is quasistatic AT2 with assembled
sparse-direct mechanics. Matrix-free operators and dynamics retain their
lecture explanations. The shared dynamic crack-propagation example remains
under the separate course/upstream workstream in issues #19 and PhAST #4.
Selecting it for classroom execution requires its own evidence and review.

The degradation law is an algebraic teaching calculation; the elastic bar is
the core inverse teaching model; the learning and hybrid practical uses a
scalar Helmholtz teaching model. These designations belong beside the relevant
student activity. Existing execution receipts describe the notebooks and
versions they measured. The curated notebooks require fresh execution receipts.

The inverse-extension contributor owns new fracture inverse evidence. The
lecture sequence reserves fracture-energy recovery, single-particle recovery,
multiple-particle recovery and a non-particle application, in that order.
The last term in the recording was transcribed as “DAC” at approximately
01:32–01:38 and 02:14–02:20. Its meaning is unresolved; no expansion or example
identity is assigned here. Selection and terminology require contributor and
maintainer confirmation before numerical panels are filled.

The two hybrid routes have separate storyboards: learned replacement of the
damage subsolve within staggering, and physical correction of a prediction.
The Helmholtz practical supports the latter teaching pattern. The learned
fracture subsolve and a complete DAgger-style data-aggregation experiment remain
extensions with their own evidence requirements. Runtime comparisons require
the complete prediction, checking, correction and fallback costs alongside
field quality and matched reference calculations.

## Placeholder and slide integration

[PLACEHOLDER_REGISTER.md](PLACEHOLDER_REGISTER.md) lists every lecture slot,
its learning question, intended content, reuse source, owner and acceptance
criteria. Guide callouts identify planned content in the learner-facing book.
Research panels are textual outlines; their labels establish no recovered
parameters, successful runs, plotted values or timings.

The `L1-Sxx`, `L2-Sxx` and `L3-Sxx` entries are proposed slide placements for a
later deck revision. They are storyboard identifiers, independent of current
slide numbers. The existing editable introduction, animations and LaTeX deck
remain retained. A later rebuild should compose each approved asset for the
slide aspect ratio and inspect actual playback and readability.

## Integration acceptance and remaining work

Local integration should verify the three-practical route in navigation,
download links and Colab entry points; retain access to all six detailed
notebooks; execute the three curated notebooks with full-run timing; rebuild
the book; and inspect lecture pages, field plots, equations and expandable
solutions at desktop and narrow widths. Preserve setup time separately from
execution time and distinguish local execution from a fresh Colab rehearsal.

Owners then fill the registered assets, provide their source and scientific
evidence, review the inverse selections, rebuild the complete lecture deck and
conduct a timed three-lecture/three-practical rehearsal. Issue #20 stays open
for its outstanding acceptance work. Numerical extension, publication and
upstream documentation issues retain their separate ownership and checks.
