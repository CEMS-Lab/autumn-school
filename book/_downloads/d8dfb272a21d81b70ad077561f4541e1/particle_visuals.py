"""HPC visual lesson: a geometry toy and strictly separated retained FEM data.

Run: python particle_visuals.py --inputs INPUTS --output OUTPUTS
INPUTS contains the allowlisted retained arrays listed in input_manifest.json.
No fracture solver is executed. The geometry-observation toy is computed here.
"""
import argparse
import hashlib
import json
import time
import zipfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
import numpy as np

BLUE, ORANGE, GREEN = "#0072B2", "#D55E00", "#009E73"
plt.rcParams.update({"font.family": "STIXGeneral", "mathtext.fontset": "stix",
    "font.size": 14, "axes.labelsize": 14, "axes.titlesize": 15,
    "legend.fontsize": 12, "figure.facecolor": "white", "savefig.facecolor": "white"})


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plate(ax, title):
    ax.set(xlim=(0, 40), ylim=(0, 40), aspect="equal", xlabel="$x$ (mm)",
           ylabel="$y$ (mm)", title=title, xticks=[0, 20, 40], yticks=[0, 20, 40])


def save(fig, out, name):
    for ext in ["png", "pdf"]:
        fig.savefig(out / (name + "." + ext), dpi=240, bbox_inches="tight", pad_inches=.18)


def movie(fig, draw, n, out, name, fps):
    animation = FuncAnimation(fig, draw, frames=n, interval=1000/fps, blit=False)
    animation.save(out / (name + ".mp4"), writer=FFMpegWriter(
        fps=fps, codec="libx264", extra_args=["-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
        "-pix_fmt", "yuv420p", "-crf", "20"]), dpi=110)


def geometry(out):
    # This is an image-of-geometry inverse problem, not simulated fracture.
    x = (np.arange(80) + .5) * .5
    X, Y = np.meshgrid(x, x)
    radius, eps = 3., 1.5
    truth = np.array([28., 23.])

    def indicator(c):
        dist = np.maximum(np.hypot(X-c[0], Y-c[1]), 1e-12)
        s = 1 / (1 + np.exp(np.clip((dist-radius)/eps, -700, 700)))
        return s, dist

    target, _ = indicator(truth)

    def evaluate(c):
        s, dist = indicator(c)
        residual = s-target
        grad = np.array([np.mean(2*residual*s*(1-s)*(X-c[0])/(eps*dist)),
                         np.mean(2*residual*s*(1-s)*(Y-c[1])/(eps*dist))])
        return np.mean(residual**2), grad

    c = np.array([34., 33.])
    path, losses, evals = [c.copy()], [evaluate(c)[0]], 1
    for _ in range(80):
        loss, grad = evaluate(c)
        evals += 1
        if np.linalg.norm(grad) < 1e-8:
            break
        direction = -grad / np.linalg.norm(grad)
        alpha = .8
        for _ in range(16):
            trial = c + alpha * direction
            trial_loss, _ = evaluate(trial)
            evals += 1
            if trial_loss <= loss + 1e-4*alpha*np.dot(grad, direction):
                c = trial
                path.append(c.copy())
                losses.append(trial_loss)
                break
            alpha *= .5
        else:
            break
    path, losses = np.array(path), np.array(losses)
    gx, gy = np.linspace(20, 36, 65), np.linspace(15, 35, 81)
    CX, CY = np.meshgrid(gx, gy)
    L = np.array([evaluate(c)[0] for c in np.c_[CX.ravel(), CY.ravel()]]).reshape(CX.shape)
    probe = np.array([30., 26.])
    h = 1e-4
    fd = np.array([(evaluate(probe+np.eye(2)[k]*h)[0]-evaluate(probe-np.eye(2)[k]*h)[0])/(2*h) for k in range(2)])
    derivative_error = np.linalg.norm(fd-evaluate(probe)[1])/np.linalg.norm(fd)
    assert derivative_error < 1e-6
    assert np.all(np.diff(losses) <= 1e-14) and losses[-1] < losses[0]*.01
    np.savez_compressed(out/"geometry_arrays.npz", x=x, target=target, path=path,
                        losses=losses, cx=gx, cy=gy, landscape=L)

    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.4), layout="constrained")
    initial = indicator(path[0])[0]
    for ax, values, title in zip(axes, [target, initial, initial-target],
            ["(a) Reference geometry image", "(b) Initial geometry image", "(c) Initial signed residual"]):
        signed = ax is axes[2]
        im = ax.imshow(values, origin="lower", extent=(0,40,0,40), cmap="coolwarm" if signed else "viridis",
                       vmin=-1 if signed else 0, vmax=1, interpolation="nearest")
        plate(ax, title)
        fig.colorbar(im, ax=ax, fraction=.045, pad=.035, label="Residual" if signed else "Indicator $s$")
    save(fig, out, "geometry_observation")
    plt.close(fig)

    fig = plt.figure(figsize=(13.6, 5.9), layout="constrained")
    ax = fig.add_subplot(121, projection="3d", computed_zorder=False)
    ax.plot_surface(CX, CY, L, cmap="viridis", rcount=81, ccount=65, linewidth=0, antialiased=True, rasterized=True)
    ax.plot(path[:,0], path[:,1], losses, color=ORANGE, lw=2.2, zorder=5)
    ax.scatter(*truth, evaluate(truth)[0], marker="*", color="black", s=90, zorder=6)
    ax.set(xlabel="$c_x$ (mm)", ylabel="$c_y$ (mm)", zlabel="Geometry loss", title="(a) A computed loss surface")
    ax.view_init(elev=33, azim=-125)
    ax.set_xticks([20,28,36]);ax.set_yticks([15,25,35]);ax.set_zticks([0,.01,.02])
    ax.xaxis.labelpad=12;ax.yaxis.labelpad=12;ax.zaxis.labelpad=16
    ax.set_zlabel("")
    ax.text2D(.02,.89,"Height: geometry loss",transform=ax.transAxes,fontsize=12)
    ax.set_box_aspect((1,1,.7))
    ax2 = fig.add_subplot(122)
    im = ax2.pcolormesh(CX, CY, L, shading="nearest", cmap="viridis")
    ax2.plot(path[:,0],path[:,1],".-",color=ORANGE,ms=3,label="Computed descent")
    ax2.plot(*path[0],"s",color=ORANGE,ms=7,label="Initial centre")
    ax2.plot(*truth,"*",color="black",ms=12,label="Reference centre")
    ax2.set(xlabel="$c_x$ (mm)",ylabel="$c_y$ (mm)",aspect="equal",title="(b) The same surface from above")
    fig.colorbar(im,ax=ax2,shrink=.8,label="Geometry loss")
    fig.legend(*ax2.get_legend_handles_labels(),loc="outside lower center",ncol=3,frameon=False)
    save(fig,out,"geometry_loss")
    plt.close(fig)

    fig = plt.figure(figsize=(14,6),layout="constrained")
    a = fig.add_subplot(121)
    im = a.imshow(initial,origin="lower",extent=(0,40,0,40),vmin=0,vmax=1,cmap="viridis",interpolation="nearest")
    reference = Circle(truth,radius,fill=False,ls="--",lw=1.5,color="white")
    a.add_patch(reference)
    plate(a,"(a) Current geometry image")
    fig.colorbar(im,ax=a,shrink=.75,label="Indicator $s$")
    b = fig.add_subplot(122,projection="3d",computed_zorder=False)
    b.plot_surface(CX,CY,L,cmap="viridis",rcount=81,ccount=65,linewidth=0,alpha=.85,rasterized=True)
    line, = b.plot([],[],[],color=ORANGE,lw=2.5,zorder=5)
    dot, = b.plot([],[],[],"o",color=ORANGE,ms=7,zorder=6)
    b.set(xlabel="$c_x$ (mm)",ylabel="$c_y$ (mm)",zlabel="Geometry loss",title="(b) Position on the loss surface")
    b.set_box_aspect((1,1,.7));b.view_init(elev=32,azim=-125)
    b.set_xticks([20,28,36]);b.set_yticks([15,25,35]);b.set_zticks([0,.01,.02])
    b.xaxis.labelpad=12;b.yaxis.labelpad=12;b.zaxis.labelpad=16
    b.set_zlabel("")
    b.text2D(.02,.89,"Height: geometry loss",transform=b.transAxes,fontsize=12)
    status = fig.suptitle("Geometry-observation toy",fontsize=16)
    fig.legend(handles=[Line2D([],[],color=".4",ls="--",label="Reference circle on image"),
                        Line2D([],[],color=ORANGE,marker="o",label="Computed centre / descent")],
               loc="outside lower center",ncol=2,frameon=False)
    indices = np.unique(np.linspace(0,len(path)-1,min(40,len(path))).astype(int))
    def draw(frame):
        i=indices[frame]
        im.set_data(indicator(path[i])[0])
        line.set_data_3d(path[:i+1,0],path[:i+1,1],losses[:i+1])
        dot.set_data_3d([path[i,0]],[path[i,1]],[losses[i]])
        status.set_text(f"Geometry-observation toy: update {i}; loss {losses[i]:.2e}")
    movie(fig,draw,len(indices),out,"geometry_descent",3)
    plt.close(fig)
    return {"model":"Smooth geometry-image mismatch; no elasticity or fracture solve",
            "radius_mm":radius,"interface_width_mm":eps,"pixel_grid":[80,80],
            "landscape_grid":[81,65],"sample_count":L.size,"analytic_fd_relative_error":float(derivative_error),
            "updates":len(path)-1,"optimization_evaluations":evals,"initial_loss":float(losses[0]),
            "final_loss":float(losses[-1]),"final_centre":path[-1].tolist()}


def retained_fem(inputs, out):
    data=json.loads((inputs/"blind_temporal_recovery.json").read_text())
    points=np.load(inputs/"mesh_nodes.npy")
    triangles=np.load(inputs/"mesh_elements.npy")
    pred=np.load(inputs/"blind_temporal_iter_pred_snapshots.npy")
    target=np.load(inputs/"blind_temporal_target_snapshots.npy")
    steps=np.load(inputs/"blind_temporal_iter_pred_steps.npy")
    history=data["history"]
    centres=np.array([r["center"] for r in history])
    losses=np.array([r["loss"] for r in history])
    truth=np.array(data["summary"]["truth_center"])
    params=json.loads((inputs/"particle_params.json").read_text())
    radius=params["radius_mm"]
    assert pred.shape==(len(history),len(steps),len(points)) and target.shape==pred.shape[1:]
    assert list(steps)==data["summary"]["selected_observation_steps"]
    recomputed=np.sum((pred-target[None,:,:])**2,axis=(1,2))/np.sum(target)
    loss_max_error=float(np.max(np.abs(recomputed-losses)))
    assert np.allclose(recomputed,losses,rtol=1e-7,atol=1e-12), (recomputed,losses)
    assert np.all(np.isfinite(pred)) and pred.min()>=-1e-8 and pred.max()<=1+1e-8
    tri=mtri.Triangulation(points[:,0],points[:,1],triangles)
    delta_max=float(np.max(np.abs(pred[:,-1]-target[-1])))
    fig=plt.figure(figsize=(14,9),layout="constrained")
    gs=fig.add_gridspec(2,6,height_ratios=[1,1])
    axes=[fig.add_subplot(gs[0,0:2]),fig.add_subplot(gs[0,2:4]),fig.add_subplot(gs[0,4:6]),
          fig.add_subplot(gs[1,0:2]),fig.add_subplot(gs[1,2:6])]
    def draw(i):
        for ax in axes:ax.clear()
        for ax,values,title in zip(axes[:3],[target[-1],pred[i,-1],pred[i,-1]-target[-1]],
                                   ["(a) Reference damage", "(b) Predicted damage", "(c) Signed damage error"]):
            signed=ax is axes[2]
            ax.tripcolor(tri,values,shading="gouraud",cmap="coolwarm" if signed else "inferno",
                         vmin=-delta_max if signed else 0,vmax=delta_max if signed else 1,rasterized=True)
            plate(ax,title)
        ax=axes[3]
        for c,colour,style in [(truth,".3","--"),(centres[0],ORANGE,":"),(centres[i],BLUE,"-")]:
            ax.add_patch(Circle(c,radius,fill=False,color=colour,ls=style,lw=2))
        ax.plot(centres[:i+1,0],centres[:i+1,1],".-",color=BLUE,ms=3)
        plate(ax,"(d) Geometry updates")
        axes[4].semilogy(range(len(losses)),losses,color=".83",lw=1.4)
        axes[4].semilogy(range(i+1),losses[:i+1],".-",color=BLUE,lw=2,ms=4)
        axes[4].set(xlabel="Inverse update",ylabel="Four-frame damage loss",xlim=(0,len(history)-1),
                    ylim=(losses.min()*.65,losses.max()*1.5),title="(e) Recorded objective history")
        axes[4].grid(alpha=.2)
        heading.set_text(f"Recorded single-particle inverse: update {i} of {len(history)-1}")
    heading=fig.suptitle("Recorded single-particle inverse",fontsize=16)
    fig.legend(handles=[Line2D([],[],color=".3",ls="--",label="Reference geometry"),
                        Line2D([],[],color=ORANGE,ls=":",lw=2,label="Initial geometry"),
                        Line2D([],[],color=BLUE,label="Current geometry / history")],
               loc="outside lower center",ncol=3,frameon=False)
    draw(len(history)-1)
    # Shared scales stay fixed through every frame.
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize
    fig.colorbar(ScalarMappable(Normalize(0,1),"inferno"),ax=axes[:2],shrink=.75,pad=.02,label="Damage $d$")
    fig.colorbar(ScalarMappable(Normalize(-delta_max,delta_max),"coolwarm"),ax=axes[2],shrink=.75,pad=.02,label="$\\hat d-d_{ref}$")
    save(fig,out,"fem_recovery")
    movie(fig,draw,len(history),out,"fem_recovery",2)
    plt.close(fig)
    fig,axes=plt.subplots(1,4,figsize=(14,4.3),layout="constrained")
    for i,ax in enumerate(axes):
        im=ax.tripcolor(tri,target[i],shading="gouraud",cmap="inferno",vmin=0,vmax=1,rasterized=True)
        plate(ax,f"({chr(97+i)}) Step {int(steps[i])}")
    fig.colorbar(im,ax=axes,shrink=.75,pad=.02,label="Damage $d$")
    save(fig,out,"fem_time")
    plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(10,5.3),layout="constrained")
    artists=[]
    for ax,values,title in zip(axes,[target[0],pred[-1,0]],["(a) Reference trajectory","(b) Recovered-geometry trajectory"]):
        artists.append(ax.tripcolor(tri,values,shading="gouraud",cmap="inferno",vmin=0,vmax=1,rasterized=True))
        plate(ax,title)
    fig.colorbar(artists[0],ax=axes,shrink=.8,label="Damage $d$")
    heading=fig.suptitle("Four retained fitting frames; no time interpolation",fontsize=15)
    def draw_time(i):
        artists[0].set_array(target[i]);artists[1].set_array(pred[-1,i])
        heading.set_text(f"Stored forward step {int(steps[i])}; frame {i+1}/4")
    movie(fig,draw_time,4,out,"fem_time",.8)
    plt.close(fig)
    summary={"model":"Retained nonlinear FEM inverse; no new fracture solve",
             "loss":data["loss"],"steps":steps.tolist(),"updates":len(history)-1,
             "initial_centre_mm":centres[0].tolist(),"final_centre_mm":centres[-1].tolist(),
             "reference_centre_mm":truth.tolist(),"radius_mm":radius,
             "initial_distance_mm":float(np.linalg.norm(centres[0]-truth)),
             "final_distance_mm":float(np.linalg.norm(centres[-1]-truth)),
             "saved_loss_max_recompute_difference":loss_max_error,
             "nonmonotone_updates":np.flatnonzero(np.diff(losses)>0).astype(int).tolist(),
             "error_colour_limit":delta_max}
    np.savez_compressed(out/"fem_arrays.npz",nodes=points,elements=triangles,prediction=pred,
                        target=target,steps=steps,centres=centres,losses=losses)
    return summary


def sparse_landscape(inputs,out):
    data=json.loads((inputs/"loss_landscape_step1454.json").read_text())
    rows=data["rows"]
    x=np.array(sorted({r["center"][0] for r in rows}))
    y=np.array(sorted({r["center"][1] for r in rows}))
    assert len(rows)==len(x)*len(y)==25 and data["grid_complete"]
    z=np.array([[next(r["loss"] for r in rows if r["center"]==[cx,cy]) for cx in x] for cy in y])
    X,Y=np.meshgrid(x,y)
    fig=plt.figure(figsize=(13,5.8),layout="constrained")
    a=fig.add_subplot(121,projection="3d")
    a.plot_surface(X,Y,z,cmap="viridis",edgecolor=".35",linewidth=.65,antialiased=False)
    a.scatter(X,Y,z,color="black",s=15,depthshade=False)
    a.set(xlabel="$c_x$ (mm)",ylabel="$c_y$ (mm)",zlabel="Single-frame damage loss",
          title="(a) 25 retained FEM evaluations")
    a.view_init(30,-120);a.set_box_aspect((1,1,.75))
    a.set_xticks([26,28,30]);a.set_yticks([21,23,25]);a.set_zticks([0,.04,.08])
    a.xaxis.labelpad=12;a.yaxis.labelpad=12;a.zaxis.labelpad=16
    a.set_zlabel("")
    a.text2D(.02,.89,"Height: single-frame damage loss",transform=a.transAxes,fontsize=12)
    b=fig.add_subplot(122)
    im=b.pcolormesh(X,Y,z,shading="nearest",cmap="viridis")
    b.scatter(X,Y,s=20,color="black",label="Evaluated centre")
    b.plot(*data["summary"]["truth_center"],"*",color="white",markeredgecolor="black",ms=14,label="Reference centre")
    b.set(xlabel="$c_x$ (mm)",ylabel="$c_y$ (mm)",aspect="equal",xticks=x,yticks=y,
          title="(b) Sample locations and values")
    fig.colorbar(im,ax=b,shrink=.8,label="Single-frame damage loss")
    fig.legend(*b.get_legend_handles_labels(),loc="outside lower center",ncol=2,frameon=False)
    save(fig,out,"fem_sampled_loss");plt.close(fig)
    np.savez_compressed(out/"sampled_landscape.npz",cx=x,cy=y,loss=z)
    return {"samples":25,"step":data["target_step"],"loss":data["loss"],
            "scope":"Single-frame same-basin sample grid; separate objective from the four-frame inverse",
            "display":"Only adjacent sampled cells joined; no dense resampling, clipping or fabricated roughness"}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--inputs",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    if (args.output/"manifest.json").exists():
        raise RuntimeError("Use a new output directory; preserve the previous receipt.")
    started=time.perf_counter()
    results={"geometry":geometry(args.output),"fem_recovery":retained_fem(args.inputs,args.output),
             "sampled_landscape":sparse_landscape(args.inputs,args.output)}
    with zipfile.ZipFile(args.output/"retained_inputs.zip","w",zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(args.inputs.iterdir()):
            if path.suffix in {".json",".npy"}:
                bundle.write(path,"inputs/"+path.name)
    results.update({"seconds":time.perf_counter()-started,"matplotlib":matplotlib.__version__,
                    "numpy":np.__version__,"renderer_sha256":sha(Path(__file__)),
                    "input_sha256":{p.name:sha(p) for p in sorted(args.inputs.iterdir()) if p.is_file()},
                    "artifact_sha256":{p.name:sha(p) for p in sorted(args.output.iterdir()) if p.is_file()},
                    "execution":"HPC CPU; retained FEM rendering plus a new geometry-observation toy"})
    (args.output/"manifest.json").write_text(json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2))


if __name__=="__main__":
    main()
