"""Bounded B3 reproduction with observational damage-KKT diagnostics.

Runs the pinned public CLI unchanged. The observer retains the exact damage
subproblem inputs and calls its public residual evaluator after each update.
It changes neither returned fields nor material/solver kernels.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
MESH_SHA = "59c3a41dff41a03fdef93bdd91f974e2d1a263a01aaa96094c125b08cb5e14be"


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def worker(out):
    import numpy as np
    import torch

    sys.path.insert(0, str(ROOT / "vendor/PhAST/src"))
    from phast.solvers.damage_solver import PhaseFieldDamageSolver
    from phast.solvers.staggered_solver import StaggeredSolver
    from phast.config.run_config import main

    torch.set_num_threads(1)
    original_solve = PhaseFieldDamageSolver.solve
    original_step = StaggeredSolver.step_full
    rows, states, displacements = [], [], []
    holder = {}
    minimum_increment = 0.0
    maximum_bc_error = 0.0
    finite = True
    maxima = {"u": 0.0, "v": 0.0, "d": 0.0}

    def observed_solve(self, H, previous, *args, **kwargs):
        h_before = H.detach().clone()
        lower = previous.detach().clone()
        initial = kwargs.get("initial_guess")
        initial = lower if initial is None else initial.detach().clone()
        fixed = kwargs.get("pf_dirichlet_mask")
        fixed = torch.zeros_like(lower, dtype=torch.bool) if fixed is None else fixed.clone()
        returned = original_solve(self, H, previous, *args, **kwargs)
        with torch.no_grad():
            # R = A d - b. At a lower bound, R >= 0 is admissible;
            # at an upper bound, R <= 0 is admissible.
            residual = self.compute_residual(h_before, returned).clone()
            initial_residual = self.compute_residual(h_before, initial).clone()
            rhs = -self.compute_residual(h_before, torch.zeros_like(returned)).clone()
            initial_residual[fixed] = 0.0
            projected = residual.clone()
            at_lower = returned <= lower + 1.e-14
            at_upper = returned >= 1.0 - 1.e-14
            active = (at_lower & (residual >= 0)) | (at_upper & (residual <= 0)) | fixed
            projected[active] = 0.0
            ref = max(float(torch.linalg.vector_norm(rhs)),
                      float(torch.linalg.vector_norm(initial_residual)), 1.e-30)
            absolute = float(torch.linalg.vector_norm(projected))
            ratio = absolute / ref
            row = {"update": len(rows), "iterations": int(self.last_iter),
                   "bounds_method": self._bounds_method,
                   "projected_residual_l2": absolute,
                   "reference_l2": ref, "projected_residual_relative": ratio,
                   "configured_tolerance": float(self.tol),
                   "independent_converged": bool(np.isfinite(ratio) and ratio <= self.tol),
                   "minimum_increment": float((returned - lower).min()),
                   "minimum_damage": float(returned.min()), "maximum_damage": float(returned.max()),
                   "finite": bool(torch.isfinite(returned).all() and torch.isfinite(residual).all()),
                   "fixed_dofs": int(fixed.sum()), "active_dofs": int(active.sum()),
                   "raw_residual_l2": float(torch.linalg.vector_norm(residual[~fixed])),
                   "solver_convergence_flag": getattr(self, "last_converged", None)}
            rows.append(row)
        return returned

    def observed_step(self):
        nonlocal minimum_increment, finite, maximum_bc_error
        holder["solver"] = self
        if not states:
            states.append(self.d.detach().cpu().numpy().copy())
            displacements.append(self.u.detach().cpu().numpy().copy())
        previous = self.d.detach().clone()
        result = original_step(self)
        mask, values = self.bcs.get_masks_and_values()
        maximum_bc_error = max(maximum_bc_error, float((self.u[mask] - values[mask]).abs().max()))
        minimum_increment = min(minimum_increment, float((self.d - previous).min()))
        finite = finite and all(bool(torch.isfinite(x).all()) for x in (self.u, self.v, self.d, self.H_elem))
        for key in maxima:
            maxima[key] = max(maxima[key], float(getattr(self, key).abs().max()))
        states.append(self.d.detach().cpu().numpy().copy())
        displacements.append(self.u.detach().cpu().numpy().copy())
        return result

    PhaseFieldDamageSolver.solve = observed_solve
    StaggeredSolver.step_full = observed_step
    sys.argv = ["phast run", str(out / "config.yaml"), "--device", "cpu", "--output_dir", str(out / "cli_output")]
    started = time.perf_counter()
    main()
    solve_seconds = time.perf_counter() - started
    solver = holder["solver"]
    np.savez_compressed(out / "trajectory.npz", nodes=solver.mesh.nodes.cpu().numpy(),
                        elements=solver.mesh.elements.cpu().numpy(), damage=np.asarray(states),
                        displacement=np.asarray(displacements),
                        state_index=np.arange(len(states)),
                        time=np.maximum(np.arange(len(states)) - 1, 0) * solver.dt)
    for row in rows:
        row["time"] = row["update"] * solver.dt
    with (out / "diagnostics.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    energy_path = out / "cli_output/energy.csv"
    energy = np.genfromtxt(energy_path, delimiter=",", names=True)
    coords = solver.mesh.nodes.cpu().numpy()
    d = states[-1]
    strip = (coords[:, 0] > 20) & (np.abs(coords[:, 1] - 20) <= 1)
    thresholds = {str(q): float(coords[strip & (d >= q), 0].max(initial=20) - 20)
                  for q in (.5, .9, .95)}
    summary = {"source": "public vendored PhAST 0.16.2; observational wrapper only",
               "model": "B3 geometric single-edge notch, dynamic plane-strain spectral AT2",
               "nodes": len(coords), "elements": len(solver.mesh.elements),
               "states_including_initial": len(states), "steps": len(states) - 1,
               "dt": solver.dt, "cli_and_observer_seconds": solve_seconds,
               "mesh_sha256": digest(out / "mesh.msh"), "finite_states": finite,
               "minimum_damage_increment": minimum_increment, "absolute_state_maxima": maxima,
               "maximum_displacement_boundary_error": maximum_bc_error,
               "energy_fields": list(energy.dtype.names),
               "finite_energy": all(np.isfinite(energy[k]).all().item() for k in energy.dtype.names),
               "maximum_projected_relative_residual": max(r["projected_residual_relative"] for r in rows),
               "damage_updates": len(rows),
               "independent_converged_updates": sum(r["independent_converged"] for r in rows),
               "unconverged_update_indices": [r["update"] for r in rows if not r["independent_converged"]],
               "residual_convention": "R=A*d-b; zero admissible lower/upper-active and pinned components; ||projected R||/max(||b||,||R(initial)||,1e-30)",
               "bound_comparison_atol": 1.e-14,
               "iterations_range": [min(r["iterations"] for r in rows), max(r["iterations"] for r in rows)],
               "final_ligament_extension_mm_by_threshold": thresholds,
               "time_convention": "Initial state index0; index k+1 is public CLI step k, labelled t=k*dt; public CFL loop convention retained",
               "scope": "Qualitative coarse public example; mesh and temporal convergence require separate comparisons",
               "python": sys.version, "torch": torch.__version__, "platform": platform.platform()}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({key: value for key, value in summary.items() if key != "unconverged_update_indices"}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--case", default="b3_observed_post_clamp")
    parser.add_argument("--bounds", choices=["post_clamp", "projected_cg"], default="post_clamp")
    parser.add_argument("--dt-safety", type=float, default=.8)
    parser.add_argument("--jacobi", action="store_true")
    args = parser.parse_args()
    out = ROOT / "evidence/propagation_20260911" / args.case
    if args.worker:
        worker(out)
        return
    import yaml

    out.mkdir(parents=True, exist_ok=False)
    raw = yaml.safe_load((ROOT / ".build/propagation-review/b3_imported.yaml").read_text())
    public_mesh = Path(raw["geometry"]["mesh_path"])
    assert digest(public_mesh) == MESH_SHA
    shutil.copy2(public_mesh, out / "mesh.msh")
    raw["geometry"]["mesh_path"] = "mesh.msh"
    raw["solver"]["bounds_method"] = args.bounds
    raw["solver"]["dt_safety"] = args.dt_safety
    if args.jacobi:
        raw["solver"]["use_multigrid"] = False
        raw["solver"]["preconditioner"] = "jacobi"
    # Keep the public recipe's complete 100-us horizon and all material,
    # cadence, precision, support and loading settings.
    (out / "config.yaml").write_text(yaml.safe_dump(raw, sort_keys=False))
    tracked = list((ROOT / "vendor/PhAST/src/phast").rglob("*.py"))
    hashes_before = {str(path.relative_to(ROOT)): digest(path) for path in tracked}
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", "--case", args.case]
    env = dict(os.environ, PYTHONUNBUFFERED="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MPLBACKEND="Agg")
    started = time.perf_counter()
    timeout = False
    with (out / "run.log").open("w") as stream:
        proc = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT, env=env, start_new_session=True)
        try:
            code = proc.wait(timeout=240)
        except subprocess.TimeoutExpired:
            timeout = True
            os.killpg(proc.pid, signal.SIGKILL)
            code = proc.wait()
    receipt = {"command": command, "whole_process_seconds": time.perf_counter() - started,
               "hard_cap_seconds": 240, "timeout": timeout, "exit_code": code,
               "script_sha256": digest(__file__), "config_sha256": digest(out / "config.yaml"),
               "vendor_unchanged": all(digest(ROOT / key) == value for key, value in hashes_before.items()),
               "vendor_source_sha256": hashes_before}
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt.items() if k != "vendor_source_sha256"}, indent=2))


if __name__ == "__main__":
    main()
