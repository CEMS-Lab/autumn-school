# Autumn School — Days 2 and 3

Choose the materials for your teaching day:

- **[Day 2 — Mechanics and Machine Learning](#machine-learning-notebooks-student-access):** six notebooks: NB1, NB2, NB3a, NB3b, NB5 and NB6, covering regression, neural networks, CNNs, physics-informed neural networks and neural operators.
- **[Day 3 — Fracture, Differentiability and PhAST](#day-3-phast):** three lecture guides and three PhAST practicals covering fracture simulation, parameter recovery and learned damage updates.

Basic mechanics, calculus and introductory Python provide the starting point.

(machine-learning-notebooks-student-access)=
## Day 2 — Mechanics and Machine Learning

All six notebooks are available in Google Colab. Click **Open in Colab**,
connect to a runtime, and run the cells in order. Use **Download notebook**
to save the Jupyter file for local use.
NB1, NB2, NB3a and NB3b download their datasets automatically when you run the data-loading cell.
The download buttons also let you save a copy for local use. NB5–6 generate
their training data within the notebooks.

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

NB3a and NB3b share the CNN dataset. The combined ZIP contains separate
`NB1`, `NB2` and `NB3` folders; use the `NB3` folder for both CNN notebooks.
For a local run, extract the individual dataset ZIP beside its notebook.

(day-3-phast)=
## Day 3 — Fracture, Differentiability and PhAST

These three PhAST notebooks are for **16 September 2026**. Click **Open in Colab**
to run them online, or **Download notebook** to save a local copy. NB3 also
provides the source and trained model in the **PhAST GNN assets ZIP**.
The notebooks include their supplied figures and animations.

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

Start with the [environment setup guide](../SETUP.md). NB1 and NB2 can use a CPU
runtime. **For NB3, select a GPU runtime in Colab before running the setup.**
NB3 downloads the supplied source and frozen model from `phast_gnn_assets.zip`
automatically; the resource button also provides the archive for local use.
The notebook verifies the source and checkpoint hashes before loading them.

The supplied outputs are preserved. These updated notebooks have not been rerun
end to end for this publication; a fresh whole-notebook Colab timing remains to
be measured. The older Helmholtz example remains in {doc}`further_practice`.

### Three connected lectures

| Lecture | Central question |
| --- | --- |
| {doc}`1. Phase-field fracture and PhAST <lectures/01_fracture_and_phast>` | How do geometry, material and loading produce a damage field? |
| {doc}`2. Differentiability and inverse applications <lectures/02_differentiability_and_inverse>` | How can a measured response tell us about an unknown input? |
| {doc}`3. Hybrid numerical and learned methods <lectures/03_hybrid_learning>` | How can a learned prediction work alongside a physical solver? |

The lecture guides connect the governing equations and illustrations to each
practical. Discussion questions provide opportunities to interpret the model
before running the corresponding calculation.

### What each practical covers

Each lab moves through **predict → explain → compute → inspect → exercise →
worked solution**. Short code cells introduce one operation at a time.
Expandable setup and implementation details keep the complete calculation
available for closer study.

| Practical | What you will do |
| --- | --- |
| {doc}`NB1 — Intro to PhAST <classroom/01_simulate_fracture>` | Inspect a notched specimen and its loading, run PhAST, and interpret crack propagation, energy curves and saved fields. |
| {doc}`NB2 — Inverse Problem using PhAST <classroom/02_gradients_and_recovery>` | Solve a 1D elastic bar with PhAST and recover its Young’s modulus from one force and one observed extension. |
| {doc}`NB3 — Hybrid FEM+DL with PhAST <classroom/03_learning_and_hybrid>` | Compare conventional FEM with a frozen graph neural network that replaces the damage subproblem on a three-hole plate. |

The optional {doc}`direct learned-replacement case study <w53_direct_replacement>`
connects Lab 3 to a retained Radius-GNO fracture trajectory and reports a
matched damage-stage timing comparison.

### Day 3 reference chapters and further practice

The reference chapters develop four complementary themes:

- **What Phase-Field Fracture Is:** energy, degradation and the length scale.
- **Hands-on with the PhAST Solver:** geometry, mesh, boundary conditions and results.
- **Differentiability and Inverse Problems:** computational graphs and checked gradients.
- **Deep Learning Integration:** training, model interfaces and physical correction.

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

The [interactive visual explorations](../explorations.html) accompany the
equations. The detailed notebooks remain available in {doc}`further_practice`
for independent study.

```{toctree}
:maxdepth: 1
:caption: Day 3 — Optional inverse experiments

research/index
```
