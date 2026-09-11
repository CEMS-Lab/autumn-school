"""Render the sampled numerical trajectory of the B3 propagation diagnostic."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.animation import FuncAnimation, PillowWriter

ROOT = Path(__file__).resolve().parents[1]

def connected_tip(d, xy, adjacency, threshold):
    active = d >= threshold
    seeds = np.flatnonzero(active & (np.abs(xy[:, 0] - 20) <= .75)
                            & (np.abs(xy[:, 1] - 20) <= .75))
    seen = set(seeds.tolist())
    queue = seeds.tolist()
    while queue:
        node = queue.pop()
        for other in adjacency[node]:
            if active[other] and other not in seen:
                seen.add(other)
                queue.append(other)
    return max(20., max((xy[i, 0] for i in seen), default=20.))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=ROOT / "assets/propagation_review")
    args = parser.parse_args()
    args.run = args.run.resolve()
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)
    path = args.run / "trajectory.npz"
    if not path.exists():
        path = args.run / "all_states.npz"
    with np.load(path, allow_pickle=False) as a:
        xy, elements = a["nodes"], a["elements"]
        time, damage = a["time"], a["damage"]
    assert damage.shape == (len(time), len(xy))
    assert np.all(np.diff(time) >= 0) and time[-1] > 0 and np.isfinite(damage).all()
    assert np.min(np.diff(damage, axis=0)) >= -1e-7
    tri = mtri.Triangulation(xy[:, 0], xy[:, 1], elements)
    adjacency = [set() for _ in xy]
    for a, b, c in elements:
        adjacency[a].update((int(b), int(c)))
        adjacency[b].update((int(a), int(c)))
        adjacency[c].update((int(a), int(b)))
    desired_us = np.r_[np.linspace(0, min(45., time[-1]*1e6), 91),
                       np.linspace(min(45., time[-1]*1e6), time[-1]*1e6, 16)]
    frames = np.unique([np.abs(time*1e6 - t).argmin() for t in desired_us])
    thresholds = (.5, .8, .9)
    rows = []
    for i in frames:
        rows.append({"state_index": int(i), "time_us": float(time[i]*1e6),
            **{f"connected_extension_d{q}": connected_tip(damage[i], xy, adjacency, q)-20.
               for q in thresholds}})
    with (args.out / "connected_extension.csv").open("w") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 11,
        "axes.titlesize": 12, "axes.labelsize": 11, "legend.fontsize": 10,
        "xtick.labelsize": 10, "ytick.labelsize": 10, "figure.dpi": 150,
        "lines.linewidth": 1.8})
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.8), layout="constrained")
    for ax, target in zip(axes, (0., 20., 30., time[-1]*1e6)):
        i = np.abs(time*1e6-target).argmin()
        field = ax.tripcolor(tri, damage[i], shading="gouraud", cmap="magma", vmin=0, vmax=1)
        ax.set(aspect="equal", xlim=(0,40), ylim=(0,40), xlabel="$x$ [mm]",
               title=rf"$t={time[i]*1e6:.1f}\,\mu\mathrm{{s}}$")
        ax.set_ylabel("$y$ [mm]" if ax is axes[0] else "")
        ax.plot([0,20],[20,20],"--",color="#62bce8",lw=1.5)
        if ax is axes[0]:
            ax.text(1,22.5,"Geometric notch",color="#62bce8",fontsize=10)
    fig.colorbar(field, ax=axes, label="$d$: 0 intact, 1 fractured", shrink=.8)
    fig.savefig(args.out / "propagation_snapshots.png", dpi=150)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(7.2,3.8), layout="constrained")
    for q, style in zip(thresholds, ("-", "--", ":")):
        ax.plot([r["time_us"] for r in rows], [r[f"connected_extension_d{q}"] for r in rows],
                style, label=rf"$d\geq {q}$")
    ax.set(xlabel=r"Physical time [$\mu$s]", ylabel="Connected extension [mm]", ylim=(-.5,21),
           title="From the notch tip to the opposite edge")
    ax.axhline(20, color=".5", lw=1, label="Remaining ligament: 20 mm")
    ax.grid(alpha=.25); ax.legend()
    fig.savefig(args.out / "connected_extension.png", dpi=150)
    plt.close(fig)
    fig, (ax, curve_ax) = plt.subplots(1,2,figsize=(9.6,4.6),layout="constrained",
                                      gridspec_kw={"width_ratios":[1,1]})
    field=ax.tripcolor(tri, damage[frames[0]], shading="gouraud", cmap="magma",vmin=0,vmax=1)
    ax.set(aspect="equal",xlim=(0,40),ylim=(0,40),xlabel="$x$ [mm]",ylabel="$y$ [mm]")
    caption=ax.set_title("Single-edge-notched tension")
    ax.plot([0,20],[20,20],"--",color="#62bce8",lw=1.5)
    ax.text(1,22.5,"Geometric notch",color="#62bce8",fontsize=10)
    fig.colorbar(field,ax=ax,label="$d$",fraction=.046,pad=.04)
    times=[r["time_us"] for r in rows]
    ext=[r["connected_extension_d0.9"] for r in rows]
    curve_ax.plot(times,ext,color=".8",lw=1.2)
    line,=curve_ax.plot([],[],color="#25689a",lw=2)
    dot,=curve_ax.plot([],[],"o",color="#d97623")
    curve_ax.set(xlim=(0,time[-1]*1e6+2),ylim=(-.5,21),xlabel=r"Physical time [$\mu$s]",
                 ylabel="Connected extension [mm]",title=r"High-damage path: $d\geq0.9$")
    curve_ax.grid(alpha=.25)
    def update(k):
        i=frames[k]
        field.set_array(damage[i])
        caption.set_text(rf"$t={time[i]*1e6:.2f}\,\mu\mathrm{{s}}$")
        line.set_data(times[:k+1],ext[:k+1]); dot.set_data([times[k]],[ext[k]])
        return field,caption,line,dot
    animation=FuncAnimation(fig,update,frames=len(frames),interval=100,blit=False)
    animation.save(args.out / "plate_crossing.gif",writer=PillowWriter(fps=10),dpi=100)
    update(len(frames)-1)
    fig.savefig(args.out / "plate_crossing_poster.png", dpi=150)
    plt.close(fig)
    ffmpeg=shutil.which("ffmpeg") or "/opt/homebrew/bin/ffmpeg"
    subprocess.run([ffmpeg,"-y","-loglevel","error","-i",str(args.out/"plate_crossing.gif"),
                    "-vf","pad=ceil(iw/2)*2:ceil(ih/2)*2",
                    "-c:v","libx264","-pix_fmt","yuv420p","-movflags","+faststart",
                    str(args.out/"plate_crossing.mp4")],check=True,timeout=60)
    record={"source_trajectory_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
        "source_run":str(args.run.relative_to(ROOT)), "states_in_archive":len(time),
        "frames":frames.tolist(),"frame_time_us":times,"last_threshold_extensions":rows[-1],
        "interpretation":"Connected nodal threshold extent on this mesh; qualitative dynamic demonstration.",
        "playback":"Selected actual states, denser during growth; original CLI physical-time labels retained; no interpolated fields. The initial state and first CLI step share label zero."}
    (args.out/"visual_record.json").write_text(json.dumps(record,indent=2))
    print(json.dumps(record,indent=2))

if __name__=="__main__":
    main()
