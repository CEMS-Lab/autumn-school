"""Regenerate the operational Practical 1 notebook; execute it separately."""
import json
from pathlib import Path
import textwrap

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "notebooks/01_phast_tiny_evolving_fracture.ipynb"
cells = []


def cell(kind, source):
    item = {"cell_type": kind, "metadata": {},
            "source": textwrap.dedent(source).strip().splitlines(keepends=True)}
    if kind == "code":
        item.update(execution_count=None, outputs=[])
    cells.append(item)


def md(text):
    cell("markdown", text)


def code(text):
    cell("code", text)


md(r'''
# Lab 01: From a notched specimen to saved PhAST results

**Learning objective:** Build a triangular finite-element mesh, seed a phase-field notch, apply symmetric tension, and run a quasistatic PhAST calculation. Reopen the saved displacement, damage and response data, then investigate how a smaller imposed separation changes the result.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/01_phast_tiny_evolving_fracture.ipynb)
[Download Practice Notebook](https://cems-lab.github.io/autumn-school/notebooks/study/01_phast_tiny_evolving_fracture.ipynb) · [Download with Worked Solutions](https://cems-lab.github.io/autumn-school/notebooks/solutions/01_phast_tiny_evolving_fracture.ipynb) · [Environment Setup](https://cems-lab.github.io/autumn-school/SETUP.md)

Pulling the top and bottom of a specimen apart stores elastic energy. A phase-field model describes the competition between that stored energy and the energy associated with a diffuse damaged region. We follow this process in a $4\times2$ rectangle containing a short, initially damaged centreline.

The calculation uses the public PhAST AT2 model, isotropic energy degradation, plane-strain kinematics and sparse-direct quasistatic mechanics. Plane strain assumes zero out-of-plane strain. Its fields illustrate diffuse damage evolution under the stated restraints. All quantities use consistent **dimensionless teaching scales**.

The workflow is **configuration → geometry → mesh import → constraints and load → solve → save and reopen → interpretation**. The same objects pass through this complete chain.
''')
code((ROOT / "source/notebooks/colab_bootstrap.py").read_text() + r'''

setup_seconds = setup_receipt["setup_seconds"]
computation_started = time.perf_counter()

import copy
import json
import os
from io import BytesIO
import numpy as np
import torch
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from IPython.display import Image, display
from day2_helpers import assets_dir, import_public_phast, load_forward_config
from day2_helpers.forward_workflow import (prepare_course_mesh, solver_configuration, solve_prepared_case,
                                         save_results, load_results, digest_file, notebook_source_hash)

torch.set_default_dtype(torch.float64)
torch.set_num_threads(min(4, os.cpu_count() or 1))
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
                    "font.size": 11, "axes.labelsize": 11, "axes.titlesize": 12,
                    "xtick.labelsize": 10, "ytick.labelsize": 10, "legend.fontsize": 10,
                    "figure.titlesize": 13, "figure.dpi": 150, "axes.grid": True,
                    "grid.alpha": .3, "grid.linestyle": "--", "lines.linewidth": 1.8})

def show_figure(fig, name, alt):
    fig.savefig(assets_dir() / name, dpi=150, bbox_inches="tight")
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=150, bbox_inches="tight")
    display(Image(data=buffer.getvalue(), alt=alt))
    plt.close(fig)

print({"torch": torch.__version__, "device": "cpu", "dtype": "float64", "cloud_setup": IN_COLAB})
''')
md(r'''
## 1. Describe the specimen and predict its response

The width is $W=4$, the height is $H=2$, and the nominal notch length is $a=0.8$. The notch is represented by nodes held at damage $d=1$ along $y=H/2$, from the left edge to $x\leq a$. The surrounding domain starts at $d=0$; its triangular connectivity remains continuous.

The total prescribed separation is $\delta=0.04\lambda$, where the load factor $\lambda$ increases from $0.0125$ to $1$. Symmetric tension prescribes

$$u_y^{\mathrm{top}}=+\frac{\delta}{2},\qquad u_y^{\mathrm{bottom}}=-\frac{\delta}{2}.$$

Horizontal displacement $u_x$ is fixed on all four exterior edges. These lateral restraints form part of this teaching case. Before running it, predict where damage will increase and how halving $\delta$ should affect the stored elastic energy.
''')
code(r'''
config = load_forward_config()  # Edit this one dictionary to define the case.
phast_info = import_public_phast(config["public_source"]["revision"])
torch.manual_seed(config["seed"])
geometry, mesh_cfg = config["geometry"], config["mesh"]
width, height, notch_length = (geometry[key] for key in ("width", "height", "notch_length"))
print({"public_revision": phast_info["revision"], "verification": phast_info["verification"],
       "geometry": geometry, "mesh": mesh_cfg, "loading": config["loading"]})

fig, ax = plt.subplots(figsize=(8, 3.8), layout="constrained")
ax.plot([0, width, width, 0, 0], [0, 0, height, height, 0], color="#245a81")
ax.plot([0, notch_length], [height/2, height/2], color="#d46b27", lw=5, label="Initial damaged centreline")
for x_arrow in np.linspace(.5, width-.5, 5):
    ax.annotate("", xy=(x_arrow, height+.27), xytext=(x_arrow, height), arrowprops={"arrowstyle": "->", "color": "#245a81"})
    ax.annotate("", xy=(x_arrow, -.27), xytext=(x_arrow, 0), arrowprops={"arrowstyle": "->", "color": "#245a81"})
ax.text(width/2, height+.35, r"$u_y=+\delta/2$", ha="center")
ax.text(width/2, -.48, r"$u_y=-\delta/2$", ha="center")
ax.text(width+.15, height/2, r"$u_x=0$ on all exterior edges", rotation=90, va="center")
ax.set(xlabel=r"$x$ [dimensionless]", ylabel=r"$y$ [dimensionless]", aspect="equal",
       xlim=(-.12, width+.4), ylim=(-.58, height+.58), title="Geometry and loading")
ax.legend(loc="upper left", bbox_to_anchor=(.015, .79))
show_figure(fig, "tiny_notched_tension_geometry.png", "Rectangle with an initially damaged centreline and outward symmetric vertical loading arrows; horizontal displacement is restrained on every exterior edge.")
''')
md(r'''
## 2. Create the mesh and inspect its boundaries

The mesh divides the rectangle into three-node triangles (T3). Set its resolution through `config["mesh"]["nx"]` and `config["mesh"]["ny"]`; an even `ny` places nodes along the damaged centreline. The boundary names `top`, `bottom`, `left` and `right` identify where we will apply constraints.

`prepare_course_mesh` is a **course helper** defined in [`day2_helpers/forward_workflow.py`](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/day2_helpers/forward_workflow.py). It creates this rectangular grid, saves and reopens its coordinates and connectivity, checks their agreement, and returns the PhAST mesh used throughout the calculation.
''')
code(r'''
prepared_mesh_path = assets_dir() / "tiny_notched_tension_prepared_mesh.npz"
mesh = prepare_course_mesh(config, prepared_mesh_path)
print({"nodes": mesh.n_nodes, "T3_elements": mesh.n_elems, "boundary_sets": sorted(mesh.node_sets)})
''')
md(r'''
### Importing a mesh from Gmsh

For a compatible, supplied Gmsh file, PhAST also provides a direct import:

```python
from phast import FEMMesh
mesh = FEMMesh("specimen.msh", device="cpu", dtype=torch.float64)
```

This optional example assumes that `specimen.msh` already exists and contains the required elements and boundary groups. The calculation below continues with the rectangular mesh created above. The [PhAST tutorials](https://cems-lab.github.io/PhAST/tutorial/index.html) connect geometry, meshing, named regions, boundary conditions and result inspection for further practice.

## 3. Attach the initial notch, boundary conditions and material

PhAST stores a scalar damage value at each node. We impose $d=1$ on the centreline mask and seed those same nodes in the solver's initial state. The full mesh view identifies the prescribed boundaries; the separate damage view shows the state before loading.

The material parameters are Young's modulus $E$, Poisson's ratio $\nu$, fracture energy $G_c$, and regularisation length $\ell$. Here $E=1$, $\nu=0.3$, $G_c=0.0005$, and $\ell=0.15$. The AT2 model balances degraded elastic energy and a smooth fracture-energy density. Its length scale determines the width over which damage varies.
''')
code(r'''
from phast.physics.boundary_conditions import symmetric_tension_bcs
from phast.physics.material import Material
from phast.solvers.staggered_solver import StaggeredSolver

def construct_solver(case, actual_mesh):
    # Every boundary mask and material value comes from this case and mesh.
    nodes = actual_mesh.nodes
    g = case["geometry"]
    precrack = ((nodes[:, 1] - g["height"]/2).abs() < 1.e-12) & (nodes[:, 0] <= g["notch_length"] + 1.e-12)
    bcs = symmetric_tension_bcs(actual_mesh, disp=case["loading"]["total_symmetric_vertical_displacement"])
    bcs.add_pf_dirichlet(torch.where(precrack)[0], value=1.0)
    material = Material(**case["material"])
    assert material.plane_stress is False  # Retain the reference case's plane-strain kinematics.
    solver = StaggeredSolver(actual_mesh, material, bcs, solver_configuration(case))
    solver.d[precrack] = 1.0
    assert solver.mesh is actual_mesh and solver.bcs is bcs and solver.material is material
    return solver, bcs, material, precrack

solver, bcs, material, precrack = construct_solver(config, mesh)
''')
md(r'''
### Inspect the mesh and initial damage

Locate the four exterior boundaries and the centreline nodes held at $d=1$. The right-hand panel shows the initial nodal damage field on the same mesh. Compare these constraints with the geometry sketch before applying the load.
''')
code(r'''
nodes = mesh.nodes.numpy()
tri = mtri.Triangulation(nodes[:, 0], nodes[:, 1], mesh.elements.numpy())
fig, axes = plt.subplots(1, 2, figsize=(11, 3.7), layout="constrained")
axes[0].triplot(tri, color="#b3bbc3", lw=.16)
for name, color in (("top", "#245a81"), ("bottom", "#245a81"), ("left", "#087f83"), ("right", "#087f83")):
    boundary = mesh.node_sets[name].numpy()
    axes[0].scatter(nodes[boundary, 0], nodes[boundary, 1], s=5, c=color)
axes[0].scatter(nodes[precrack, 0], nodes[precrack, 1], s=16, c="#d46b27", label=r"Locked $d=1$ nodes")
axes[0].legend(loc="upper right")
axes[0].set_title("Actual T3 mesh and constrained nodes")
field = axes[1].tripcolor(tri, solver.d.numpy(), cmap="magma", vmin=0, vmax=1, shading="gouraud")
axes[1].set_title("Initial damage, before loading")
for ax in axes:
    ax.set(xlabel=r"$x$ [dimensionless]", ylabel=r"$y$ [dimensionless]", aspect="equal")
    ax.grid(False)
fig.colorbar(field, ax=axes[1], label=r"Damage $d$: 0 intact; 1 damaged")
show_figure(fig, "tiny_notched_tension_initial_notch.png", "Actual imported triangular mesh with its constrained exterior nodes and locked centreline nodes; separate full initial damage field with scale zero to one.")
print({"locked_precrack_nodes": int(precrack.sum()), "last_locked_x": float(mesh.nodes[precrack, 0].max()),
       "material_kinematics": "plane stress" if material.plane_stress else "plane strain"})
''')
md(r'''
## 4. Apply the load schedule and solve

At each prescribed separation, the staggered scheme alternates mechanical equilibrium, the damage-driving history, and the phase-field update until its tolerance is met. The load factor indexes a sequence of quasistatic equilibrium problems. The mechanics subproblem uses SciPy's sparse-direct backend.

The helper below advances **the `solver` constructed above**. Within each load step it checks the imposed displacements, damage bounds, irreversibility and convergence of the staggered iterates. The selected criterion is `relative`, with the Euclidean ($L^2$) norm. At staggered iteration $k$, the recorded quantity `stagger_residual` is

$$\eta_k=\max\left(\frac{\|\mathbf u^k-\mathbf u^{k-1}\|_2}{\|\mathbf u^k\|_2+\epsilon},\frac{\|\mathbf d^k-\mathbf d^{k-1}\|_2}{\|\mathbf d^k\|_2+\epsilon}\right),\qquad \epsilon=10^{-30}.$$

The update is accepted when both relative changes fall below $10^{-5}$. This iterate-change measure describes stabilization of the coupled fields; mechanical equilibrium is handled by the mechanics subproblem and its convergence checks. The mechanics and staggered nonconvergence checks stay enabled throughout.
''')
code(r'''
loading = config["loading"]
load_factors = torch.linspace(loading["first_load_factor"], loading["last_load_factor"], loading["n_load_steps"])
print({"increments": len(load_factors), "first_separation": float(load_factors[0] * loading["total_symmetric_vertical_displacement"]),
       "final_separation": float(load_factors[-1] * loading["total_symmetric_vertical_displacement"])})
result = solve_prepared_case(solver, config, load_factors, precrack, phast_info)
assert result["solver"] is solver and solver.mesh is mesh
summary = result["metadata"]["summary"]
assert summary["incremental_damage_outside_sum"] > 1.0
assert summary["incremental_damage_outside_max"] > 1.e-3
assert summary["solve_seconds"] < config["limits"]["solver_seconds_hard"]
print({"solve_seconds": round(summary["solve_seconds"], 2), "load_steps": summary["load_steps"],
       "checks": result["metadata"]["checks"]})
''')
md(r'''
## 5. Save and reopen the numerical results

The result archive contains coordinates, triangle connectivity, boundary labels, initial and final damage, the final displacement vector, and selected state snapshots. The JSON companion records the complete configuration, public solver revision, resolved plane-strain state and relative-$L^2$ convergence criterion, conventions, checks and the scalar trace at every load step. `snapshot_steps` identifies each saved state; step zero denotes the initial condition. Reloading checks boundary indices, increasing snapshot IDs and agreement between the named initial/final arrays and the corresponding snapshots.

These are portable **post-processing results**. They can be reopened with NumPy and JSON independently of a live solver object. A restart workflow additionally requires the solver's full internal state.
''')
code(r'''
result["metadata"]["source_hashes"] = {
    name: digest_file(COURSE_ROOT / name) for name in (
        "notebooks/day2_helpers/forward_workflow.py",
        "configs/day2_forward/tiny_notched_tension.json")}
notebook_path = "notebooks/01_phast_tiny_evolving_fracture.ipynb"
result["metadata"]["notebook_source"] = {
    "path": notebook_path,
    "cell_source_sha256": notebook_source_hash(COURSE_ROOT / notebook_path),
    "authored_file_sha256": digest_file(COURSE_ROOT / notebook_path)}
field_path, metadata_path = save_results(result, assets_dir())
saved, record = load_results(field_path, metadata_path)
for name, array in result["arrays"].items():
    np.testing.assert_array_equal(saved[name], array)
assert record["config"] == config
print({"fields_file": field_path.name, "case_file": metadata_path.name,
       "displacement_shape": saved["final_displacement"].shape,
       "kinematics": record["resolved_model"]["kinematics"],
       "stagger_criterion": record["resolved_solver"]["stagger_criterion"],
       "stagger_norm": record["resolved_solver"]["stagger_norm"], "reload": "all arrays match exactly"})
''')
md(r'''
## 6. Interpret displacement, damage and reaction

All plots in this section use the reopened files. The displacement view displays the vertical component $u_y$ at the final increment. A deformed outline, magnified by a stated factor, makes the displacement direction visible. Read it alongside the full damage field: increasing damage reduces the local stiffness.
''')
code(r'''
nodes, triangles = saved["nodes"], saved["elements"]
tri = mtri.Triangulation(nodes[:, 0], nodes[:, 1], triangles)
u = saved["final_displacement"]
deformation_scale = 5
fig, axes = plt.subplots(1, 2, figsize=(11, 3.7), layout="constrained")
umax = np.abs(u[:, 1]).max()
image = axes[0].tripcolor(tri, u[:, 1], cmap="coolwarm", vmin=-umax, vmax=umax, shading="gouraud")
fig.colorbar(image, ax=axes[0], label=r"$u_y$ [dimensionless]")
axes[0].set_title("Vertical displacement at final load")
deformed = nodes + deformation_scale * u
for name in ("left", "right", "top", "bottom"):
    idx = saved["boundary_" + name]
    axes[1].plot(nodes[idx, 0], nodes[idx, 1], color="#9da6af", lw=1, linestyle="--")
    axes[1].plot(deformed[idx, 0], deformed[idx, 1], color="#245a81", lw=2)
axes[1].plot([], [], "--", color="#9da6af", label="Reference outline")
axes[1].plot([], [], color="#245a81", label=f"Deformed outline ({deformation_scale}×)")
axes[1].legend(loc="center")
axes[1].set_title("Symmetric separation of the boundaries")
for ax in axes:
    ax.set(xlabel=r"$x$ [dimensionless]", ylabel=r"$y$ [dimensionless]", aspect="equal")
show_figure(fig, "tiny_notched_tension_displacement.png", "Final vertical displacement with a symmetric color range, alongside the reference and five-times magnified deformed specimen outlines.")

fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.5), layout="constrained")
for ax, name, title in zip(axes, ("seeded_damage", "first_damage", "final_damage"),
                         ("Initial condition", "First load increment", "Final load increment")):
    field = ax.tripcolor(tri, saved[name], cmap="magma", vmin=0, vmax=1, shading="gouraud")
    ax.set(title=title, xlabel=r"$x$ [dimensionless]", ylabel=r"$y$ [dimensionless]", aspect="equal")
    ax.grid(False)
fig.colorbar(field, ax=axes, label=r"Damage $d$: 0 intact; 1 damaged")
show_figure(fig, "tiny_notched_tension_damage.png", "Full initial, first-increment and final PhAST damage fields, all using the same damage scale from zero to one.")

fig, ax = plt.subplots(figsize=(7, 3.6), layout="constrained")
field = ax.tripcolor(tri, saved["incremental_damage"], cmap="viridis", shading="gouraud", vmin=0)
ax.set(title="Damage accumulated after the first increment", xlabel=r"$x$ [dimensionless]", ylabel=r"$y$ [dimensionless]", aspect="equal")
ax.grid(False)
fig.colorbar(field, ax=ax, label=r"$\max(d_{60}-d_1,0)$")
show_figure(fig, "tiny_notched_tension_increment.png", "Full spatial field of positive damage accrued after the first increment, with a labelled quantitative color scale.")
''')
md(r'''
The top reaction $F_y$ is the sum of the internal vertical forces at the prescribed top nodes. Plotting it against the total separation $\delta$ connects the imposed motion to the mechanical response. The nodal damage sum tracks field evolution on this fixed mesh; its value depends on mesh density. The staggered-iteration plot shows the computational effort at each load level.
''')
code(r'''
trace = record["trace"]
separation = np.array([row["applied_separation"] for row in trace])
reaction = np.array([row["reaction_top_y"] for row in trace])
fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.5), layout="constrained")
axes[0].plot(separation, reaction, color="#245a81")
axes[0].set(ylabel=r"Top reaction $F_y$ [dimensionless]", title="Reaction–separation response")
axes[1].plot(separation, [row["damage_outside_sum"] for row in trace], color="#d46b27")
axes[1].set(ylabel="Nodal damage sum outside precrack", title="Diffuse damage evolution")
axes[2].plot(separation, [row["stagger_iterations"] for row in trace], color="#087f83")
axes[2].set(ylabel="Staggered iterations", title="Coupling effort per increment")
for ax in axes:
    ax.set_xlabel(r"Separation $\delta$ [dimensionless]")
show_figure(fig, "tiny_notched_tension_response.png", "Reaction against prescribed separation, nodal damage sum outside the initial notch, and staggered coupling iterations at each increment.")
''')
md(r'''
## 7. Change one input: halve the imposed separation

For a fixed damage field, linear-elastic energy scales with the square of the imposed displacement. Halving the separation therefore reduces that elastic driving energy to one quarter. In the coupled calculation, damage also changes; the new equilibrium response can be assessed from the computed fields.

Copy the configuration and change only the total separation from $0.04$ to $0.02$. Reuse the imported mesh, build a fresh material/constraint/solver state, and execute the same 60 load factors. Predict the relative final damage before running the cell.
''')
code(r'''
smaller_config = copy.deepcopy(config)
smaller_config["loading"]["total_symmetric_vertical_displacement"] *= .5
smaller_solver, smaller_bcs, smaller_material, smaller_precrack = construct_solver(smaller_config, mesh)
smaller_result = solve_prepared_case(smaller_solver, smaller_config, load_factors, smaller_precrack, phast_info)
smaller_fields, smaller_json = save_results(smaller_result, assets_dir(), "tiny_notched_tension_half_load")
smaller_saved, smaller_record = load_results(smaller_fields, smaller_json)
for name, array in smaller_result["arrays"].items():
    np.testing.assert_array_equal(smaller_saved[name], array)
assert np.array_equal(smaller_saved["nodes"], saved["nodes"])
assert np.array_equal(smaller_saved["elements"], saved["elements"])
outside = ~saved["precrack"]
assert smaller_saved["final_damage"][outside].sum() < saved["final_damage"][outside].sum()
assert smaller_record["trace"][-1]["applied_separation"] == .5 * record["trace"][-1]["applied_separation"]

fig, axes = plt.subplots(1, 3, figsize=(13.5, 3.6), layout="constrained")
for ax, data, title in zip(axes[:2], (smaller_saved, saved), (r"Final damage: $\delta=0.02$", r"Final damage: $\delta=0.04$")):
    field = ax.tripcolor(tri, data["final_damage"], cmap="magma", vmin=0, vmax=1, shading="gouraud")
    ax.set(title=title, xlabel=r"$x$ [dimensionless]", ylabel=r"$y$ [dimensionless]", aspect="equal")
    ax.grid(False)
fig.colorbar(field, ax=axes[:2], label=r"Damage $d$")
for case_record, style, label in ((record, "-", r"$\delta_{\max}=0.04$"), (smaller_record, "--", r"$\delta_{\max}=0.02$")):
    axes[2].plot([r["applied_separation"] for r in case_record["trace"]], [r["reaction_top_y"] for r in case_record["trace"]], style, label=label)
axes[2].set(title="Response for each loading history", xlabel=r"$\delta$ [dimensionless]", ylabel=r"$F_y$ [dimensionless]")
axes[2].legend()
show_figure(fig, "tiny_notched_tension_comparison.png", "Final damage for half and full imposed separation on a shared zero-to-one color scale, with both reaction–separation curves.")
print({"full_load_damage_sum": float(saved["final_damage"][outside].sum()),
       "half_load_damage_sum": float(smaller_saved["final_damage"][outside].sum()),
       "half_load_solve_seconds": round(smaller_record["summary"]["solve_seconds"], 2)})
''')
md(r'''
## Key takeaways

- A single configuration defines geometry, mesh, material, initial damage and the prescribed loading; the reopened mesh is the mesh used by PhAST.
- The initial notch is a locked damage condition. Its nodal endpoint follows the chosen mesh spacing.
- Quasistatic staggered updates couple mechanical equilibrium with diffuse damage evolution. The reaction curve and spatial fields complement one another.
- Portable NPZ/JSON results retain enough numerical information to reproduce the post-processing figures and compare controlled changes to the input.

For independent practice, use the accompanying conceptual and numerical exercises. Mesh refinement and alternative boundary restraints are natural follow-up studies when investigating the dependence of the damage pattern on the model and discretisation.
''')
code(r'''
computation_seconds = time.perf_counter() - computation_started
receipt = {"scope": "all notebook computations after setup, including two full solves, assertions, save/reload and figures",
           "setup_seconds": setup_seconds, "computation_seconds": computation_seconds,
           "installation": "pip installation during cloud setup" if IN_COLAB else "pre-existing local environment",
           "platform": record["environment"], "source_hashes": record["source_hashes"],
           "notebook_source": record["notebook_source"],
           "reference_solve_seconds": record["summary"]["solve_seconds"],
           "half_load_solve_seconds": smaller_record["summary"]["solve_seconds"],
           "reference_checks": record["checks"], "half_load_checks": smaller_record["checks"],
           "reload_equality": True, "one_changed_input": "loading.total_symmetric_vertical_displacement",
           "half_load_has_lower_nodal_damage_sum": True, "colab_execution": IN_COLAB}
(assets_dir() / "tiny_notched_tension_notebook_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
assert computation_seconds < config["limits"]["notebook_seconds_hard"]
print({"complete_computation_seconds": round(computation_seconds, 2), "results": "saved and reopened successfully"})
''')

original = json.loads(TARGET.read_text())
notebook = {"cells": cells, "metadata": original["metadata"], "nbformat": 4, "nbformat_minor": 5}
for i, item in enumerate(cells):
    item["id"] = f"forward-{i:02d}"
TARGET.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n")
print(f"Built {TARGET.name}: {len(cells)} cells. Execute with scripts/run_course.py --notebook 1.")
