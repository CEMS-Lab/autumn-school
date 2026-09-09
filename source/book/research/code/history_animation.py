"""Render the source-audited history teaching primitive on HPC, not a FEM run."""
import argparse
import hashlib
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np
from history_lesson import history_rules

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=False)
plt.rcParams.update({"font.family": "STIXGeneral", "mathtext.fontset": "stix",
                     "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
                     "xtick.labelsize": 12, "ytick.labelsize": 12,
                     "savefig.facecolor": "white"})
blue, red, green = "#0072B2", "#D55E00", "#009E73"
result, checks = history_rules()
energy = np.array([.2, .65, 1., .55, .85, 1., 1.25, .75, 1.45])
history = np.maximum.accumulate(energy)
old = np.r_[0., history[:-1]]
weight = 1 / (1 + np.exp(-12*(energy-old)))
exact = np.where(energy > old, 1., np.where(energy < old, 0., .5))
checks.update(history_never_falls=bool(np.all(np.diff(history)>=0)),
              history_contains_current=bool(np.all(history>=energy)),
              reverse_weights_sum_to_one=bool(np.allclose(weight+(1-weight),1)))
assert all(checks.values()), checks
np.savez_compressed(args.output/"history_animation_arrays.npz", energy=energy,
                    history=history, old_history=old, exact_weight=exact,
                    surrogate_weight=weight, teaching_scale=12.)

fig = plt.figure(figsize=(11.6, 7.8))
gs = fig.add_gridspec(2, 2, top=.85, bottom=.19, left=.085, right=.96,
                      hspace=.57, wspace=.32, height_ratios=[.75,1])
axes = [fig.add_subplot(gs[0,:]),fig.add_subplot(gs[1,0]),fig.add_subplot(gs[1,1])]
heading = fig.text(.5,.972,"",ha="center",va="top",fontsize=17)
status = fig.text(.5,.945,"",ha="center",va="top",fontsize=13)
fig.text(.5,.035,"Dimensionless teaching example at one material point. Sigmoid scale = 12.",
         ha="center",fontsize=12)
xx = np.linspace(0,1.6,601)

def draw(i):
    for ax in axes:
        ax.clear()
        ax.spines[["top","right"]].set_visible(False)
        ax.grid(alpha=.17)
    heading.set_text(f"Step {i+1} of {len(energy)}: energy, memory and reverse sensitivity")
    action = ("New maximum: current energy takes over." if energy[i] > old[i] else
              "Unloading / reloading below the peak: earlier history stays active."
              if energy[i] < old[i] else "Tie: the hard maximum has a kink here.")
    status.set_text(action)
    ax=axes[0]
    steps=np.arange(1,i+2)
    ax.plot(steps,energy[:i+1],color=blue,marker="o",ms=5,label="Current energy")
    ax.step(steps,history[:i+1],where="post",color=red,lw=2,label="Stored maximum")
    ax.scatter([i+1],[history[i]],color=red,s=45,zorder=4)
    ax.set(xlim=(.7,9.3),ylim=(0,1.6),xticks=np.arange(1,10),
           xlabel="Loading step",ylabel="Energy / history",
           title="(a) Memory survives unloading")
    ax.legend(loc="upper left",bbox_to_anchor=(.30,1.02),ncol=2,frameon=False,fontsize=12)
    ax=axes[1]
    ax.plot(xx,np.maximum(old[i],xx),color=blue,lw=2.5)
    ax.axvline(old[i],color=".55",ls=":",lw=1.2)
    ax.scatter(energy[i],history[i],s=65,color=red,zorder=4)
    ax.set(xlim=(0,1.6),ylim=(0,1.65),xlabel=r"Current energy $\psi^+$",
           ylabel=r"Updated history $H_{n+1}$",title="(b) A continuous value; a kink in slope")
    ax=axes[2]
    below=xx<old[i]; above=xx>old[i]
    ax.plot(xx[below],np.zeros(sum(below)),color=blue,lw=2.5)
    ax.plot(xx[above],np.ones(sum(above)),color=blue,lw=2.5,label="Hard branch")
    ax.plot(xx,1/(1+np.exp(-12*(xx-old[i]))),color=green,lw=2,label="Surrogate")
    ax.axvline(old[i],color=".55",ls=":",lw=1.2)
    ax.scatter([old[i]],[.5],facecolors="none",edgecolors=blue,s=100,zorder=6)
    ax.scatter([energy[i]],[weight[i]],color=green,s=60,zorder=4)
    ax.scatter([energy[i]],[exact[i]],color=red,s=45,zorder=5)
    ax.set(xlim=(0,1.6),ylim=(-.08,1.12),yticks=[0,.5,1],
           xlabel=r"Current energy $\psi^+$",ylabel="Current-energy reverse weight",
           title="(c) Which input receives sensitivity?")
    ax.legend(loc="upper center",bbox_to_anchor=(.5,-.28),ncol=2,frameon=False,fontsize=12)
    return axes

draw(5)
for ext in ("png","pdf"):
    fig.savefig(args.output/f"history_switch.{ext}",dpi=220)
movie=FuncAnimation(fig,draw,frames=len(energy),interval=2000,repeat=False)
movie.save(args.output/"history_switch.mp4",dpi=120,
           writer=FFMpegWriter(fps=.5,codec="libx264",extra_args=[
               "-pix_fmt","yuv420p","-vf","pad=ceil(iw/2)*2:ceil(ih/2)*2",
               "-movflags","+faststart","-crf","18"]))
plt.close(fig)
# Receipts retain both a passing smooth-sibling test and the hard-map mismatch.
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=[Path(__file__),Path(__file__).with_name("history_lesson.py")]
receipt={"scope":"Dimensionless history primitive; not a new fracture solve",
         "job_id":os.environ.get("SLURM_JOB_ID"),
         "sources":{p.name:sha(p) for p in sources}, "checks":checks,
         "hard_fd":result["hard_fd"],"surrogate_reverse":result["surrogate"],
         "smooth_sibling_fd":result["smooth_fd"],
         "frames":9,"playback_seconds":18,"teaching_sigmoid_scale":12,
         "matplotlib":matplotlib.__version__,"numpy":np.__version__,
         "artifacts":{p.name:sha(p) for p in sorted(args.output.iterdir())}}
(args.output/"history_manifest.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
