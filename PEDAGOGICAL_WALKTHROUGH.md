# Pedagogical Overhaul: Implementation Plan & Walkthrough Artifact

This document records the design transformation of the **PhAST Autumn School** interactive textbook and computational lab notebooks (`https://cems-lab.github.io/autumn-school/book/`), aligning the course with the pedagogical decorum of **[Dive into Deep Learning (D2L)](https://d2l.ai)** and **[Applied Deep Learning for Physics (ADL4P)](https://tum-pbs.github.io/ADL4P/)**.

---

## 1. Implementation Plan & Motivation

### Background
The initial course materials were drafted by an automated LLM agent under rigid compliance prompts. This produced characteristic AI anti-patterns:
- **Dramatic, failure-focused phrasing:** Over-emphasizing what fails or breaks (e.g. "Why average predictions can fail", "the stationary trap", "limiting factors").
- **Binary contrastive tropes:** Correcting imaginary opponents using rigid "X, not Y" or "while that is done, this is left undone" syntax.
- **Bureaucratic compliance checklists:** Mandating repetitive "minimum result cards" and testing students on verifying 10-digit floating-point outputs from specific runs.
- **Lecturing meta-commentary:** Excessive discussion of what the software does not do, rather than guiding students through the physical mechanisms.

### Architectural Transformation
The course was refactored around a **six-hour curriculum** (3 hours interactive demonstration + 3 hours practical lab exercises) structured into four clear computational milestones:
1. **Pillar 1: Phase-Field Fracture Fundamentals** (Chapters 1 & 2 + Lab 02): Variational Griffith energy, regularisation length scale $\ell$, degradation function $g(d)$, and AT1 vs. AT2 models.
2. **Pillar 2: End-to-End Simulation with PhAST** (Chapters 3 & 4 + Lab 01): Structured T3 meshing, Dirichlet and notch boundary conditions, staggered displacement-damage solver, reaction force curves, and diffuse crack visualization.
3. **Pillar 3: Differentiability and Inverse Discovery** (Chapters 5 & 5a + Lab 03): PyTorch automatic differentiation, directional finite differences, vector-Jacobian products through staggered updates, and inverse parameter identification.
4. **Pillar 4: Deep Learning as Plug-and-Play** (Chapter 6 + Labs 04 & 05): Training neural field adapters, model checkpoint saving/reloading, residual-gated proposal evaluation, and hybrid solver corrections.

---

## 2. Walkthrough of Changes Made

### A. Book Chapters Overhauled (`source/book/`)
- **`index.md`:** Welcoming, tutorial introduction establishing the 4 pillars and course workflow.
- **`00_welcome_and_routes.md`:** Replaced bureaucratic checklists with engineering best practices (Problem Setup, Discretization, Observations, Verification).
- **`01_crack_representations.md`:** Introduced a comprehensive comparative table (Sharp vs. CZM vs. XFEM vs. Phase Field) and eliminated defensive "X not Y" contrastive prose.
- **`02_phase_field_energy.md`:** Clear derivation of AT1 and AT2 energy functionals, degradation derivatives, and cohesive lab link.
- **`03_staggered_solution.md`:** Clean presentation of linear momentum balance, the damage subproblem (diffusion analogy), and the staggered alternating minimization loop.
- **`04_fem_to_tensors.md`:** Connecting continuous weak forms to discrete PyTorch tensors, element quadrature, and the flagship PhAST simulation tutorial.
- **`05_differentiation_and_inverse.md`:** Mathematical formulation of autodiff vs. finite differences and gradient-based parameter recovery.
- **`06_learning_adapter.md`:** Refactored evaluation section to focus on physical residuals, admissibility constraints, and generalization rather than failure modes.
- **`07_practice_references.md`:** Synthesized key takeaways, best practices for computational exploration, and review questions.

### B. Lab Notebooks Overhauled (`source/book/labs/`)
All notebooks were upgraded with:
- Standardized action badges (`[Download Practice Notebook]`, `[Download with Worked Solutions]`, `[Environment Setup]`, `[Open in Colab]`).
- Clear, undergraduate-friendly learning objectives.
- Meaningful engineering exercises with collapsible `Hint` and `Worked Solution` dropdowns, eliminating all floating-point verification quizzes.

### C. Visual Styling (`source/book/_static/learning_book.css`)
- Modern system sans-serif typography (`Inter`, `-apple-system`, `Segoe UI`, `Roboto`).
- Crisp monospace stack for code blocks (`ui-monospace`, `SF Mono`, `Source Code Pro`).
- Softened header accent line (`h1::after`).
- Styled badge links (`.badge-row`, `.badge-link`) for all notebook tutorials.

---

## 3. Highlighting and Automated Verification

To ensure that future contributions and automated builds continuously maintain these standards without causing delays:
1. **Authoritative Directives Document:** [DESIGN_DIRECTIVES.md](DESIGN_DIRECTIVES.md) codifies tone, forbidden phrases, notebook anatomy, and Matplotlib plotting parameters.
2. **Automated Sphinx Build Hook:** `scripts/check_design_directives.py` validates compliance in **under 0.05 seconds** on every Sphinx HTML build.
3. **Smoke Check Integration:** `scripts/check_book_theme.py` enforces directives compliance as part of repository validation.
