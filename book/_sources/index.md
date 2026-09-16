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

The materials below belong to Day 3. The PhAST practicals are labelled
**Lab 1–Lab 3**; the Day 2 machine learning notebooks above are labelled
**NB1, NB2, NB3a, NB3b, NB5 and NB6**. Each day has its own setup and data requirements.

### Three connected lectures

| Lecture | Central question |
| --- | --- |
| {doc}`1. Phase-field fracture and PhAST <lectures/01_fracture_and_phast>` | How do geometry, material and loading produce a damage field? |
| {doc}`2. Differentiability and inverse applications <lectures/02_differentiability_and_inverse>` | How can a measured response tell us about an unknown input? |
| {doc}`3. Hybrid numerical and learned methods <lectures/03_hybrid_learning>` | How can a learned prediction work alongside a physical solver? |

The lecture guides connect the governing equations and illustrations to each
practical. Discussion questions provide opportunities to interpret the model
before running the corresponding calculation.

### Three PhAST practical notebooks

Each lab moves through **predict → explain → compute → inspect → exercise →
worked solution**. Short code cells introduce one operation at a time.
Expandable setup and implementation details keep the complete calculation
available for closer study.

| Practical | What you will do |
| --- | --- |
| {doc}`Lab 1 — Simulate and interpret fracture <classroom/01_simulate_fracture>` | Inspect a notched specimen and its loading, run PhAST, and interpret crack propagation, energy curves and saved fields. |
| {doc}`Lab 2 — Gradients and parameter recovery <classroom/02_gradients_and_recovery>` | Solve a 1D elastic bar with PhAST and recover its Young’s modulus from one force and one observed extension. |
| {doc}`Lab 3 — Learned damage updates <classroom/03_learning_and_hybrid>` | Compare classical damage, a trained graph-network initial guess and checked direct replacement on a three-hole plate. |

The optional {doc}`direct learned-replacement case study <w53_direct_replacement>`
connects Lab 3 to a retained Radius-GNO fracture trajectory and reports a
matched damage-stage timing comparison.

The Day 3 notebook downloads use the files updated on **15 September 2026**. Each page
includes a Colab link, notebook downloads and one conceptual recap answer.
All three practicals use PhAST. The older Helmholtz training example remains
in {doc}`further_practice` as optional background.

Colab opens the notebooks on the published `main` branch. Local changes appear
there after publication; use the downloads below to inspect this edition.

| Open published edition | Download this edition |
| --- | --- |
| [Lab 1 in Colab](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/01_simulate_fracture.ipynb) | [Dynamic plate notebook](../notebooks/study/classroom/01_simulate_fracture.ipynb) |
| [Lab 2 in Colab](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/02_gradients_and_recovery.ipynb) | [Single-force bar notebook](../notebooks/study/classroom/02_gradients_and_recovery.ipynb) |
| [Lab 3 in Colab](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/03_learning_and_hybrid.ipynb) | [Learned damage notebook](../notebooks/study/classroom/03_learning_and_hybrid.ipynb) |

Start with the [environment setup guide](../SETUP.md). Lab 3 also requires the
instructor-supplied `mesh_graph_net.pt`; obtain it before starting. Lab 2 retains
its supplied figures and animation. Labs 1 and 3 generate their visual results
when executed. Runtime depends on mesh size, solver settings, comparisons and
animation export; a fresh whole-notebook Colab timing is still required.

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
:caption: Day 3 — Lecture guides

lectures/01_fracture_and_phast
lectures/02_differentiability_and_inverse
lectures/03_hybrid_learning
```

```{toctree}
:maxdepth: 1
:caption: Day 3 — PhAST practicals

classroom/01_simulate_fracture
classroom/02_gradients_and_recovery
classroom/03_learning_and_hybrid
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
