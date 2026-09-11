# Pedagogical, Textual, and Visual Design Directives

This document defines the authoritative quality and design directives for the PhAST Autumn School course companion, notebooks, and slides. Every human author and LLM agent must follow these directives to maintain the educational decorum of **[Dive into Deep Learning (D2L)](https://d2l.ai)** and **[Applied Deep Learning for Physics (ADL4P)](https://tum-pbs.github.io/ADL4P/)**.

---

## 1. Tone and Textual Standards

### A. Educational Decorum
- **Audience:** Written in plain, clear, and encouraging educational language accessible to an **undergraduate student** in engineering, physics, or computer science.
- **Tone:** Objective, pedagogical, welcoming, and clear. Avoid dramatic storytelling, conversational filler, and defensive administrative bureaucracy.
- **Pedagogical Flow:** Always introduce physical intuition and real-world mechanics context *before* presenting formal variational equations, discrete tensors, or code blocks.

### B. Prohibited Phrasing & Linguistic Anti-Patterns
1. **NO Negative / Failure-Obsessed Framing:**
   - ❌ *Avoid:* "Why average predictions fail", "the stationary trap", "a fatal flaw", "these are the limiting factors", "the solver fails", "failed recovery".
   -  *Use:* "Branch selection in multi-valued energy landscapes", "stationary points in non-convex potentials", "domain of applicability", "assumptions and trade-offs", "convergence criteria".
2. **NO Binary / Contrastive AI Formulas ("X, not Y" and "While A, B is not done"):**
   - ❌ *Avoid:* "A quasi-Newton method describes a nonlinear solver, while XFEM describes a crack representation", "A neural model is an adapter, not a solver", "While that is done, this is left undone".
   -  *Use:* State concepts constructively and define their modular relationships clearly without correcting an imaginary opponent.
3. **NO Compliance Checklists & Log-Dumping Quizzes:**
   - ❌ *Avoid:* Mandating rigid "Minimum result cards" or quizzing students on verifying 10-digit floating-point outputs from specific runs.
   -  *Use:* Meaningful engineering exercises that test conceptual understanding (e.g., Taylor series truncation error analysis, physical consequences of branch averaging, varying length scale $\ell$ to inspect damage width).

---

## 2. Notebook Structure & Anatomy (The D2L / ADL4P Blueprint)

Every tutorial notebook must follow a standardized 6-part anatomy:

1. **Header & Action Badges:**
   - Title (`# Clear, Descriptive Title`)
   - **Learning Objective:** A 1–2 sentence pedagogical summary of what the student will build and understand.
   - Action badges: One-click `[Open in Colab]` badge (`colab-badge.svg`), `[Download Practice Notebook]`, `[Download with Worked Solutions]`, and `[Environment Setup]`.
2. **Interactive Cloud Execution (Google Colab Ready):**
   - The opening code cell must include automated Google Colab detection and bootstrapping: cloning `https://github.com/CEMS-Lab/autumn-school.git` if running on a fresh cloud instance and setting `sys.path` to include `notebooks/` and `vendor/PhAST/src` without requiring manual file uploads.
3. **Physical Motivation & Governing Equations:**
   - Concise conceptual introduction with an intuitive physical diagram or schematic.
   - Clean mathematical formulation with all symbols defined upon appearance.
3. **Step-by-Step Code Walkthrough:**
   - Code blocks interleaved with explanatory markdown.
   - Clear comments explaining tensor dimensions, coordinate conventions, boundary masks, and PyTorch autograd calls.
4. **Physical Interpretation of Results:**
   - Visual inspection of spatial fields (displacement $u$, damage $d$) and integral curves (reaction force vs. displacement).
   - Direct explanation of what the plots reveal about material physics (elastic stretching, peak load, crack localization, softening).
5. **Key Takeaways (Summary):**
   - 3–4 bullet points summarizing the core physical and numerical concepts.
6. **Student Exercises (with Expandable Hints and Worked Solutions):**
   - **Exercise 1 (Analytical / Conceptual):** Deriving a formula, proving a property, or reasoning about physical scales.
   - **Exercise 2 (Numerical / Practical):** Modifying a parameter in code, testing convergence, or evaluating trade-offs.
   - Each exercise must feature collapsible `Hint` and `Worked Solution` dropdown admonitions.

---

## 3. Visual and Plotting Standards

### A. Document Typography & Layout
- **Prose Font:** Clean system sans-serif stack (`Inter`, `-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`, `Helvetica Neue`).
- **Code Font:** Modern monospace stack (`ui-monospace`, `SF Mono`, `Source Code Pro`, `JetBrains Mono`, `Menlo`, `Consolas`).
- **Headings:** Bold, clean, modern headers with subtle accent bars.
- **Callout Admonitions:** Clean native Sphinx/Bootstrap admonitions (`note`, `tip`, `important`) with soft backgrounds and high contrast in both dark and light modes.

### B. Matplotlib Plotting Directives
All generated plots in notebooks and book chapters must follow strict publication-grade formatting:
```python
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 11,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 13,
    'figure.dpi': 150,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'lines.linewidth': 1.8,
})
```
- **Color Palettes:**
  - For line plots: High-contrast palettes with distinct line styles (`-`, `--`, `-.`) for accessibility.
  - For continuous scalar fields (damage $d$, strain energy $\psi^+$): Perceptually uniform colormaps (`viridis`, `magma`, `plasma`, `coolwarm`).
  - Label colorbars clearly with the field symbol, convention ($d=0$ intact, $d=1$ broken), and physical units.
- **Axes & Labels:** Always label axes with physical quantities and units (e.g., `Applied Displacement u [mm]`, `Reaction Force F [kN]`).
- **Layout:** Always use `plt.tight_layout()` or `layout='constrained'` to prevent label clipping.

---

## 4. Course Curriculum Mapping (Six-Hour Workshop)

The current six-hour event window contains a 150-minute lecture core and three
50-minute practicals, with 60 minutes for breaks, questions and support.
Issue #20 and TEACHING_SCHEDULE.md supersede the earlier contact-time allocation.
The four conceptual pillars remain, grouped into three classroom notebooks:

| Pillar | Core Theme | Lecture Milestone | Hands-On Lab Notebook |
| :--- | :--- | :--- | :--- |
| **1. Phase-Field Fundamentals** | Physics of brittle fracture & diffuse crack bands | Chapters 1 & 2: Griffith energy, regularisation $\ell$, $g(d)$, AT1 vs. AT2 | **Classroom Lab 2:** Degradation derivatives followed by elastic-bar recovery |
| **2. End-to-End Simulation** | Finite element tensors & staggered solver | Chapters 3 & 4: Weak forms, T3 meshing, boundary conditions, staggered loop | **Classroom Lab 1:** Notched tension in PhAST, fields and reaction curves |
| **3. Differentiable Mechanics** | Automatic differentiation & inverse discovery | Chapter 5 & 5a: Computational graphs, VJPs, gradient verification | **Classroom Lab 2:** Differentiable 1D bar, sensitivity verification and modulus recovery |
| **4. Deep Learning Integration** | Plug-and-play neural surrogates & hybrid loops | Chapter 6: Neural operators, model checkpoints, physics residual gating | **Classroom Lab 3:** Train, save, reload, assess and correct a teaching field |

The original six notebooks remain in the detailed-reference library. The
algebraic teaser is optional self-study.

### Concise classroom code

- Whole-notebook execution, plots and exports must complete in less than 120
  seconds. Target 60 seconds locally and retain a fresh Colab timing receipt.
  Record dependency installation separately. This supersedes earlier runtime
  budgets; the full policy is in `source/planning/RUNTIME_POLICY_20260911.md`.

- Aim for at most 12 nonblank lines per visible code cell and one clear purpose.
- Introduce each operation in a short Markdown paragraph before its cell.
- Keep the material, boundary conditions, loading, solver call, autograd call
  and prediction → loss → backward → optimiser step visible.
- Fold environment setup, long plotting and validation details in HTML and
  provide compatible collapsed-input metadata for notebook readers.
- Keep supporting functions inspectable, documented and covered by runtime
  receipts; a short cell must preserve the numerical inputs and scientific scope.
- Use labelled example outlines and animation storyboards for requested future
  content. Reserve author assignments and acceptance checks for planning files.
