"""Generate the five small, canonical UKACM day-two notebooks.

This script is intentionally checked in beside the notebooks so their compact,
repeated setup cells and source-boundary statements can be regenerated without
hand-editing JSON.  It does not execute notebooks; see ``reviews/notebook_runtime.md``
for the executed outputs and receipts.
"""

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import nbformat as nbf


COURSE = Path(__file__).resolve().parents[1]
NOTEBOOKS = COURSE / "notebooks"


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

            This is an actual **public PhAST** AT2 phase-field solve, run on a
            CPU with a structured triangular mesh.  It makes a rectangle,
            identifies its boundaries, applies symmetric tension, locks a
            centreline precrack, and advances sixty **quasi-static load
            increments**.  It is not a physical-time dynamic simulation and
            it does not use XFEM.

            The execution pin is `CEMS-Lab/PhAST@f6324f899f0701769810be117f27f1208f7a582e`
            (version 0.16.2).  The tested local route is source-first import:
            `PYTHONPATH=<public-PhAST>/src python`.  The course bundle prefers
            `vendor/PhAST/src` and verifies its manifest if Git metadata is not
            present.  `python -m pip install ./vendor/PhAST` is a preparatory
            setup option, not part of the recorded notebook timing.  The next
            cell verifies that the public pin, rather than a neighbouring
            private checkout, was imported.

            **What to look for.** `d=0` means intact-like and `d=1` means
            fully broken.  The locked centreline is only the initial crack.
            The calculation must show a positive increment of damage outside
            that set as load increases; otherwise it is a setup check, not the
            promised evolving-damage result.
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

            The next cell is the same transparent setup used by the runner.
            It first generates the T3 mesh in memory, then saves and reloads a
            small prepared **tensor-mesh** file.  This is a recovery/import
            route for the course specimen—not a claim that an external mesh
            file with physical groups was used.  `identify_boundaries()` makes
            the `left`, `right`, `top`, and `bottom` node labels; the explicit
            centreline mask labels the precrack.
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
            to the configured tolerance.  The public implementation contains
            both assembled sparse and matrix-free element-operator paths; this
            notebook demonstrates the assembled sparse-direct mechanics route,
            so it does not claim that no matrices are constructed.

            A quasi-Newton/Newton method would be a nonlinear **solution
            algorithm**, while XFEM would be a crack **representation**.  The
            present calculation instead uses a regularised phase-field
            formulation on T3 elements.
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
            # The checks describe the promised evidence, not an aesthetic judgement.
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
            top prescribed-displacement nodes; it is a compact response
            diagnostic, not a calibrated experimental force.  The damage
            fields and the increase outside the locked precrack are the key
            evidence that the computation evolved.

            Try changing only `Gc`, `l0`, the total displacement, or the mesh
            density in `configs/day2_forward/tiny_notched_tension.json`, then
            rerun.  State both the observed change and a limitation: this is a
            small plane problem with a hand-made mesh, a selected energy split,
            and no mesh-convergence study.  Do not compare its wall time to a
            dynamic impact example or to an unmeasured Colab run.
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

            We use `d=0` for intact and `d=1` for broken, `eta=10^{-7}`, and
            `float64`.  The comparison is deliberately local and smooth: it
            is not a claim that every coupled fracture route is automatically
            differentiable through history updates, convergence logic, clamps,
            or active sets.
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
            **Why this matters.** PyTorch tensors make automatic differentiation
            available for tensor operations that remain connected to a scalar
            loss.  A full solver derivative additionally depends on the chosen
            route: boundary treatment, linear/nonlinear solve, history update,
            detaches, clipping, and convergence behaviour all matter.  The
            next notebook keeps that chain visible in a small original bar toy.
            '''
        ),
    ]


def inverse_toy():
    return [
        markdown(
            r'''
            # 03 — A tiny differentiable inverse exercise (course-owned toy)

            This notebook is an original one-dimensional elastic-bar tensor
            exercise.  It is **not a PhAST fracture inverse**, does not use
            research data, and should not be used to infer the differentiability
            of a history-dependent damage calculation.  It makes the chain
            explicit: trainable modulus → stiffness tensor → linear solve →
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
            The bar is intentionally simple enough that its exact sensitivity
            is known.  In a fracture inverse exercise, nonsmooth history maxima,
            irreversibility constraints, load path, solver tolerance, and the
            observation design require additional verification.  This toy gives
            learners a short place to diagnose AD versus finite differences
            before encountering those complications.
            '''
        ),
    ]


def training_reload():
    return [
        markdown(
            r'''
            # 04 — Train, save, reload, and compare a tiny field model

            We train one small MLP on an original, course-owned
            `ToyHelmholtzProblem`.  It is a fast field equation with a known
            discrete residual, designed to demonstrate data splits, checkpoint
            metadata, and a held-out field comparison.  It is **not PhAST
            fracture data**, a trained public `learned_damage` model, or a
            claim of fracture acceleration.

            Feature contract: nodewise `[x/L, y/H, load_factor]`, all
            dimensionless, in exactly that order; output: one nodewise
            damage-like proposal in `[0,1]`.  Whole load cases—not individual
            nodes—are separated into train/validation/test splits.
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
            print({"MLP_heldout_RMSE": heldout_rmse, "RBF_heldout_RMSE": rbf_rmse, "RBF_scope": "same toy feature contract only"})
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
            An MLP and RBF can both consume this *toy* nodewise representation;
            a CNN would require mesh-to-grid maps, and a GNN/GNO would require
            connectivity/operator inputs.  A model name alone is not a
            compatibility guarantee.
            '''
        ),
    ]


def hybrid_adapter():
    return [
        markdown(
            r'''
            # 05 — A compatible proposal, residual check, and fallback

            This notebook connects the checkpoint from notebook 04 to a
            **course-owned teaching adapter**.  The adapter verifies its
            feature order and mesh signature, predicts under `torch.no_grad()`,
            projects bounds and irreversibility, evaluates the discrete
            `ToyHelmholtzProblem` residual, and falls back to the reference
            solve when the proposal fails the gate.

            The public PhAST learned-damage hook is an inference interface with
            detached/no-gradient prediction.  This notebook does not train
            through that hook and its residual is not a PhAST AT2 residual.
            It teaches the reusable logic: proposal → compatibility →
            constraint projection → assess → correction/record.
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
            # One correction record is a replay-style teaching artefact, not an
            # end-to-end DAgger result. Reference-label cost remains part of any
            # later retraining comparison.
            replay_record = {
                "scope": "course-owned ToyHelmholtzProblem; one offline correction record, not PhAST DAgger",
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
            A genuine offline DAgger cycle would collect model-induced states,
            obtain reference labels, aggregate only training data, retrain, and
            reassess a frozen held-out set.  The small record above is the
            transparent first step, not evidence that such a loop has been run
            for PhAST fracture or that a learned proposal accelerates it.
            '''
        ),
    ]


def main():
    NOTEBOOKS.mkdir(parents=True, exist_ok=True)
    write_notebook("01_phast_tiny_evolving_fracture.ipynb", first_fracture())
    write_notebook("02_degradation_autograd.ipynb", degradation())
    write_notebook("03_tiny_derivative_inverse_toy.ipynb", inverse_toy())
    write_notebook("04_train_save_reload_adapter.ipynb", training_reload())
    write_notebook("05_hybrid_reference_correction.ipynb", hybrid_adapter())
    print("Generated five UKACM day-two notebooks in", NOTEBOOKS)


if __name__ == "__main__":
    main()
