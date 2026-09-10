"""Forward-only teaching loop and portable numerical results for Practical 1."""
from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import torch

SCHEMA = "phast-course-forward-v1"


def digest_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def configuration_hash(config):
    return hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()


def notebook_source_hash(path):
    """Hash authored cell types and text independently of retained outputs."""
    notebook = json.loads(Path(path).read_text(encoding="utf-8"))
    cells = [{"cell_type": cell["cell_type"],
              "source": "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]}
             for cell in notebook["cells"]]
    return hashlib.sha256(json.dumps(cells, sort_keys=True).encode()).hexdigest()


def solver_configuration(config):
    """Translate the public course case into the public solver configuration."""
    from phast.solvers.staggered_solver import SolverConfig
    settings = dict(config["solver"])
    settings["backend"] = settings.pop("mechanics_backend")
    settings["preconditioner"] = settings.pop("damage_preconditioner")
    return SolverConfig(**settings)


def solve_prepared_case(solver, config, load_factors, precrack, phast_info):
    """Advance the exact solver constructed in the notebook and check every step.

    All inputs are retained as constructed: this routine creates neither a mesh
    nor boundary conditions. The mesh is T3 and states use CPU float64.
    """
    mesh, bcs = solver.mesh, solver.bcs
    expected = torch.linspace(config["loading"]["first_load_factor"],
                              config["loading"]["last_load_factor"],
                              config["loading"]["n_load_steps"], dtype=torch.float64)
    torch.testing.assert_close(load_factors, expected, rtol=0, atol=0)
    assert solver.config.fail_on_mechanics_nonconvergence
    assert solver.config.fail_on_stagger_nonconvergence
    assert solver.config.solver_type == config["solver"]["solver_type"] == "quasi_static"
    assert solver.config.stagger_criterion == "relative" and solver.config.stagger_norm == "l2"
    assert not solver.config.adaptive_stagger_tol
    assert mesh.nodes.dtype == torch.float64 and solver.u.device.type == "cpu"
    assert precrack.dtype == torch.bool and precrack.shape == (mesh.n_nodes,)
    assert bool(precrack.any()) and bool((~precrack).any())
    assert torch.all(solver.d[precrack] == 1)
    tolerance = 1.e-10
    top, bottom = mesh.node_sets["top"], mesh.node_sets["bottom"]
    exterior = torch.unique(torch.cat([mesh.node_sets[k] for k in ("left", "right", "top", "bottom")]))
    seeded = solver.d.detach().clone()
    previous = seeded.clone()
    snapshots = {0: seeded}
    displacement_snapshots = {0: solver.u.detach().clone()}
    trace, caught_messages = [], []
    started = time.perf_counter()
    max_bc_error, minimum_increment = 0.0, 0.0
    for step, factor in enumerate(load_factors, start=1):
        step_started = time.perf_counter()
        bcs.load_factor = float(factor)
        mask, values = bcs.get_masks_and_values()
        prescribed = config["loading"]["total_symmetric_vertical_displacement"] * float(factor) / 2
        assert mask[exterior, 0].all() and mask[top, 1].all() and mask[bottom, 1].all()
        torch.testing.assert_close(values[top, 1], torch.full_like(values[top, 1], prescribed))
        torch.testing.assert_close(values[bottom, 1], torch.full_like(values[bottom, 1], -prescribed))
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            solver.step_full()
        caught_messages.extend(str(item.message) for item in caught)
        assert torch.isfinite(solver.u).all() and torch.isfinite(solver.d).all()
        assert float(solver.d.min()) >= -tolerance and float(solver.d.max()) <= 1 + tolerance
        increment_min = float((solver.d - previous).min())
        minimum_increment = min(minimum_increment, increment_min)
        assert increment_min >= -tolerance, "Damage irreversibility at this load step"
        torch.testing.assert_close(solver.d[precrack], torch.ones_like(solver.d[precrack]), atol=tolerance, rtol=0)
        bc_error = float((solver.u[mask] - values[mask]).abs().max())
        max_bc_error = max(max_bc_error, bc_error)
        assert bc_error <= tolerance
        assert float(solver._last_residual) <= config["solver"]["stagger_tol"]
        internal = solver.fem.internal_force(solver.u, solver.d)
        trace.append({"step": step, "load_factor": float(factor),
                      "applied_separation": 2 * prescribed,
                      "reaction_top_y": float(internal[top, 1].sum()),
                      "damage_outside_sum": float(solver.d[~precrack].sum()),
                      "damage_outside_max": float(solver.d[~precrack].max()),
                      "max_displacement": float(solver.u.abs().max()),
                      "stagger_iterations": int(solver._last_stagger_iter),
                      "stagger_residual": float(solver._last_residual),
                      "boundary_value_error": bc_error,
                      "minimum_damage_increment": increment_min,
                      "step_seconds": time.perf_counter() - step_started})
        if step in {1, len(load_factors) // 2, len(load_factors)}:
            snapshots[step] = solver.d.detach().clone()
            displacement_snapshots[step] = solver.u.detach().clone()
        previous = solver.d.detach().clone()
    elapsed = time.perf_counter() - started
    assert not caught_messages, caught_messages
    first, final = snapshots[1], snapshots[len(load_factors)]
    increment = (final - first).clamp_min(0)
    arrays = {"nodes": mesh.nodes, "elements": mesh.elements, "precrack": precrack,
              "seeded_damage": seeded, "first_damage": first, "final_damage": final,
              "incremental_damage": increment, "final_displacement": solver.u.detach(),
              "snapshot_steps": torch.tensor(sorted(snapshots)),
              "damage_snapshots": torch.stack([snapshots[k] for k in sorted(snapshots)]),
              "displacement_snapshots": torch.stack([displacement_snapshots[k] for k in sorted(snapshots)])}
    arrays.update({f"boundary_{name}": mesh.node_sets[name] for name in ("left", "right", "top", "bottom")})
    arrays = {key: value.detach().cpu().numpy().copy() for key, value in arrays.items()}
    summary = {"nodes": mesh.n_nodes, "elements": mesh.n_elems,
               "load_steps": len(load_factors), "solve_seconds": elapsed,
               "incremental_damage_outside_sum": float(increment[~precrack].sum()),
               "incremental_damage_outside_max": float(increment[~precrack].max()),
               "final_damage_outside_max": float(final[~precrack].max()), "warnings": caught_messages}
    metadata = {"schema_version": SCHEMA, "config": config, "config_sha256": configuration_hash(config),
                "phast": phast_info, "summary": summary, "trace": trace,
                "resolved_model": {"plane_stress": bool(solver.material.plane_stress),
                                   "kinematics": "plane stress" if solver.material.plane_stress else "plane strain",
                                   "energy_split": solver.material.energy_split,
                                   "phase_field_model": solver.material.pf_model},
                "resolved_solver": {"solver_type": solver.config.solver_type,
                                    "stagger_criterion": solver.config.stagger_criterion,
                                    "stagger_norm": solver.config.stagger_norm,
                                    "stagger_tolerance": solver.config.stagger_tol,
                                    "adaptive_stagger_tolerance": bool(solver.config.adaptive_stagger_tol)},
                "conventions": {"units": "dimensionless teaching scales",
                                "coordinates": "x,y; rectangle [0,width] x [0,height]",
                                "displacement": "nodal ux,uy; same length scale as coordinates",
                                "damage": "0 intact; 1 fully damaged",
                                "reaction_top_y": "sum of internal y-force on top prescribed nodes",
                                "damage_outside_sum": "mesh-dependent nodal sum outside locked precrack",
                                "stagger_residual": "maximum relative L2 iterate change of displacement and damage; denominator is current-iterate L2 norm plus 1e-30",
                                "snapshot_steps": "0 seeded; subsequent IDs index quasistatic load increments",
                                "boundary_conditions": "ux=0 on all exterior edges; uy=+/-separation/2 on top/bottom; d=1 on precrack"},
                "checks": {"finite_states": True, "damage_bounds": True, "irreversibility": True,
                           "maximum_boundary_error": max_bc_error, "minimum_damage_increment": minimum_increment,
                           "state_tolerance": tolerance, "strict_mechanics_and_stagger_flags": True,
                           "stagger_residual_checked_each_step": True, "warning_count": len(caught_messages)},
                "environment": {"python": sys.version.split()[0], "platform": platform.platform(),
                                "machine": platform.machine(), "torch": torch.__version__,
                                "numpy": np.__version__, "device": "cpu", "dtype": "float64",
                                "torch_threads": torch.get_num_threads()}}
    return {"arrays": arrays, "metadata": metadata, "solver": solver}


def save_results(result, directory, stem="tiny_notched_tension"):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    field_path, metadata_path = directory / f"{stem}_fields.npz", directory / f"{stem}_summary.json"
    np.savez_compressed(field_path, **result["arrays"])
    record = dict(result["metadata"])
    record["fields_sha256"] = digest_file(field_path)
    metadata_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return field_path, metadata_path


def load_results(field_path, metadata_path):
    """Read portable arrays and validate their schema, dimensions and hash."""
    record = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
    assert record["schema_version"] == SCHEMA
    assert record["fields_sha256"] == digest_file(field_path)
    assert record["config_sha256"] == configuration_hash(record["config"])
    with np.load(field_path, allow_pickle=False) as archive:
        arrays = {key: archive[key].copy() for key in archive.files}
    n = record["summary"]["nodes"]
    assert arrays["nodes"].shape == arrays["final_displacement"].shape == (n, 2)
    assert arrays["elements"].shape == (record["summary"]["elements"], 3)
    assert arrays["elements"].dtype.kind in "iu"
    assert arrays["elements"].min() >= 0 and arrays["elements"].max() < n
    assert arrays["precrack"].dtype == bool
    for name in ("precrack", "seeded_damage", "first_damage", "final_damage", "incremental_damage"):
        assert arrays[name].shape == (n,)
    for name in ("left", "right", "top", "bottom"):
        indices = arrays[f"boundary_{name}"]
        assert indices.ndim == 1 and indices.size > 0
        assert indices.dtype.kind in "iu"
        assert indices.min() >= 0 and indices.max() < n
        assert len(np.unique(indices)) == len(indices)
    assert all(np.isfinite(value).all() for value in arrays.values())
    steps = arrays["snapshot_steps"]
    n_steps = record["config"]["loading"]["n_load_steps"]
    assert steps.ndim == 1 and steps.dtype.kind in "iu" and len(steps) >= 3
    assert np.all(steps[1:] > steps[:-1]) and np.all((0 <= steps) & (steps <= n_steps))
    assert steps[0] == 0 and steps[1] == 1 and steps[-1] == n_steps
    k = len(steps)
    assert arrays["damage_snapshots"].shape == (k, n)
    assert arrays["displacement_snapshots"].shape == (k, n, 2)
    np.testing.assert_array_equal(arrays["damage_snapshots"][0], arrays["seeded_damage"])
    np.testing.assert_array_equal(arrays["damage_snapshots"][1], arrays["first_damage"])
    np.testing.assert_array_equal(arrays["damage_snapshots"][-1], arrays["final_damage"])
    np.testing.assert_array_equal(arrays["displacement_snapshots"][-1], arrays["final_displacement"])
    assert len(record["trace"]) == record["summary"]["load_steps"] == n_steps
    assert [row["step"] for row in record["trace"]] == list(range(1, n_steps + 1))
    resolved = record["resolved_model"]
    assert isinstance(resolved["plane_stress"], bool)
    assert resolved["kinematics"] == ("plane stress" if resolved["plane_stress"] else "plane strain")
    assert record["resolved_solver"]["stagger_criterion"] == "relative"
    assert record["resolved_solver"]["stagger_norm"] == "l2"
    return arrays, record
