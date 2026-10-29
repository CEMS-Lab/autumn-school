# UKACM Autumn School 2026 — Mechanics and Machine Learning

Lecture notes and Jupyter notebooks for Days 2 and 3 of the UKACM Autumn School
2026. The course connects machine learning with solid mechanics, phase-field
fracture, differentiable simulation and inverse problems.

**Lecturer: [Sathiskumar Anusuya Ponnusami](https://saponnusami.com)**

Queen Mary University of London.

**[Read the course book](https://cems-lab.github.io/autumn-school/book/index.html)** ·
**[Open the notebooks](https://cems-lab.github.io/autumn-school/book/index.html#machine-learning-notebooks-student-access)** ·
**[Report an issue](https://github.com/CEMS-Lab/autumn-school/issues)**

## Day 2 — Mechanics and Machine Learning

Six notebooks introduce the main methods through explanations, code and visual
examples:

- **NB1:** Linear and Logistic Regression
- **NB2:** Neural Networks
- **NB3a:** How a CNN Works
- **NB3b:** CNNs on Microstructures
- **NB5:** Physics Informed Neural Networks
- **NB6:** Neural Operators

The [Day 2 notebook page](https://cems-lab.github.io/autumn-school/book/index.html#machine-learning-notebooks-student-access)
provides **Open in Colab** buttons, notebook downloads and dataset downloads.
NB1, NB2, NB3a and NB3b download their datasets through the data-loading cells;
NB5 and NB6 generate their training data within the notebooks.

## Day 3 — Fracture, Differentiability and PhAST

Three practicals use [PhAST](https://github.com/CEMS-Lab/PhAST) to connect
finite element simulation, automatic differentiation and learned models.

| Practical | Main example | Run online |
| --- | --- | --- |
| [NB1 — Intro to PhAST](https://cems-lab.github.io/autumn-school/book/classroom/01_simulate_fracture.html) | Simulate fracture in a notched plate and examine the evolving fields. | [Open in Colab](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/NB1%20-%20Intro%20to%20PhAST.ipynb) |
| [NB2 — Inverse Problem using PhAST](https://cems-lab.github.io/autumn-school/book/classroom/02_gradients_and_recovery.html) | Recover a bar's Young's modulus from one applied force and one observed tip displacement. | [Open in Colab](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/NB2%20-%20Inverse%20Problem%20using%20PhAST.ipynb) |
| [NB3 — Hybrid FEM+DL with PhAST](https://cems-lab.github.io/autumn-school/book/classroom/03_learning_and_hybrid.html) | Compare FEM with a trained graph neural network that directly replaces the damage subproblem. | [Open in Colab](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/NB3%20-%20Hybrid%20FEM%2BDL%20with%20PhAST.ipynb) |

The [Day 3 course page](https://cems-lab.github.io/autumn-school/book/index.html#day-3-phast)
includes the lecture guides, notebook downloads and
[PhAST GNN assets](https://cems-lab.github.io/autumn-school/datasets/phast/phast_gnn_assets.zip)
for NB3. Reference chapters explain the governing equations and numerical methods.

## Getting started

Basic mechanics, calculus and introductory Python are useful prerequisites.
Open a notebook in Colab, connect to a runtime, and run its cells in order.
Use a fresh runtime and follow the notebook's installation cells. Day 3 NB1
and NB2 support CPU execution; **select a GPU runtime for Day 3 NB3**.
For local Jupyter use, follow the [setup guide](SETUP.md).

The online book displays saved notebook outputs, including figures and
animations. Run the notebooks to calculate new results or explore different
parameters. The [offline reading section](https://cems-lab.github.io/autumn-school/book/index.html#offline-reading)
provides a PDF of the Day 3 materials for course participants with limited
internet access. The PDF is internal documentation and is not to be distributed.

## Course materials and acknowledgements

Course materials prepared by [Allamaprabhu Ani](https://allamaprabhuani.github.io)
and [Sathiskumar Anusuya Ponnusami](https://saponnusami.com), CEMS-Lab,
for the [UKACM Autumn School 2026](https://www.ukacm-school.uk/home).

See [sources and attribution](ATTRIBUTION.md) and
[third-party notices](THIRD_PARTY_NOTICES.md) for references and software
licences. Please contact the course authors before republishing or adapting
the original teaching materials.

Corrections and suggestions are welcome through
[GitHub issues](https://github.com/CEMS-Lab/autumn-school/issues).
[Contributor guidance](CONTRIBUTING.md) explains how to edit the source and
rebuild the book.
