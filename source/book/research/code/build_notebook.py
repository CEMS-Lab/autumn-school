"""Assemble a self-contained notebook; numerical execution is a separate HPC step."""
import ast
import base64
import hashlib
import re
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parents[1]
lab = (ROOT / "code/lab.py").read_text()
plot_source = (ROOT / "code/render.py").read_text()
functions = {node.name: ast.get_source_segment(lab, node)
             for node in ast.parse(lab).body if isinstance(node, ast.FunctionDef)}
plots = {}
active = False
statements = []
for node in ast.parse(plot_source).body:
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "g" for t in node.targets):
        active = True
    if not active:
        continue
    statements.append(ast.get_source_segment(plot_source, node))
    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "save":
        name = ast.literal_eval(node.value.args[1])
        plots[name] = "\n".join(statements)
        statements = []
        if name == "hybrid":
            break
assert len(plots) == 7

cells = []
def md(text):
    text = re.sub(r":::\{admonition\} (.*?)\n:class: dropdown\n", r"### \1\n", text)
    text = re.sub(r"^:::\s*$", "", text, flags=re.M)
    cells.append(nbformat.v4.new_markdown_cell(text.strip()))

def code(text):
    cells.append(nbformat.v4.new_code_cell(text.strip()))

md("""# From gradients to reliable inverse experiments

## A self-contained computational notebook

We work from particle geometry and observations to gradients, optimisation,
uncertainty and a learned initial guess. All derivations needed for the six
executed examples, the complete numerical and plotting code, and the worked
answers are included below. External references are optional.

Prerequisites: scalar differentiation, vectors and matrix multiplication.
The examples are analytic and small linear-algebra models, adapted to
questions that arise in fracture inversion. Their successful results do not
constitute a new full fracture-inverse demonstration.

### Environment and execution

Python 3.11, NumPy, PyTorch, Matplotlib 3.7 or newer, and IPython are required.
Jupyter or another notebook reader displays the retained outputs. No local
data files, helper modules, network downloads or course checkout are needed.
Run the cells in order. This project's research executions use HPC.
Installation and queue time are separate from whole-notebook execution time.
Dependencies can be installed in an isolated environment with:

    python -m pip install numpy torch 'matplotlib>=3.7' ipython jupyter

### What to inspect

1. State the unknowns and observations before interpreting a recovery.
2. Predict each plot, run its cells, then compare with the worked explanation.
3. Keep derivative correctness, recovered parameters and computational cost
   as separate questions.
4. Full numerical arrays and check outcomes remain in the final cell's
   in-memory dictionaries, including inconvenient or negative findings.
""")
attachment = base64.b64encode((ROOT / "figures/inverse_workflow.png").read_bytes()).decode()
cell = nbformat.v4.new_markdown_cell(
    "![Inverse workflow: parameters, forward states, observations, loss, reverse sensitivity and update.](attachment:workflow.png)")
cell["attachments"] = {"workflow.png": {"image/png": attachment}}
cells.append(cell)
code("""import time
notebook_started = time.perf_counter()
import platform
from io import BytesIO
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.lines import Line2D
from IPython.display import Image, display

torch.set_default_dtype(torch.float64)
torch.set_num_threads(2)
plt.rcParams.update({
    "font.family": "STIXGeneral", "mathtext.fontset": "stix",
    "font.size": 12, "axes.titlesize": 13, "axes.labelsize": 12,
    "legend.fontsize": 10, "figure.dpi": 130,
})
BLUE, ORANGE, GREEN = "#0072B2", "#D55E00", "#009E73"
results, checks = {}, {}
d = results

def save(fig, name):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=180, bbox_inches="tight", pad_inches=.12)
    display(Image(data=buffer.getvalue(), alt=name.replace("_", " ")))
    plt.close(fig)

print({"python": platform.python_version(), "torch": torch.__version__,
       "numpy": np.__version__, "matplotlib": matplotlib.__version__,
       "device": "CPU", "dtype": str(torch.get_default_dtype())})
""")

chapters = [
    ("01_geometry", ["geometry"]),
    ("02_observations", ["quadrature"]),
    ("03_derivatives", ["solve_loss", "derivatives"]),
    ("04_recovery", ["conditioning", "observations"]),
    ("05_learning", ["hybrid"]),
    ("06_applications", []),
]
figure_re = re.compile(r"```\{figure\} figures/(\w+)\.png\n(.*?)\n```", re.S)
for name, names in chapters:
    text = (ROOT / (name + ".md")).read_text()
    position = 0
    inserted = False
    for match in figure_re.finditer(text):
        md(text[position:match.start()])
        if not inserted:
            definitions = "\n\n".join(functions[n] for n in names)
            calls = []
            for n in names:
                if n == "solve_loss":
                    continue
                calls.append(f"results[{n!r}], outcomes = {n}()\n"
                             "checks.update({key: bool(value) for key, value in outcomes.items()})\n"
                             "print(outcomes)\nassert all(outcomes.values())")
            code(definitions + "\n\n" + "\n\n".join(calls))
            inserted = True
        code(plots[match.group(1)])
        caption = "\n".join(line for line in match.group(2).splitlines() if not line.startswith(":"))
        md(caption)
        position = match.end()
    md(text[position:])

md("""# Inspect the results together

The following summary is calculated from this notebook's own execution.
The complete FD sweep and optimisation paths remain in `results`; the
figures do not replace those arrays. The checks include the deliberately
retained zero separating gradient at coincident centres.
""")
code("""assert len(checks) == 15 and all(checks.values()), checks
print(f"Checks passed: {sum(checks.values())} / {len(checks)}")
print(f"AD derivative: {results['derivatives']['ad']:.6g}")
print(f"Implicit derivative: {results['derivatives']['implicit']:.6g}")
print(f"Best sampled FD discrepancy: {min(results['derivatives']['relative_error']):.3g}")
truth = np.array(results["observations"]["truth"])
for i, path in enumerate(results["observations"]["models"]["two_observations"]["paths"]):
    print(f"Two-observation estimate from start {i+1}: {path[-1][:2]}; "
          f"parameter error {np.linalg.norm(np.array(path[-1][:2])-truth):.3g}")
print("CG iterations, zero / learned start:",
      len(results["hybrid"]["zero_residuals"])-1,
      len(results["hybrid"]["warm_residuals"])-1)
notebook_seconds = time.perf_counter() - notebook_started
print(f"Cell execution including imports and rendering: {notebook_seconds:.2f} s")
assert notebook_seconds < 300, "Notebook execution exceeded the course budget."
""")
md("""# Further reading and scope

The original explanations and examples above are self-contained.
[Advanced Deep Learning for Physics](https://tum-pbs.github.io/ADL4P/)
informed the question--derivation--computation approach. Its lectures are
additional perspectives, not prerequisites for reproducing this notebook.

The application protocols describe subsequent fracture research, GNNs,
observation selection and probabilistic inference. These are distinguished
from the six computations actually executed here. In particular, the learned
linear map is not a trained fracture GNN, and the linear Gaussian posterior
is not a posterior for particle positions in a cracking specimen.
""")
notebook = nbformat.v4.new_notebook(cells=cells, metadata={
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.11"},
    "provenance": {
        "status": "unexecuted source; execute on HPC before distribution",
        "lab_source_sha256": hashlib.sha256(lab.encode()).hexdigest(),
        "figure_generator_sha256": hashlib.sha256(plot_source.encode()).hexdigest(),
        "scope": "Original analytic and linear-algebra teaching examples",
    },
})
out = ROOT / "notebooks"
out.mkdir(exist_ok=True)
nbformat.write(notebook, out / "inverse_experiments_source.ipynb")
print(f"Assembled {len(cells)} cells; {sum(c.cell_type=='code' for c in cells)} code cells.")
