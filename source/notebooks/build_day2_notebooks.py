"""Generate the five small, canonical UKACM day-two notebooks.

This script is intentionally checked in beside the notebooks so their compact,
repeated setup cells and source-boundary statements can be regenerated without
hand-editing JSON.  It does not execute notebooks; see ``reviews/notebook_runtime.md``
for the executed outputs and receipts.

Course material created by Allamaprabhu Ani; presented by Sathiskumar A. Ponnusami,
CEMS-Lab, UKACM Autumn School 2026. Attribution does not replace bundled licences.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent

import nbformat as nbf


COURSE = Path(__file__).resolve().parents[2]
NOTEBOOKS = COURSE / "notebooks"
COURSE_ATTRIBUTION = {
    "creator": "Allamaprabhu Ani",
    "presenter": "Sathiskumar A. Ponnusami",
    "presenter_affiliation": "Queen Mary University of London · CEMS-Lab",
    "affiliation": "CEMS-Lab",
    "course": "UKACM Autumn School 2026",
}


def markdown(text: str):
    return nbf.v4.new_markdown_cell(dedent(text).strip() + "\n")


def code(text: str):
    return nbf.v4.new_code_cell(dedent(text).strip() + "\n")


BOOTSTRAP = r'''
from pathlib import Path
import sys

def locate_course_root():
    for base in (Path.cwd(), *Path.cwd().parents, Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()):
        direct = base / "teaching" / "ukacm_autumn_school_2026"
        if (direct / "notebooks" / "day2_helpers").is_dir():
            return direct
        if (base / "notebooks" / "day2_helpers").is_dir():
            return base
    raise FileNotFoundError("Could not find teaching/ukacm_autumn_school_2026.")

COURSE_ROOT = locate_course_root()
if str(COURSE_ROOT / "notebooks") not in sys.path:
    sys.path.insert(0, str(COURSE_ROOT / "notebooks"))

import matplotlib.pyplot as plt
import numpy as np
import torch
from io import BytesIO
from IPython.display import Image, display

from day2_helpers import assets_dir

torch.set_default_dtype(torch.float64)

def display_figure(figure, dpi=150, alt="Rendered teaching figure"):
    """Embed a PNG even when nbclient uses a non-interactive Agg backend."""
    buffer = BytesIO()
    figure.savefig(buffer, format="png", dpi=dpi, bbox_inches="tight")
    display(Image(data=buffer.getvalue(), alt=alt))

print({"course_layout": "teaching/ukacm_autumn_school_2026 located", "torch": torch.__version__, "device": "cpu", "dtype": str(torch.get_default_dtype())})
'''


def write_notebook(filename: str, cells: list):
    notebook = nbf.v4.new_notebook(cells=cells)
    notebook.metadata = {
        **COURSE_ATTRIBUTION,
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10"},
        "ukacm_scope": "September 2026 day-two teaching companion",
    }
    with (NOTEBOOKS / filename).open("w", encoding="utf-8") as handle:
        nbf.write(notebook, handle)


def first_fracture():
    return [
        markdown(
            r'''
            # 01 — Public PhAST: a tiny evolving phase-field calculation

            This exercise solves an AT2 phase-field problem with PhAST on a
            structured triangular mesh. A rectangular specimen undergoes
            symmetric tension while a centreline precrack remains fixed.
            Sixty **quasi-static load increments** trace its damage evolution;
            the load factor parameterises the imposed displacement.

            The course bundle supplies PhAST 0.16.2. Follow the environment
            setup guide before running the notebook; the opening cells load
            the case configuration and identify the source revision.

            **What to look for.** `d=0` means intact-like and `d=1` means
            fully broken. Compare the seeded, first-load and final damage
            fields. Damage gained outside the locked centreline shows how
            the diffuse damaged region evolves under increasing tension.
            '''
        ),
        code(BOOTSTRAP),
        code(
            r'''
            from day2_helpers import import_public_phast, load_forward_config, run_notched_tension

            config = load_forward_config()
            phast_info = import_public_phast(config["public_source"]["revision"])
            print(phast_info)
            print({k: config[k] for k in ("geometry", "mesh", "material", "loading", "solver", "limits")})
            '''
        ),
        markdown(
            r'''
            ## Geometry, mesh, labelled boundaries, material, and constraints

            The next cell illustrates the specimen setup by generating a T3 mesh
            and saving and reopening its coordinate and connectivity arrays.
            `identify_boundaries()` supplies the `left`, `right`, `top`, and
            `bottom` node labels; a centreline mask selects the precrack.
            The later solve constructs its inputs from the case configuration,
            so use that configuration when changing the specimen or material.
            '''
        ),
        code(
            r'''
            from day2_helpers.course_tools import _structured_triangles
            from phast.core.mesh import FEMMesh
            from phast.physics.boundary_conditions import symmetric_tension_bcs
            from phast.physics.material import Material

            geometry, mesh_cfg, material_cfg, loading = (
                config["geometry"], config["mesh"], config["material"], config["loading"]
            )
            width, height = geometry["width"], geometry["height"]
            x = torch.linspace(0.0, width, mesh_cfg["nx"] + 1, dtype=torch.float64)
            y = torch.linspace(0.0, height, mesh_cfg["ny"] + 1, dtype=torch.float64)
            xx, yy = torch.meshgrid(x, y, indexing="xy")
            nodes_preview = torch.stack((xx.reshape(-1), yy.reshape(-1)), dim=1)
            elements_preview = _structured_triangles(mesh_cfg["nx"], mesh_cfg["ny"])
            mesh_preview = FEMMesh.from_tensors(nodes_preview, elements_preview, device="cpu", dtype=torch.float64)
            mesh_preview.identify_boundaries()

            bcs_preview = symmetric_tension_bcs(mesh_preview, disp=loading["total_symmetric_vertical_displacement"])
            precrack_mask = ((nodes_preview[:, 1] - height / 2).abs() < 1.0e-12) & (nodes_preview[:, 0] <= geometry["notch_length"] + 1.0e-12)
            precrack_nodes = torch.where(precrack_mask)[0]
            bcs_preview.add_pf_dirichlet(precrack_nodes, value=1.0)
            material_preview = Material(
                E=material_cfg["E"], nu=material_cfg["nu"], Gc=material_cfg["Gc"], l0=material_cfg["l0"],
                rho=material_cfg["rho"], eta_residual=material_cfg["eta_residual"],
                energy_split=material_cfg["energy_split"], pf_model=material_cfg["pf_model"],
            )

            prepared_mesh = assets_dir() / "tiny_notched_tension_prepared_mesh.npz"
            np.savez_compressed(
                prepared_mesh,
                nodes=nodes_preview.numpy(), elements=elements_preview.numpy(), precrack_nodes=precrack_nodes.numpy(),
                **{name: index.numpy() for name, index in mesh_preview.node_sets.items()},
            )
            imported = np.load(prepared_mesh)
            assert np.array_equal(imported["elements"], elements_preview.numpy())
            print({
                "geometry": f"{width} × {height} rectangle; centreline notch length {geometry['notch_length']}",
                "mesh": f"{mesh_preview.n_nodes} nodes / {mesh_preview.n_elems} T3 elements",
                "boundary_labels": sorted(mesh_preview.node_sets),
                "precrack_nodes": len(precrack_nodes),
                "prepared_tensor_mesh": "assets/day2_forward/tiny_notched_tension_prepared_mesh.npz",
                "material": {key: material_cfg[key] for key in ("E", "nu", "Gc", "l0", "pf_model")},
                "BC": "x fixed on exterior; top/bottom symmetric vertical displacement; d=1 on precrack",
            })
            '''
        ),
        markdown(
            r'''
            ## Route and representation

            The selected mechanics route is `solver_type="quasi_static"` with
            the SciPy sparse-direct backend.  It performs a staggered update:
            mechanics → tensile/history update → phase-field damage → repeat
            to the configured tolerance. The mechanics step assembles a sparse
            matrix and solves the resulting linear system directly.

            A quasi-Newton/Newton method describes a nonlinear **solution
            algorithm**, while XFEM describes a crack **representation**.
            Here the crack is represented by a regularised phase field on T3
            elements.
            '''
        ),
        code(
            r'''
            # The helper writes a small JSON/NPZ receipt under assets/day2_forward/.
            # It also has a 300-second limit recorded in the configuration;
            # the external notebook executor enforces the process-level timeout.
            result = run_notched_tension(config)
            summary = result["summary"]
            summary
            '''
        ),
        code(
            r'''
            # Check convergence, irreversibility and damage evolution numerically.
            assert summary["solve_seconds"] < config["limits"]["solver_seconds_hard"]
            assert summary["incremental_damage_outside_sum"] > 1.0
            assert summary["incremental_damage_outside_max"] > 1.0e-3
            assert not summary["warnings"], summary["warnings"]
            print("Evolving-damage assertions passed.")
            '''
        ),
        code(
            r'''
            import matplotlib.tri as mtri

            nodes = result["nodes"].detach().cpu().numpy()
            triangles = result["elements"].detach().cpu().numpy()
            tri = mtri.Triangulation(nodes[:, 0], nodes[:, 1], triangles)
            seeded = result["seeded_damage"].detach().cpu().numpy()
            first = result["first_damage"].detach().cpu().numpy()
            final = result["final_damage"].detach().cpu().numpy()
            increment = result["incremental_damage"].detach().cpu().numpy()

            fig, axes = plt.subplots(1, 3, figsize=(14, 3.5), constrained_layout=True)
            for ax, field, title in zip(
                axes,
                (seeded, first, final),
                ("Locked precrack before solve", "After first load increment", "After final load increment"),
            ):
                image = ax.tripcolor(tri, field, shading="gouraud", vmin=0, vmax=1, cmap="magma")
                ax.triplot(tri, color="white", lw=0.06, alpha=0.20)
                ax.set(title=title, xlabel="x", ylabel="y", aspect="equal")
            fig.colorbar(image, ax=axes, label="damage d")
            fig.savefig(assets_dir() / "tiny_notched_tension_damage.png", dpi=160, bbox_inches="tight")
            display_figure(fig, alt="Three PhAST damage fields: locked precrack, first load increment, and final diffuse damage field.")
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(6.4, 3.6), constrained_layout=True)
            ax.tripcolor(tri, increment, shading="gouraud", cmap="viridis")
            ax.set(title="New damage accrued after the first increment", xlabel="x", ylabel="y", aspect="equal")
            fig.colorbar(ax.collections[0], ax=ax, label="max(d_final − d_step1, 0)")
            fig.savefig(assets_dir() / "tiny_notched_tension_increment.png", dpi=160, bbox_inches="tight")
            display_figure(fig, alt="Map of incremental damage accumulated after the first load increment.")
            plt.close(fig)
            '''
        ),
        code(
            r'''
            trace = result["trace"]
            load = np.array([row["load_factor"] for row in trace])
            reaction = np.array([row["reaction_top_y"] for row in trace])
            outside_sum = np.array([row["damage_outside_sum"] for row in trace])
            stagger = np.array([row["stagger_iterations"] for row in trace])

            fig, axes = plt.subplots(1, 3, figsize=(14, 3.5), constrained_layout=True)
            axes[0].plot(load, reaction, marker="o", ms=2)
            axes[0].set(xlabel="load factor", ylabel="top internal-force sum", title="Response extracted from the final state")
            axes[1].plot(load, outside_sum, marker="o", ms=2)
            axes[1].set(xlabel="load factor", ylabel="sum(d outside locked precrack)", title="Damage evolution outside initial crack")
            axes[2].plot(load, stagger, marker="o", ms=2)
            axes[2].set(xlabel="load factor", ylabel="stagger iterations", title="Coupling iterations per load step")
            fig.savefig(assets_dir() / "tiny_notched_tension_response.png", dpi=160, bbox_inches="tight")
            display_figure(fig, alt="PhAST load response, damage-outside-precrack trace, and stagger iteration count.")
            plt.close(fig)

            print({
                "mesh": f"{summary['nodes']} nodes / {summary['elements']} T3 elements",
                "setup_seconds": round(summary["setup_seconds"], 2),
                "solve_seconds": round(summary["solve_seconds"], 2),
                "incremental_damage_outside_sum": round(summary["incremental_damage_outside_sum"], 4),
                "incremental_damage_outside_max": round(summary["incremental_damage_outside_max"], 4),
            })
            '''
        ),
        markdown(
            r'''
            ## Interpret, then change one input

            The reaction plotted here is the sum of the internal force at the
            top prescribed-displacement nodes. Read this response alongside
            the damage fields to connect the imposed loading to the evolving
            damaged region.

            Try changing only `Gc`, `l0`, the total displacement, or the mesh
            density in `configs/day2_forward/tiny_notched_tension.json`, then
            rerun. Explain the change using the model assumptions: a two-dimensional
            specimen, a structured mesh and the selected energy split. Compare
            successive mesh refinements before interpreting the calculated damage
            pattern as independent of discretisation.
            '''
        ),
    ]


def degradation():
    return [
        markdown(
            r'''
            # 02 — Degradation law and automatic differentiation

            This short exercise checks the exact standard normalised
            degradation law in the pinned public PhAST source:

            $$
            g(d)=(1-\eta)(1-d)^2+\eta, \qquad
            g'(d)=-2(1-\eta)(1-d).
            $$

            We use $d=0$ for intact and $d=1$ for broken, $\eta=10^{-7}$, and
            `float64`. We compare analytic, automatic and finite-difference
            derivatives of this smooth scalar material law. A coupled fracture
            derivative also depends on history updates, constraints and the
            solution procedure.
            '''
        ),
        code(BOOTSTRAP),
        code(
            r'''
            from day2_helpers import import_public_phast
            phast_info = import_public_phast()
            from phast.physics.material import Material

            eta = 1.0e-7
            material = Material(E=1.0, nu=0.3, Gc=1.0, l0=0.1, rho=1.0, eta_residual=eta)

            def g_analytic(d):
                return (1.0 - eta) * (1.0 - d) ** 2 + eta

            def gp_analytic(d):
                return -2.0 * (1.0 - eta) * (1.0 - d)

            d = torch.tensor(0.25, dtype=torch.float64, requires_grad=True)
            g_phast = material.degradation(d)
            (g_ad,) = torch.autograd.grad(g_phast, d)
            h = 1.0e-6
            g_fd = (g_analytic(d.detach() + h) - g_analytic(d.detach() - h)) / (2.0 * h)
            expected = gp_analytic(d.detach())
            print({
                "public_source": phast_info,
                "d": float(d.detach()),
                "g_from_public_material": float(g_phast.detach()),
                "analytic_g_prime": float(expected),
                "autograd_g_prime": float(g_ad),
                "central_fd_g_prime": float(g_fd),
            })
            '''
        ),
        code(
            r'''
            endpoints = material.degradation(torch.tensor([0.0, 1.0], dtype=torch.float64))
            ad_error = abs(float(g_ad - expected))
            fd_error = abs(float(g_fd - expected))
            assert abs(float(endpoints[0]) - 1.0) < 1.0e-12
            assert abs(float(endpoints[1]) - eta) < 1.0e-12
            assert ad_error < 1.0e-12
            assert fd_error < 1.0e-8
            print({"g(0)": float(endpoints[0]), "g(1)": float(endpoints[1]), "AD_error": ad_error, "FD_error": fd_error})
            '''
        ),
        code(
            r'''
            d_plot = torch.linspace(0.0, 1.0, 400, dtype=torch.float64)
            fig, axes = plt.subplots(1, 2, figsize=(10, 3.5), constrained_layout=True)
            axes[0].plot(d_plot, material.degradation(d_plot), label=r"$g(d)$")
            axes[0].scatter([0, 1], endpoints, color="black", zorder=3)
            axes[0].set(xlabel="damage d", ylabel="degradation", title="Residual stiffness remains at d=1")
            axes[0].legend()
            axes[1].plot(d_plot, gp_analytic(d_plot), label=r"$g'(d)$")
            axes[1].axhline(0, color="black", lw=0.7)
            axes[1].set(xlabel="damage d", ylabel="derivative", title="Analytic derivative")
            axes[1].legend()
            fig.savefig(assets_dir() / "degradation_autograd.png", dpi=160, bbox_inches="tight")
            display_figure(fig, alt="Standard degradation function and its analytic derivative over damage from zero to one.")
            plt.close(fig)
            '''
        ),
        markdown(
            r'''
            **Why this matters.** Automatic differentiation follows the tensor
            operations connected to a scalar loss. For a complete solver, trace
            that connection through the boundary conditions, equilibrium solve,
            history update and active constraints. The next exercise develops
            this parameter-to-observation chain for an elastic bar.
            '''
        ),
    ]


def inverse_toy():
    return [
        markdown(
            r'''
            # 03 — Recovering the stiffness of an elastic bar

            We recover the elastic modulus of a one-dimensional bar from
            synthetic displacement observations. Linear elasticity gives a
            smooth parameter-to-observation map with an analytic sensitivity:
            trainable modulus → stiffness tensor → linear solve →
            observed displacement → scalar loss.
            '''
        ),
        code(BOOTSTRAP),
        code(
            r'''
            torch.manual_seed(20260909)
            n_elements, length, area = 40, 1.0, 1.0
            h = length / n_elements
            # Unit-modulus stiffness. E remains a differentiable scalar multiplier.
            K0 = torch.zeros((n_elements + 1, n_elements + 1), dtype=torch.float64)
            local = torch.tensor([[1.0, -1.0], [-1.0, 1.0]], dtype=torch.float64) * area / h
            for e in range(n_elements):
                K0[e:e+2, e:e+2] += local

            def tip_displacement(E, load):
                K_free = (E * K0)[1:, 1:]
                force = torch.zeros(n_elements, dtype=torch.float64)
                force[-1] = load
                return torch.linalg.solve(K_free, force)[-1]

            E_probe = torch.tensor(1.8, dtype=torch.float64, requires_grad=True)
            u_probe = tip_displacement(E_probe, 1.1)
            (du_dE_ad,) = torch.autograd.grad(u_probe, E_probe)
            h_fd = 1.0e-6
            du_dE_fd = (tip_displacement(E_probe.detach() + h_fd, 1.1) - tip_displacement(E_probe.detach() - h_fd, 1.1)) / (2*h_fd)
            du_dE_exact = -u_probe.detach() / E_probe.detach()
            print({"u_tip": float(u_probe.detach()), "AD": float(du_dE_ad), "FD": float(du_dE_fd), "analytic": float(du_dE_exact)})
            assert abs(float(du_dE_ad - du_dE_exact)) < 1.0e-12
            assert abs(float(du_dE_fd - du_dE_exact)) < 1.0e-8
            '''
        ),
        code(
            r'''
            # Whole load cases are kept separate: train, validation, and held-out.
            E_true = torch.tensor(2.4, dtype=torch.float64)
            train_loads = torch.tensor([0.35, 0.75, 1.15, 1.55], dtype=torch.float64)
            validation_load = torch.tensor(0.95, dtype=torch.float64)
            heldout_load = torch.tensor(1.35, dtype=torch.float64)
            observed_train = torch.stack([tip_displacement(E_true, load) for load in train_loads]).detach()
            observed_validation = tip_displacement(E_true, validation_load).detach()
            observed_heldout = tip_displacement(E_true, heldout_load).detach()

            log_E = torch.nn.Parameter(torch.log(torch.tensor(0.9, dtype=torch.float64)))
            optimiser = torch.optim.Adam([log_E], lr=0.08)
            history = []
            for iteration in range(180):
                optimiser.zero_grad(set_to_none=True)
                E_trial = torch.exp(log_E)
                predicted = torch.stack([tip_displacement(E_trial, load) for load in train_loads])
                loss = torch.mean((predicted - observed_train) ** 2)
                loss.backward()
                optimiser.step()
                if iteration % 10 == 0 or iteration == 179:
                    with torch.no_grad():
                        val_error = abs(tip_displacement(torch.exp(log_E), validation_load) - observed_validation)
                    history.append((iteration + 1, float(torch.exp(log_E).detach()), float(loss.detach()), float(val_error)))

            E_fit = torch.exp(log_E).detach()
            heldout_prediction = tip_displacement(E_fit, heldout_load)
            print({"E_true": float(E_true), "E_fit": float(E_fit), "heldout_observed": float(observed_heldout), "heldout_prediction": float(heldout_prediction)})
            assert abs(float(E_fit - E_true)) < 2.0e-3
            '''
        ),
        code(
            r'''
            history_array = np.array(history)
            response_loads = torch.linspace(0.2, 1.7, 80, dtype=torch.float64)
            true_response = np.array([float(tip_displacement(E_true, load)) for load in response_loads])
            fit_response = np.array([float(tip_displacement(E_fit, load)) for load in response_loads])
            fig, axes = plt.subplots(1, 2, figsize=(10, 3.5), constrained_layout=True)
            axes[0].plot(response_loads, true_response, label="synthetic observation")
            axes[0].plot(response_loads, fit_response, "--", label="recovered modulus")
            axes[0].scatter([heldout_load], [observed_heldout], color="black", label="held-out case")
            axes[0].set(xlabel="load", ylabel="tip displacement", title="Response recovery")
            axes[0].legend()
            axes[1].semilogy(history_array[:, 0], history_array[:, 2], label="training loss")
            axes[1].semilogy(history_array[:, 0], history_array[:, 3], label="validation absolute error")
            axes[1].set(xlabel="iteration", ylabel="error", title="Optimisation history")
            axes[1].legend()
            fig.savefig(assets_dir() / "tiny_inverse_bar.png", dpi=160, bbox_inches="tight")
            display_figure(fig, alt="Toy elastic-bar response recovery and optimisation history.")
            plt.close(fig)
            '''
        ),
        markdown(
            r'''
            Compare the recovered modulus and held-out displacement with their
            reference values. The analytic bar sensitivity helps explain the
            agreement between automatic differentiation and finite differences.
            Extending the calculation to fracture introduces a load-dependent
            history, irreversibility constraints and sensitivity to the chosen
            observations and solver tolerance.
            '''
        ),
    ]


def training_reload():
    return [
        markdown(
            r'''
            # 04 — Train, save, reload, and compare a tiny field model

            We train a small multilayer perceptron on solutions of
            `ToyHelmholtzProblem`, a linear field equation with a known discrete
            residual. This model problem lets us study data splits, saved model
            metadata and predictions at held-out loads.

            Feature contract: nodewise `[x/L, y/H, load_factor]`, all
            dimensionless, in exactly that order; output: one nodewise
            damage-like proposal in `[0,1]`. Training, validation and test sets
            contain separate whole load cases, so each field belongs to one split.
            '''
        ),
        code(BOOTSTRAP),
        code(
            r'''
            from day2_helpers.course_tools import (
                FEATURE_ORDER, TinyDamageMLP, ToyHelmholtzProblem,
                load_toy_model, make_toy_checkpoint, normalise_features,
            )

            checkpoint_path = assets_dir() / "models" / "tiny_damage_mlp.pt"
            checkpoint = make_toy_checkpoint(checkpoint_path, epochs=400, force=True)
            metadata = checkpoint["metadata"]
            print({"checkpoint": str(checkpoint_path.relative_to(COURSE_ROOT)), "metadata": metadata, "history": checkpoint["history"], "metrics": checkpoint["metrics"]})
            '''
        ),
        code(
            r'''
            # Reload into a fresh model instance; compare the two predictions exactly.
            problem = ToyHelmholtzProblem()
            heldout_load = 1.00
            heldout_features = problem.features(heldout_load)
            heldout_reference = problem.reference_field(heldout_load)
            mean = torch.tensor(metadata["normalisation_mean"], dtype=torch.float64)
            scale = torch.tensor(metadata["normalisation_scale"], dtype=torch.float64)
            original = TinyDamageMLP(width=metadata["width"]).to(dtype=torch.float64)
            original.load_state_dict(checkpoint["state_dict"])
            original.eval()
            reloaded, reloaded_metadata = load_toy_model(checkpoint_path)
            with torch.no_grad():
                prediction_before = original(normalise_features(heldout_features, mean, scale)).squeeze(1)
                prediction_after = reloaded(normalise_features(heldout_features, mean, scale)).squeeze(1)
            reload_difference = float((prediction_before - prediction_after).abs().max())
            heldout_rmse = float(torch.sqrt(torch.mean((prediction_after - heldout_reference) ** 2)))
            print({"reload_max_abs_difference": reload_difference, "heldout_rmse": heldout_rmse, "feature_order": reloaded_metadata["feature_order"]})
            assert reload_difference < 1.0e-12
            assert heldout_rmse < 0.07
            '''
        ),
        code(
            r'''
            # A compatible RBF reference alternative shares the same nodewise features,
            # but is a distinct architecture with its own resolution/data assumptions.
            train_loads = metadata["splits"]["train"]
            train_features, train_targets = problem.case_tensor(train_loads)
            z_train = normalise_features(train_features, mean, scale)
            z_test = normalise_features(heldout_features, mean, scale)
            squared_distance = torch.cdist(z_test, z_train) ** 2
            weights = torch.exp(-squared_distance / 0.18)
            rbf_prediction = (weights @ train_targets).squeeze(1) / weights.sum(dim=1).clamp_min(1.0e-15)
            rbf_rmse = float(torch.sqrt(torch.mean((rbf_prediction - heldout_reference) ** 2)))
            print({"MLP_heldout_RMSE": heldout_rmse, "RBF_heldout_RMSE": rbf_rmse, "RBF_scope": "shared nodewise feature contract for the discrete Helmholtz model"})
            '''
        ),
        code(
            r'''
            def field_image(values):
                return values.detach().reshape(problem.ny, problem.nx).cpu().numpy()

            error = prediction_after - heldout_reference
            fig, axes = plt.subplots(1, 4, figsize=(14, 3.2), constrained_layout=True)
            for ax, values, title, cmap, limits in (
                (axes[0], heldout_reference, "held-out toy reference", "magma", (0, 1)),
                (axes[1], prediction_after, "reloaded MLP", "magma", (0, 1)),
                (axes[2], rbf_prediction, "compatible RBF baseline", "magma", (0, 1)),
                (axes[3], error, "MLP − reference", "coolwarm", (-0.15, 0.15)),
            ):
                image = ax.imshow(field_image(values), origin="lower", extent=(0,1,0,1), cmap=cmap, vmin=limits[0], vmax=limits[1])
                ax.set(title=title, xlabel="x/L", ylabel="y/H", aspect="equal")
                fig.colorbar(image, ax=ax, shrink=0.78)
            fig.savefig(assets_dir() / "tiny_mlp_heldout_field.png", dpi=160, bbox_inches="tight")
            display_figure(fig, alt="Held-out toy reference, reloaded MLP field, compatible RBF field, and MLP error.")
            plt.close(fig)
            '''
        ),
        markdown(
            r'''
            The checkpoint stores the architecture width, weight `state_dict`,
            feature order and units, normalisation, dtype/device, mesh
            signature, data provenance, splits, seed, and training duration.
            An MLP and an RBF interpolant can both consume this nodewise
            representation. A CNN requires mesh-to-grid maps, while a GNN/GNO
            requires connectivity or operator inputs. Define these mappings
            explicitly when changing the model architecture.
            '''
        ),
    ]


def hybrid_adapter():
    return [
        markdown(
            r'''
            # 05 — A compatible proposal, residual check, and fallback

            This notebook connects the trained model from notebook 04 to an
            adapter for the same linear field problem. The adapter verifies its
            feature order and mesh signature, predicts under `torch.no_grad()`,
            projects bounds and irreversibility, evaluates the discrete
            `ToyHelmholtzProblem` residual, and falls back to the reference
            solve when the proposal fails the gate.

            The residual measures agreement with the discrete Helmholtz-like
            equation. Prediction takes place with fixed model weights, followed
            by a reference solve when correction is needed:
            proposal → compatibility → constraint projection → assess → correction.
            '''
        ),
        code(BOOTSTRAP),
        code(
            r'''
            import json
            from day2_helpers.course_tools import (
                FEATURE_ORDER, ToyDamageAdapter, ToyHelmholtzProblem,
                load_toy_model, make_toy_checkpoint,
            )

            checkpoint_path = assets_dir() / "models" / "tiny_damage_mlp.pt"
            if not checkpoint_path.exists():
                # This makes the notebook independently executable. In the normal
                # sequence notebook 04 has already produced this exact artifact.
                make_toy_checkpoint(checkpoint_path, epochs=400, force=True)
            model, metadata = load_toy_model(checkpoint_path)
            problem = ToyHelmholtzProblem()
            adapter = ToyDamageAdapter(model, metadata, problem)
            print({"interface_version": metadata["interface_version"], "feature_order": metadata["feature_order"], "mesh_signature": metadata["mesh_signature"]})
            '''
        ),
        code(
            r'''
            # Compatible held-out request. d_previous comes from a lower-load state.
            load_factor = 0.94
            d_previous = problem.reference_field(0.82)
            proposal = adapter.propose(problem.features(load_factor), d_previous=d_previous)
            assessment = adapter.assess(proposal, load_factor, residual_limit=0.30)
            reference = problem.reference_field(load_factor)
            corrected = proposal if assessment["accepted"] else adapter.fallback(load_factor, d_previous)
            print({"normal_proposal": assessment, "field_rmse": float(torch.sqrt(torch.mean((proposal-reference)**2)))})
            assert assessment["accepted"], assessment

            # A deliberately corrupted field is projected but fails the same residual gate.
            corrupted = torch.where(
                problem.boundary_mask,
                torch.zeros_like(proposal),
                (proposal + 0.30 * torch.sin(12 * problem.coordinates[:, 0])).clamp(0, 1),
            )
            rejected = adapter.assess(corrupted, load_factor, residual_limit=0.30)
            fallback = adapter.fallback(load_factor, d_previous)
            print({"corrupted_proposal": rejected, "fallback_residual": problem.relative_residual(fallback, load_factor)})
            assert not rejected["accepted"], rejected
            assert problem.relative_residual(fallback, load_factor) < 1.0e-10
            '''
        ),
        code(
            r'''
            # Explicitly demonstrate an interface failure instead of silently reshaping input.
            try:
                adapter.propose(
                    problem.features(load_factor),
                    feature_order=("load_factor", "x_over_L", "y_over_H"),
                )
            except ValueError as error:
                compatibility_message = str(error)
            else:
                raise AssertionError("An incompatible feature order was unexpectedly accepted.")
            print("Expected incompatibility:", compatibility_message)

            nan_features = problem.features(load_factor).clone()
            nan_features[0, 0] = float("nan")
            try:
                adapter.propose(nan_features)
            except ValueError as error:
                finiteness_message = str(error)
            else:
                raise AssertionError("A non-finite adapter input was unexpectedly accepted.")
            print("Expected finite-input rejection:", finiteness_message)
            '''
        ),
        code(
            r'''
            def field_image(values):
                return values.detach().reshape(problem.ny, problem.nx).cpu().numpy()

            fig, axes = plt.subplots(1, 4, figsize=(14, 3.2), constrained_layout=True)
            panels = (
                (proposal, "compatible proposal", "magma", (0, 1)),
                (reference, "reference field", "magma", (0, 1)),
                (corrupted, "rejected proposal", "magma", (0, 1)),
                (fallback - reference, "fallback − reference", "coolwarm", (-0.02, 0.02)),
            )
            for ax, field, title, cmap, limits in zip(axes, *zip(*panels)):
                image = ax.imshow(field_image(field), origin="lower", extent=(0,1,0,1), cmap=cmap, vmin=limits[0], vmax=limits[1])
                ax.set(title=title, xlabel="x/L", ylabel="y/H", aspect="equal")
                fig.colorbar(image, ax=ax, shrink=0.78)
            fig.savefig(assets_dir() / "toy_adapter_fallback.png", dpi=160, bbox_inches="tight")
            display_figure(fig, alt="Toy adapter's compatible proposal, reference, rejected proposal, and fallback error.")
            plt.close(fig)
            '''
        ),
        code(
            r'''
            # Save one proposal/reference pair for an offline replay dataset.
            # Include reference-label cost in a later retraining comparison.
            replay_record = {
                "scope": "course-owned ToyHelmholtzProblem; one offline proposal/reference correction record",
                "load_factor": load_factor,
                "feature_order": list(FEATURE_ORDER),
                "normal_assessment": assessment,
                "rejected_assessment": rejected,
                "correction": "classical ToyHelmholtzProblem reference solve",
                "heldout_evaluation_frozen": True,
            }
            replay_path = assets_dir() / "toy_adapter_replay_record.json"
            replay_path.write_text(json.dumps(replay_record, indent=2), encoding="utf-8")
            print({"replay_record": str(replay_path.relative_to(COURSE_ROOT)), "decision": "accept compatible / fallback rejected"})
            '''
        ),
        markdown(
            r'''
            The saved correction record pairs a model proposal with its reference
            solution. An offline DAgger extension uses such records in a repeated
            cycle: collect states visited by the current model, obtain reference
            labels, add those cases to the training data, retrain, and evaluate
            on a fixed held-out set. Include the cost of reference solves when
            assessing the computational benefit of that cycle.
            '''
        ),
    ]


def export_previews():
    """Render the six retained canonical notebooks with compact presenter credits."""
    from nbconvert import HTMLExporter

    destination = NOTEBOOKS / "html"
    destination.mkdir(parents=True, exist_ok=True)
    notebooks = sorted(NOTEBOOKS.glob("0[0-5]*.ipynb"))
    if len(notebooks) != 6:
        raise ValueError("Expected the six canonical course notebooks.")
    exporter = HTMLExporter(template_name="lab")
    for path in notebooks:
        notebook = nbf.read(path, as_version=4)
        nbf.validate(notebook)
        body, _ = exporter.from_notebook_node(notebook)
        credits = (
            '<meta name="author" content="Allamaprabhu Ani">\n'
            '<meta name="presenter" content="Sathiskumar A. Ponnusami">\n'
            '<meta name="presenter-affiliation" content="Queen Mary University of London · CEMS-Lab">\n'
        )
        footer = (
            '<footer style="max-width:1100px;margin:2rem auto;padding:1rem 2rem;'
            'border-top:1px solid #b8c2cb;font:14px/1.6 system-ui,sans-serif">'
            'Presented by Sathiskumar A. Ponnusami · Queen Mary University of London · CEMS-Lab'
            '<br>© 2026 CEMS-Lab · UKACM Autumn School 2026</footer>'
        )
        body = body.replace("</head>", credits + "</head>", 1)
        body = body.replace("</body>", footer + "</body>", 1)
        (destination / (path.stem + ".html")).write_text(body, encoding="utf-8")
    print("Exported six retained notebook previews to", destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--previews-only", action="store_true",
                        help="Render existing canonical notebooks to HTML while retaining their executions.")
    parser.add_argument("--legacy-output", type=Path,
                        help="Export historical starter templates into a separate folder.")
    args = parser.parse_args()
    if args.previews_only:
        export_previews()
        return
    if args.legacy_output is None:
        parser.error("Current lessons are authored in notebooks/. Use build_lab_pages.py for the book, sync_bootstrap.py for setup, or --legacy-output for historical templates.")
    global NOTEBOOKS
    destination = args.legacy_output.resolve()
    if destination == (COURSE / "notebooks").resolve():
        parser.error("Historical templates require a separate output directory.")
    NOTEBOOKS = destination
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    write_notebook("01_phast_tiny_evolving_fracture.ipynb", first_fracture())
    write_notebook("02_degradation_autograd.ipynb", degradation())
    write_notebook("03_tiny_derivative_inverse_toy.ipynb", inverse_toy())
    write_notebook("04_train_save_reload_adapter.ipynb", training_reload())
    write_notebook("05_hybrid_reference_correction.ipynb", hybrid_adapter())
    print("Generated five UKACM day-two notebooks in", NOTEBOOKS)


if __name__ == "__main__":
    main()
