# Ceyron reference audit and differentiability notebook design

Reference inspection: 9 September 2026. This is an original planning note for
the local next edition. It records inspected source and design choices; it is
not a notebook execution receipt or a publication-readiness claim.

## Scope and relationship to the existing course

The course already has the one-dimensional elastic-bar inverse lesson,
`notebooks/03_tiny_derivative_inverse_toy.ipynb`, introduced in
`source/book/05_differentiation_and_inverse.md`. That lesson checks a modulus
derivative, recovers a synthetic modulus and checks a held-out load. The
three-step algebraic example in `05a_backpropagation_step_by_step.md` already
explains reverse accumulation and the sum over uses of a shared parameter.

The new diffusion unrolling lesson should connect those ideas to a small
evolving field. Its distinct question is: **how does one parameter used at
every time step influence a final observation?** It provides complementary
time-step and parameter-accumulation pedagogy, not another inverse-recovery
deliverable or a replacement for the bar lesson. A visible optimiser update
can demonstrate the use of a gradient without adding a second full inverse
study to the classroom route.

Label diffusion as a teaching field model. It is not phase-field fracture or
an actual PhAST calculation. The transfer is the chain rule through repeated
discrete update maps; damage history, active sets and coupled fracture
convergence remain separate scientific questions.

## Reference 1: Hybridization in JAX with AD

Inspected repository commit:
[`61ee2629f5800d92fba64492a0f81efe3a6a7c39`](https://github.com/Ceyron/hybridization-in-jax/tree/61ee2629f5800d92fba64492a0f81efe3a6a7c39).
The [MIT licence](https://github.com/Ceyron/hybridization-in-jax/blob/61ee2629f5800d92fba64492a0f81efe3a6a7c39/LICENSE)
names Felix Köhler, copyright 2026. Preserve its notice if incorporating
substantial source portions. This course adaptation should use original
PyTorch code, equations, diagrams and prose, with source attribution.

The supplied [YouTube video](https://www.youtube.com/watch?v=g1guv-fkIrQ) has
the title "Neural-Hybrid Correctors with Solver-in-the-loop in JAX" and author
Machine Learning & Simulation, verified through public YouTube oEmbed
metadata. The repository README identifies it as the second practical.
The video was **not watched**: direct page access was throttled, and no
transcript was obtained. No claims about its spoken explanations or pacing
are based on viewing it.

All four notebook sources were read; their code was not executed and their
stored plot images were not visually inspected. The following descriptions
refer to source cells and output types, not independently reproduced results.

| Source | Actual format and observed progression |
| --- | --- |
| [zeroth_getting_started.ipynb](https://github.com/Ceyron/hybridization-in-jax/blob/61ee2629f5800d92fba64492a0f81efe3a6a7c39/practical_session/zeroth_getting_started.ipynb) | 31-cell notebook. Explain state shape; plot initial field; construct and inspect the stepper; run one and several steps; plot after each experiment; introduce compilation and repeated stepping; record and animate a trajectory. |
| [first_data_assimilation.ipynb](https://github.com/Ceyron/hybridization-in-jax/blob/61ee2629f5800d92fba64492a0f81efe3a6a7c39/practical_session/first_data_assimilation.ipynb) | 17-cell notebook. Reuse the forward model; formulate recovery of an initial field; optimise; compare loss and recovery error; show truth/initial/recovered fields; discuss chaotic predictability; identify diffusivity from trajectory observations. This is the closest reference for a differentiability practical. |
| [second_neural_hybrid_corrector.ipynb](https://github.com/Ceyron/hybridization-in-jax/blob/61ee2629f5800d92fba64492a0f81efe3a6a7c39/practical_session/second_neural_hybrid_corrector.ipynb) | 54-cell notebook. Inspect coarse/fine mismatch; define an additive neural correction; compare one-step and three-step training for hybrid and pure predictors; evaluate held-out rollouts through six-panel animation, spectra and time-dependent errors; invite parameter changes. |
| [_second_data_generation.ipynb](https://github.com/Ceyron/hybridization-in-jax/blob/61ee2629f5800d92fba64492a0f81efe3a6a7c39/practical_session/_second_data_generation.ipynb) | 18-cell supporting notebook. Generate separate training/test trajectories at fine resolution, map to coarse resolution and save compact arrays. Expensive preparation is separated from the teaching route. No datasets were downloaded during this audit. |

Cell counts include each notebook's trailing empty cell. The main transferable
pattern is a short explanation followed by an executable experiment and an
immediate plot. Physics and array shapes appear before optimisation. The same
forward map supports successive questions. Training loss is supplemented by
field comparisons and held-out behaviour. The reference explains the changed
temporal loss reduction when comparing one-step and three-step training.

Limitations to account for in an original lesson:

- The first practical puts much of each optimisation in one large cell.
  Split forward, loss, backward and update operations into inspectable cells.
- Exercises are mainly invitations to change constants; explicit prediction,
  answer and worked-solution cells are largely absent.
- The README says animation outputs were removed to reduce size. Retain
  lightweight static field snapshots in our notebook as a visible fallback.
- Zeroth cell 12 computes `after_ic`, but cell 14 plots `ic` again. Plot the
  updated state in the original lesson.
- Lyapunov-time explanations concern the chaotic-flow example. They should
  not be transferred as a claimed limitation or timescale of diffusion or
  fracture without a separate argument.

## Reference 2: Machine Learning and Simulation, English material

Inspected repository commit:
[`a2e50a9df4bb6e938901b33fd957c06ac06b5224`](https://github.com/Ceyron/machine-learning-and-simulation/tree/a2e50a9df4bb6e938901b33fd957c06ac06b5224/english).
The [MIT licence](https://github.com/Ceyron/machine-learning-and-simulation/blob/a2e50a9df4bb6e938901b33fd957c06ac06b5224/LICENSE.txt)
names Felix Köhler, copyright 2021. The English directory includes separate
adjoints/autodiff, FEniCS, neural-operator and simulation topics. Five relevant
sources were read; unrelated ML material was not audited. No selected source
was executed, and notebook plot descriptions below follow the code.

| Exact source permalink | Format and design contribution |
| --- | --- |
| [adjoint_linear_system_example.py](https://github.com/Ceyron/machine-learning-and-simulation/blob/a2e50a9df4bb6e938901b33fd957c06ac06b5224/english/adjoints_sensitivities_automatic_differentiation/adjoint_linear_system_example.py) | Python script, not a notebook. Define a tiny linear system and synthetic reference; solve at guessed input; calculate loss; compare adjoint, forward and finite-difference sensitivities. A compact conceptual bridge from a solve to a scalar derivative; no plots or recovery loop. |
| [adjoint_non_linear_system_jax_jacobians.py](https://github.com/Ceyron/machine-learning-and-simulation/blob/a2e50a9df4bb6e938901b33fd957c06ac06b5224/english/adjoints_sensitivities_automatic_differentiation/adjoint_non_linear_system_jax_jacobians.py) | Python script. Define residual/state/parameter/loss and matrix dimensions before code. JAX provides local residual and loss derivatives; SciPy finds the root; explicit implicit-sensitivity equations produce gradients. This is not direct backpropagation through SciPy. |
| [curse_of_unrolling_against_implicit_diff.ipynb](https://github.com/Ceyron/machine-learning-and-simulation/blob/a2e50a9df4bb6e938901b33fd957c06ac06b5224/english/adjoints_sensitivities_automatic_differentiation/curse_of_unrolling_against_implicit_diff.ipynb) | 32-cell notebook. State a precise derivative-convergence question; plot scalar objectives; compute iterates; compare state/loss errors; add derivative errors; derive the observed transient; invite parameter changes; add an implicit comparison. Strong optional pattern: observe an unexpected result, then explain it analytically. |
| [cantilever_beam_linear_elasticity.py](https://github.com/Ceyron/machine-learning-and-simulation/blob/a2e50a9df4bb6e938901b33fd957c06ac06b5224/english/fenics/cantilever_beam_linear_elasticity.py) | Python script. Governing equations, symbol glossary and geometry sketch precede mesh/space, boundary conditions, strain/stress, weak form, solve and postprocessing. Exports displacement and stress to XDMF; it has no notebook field plots or sensitivity calculation. |
| [simple_unet_poisson_solver_in_jax.ipynb](https://github.com/Ceyron/machine-learning-and-simulation/blob/a2e50a9df4bb6e938901b33fd957c06ac06b5224/english/neural_operators/simple_unet_poisson_solver_in_jax.ipynb) | 27-cell notebook. Explain PDE and forcing distribution; construct exact solver data; inspect shapes and physical fields; expose train/test split; build/train model; show loss, a held-out prediction overlay and aggregate error. It is a learned surrogate, not a solver-in-the-loop hybrid. |

These sources support original examples rather than literal transcription.
In the unrolling notebook, cell 29 omits the negative sign stated in cell 28;
the default zero exact derivative masks this in the absolute-error plot.
Cell 25's burn-in statement is inconsistent with its stated parameter and
learning rate. In the nonlinear script, the second residual's cubic factor
has zero derivative at its exact root; the nonsingularity needed for the
displayed implicit formula therefore requires care. Use a fresh, analytically
checked example for any such extension. The cantilever explanation also
describes a tensor orthogonality too broadly: a symmetric tensor is orthogonal
to a skew-symmetric tensor, not to every nonsymmetric tensor.

The small-script timing outputs are not a verified performance benchmark.
This audit establishes their teaching structure, not runtime, reproducibility,
convergence or fitness for the current course environment.

## Cell model for the original diffusion lesson

Use the repeating unit **short equation → visible code → interpretable plot →
predict a change → check → worked solution**. Every cell should answer a small
question. Separate physical time steps, the backward traversal and optimiser
iterations in notation, code and captions.

| Learning step | Visible computation or evidence |
| --- | --- |
| 1. Connect and define | Name the bar/algebraic prerequisites, diffusion equation, boundary conditions, fixed grid, parameter, initial field and final observation. State toy scope. |
| 2. Predict and run | Plot the initial condition; predict the effect of increased diffusivity; expose the numerical time-step formula and a short forward loop. |
| 3. Inspect evolution | Plot several full spatial profiles with consistent axes and physical time labels. State the stability condition for the selected explicit scheme, if used. |
| 4. Build a loss | Define the observation and scalar loss in their own cell. Keep any synthetic target and its generating parameter visible. |
| 5. Differentiate | Show an autograd call and an explicit backward loop side by side conceptually. Seed the final adjoint; propagate through every step; record each local parameter contribution before summing. |
| 6. Check the sum | Compare manual reverse accumulation, PyTorch autograd and a centred finite-difference spacing sweep for the same fixed discrete map. Plot per-step gradient contributions. |
| 7. Use the gradient | Show the parameter update separately from differentiation; compare loss before and after a suitably chosen update. Do not present every gradient step as guaranteed to improve loss. |
| 8. Change one thing | Predict then change horizon, observation location or diffusivity; inspect the changed field and gradient. Include a runnable exercise, hint and independently checked solution. |

For a state update `u_next = S(u, p)`, use the same symbols as the existing
backpropagation chapter: `A_n` for the local state Jacobian, `B_n` for the
local parameter derivative and `lambda_n` for the adjoint. A fixed initial
condition and parameter-independent terminal loss remove the initial-state
and direct-loss derivative terms in this chosen experiment; explain why they
vanish rather than presenting their absence as a general rule. If intermediate
losses or parameter-dependent boundaries/observations are introduced, include
their extra adjoint sources and parameter contributions.

A finite-difference agreement checks the specified discrete computation at
the tested parameter and spacing. It does not establish continuum convergence,
global smoothness, identifiability or a fracture-path derivative. A truncated
time evolution is the intended forward model here; this differs from stopping
an iterative equilibrium solver before convergence. Do not conflate those
two meanings of unrolling.

Retain full-field plots and measured complete execution time after setup.
Follow the course's under-300-second acceptance criterion and report platform,
precision and exact command after running the finished notebook. Keep setup,
local execution and fresh-Colab evidence distinct. This note supplies no new
execution or visual-QA evidence; those gates remain the notebook author's and
integration review's work.

## Complementary primary teaching references and Colab review

Bounded follow-up, 9 September 2026: three current teaching pages were read,
with notebook/source formats checked. No external example was executed, and
no external code or image was copied. These references refine the existing
lesson; they do not add a JAX or FEniCS dependency to the PyTorch practical.

| Primary reference | Concrete structure to adapt |
| --- | --- |
| [JAX: Automatic differentiation](https://docs.jax.dev/en/latest/automatic-differentiation.html), [MyST/Jupytext source](https://github.com/jax-ml/jax/blob/831d9d4d8d5bf7b8a615992ff3fb8d749b6dd610/docs/automatic-differentiation.md) | Introduce a scalar derivative with a tiny executable example; compare a known analytic derivative; explicitly choose the differentiated argument; obtain loss and gradient; check scalar and directional derivatives numerically. Keep the chosen input, scalar output and expected derivative shape visible before an AD call. The page uses numerical output rather than field plots, so retain the diffusion lesson's spatial figures. |
| [DOLFINx: A known analytical solution](https://jsdokken.com/dolfinx-tutorial/chapter2/heat_code.html), [26-cell notebook](https://github.com/jorgensd/dolfinx-tutorial/blob/c752d010ddbabf98b3e71e7a562f07ad7a738c26/chapter2/heat_code.ipynb) | Alternate small prose/code cells for parameters, mesh, exact solution, boundary conditions, variational form, assembled objects and solver. Then expose the complete time loop and verify the final field. Its final nodal error and integrated L2 error answer different questions: exact nodal agreement does not imply an exact field between nodes. Our discrete-mode check should likewise retain its stated discrete scope. |
| [DOLFINx: Diffusion of a Gaussian function](https://jsdokken.com/dolfinx-tutorial/chapter2/diffusion_code.html), [29-cell notebook](https://github.com/jorgensd/dolfinx-tutorial/blob/c752d010ddbabf98b3e71e7a562f07ad7a738c26/chapter2/diffusion_code.ipynb) | Define the initial field and domain; create time-labelled output; explain reusable and changing solver objects; update, solve, save and plot within the visible time loop. Preserve physical time labels and consistent colour limits for comparison. The PyVista/ParaView and MPI/PETSc machinery belongs to that FEM example; lightweight static Matplotlib outputs suit the existing Colab lesson. |

Source snapshots: JAX `831d9d4d8d5bf7b8a615992ff3fb8d749b6dd610`;
DOLFINx tutorial `c752d010ddbabf98b3e71e7a562f07ad7a738c26`. JAX's repository
uses [Apache 2.0](https://github.com/jax-ml/jax/blob/831d9d4d8d5bf7b8a615992ff3fb8d749b6dd610/LICENSE).
The two inspected DOLFINx pages explicitly identify Jørgen S. Dokken and
distribute their adapted tutorial content under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Reused page material
would need credit, a licence link and an indication of changes. Both DOLFINx
chapters have paired `.ipynb` and Jupytext `.py` sources; their existence is
not evidence of a successful fresh Colab run. Use the patterns above in
original course material without importing the external runtime stack.

### Read-only Colab portability findings

The inspected diffusion builder has a useful minimal runtime boundary:
CPU tensors, explicit float64, standard PyTorch/NumPy/Matplotlib imports,
relative `diffusion_results` output, synthetic inputs and embedded PNGs.
Students should open the generated `.ipynb`; the authoring builder's Sphinx-
independent HTML renderer and local subprocess/kernel machinery are not
notebook dependencies. The reviewed local receipt identifies Python 3.10.18
and PyTorch 2.8.0 and explicitly records fresh Colab as untested.

Concrete checks for the notebook author and the actual Colab rehearsal:

1. **Do not count human reading as computation.** In the reviewed source,
   the final cell asserts that wall time since the early imports cell is under
   300 seconds. Manual teaching use would fail after a five-minute reading or
   exercise pause. Keep the hard execution gate in the automated runner;
   report interactive session time separately, or accumulate computation-only
   cell timings. This issue was sent to the builder's author for correction.
2. **Verify the delivered file in a fresh CPU runtime.** Open the exact notebook,
   restart, run every cell in order, and retain its package versions, numerical
   checks and complete run time. A Colab badge, proposed setup cell or local
   Linux/macOS run does not establish that this step passed.
3. **Keep setup small and reproducible.** The current optional unpinned
   `%pip install torch numpy matplotlib` is a proposed dependency route.
   Check the installed versions first; record the versions that actually pass
   in Colab and avoid an unnecessary accelerator or FEniCS installation.
4. **Check notebook presentation and saved outputs in Colab.** Confirm inline
   equations, all five plots and worked-answer controls render, and that NPZ
   and JSON reload succeed. Provide a clear way to download the resulting
   files from the session; writing a relative directory alone is not a learner
   handoff. Keep the independently readable static outputs available.
5. **Preserve evidence boundaries.** Report fresh Colab separately from local
   execution and from student-edited experiments. Keep changed-input
   assertions explained, and retain the distinction between a derivative
   check, successful synthetic recovery and physical/mesh convergence.

This is a source and design review, not a fresh Colab execution receipt.
