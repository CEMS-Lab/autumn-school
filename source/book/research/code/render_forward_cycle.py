"""A labelled algorithm animation; retained FEM context, illustrative local rules."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.animation import FFMpegWriter


def render(inputs: Path, output: Path):
    if inputs.is_file():
        # The public panel archive contains the same retained mesh and frames.
        with np.load(inputs, allow_pickle=False) as data:
            nodes, cells = data["nodes"], data["elements"]
            steps, damage = data["steps"], data["damage"]
    else:
        nodes = np.load(inputs / "mesh_nodes.npy", allow_pickle=False)
        cells = np.load(inputs / "mesh_elements.npy", allow_pickle=False)
        with np.load(inputs / "truth_damage_snapshots.npz", allow_pickle=False) as data:
            steps, damage = data["snapshot_steps"], data["snapshots"]
    tri = mtri.Triangulation(nodes[:, 0], nodes[:, 1], cells)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                         "axes.titlesize": 13, "axes.labelsize": 12,
                         "xtick.labelsize": 11, "ytick.labelsize": 11})
    titles = ["1. Prescribe the loading", "2. Advance the displacement",
              "3. Evaluate tensile energy", "4. Update the memory",
              "5. Solve for damage", "6. Apply damage bounds",
              "7. Repeat the forward cycle", "8. Follow sensitivity backwards"]
    formulas = [r"$s(t)=\frac{1}{2}[1-\cos(\pi t/t_r)]$",
                r"$u_{n+1}^{\rm pred}=u_n+\Delta t\,v_n+\frac{1}{2}\Delta t^2 a_n$",
                r"$\langle q\rangle_+=\max(0,q)$",
                r"$H_{n+1}=\max(H_n,\psi^+)$",
                r"$A(H,G_c,\ell_0)\widetilde d=b(H,G_c,\ell_0)$",
                r"$d_{n+1}=\min(1,\max(d_n,\widetilde d))$",
                r"$z_{n+1}=F_n(z_n,\theta)$",
                r"$\overline{z}_n=(\partial F_n/\partial z_n)^T\overline{z}_{n+1}+\partial J_n/\partial z_n$"]
    notes = ["Fixed supports select prescribed entries.\nThe cosine ramp joins its plateau continuously.",
             "Tensor operations retain the dependence on\nmaterial properties and earlier states.",
             "The positive part has a kink at zero.\nIts square has a continuous first derivative.",
             "Forward: keep the exact maximum.\nBackward option: sigmoid-weighted surrogate.",
             "Differentiate the reduced equation.\nThe operator and source both contribute.",
             "Interior: sensitivity enters the solve.\nLower bound: it enters previous damage.",
             "Updated damage changes subsequent forces.\nThe crack path emerges from this coupling.",
             "Traverse every relevant dependency.\nA surrogate VJP keeps its surrogate meaning."]
    labels = ["Load", "Motion", "Energy", "History", "Solve", "Bounds", "Repeat", "Reverse"]
    fig = plt.figure(figsize=(12, 7), dpi=110, facecolor="white")
    writer = FFMpegWriter(fps=6, codec="libx264", extra_args=["-pix_fmt", "yuv420p", "-crf", "22"])
    total = 8 * 30

    def draw(frame):
        stage, tick = divmod(frame, 30)
        fraction = tick / 29
        fig.clear()
        fig.text(.045, .947, titles[stage], fontsize=20, weight="bold")
        fig.text(.045, .904, "One forward cycle, then its reverse route", fontsize=13, color="#526168")
        ax = fig.add_axes([.07, .26, .35, .60])
        saved = min(len(steps)-1, int(fraction * len(steps))) if stage == 6 else len(steps)-1
        ax.tripcolor(tri, damage[saved], shading="gouraud", cmap="Greys", vmin=0, vmax=1)
        ax.set(xlim=(0, 40), ylim=(0, 40), aspect="equal", xlabel="x (mm)", ylabel="y (mm)",
               xticks=[0, 20, 40], yticks=[0, 20, 40])
        ax.set_title(f"Recorded damage: step {int(steps[saved])}" if stage == 6 else "Retained final damage (context)", pad=10)
        fig.text(.50, .81, formulas[stage], fontsize=18)
        fig.text(.50, .70, notes[stage], fontsize=13, linespacing=1.6)
        right = fig.add_axes([.53, .29, .40, .29])
        q = np.linspace(-.5, 1.5, 301)
        if stage == 0:
            t = np.linspace(0, 1.5, 301)
            val = np.where(t < 1, .5*(1-np.cos(np.pi*t)), 1)
            right.plot(t, val, color="#0072b2", lw=2)
            x = fraction*1.5
            right.plot(x, .5*(1-np.cos(np.pi*x)) if x<1 else 1, "o", color="#d55e00")
            right.set(xlabel="Time / ramp duration", ylabel="Load factor")
        elif stage == 2:
            right.plot(q, np.maximum(q, 0), color="#0072b2", lw=2)
            x = 2*fraction-.5
            right.plot(x, max(0,x), "o", color="#d55e00")
            right.set(xlabel="Illustrative principal strain q", ylabel="Positive part")
        elif stage == 3:
            x = .5+fraction
            right.plot(q, np.maximum(1,q), color="#0072b2", lw=2, label="Forward maximum")
            right.plot(x, max(1,x), "o", color="#d55e00")
            right.axvline(1,color="#7a858a",ls=":")
            right.set(xlabel="Illustrative current energy", ylabel="History", ylim=(0,1.65))
            weight = 1/(1+np.exp(-12*(x-1)))
            fig.text(.53,.20,f"Surrogate current-energy weight: {weight:.3f} (k = 12)",fontsize=11,color="#007d59")
        elif stage == 5:
            right.plot(q, np.minimum(1,np.maximum(.4,q)),color="#0072b2",lw=2)
            x=2*fraction-.5
            right.plot(x,min(1,max(.4,x)),"o",color="#d55e00")
            right.set(xlabel="Illustrative unconstrained damage",ylabel="Bounded damage",ylim=(0,1.15))
        else:
            right.axis("off")
            extra = {
                1: "$M a = f^{\\rm ext}-f^{\\rm int}-f^{\\rm damp}$\n\nFixed boundary values are re-applied.",
                4: "$A^T\\lambda=g$\n\n$J_q=\\lambda^T(b_q-A_q\\widetilde d)$\n\nCheck measured solve residuals.",
                6: "1,600 forward steps\n12 retained damage frames\n\nPlayback uses the 12 retained frames.",
                7: "Loss -> damage -> history -> energy\n-> mechanics -> material parameters\n\nCheck branches and finite differences."
            }
            right.text(0,.8,extra[stage],va="top",fontsize=13,linespacing=1.55)
        if stage in (0,2,3,5):
            right.grid(alpha=.22);right.spines[["top","right"]].set_visible(False)
        for j,label in enumerate(labels):
            x=.052+j*.119
            fig.text(x,.145,label,fontsize=12,color="#0072b2" if j==stage else "#627078",weight="bold" if j==stage else "normal")
            if j<7:fig.text(x+.09,.145,"<" if stage==7 else ">",fontsize=12,color="#9aa4aa")
        fig.text(.045,.077,"Full plate damage: white 0, black 1. Stages follow computational order; playback is paced for reading.",fontsize=10,color="#526168")
        fig.text(.045,.048,"Retained plate damage frames with illustrative energy/history curves.",fontsize=10,color="#526168")
    with writer.saving(fig, str(output / "forward_cycle.mp4"), dpi=110):
        for frame in range(total):
            draw(frame)
            if frame == 3*30+15:
                fig.savefig(output / "forward_cycle.png", dpi=150)
            if frame % 30 == 15:
                fig.savefig(output / f"cycle_scene_{frame//30+1}.png", dpi=110)
            writer.grab_frame()
    plt.close(fig)
    receipt = {"kind":"Algorithm walkthrough with illustrative local curves and retained FEM context",
               "frames":total,"fps":6,"duration_seconds":40,"retained_steps":steps.tolist(),
               "new_forward_solve":False,"reconstructed_energy_or_history":False,
               "full_damage_range":[0,1]}
    (output / "forward_cycle_manifest.json").write_text(json.dumps(receipt,indent=2)+"\n")
    return receipt


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True,
                        help="Retained input directory or public history_plate_arrays.npz")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    render(args.inputs, args.output)
