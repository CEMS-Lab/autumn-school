"""Bounded local load-extension experiment using the unchanged public solver."""
from __future__ import annotations
import argparse
import json
import signal
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "notebooks"))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--opening", type=float, default=0.08)
    parser.add_argument("--nx", type=int, default=96)
    parser.add_argument("--steps", type=int, default=60)
    parser.add_argument("--max-stagger", type=int, default=200)
    parser.add_argument("--cap", type=int, default=240)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    def expired(*_):
        raise TimeoutError(f"Experiment reached {args.cap} second cap")
    signal.signal(signal.SIGALRM, expired)
    signal.alarm(args.cap)
    started = time.perf_counter()
    import numpy as np
    import torch
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.tri as mtri
    from day2_helpers import import_public_phast, load_forward_config
    from day2_helpers.forward_workflow import (prepare_course_mesh, solver_configuration,
        solve_prepared_case, save_results)
    config = load_forward_config()
    config["loading"]["total_symmetric_vertical_displacement"] = args.opening
    config["loading"]["n_load_steps"] = args.steps
    config["mesh"].update(nx=args.nx, ny=args.nx // 2)
    config["solver"]["max_stagger"] = args.max_stagger
    info = import_public_phast(config["public_source"]["revision"])
    from phast.physics.boundary_conditions import symmetric_tension_bcs
    from phast.physics.material import Material
    from phast.solvers.staggered_solver import StaggeredSolver
    torch.set_num_threads(2)
    torch.manual_seed(config["seed"])
    mesh = prepare_course_mesh(config, args.out / "mesh.npz")
    nodes = mesh.nodes
    precrack = ((nodes[:, 1] - config["geometry"]["height"] / 2).abs() < 1e-12)
    precrack &= nodes[:, 0] <= config["geometry"]["notch_length"] + 1e-12
    bcs = symmetric_tension_bcs(mesh, disp=args.opening)
    bcs.add_pf_dirichlet(torch.where(precrack)[0], value=1.)
    solver = StaggeredSolver(mesh, Material(**config["material"]), bcs,
                             solver_configuration(config))
    solver.d[precrack] = 1.
    factors = torch.linspace(config["loading"]["first_load_factor"], 1., args.steps,
                             dtype=torch.float64)
    report = {"config": config, "status": "started"}
    (args.out / "configuration.json").write_text(json.dumps(config, indent=2))
    try:
        result = solve_prepared_case(solver, config, factors, precrack, info,
                                     retain_history=True)
        save_results(result, args.out, "load_extension")
        d = result["arrays"]["final_damage"]
        xy = result["arrays"]["nodes"]
        center = np.isclose(xy[:, 1], 1.)
        mid = d[center]
        xpos = xy[center, 0]
        report.update(status="passed", steps=args.steps,
            threshold_fronts={str(t): float(xpos[mid >= t].max()) for t in (.5, .8, .9)},
            minimum_ligament_damage=float(mid[xpos >= .8].min()),
            peak_reaction=max(x["reaction_top_y"] for x in result["metadata"]["trace"]),
            final_reaction=result["metadata"]["trace"][-1]["reaction_top_y"])
        fig, ax = plt.subplots(1, 2, figsize=(11, 3.6), layout="constrained")
        tri = mtri.Triangulation(xy[:, 0], xy[:, 1], result["arrays"]["elements"])
        im = ax[0].tripcolor(tri, d, vmin=0, vmax=1, cmap="magma", shading="gouraud")
        ax[0].set(aspect="equal", xlabel="$x$", ylabel="$y$", title="Final damage")
        fig.colorbar(im, ax=ax[0], label="$d$")
        tr = result["metadata"]["trace"]
        ax[1].plot([x["applied_separation"] for x in tr], [x["reaction_top_y"] for x in tr])
        ax[1].set(xlabel="Opening", ylabel="Top reaction", title="Load response")
        fig.savefig(args.out / "field_response.png", dpi=150)
        plt.close(fig)
    except Exception as exc:
        report.update(status="failed", error=repr(exc))
    finally:
        report["complete_seconds"] = time.perf_counter() - started
        signal.alarm(0)
        (args.out / "receipt.json").write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2), flush=True)

if __name__ == "__main__":
    main()
