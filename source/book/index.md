# Autumn School — Days 2 and 3

**Lecturer: [Sathiskumar Anusuya Ponnusami](https://saponnusami.com)**  
Queen Mary University of London.

This course introduces machine learning methods for computational mechanics,
with applications to fracture simulation, material parameter identification
and hybrid finite element models. Lectures develop the mathematical formulation;
Jupyter notebooks provide worked computational examples.

**Prerequisites:** Undergraduate mechanics, calculus and introductory Python programming.

**Course materials:** Lecture notes, Jupyter notebooks, datasets, visual demonstrations
and worked exercises.

- **[Day 2 — Mechanics and Machine Learning](#machine-learning-notebooks-student-access):** six notebooks covering regression, neural networks, convolutional neural networks, physics-informed neural networks and neural operators.
- **[Day 3 — Fracture, Differentiability and PhAST](#day-3-phast):** three lecture guides and three PhAST practicals covering fracture simulation, parameter recovery and learned damage updates.

(machine-learning-notebooks-student-access)=
## Day 2 — Mechanics and Machine Learning

The Day 2 notebooks introduce supervised learning, convolutional models for
microstructure data, physics-informed neural networks and neural operators.
Examples connect model formulation, training and interpretation of predictions.

**Notebook access:** Select **Open in Colab** to run a notebook online, or
**Download notebook** for local Jupyter use. Run the cells in order, beginning
with the installation and data-loading cells.

```{raw} html
<div style="overflow-x:auto">
<table class="table"><thead><tr><th>Notebook</th><th>Google Colab</th><th>Notebook download</th><th>Dataset</th></tr></thead><tbody>
<tr><td>NB1: Linear and Logistic Regression</td><td><a class="badge-link" href="https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/machine_learning/NB1_Linear_and_Logistic_Regression.ipynb" target="_blank" rel="noopener"><img src="_static/colab-badge.svg" alt="Open in Colab" width="117" height="20" style="min-width:117px;max-width:none;height:20px"></a></td><td><a class="badge-link" href="../notebooks/machine_learning/NB1_Linear_and_Logistic_Regression.ipynb" download>Download notebook</a></td><td><a class="badge-link" href="../datasets/machine_learning/NB1_data.zip" download>Download NB1 data</a></td></tr>
<tr><td>NB2: Neural Networks</td><td><a class="badge-link" href="https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/machine_learning/NB2_Neural_Networks.ipynb" target="_blank" rel="noopener"><img src="_static/colab-badge.svg" alt="Open in Colab" width="117" height="20" style="min-width:117px;max-width:none;height:20px"></a></td><td><a class="badge-link" href="../notebooks/machine_learning/NB2_Neural_Networks.ipynb" download>Download notebook</a></td><td><a class="badge-link" href="../datasets/machine_learning/NB2_data.zip" download>Download NB2 data</a></td></tr>
<tr><td>NB3a: How a CNN Works</td><td><a class="badge-link" href="https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/machine_learning/NB3a_How_a_CNN_Works.ipynb" target="_blank" rel="noopener"><img src="_static/colab-badge.svg" alt="Open in Colab" width="117" height="20" style="min-width:117px;max-width:none;height:20px"></a></td><td><a class="badge-link" href="../notebooks/machine_learning/NB3a_How_a_CNN_Works.ipynb" download>Download notebook</a></td><td><a class="badge-link" href="../datasets/machine_learning/NB3_data.zip" download>Download CNN data</a></td></tr>
<tr><td>NB3b: CNNs on Microstructures</td><td><a class="badge-link" href="https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/machine_learning/NB3b_CNNs_on_Microstructures.ipynb" target="_blank" rel="noopener"><img src="_static/colab-badge.svg" alt="Open in Colab" width="117" height="20" style="min-width:117px;max-width:none;height:20px"></a></td><td><a class="badge-link" href="../notebooks/machine_learning/NB3b_CNNs_on_Microstructures.ipynb" download>Download notebook</a></td><td><a class="badge-link" href="../datasets/machine_learning/NB3_data.zip" download>Download CNN data</a></td></tr>
<tr><td>NB5: Physics Informed Neural Networks</td><td><a class="badge-link" href="https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/machine_learning/NB5_Physics_Informed_Neural_Networks.ipynb" target="_blank" rel="noopener"><img src="_static/colab-badge.svg" alt="Open in Colab" width="117" height="20" style="min-width:117px;max-width:none;height:20px"></a></td><td><a class="badge-link" href="../notebooks/machine_learning/NB5_Physics_Informed_Neural_Networks.ipynb" download>Download notebook</a></td><td>Generated in the notebook</td></tr>
<tr><td>NB6: Neural Operators</td><td><a class="badge-link" href="https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/machine_learning/NB6_Neural_Operators.ipynb" target="_blank" rel="noopener"><img src="_static/colab-badge.svg" alt="Open in Colab" width="117" height="20" style="min-width:117px;max-width:none;height:20px"></a></td><td><a class="badge-link" href="../notebooks/machine_learning/NB6_Neural_Operators.ipynb" download>Download notebook</a></td><td>Generated in the notebook</td></tr>
</tbody></table></div>
<p><a class="badge-link" href="../datasets/machine_learning/All_notebook_data.zip" download>Download all notebook datasets (ZIP)</a></p>
```

**Datasets:** NB1, NB2, NB3a and NB3b download their data automatically;
NB5 and NB6 generate training data within the notebooks.
NB3a and NB3b share the CNN dataset. The combined ZIP contains separate
`NB1`, `NB2` and `NB3` folders; use the `NB3` folder for both CNN notebooks.
For a local run, extract the individual dataset ZIP beside its notebook.

(day-3-phast)=
## Day 3 — Fracture, Differentiability and PhAST

**Teaching date:** 16 September 2026.

Day 3 develops three applications of PhAST: dynamic fracture simulation,
gradient-based recovery of an elastic modulus, and a learned replacement for
the damage subproblem. Each practical includes code, saved numerical results
and visualisations.

**Notebook access:** The table below provides Colab links and local downloads.
The **PhAST GNN assets ZIP** contains the solver source and trained model used in NB3.

```{raw} html
<span id="three-phast-practical-notebooks"></span>
```

```{raw} html
<div class="ml-notebook-access" style="overflow-x:auto;">
<table class="table">
<thead><tr><th>Day 3 notebook</th><th>Run online</th><th>Download</th><th>Resources</th></tr></thead>
<tbody>
<tr><td>NB1 — Intro to PhAST</td><td><a class="badge-link" href="https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/NB1%20-%20Intro%20to%20PhAST.ipynb" target="_blank" rel="noopener"><img src="_static/colab-badge.svg" alt="Open in Colab" width="117" height="20" style="min-width:117px;max-width:none;height:20px"></a></td><td><a class="badge-link" href="../notebooks/study/classroom/NB1%20-%20Intro%20to%20PhAST.ipynb" download>Download notebook</a></td><td>Prepared in the notebook</td></tr>
<tr><td>NB2 — Inverse Problem using PhAST</td><td><a class="badge-link" href="https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/NB2%20-%20Inverse%20Problem%20using%20PhAST.ipynb" target="_blank" rel="noopener"><img src="_static/colab-badge.svg" alt="Open in Colab" width="117" height="20" style="min-width:117px;max-width:none;height:20px"></a></td><td><a class="badge-link" href="../notebooks/study/classroom/NB2%20-%20Inverse%20Problem%20using%20PhAST.ipynb" download>Download notebook</a></td><td>Prepared in the notebook</td></tr>
<tr><td>NB3 — Hybrid FEM+DL with PhAST</td><td><a class="badge-link" href="https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/NB3%20-%20Hybrid%20FEM%2BDL%20with%20PhAST.ipynb" target="_blank" rel="noopener"><img src="_static/colab-badge.svg" alt="Open in Colab" width="117" height="20" style="min-width:117px;max-width:none;height:20px"></a></td><td><a class="badge-link" href="../notebooks/study/classroom/NB3%20-%20Hybrid%20FEM%2BDL%20with%20PhAST.ipynb" download>Download notebook</a></td><td><a class="badge-link" href="../datasets/phast/phast_gnn_assets.zip" download>Download PhAST GNN assets ZIP</a></td></tr>
</tbody></table></div>
```

**Computing requirements:** NB1 and NB2 support a CPU runtime.
**NB3 requires a GPU runtime in Colab.** Follow the
[environment setup guide](../SETUP.md) and the installation cells in each notebook.
NB3 downloads and verifies its solver source and trained model automatically.

**Saved results:** The book displays the outputs supplied with the notebooks.
The notebooks were not rerun end to end for this edition. New calculations
require execution in Colab or a local Jupyter environment.

### Lecture topics

| Lecture | Topics |
| --- | --- |
| {doc}`1. Phase-field fracture and PhAST <lectures/01_fracture_and_phast>` | Fracture energy, damage evolution, finite element discretisation and boundary conditions. |
| {doc}`2. Differentiability and inverse applications <lectures/02_differentiability_and_inverse>` | Automatic differentiation, sensitivity analysis, derivative verification and parameter recovery. |
| {doc}`3. Hybrid numerical and learned methods <lectures/03_hybrid_learning>` | Learned field predictions, model integration and comparison with finite element solutions. |

### Practical learning outcomes

On completion of the practicals, students should be able to:

| Practical | Learning outcome |
| --- | --- |
| {doc}`NB1 — Intro to PhAST <classroom/01_simulate_fracture>` | Inspect a notched specimen and its loading, run PhAST, and interpret crack propagation, energy curves and saved fields. |
| {doc}`NB2 — Inverse Problem using PhAST <classroom/02_gradients_and_recovery>` | Solve a 1D elastic bar with PhAST and recover its Young’s modulus from one force and one observed extension. |
| {doc}`NB3 — Hybrid FEM+DL with PhAST <classroom/03_learning_and_hybrid>` | Compare conventional FEM with a frozen graph neural network that replaces the damage subproblem on a three-hole plate. |

The optional {doc}`direct learned-replacement case study <w53_direct_replacement>`
extends NB3 with a Radius-GNO fracture example and a comparison of damage-update
computation times under matched conditions.

### Day 3 reference chapters and further practice

The reference chapters provide additional mathematical and computational detail:

- **Phase-field fracture:** energy, degradation and the regularisation length scale.
- **Finite element simulation:** geometry, mesh, boundary conditions and field interpretation.
- **Differentiability and inverse problems:** computational graphs and derivative verification.
- **Machine learning integration:** training, model interfaces and physical correction in the supplementary examples.

Throughout the book, $d=0$ denotes intact material and $d=1$ denotes fully
damaged material. Symbols and assumptions are introduced beside their equations.

```{toctree}
:maxdepth: 1
:caption: Day 3 — PhAST practicals

classroom/01_simulate_fracture
classroom/02_gradients_and_recovery
classroom/03_learning_and_hybrid
```

```{toctree}
:maxdepth: 1
:caption: Day 3 — Lecture guides

lectures/01_fracture_and_phast
lectures/02_differentiability_and_inverse
lectures/03_hybrid_learning
```

```{toctree}
:maxdepth: 1
:caption: Day 3 — Optional direct-replacement case study

w53_direct_replacement
```

```{toctree}
:maxdepth: 1
:caption: Day 3 — Reference chapters

00_welcome_and_routes
01_crack_representations
02_phase_field_energy
03_staggered_solution
04_fem_to_tensors
05_differentiation_and_inverse
06_learning_adapter
07_practice_references
further_practice
```

The [interactive visual explorations](../explorations.html) illustrate the
governing equations. {doc}`further_practice` includes supplementary notebooks
and the scalar Helmholtz example for independent study.

```{toctree}
:maxdepth: 1
:caption: Day 3 — Optional inverse experiments

research/index
```

(offline-reading)=
### Offline reading

**Offline edition:** The Day 3 PDF contains the lecture notes, worked notebooks
and reference chapters, including equations, code and saved plots. Animations
are represented by selected frames.

Internal documentation for course participants. Copyrighted material; not to be
distributed.

```{raw} html
<p><a href="../downloads/PhAST_Autumn_School_2026_Day3.pdf" download>Download the Day 3 book (PDF, 7.3 MB)</a></p>
```

Running the notebooks in Colab and opening the linked animations requires an
internet connection.
