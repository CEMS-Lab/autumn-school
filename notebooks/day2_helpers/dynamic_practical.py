"""Portable B3 classroom calculation and compact scientific visual outputs.

Prepared by Allamaprabhu Ani and Sathiskumar A. Ponnusami, CEMS-Lab.
Uses the pinned public PhAST solver and public B3 mesh. The observer records
constrained residuals and sampled states without changing a returned solution.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "configs/day2_forward/b3_classroom"
MESH_SHA = "59c3a41dff41a03fdef93bdd91f974e2d1a263a01aaa96094c125b08cb5e14be"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def case_files():
    """Return the portable input files after checking the public mesh hash."""
    mesh = CASE / "mesh.msh"
    if sha(mesh) != MESH_SHA:
        raise ValueError("The public B3 mesh differs from the recorded teaching input.")
    return CASE / "config.yaml", mesh


def load_case():
    import yaml
    config, _mesh = case_files()
    return yaml.safe_load(config.read_text())


def setup_figure():
    """Actual imported T3 mesh, displacement supports and smooth load ramp."""
    import matplotlib.pyplot as plt
    import meshio

    _config, mesh_path = case_files()
    raw = meshio.read(str(mesh_path))
    nodes, triangles = raw.points[:, :2], raw.cells_dict["triangle"]
    fig, ax = plt.subplots(1, 3, figsize=(11.5, 3.4), layout="constrained")
    ax[0].triplot(nodes[:, 0], nodes[:, 1], triangles, lw=.3, color="#4c6a7b")
    ax[0].set(title=f"Imported mesh: {len(nodes):,} nodes", xlabel="x [mm]", ylabel="y [mm]", aspect="equal")
    ax[1].plot([0,40,40,0,0], [0,0,40,40,0], color="#22485c")
    ax[1].plot([0,20], [20,20], color="#ec8b32", lw=3)
    for x in (8,20,32):
        ax[1].annotate("", (x,46), (x,40), arrowprops={"arrowstyle":"->", "color":"#267eaf"})
        ax[1].annotate("", (x,-6), (x,0), arrowprops={"arrowstyle":"->", "color":"#267eaf"})
    ax[1].text(20,48,r"$u_y=+0.002\,s(t)$ mm",ha="center",fontsize=10)
    ax[1].text(20,-11,r"$u_y=-0.002\,s(t)$ mm",ha="center",fontsize=10)
    ax[1].text(20,26,"20 mm geometric notch",ha="center",fontsize=9)
    ax[1].set(title=r"Left and right edges: $u_x=0$",xlim=(-4,44),ylim=(-13,53),aspect="equal")
    ax[1].axis("off")
    t=np.linspace(0,100,201); z=np.clip(t/20,0,1); ramp=z*z*(3-2*z)
    ax[2].plot(t,.004*ramp,color="#d47924")
    ax[2].set(title="Smooth ramp and hold",xlabel=r"Time [$\mu$s]",ylabel="Total separation [mm]")
    return fig


def run_case(output_dir, timeout_seconds=95):
    """Run one fresh CPU baseline, including outputs, within a hard subprocess cap.

    Setup/installation precedes this call. The notebook execution gate provides
    the separate 120-second limit for the complete plot-and-solve sequence.
    """
    from .course_tools import import_public_phast
    source = import_public_phast()
    config, _mesh = case_files()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
               PYTHONUNBUFFERED="1", MPLBACKEND="Agg",
               PYTHONPATH=str(ROOT / "vendor/PhAST/src") + os.pathsep + str(ROOT / "notebooks"))
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", str(out)]
    started = time.perf_counter(); timed_out = False
    with (out / "run.log").open("w") as log:
        proc = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                env=env, start_new_session=True)
        try:
            code = proc.wait(timeout=min(float(timeout_seconds), 95.0))
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, signal.SIGKILL)
            code = proc.wait()
    receipt = {"whole_process_seconds":time.perf_counter()-started,
               "hard_cap_seconds":min(float(timeout_seconds),95.0),
               "timeout":timed_out,"exit_code":code,"phast":source,
               "config_sha256":sha(config),"mesh_sha256":MESH_SHA,
               "helper_sha256":sha(__file__),"threads":1,"device":"cpu"}
    (out/"runtime.json").write_text(json.dumps(receipt,indent=2)+"\n")
    if code != 0 or timed_out:
        raise RuntimeError(f"The run stopped within its time budget. Inspect {out/'run.log'}.")
    summary=json.loads((out/"summary.json").read_text())
    if not summary["all_checks_pass"]:
        raise RuntimeError(f"Inspect the recorded numerical diagnostics in {out}.")
    return out


def load_results(output_dir):
    out=Path(output_dir)
    with np.load(out/"trajectory.npz",allow_pickle=False) as archive:
        arrays={key:archive[key].copy() for key in archive.files}
    return arrays,json.loads((out/"summary.json").read_text())


def result_figure(output_dir):
    import matplotlib.pyplot as plt
    arrays,_summary=load_results(output_dir)
    t=arrays["time"]*1e6; nodes=arrays["nodes"]; tri=arrays["elements"]
    targets=[12,20,26,35]
    fig,axes=plt.subplots(1,4,figsize=(11.5,3.0),layout="constrained")
    for ax,target in zip(axes,targets):
        k=int(np.argmin(abs(t-target)))
        im=ax.tripcolor(nodes[:,0],nodes[:,1],tri,arrays["damage"][k],shading="gouraud",cmap="magma",vmin=0,vmax=1)
        ax.set(title=rf"$t={t[k]:.1f}\,\mu$s",xlabel="x [mm]",ylabel="y [mm]",aspect="equal")
        ax.grid(False)
    fig.colorbar(im,ax=axes,shrink=.8,label="Damage d: 0 intact, 1 broken")
    return fig


def energy_figure(output_dir):
    import matplotlib.pyplot as plt
    energy=np.genfromtxt(Path(output_dir)/"cli_output/energy.csv",delimiter=",",names=True)
    fig,ax=plt.subplots(figsize=(7.2,3.5),layout="constrained")
    for key,color,style in [("elastic","#267eaf","-"),("fracture","#d47924","--"),("kinetic","#198d83","-.")]:
        ax.plot(energy["time"]*1e6,energy[key],label=key.capitalize(),color=color,ls=style)
    ax.set(xlabel=r"Time [$\mu$s]",ylabel="Energy per unit thickness [N]",title="Stored, fracture and kinetic energy")
    ax.legend()
    return fig


def make_animation(output_dir, frames=40):
    """Encode selected computed states; no interpolation of physical fields."""
    import matplotlib.pyplot as plt
    from PIL import Image
    arrays,_=load_results(output_dir);x=arrays["nodes"];tri=arrays["elements"]
    # Resolve initiation and propagation before the 100-us hold state.
    times=arrays["time"]; first=np.flatnonzero(times<=40.e-6)
    selected=np.unique(np.r_[np.linspace(0,first[-1],frames-1,dtype=int),len(times)-1])
    fig,ax=plt.subplots(figsize=(5.2,4.2),layout="constrained")
    im=ax.tripcolor(x[:,0],x[:,1],tri,arrays["damage"][0],shading="gouraud",cmap="magma",vmin=0,vmax=1)
    ax.set(xlabel="x [mm]",ylabel="y [mm]",aspect="equal");ax.grid(False)
    fig.colorbar(im,ax=ax,label="Damage d: 0 intact, 1 broken")
    images=[]
    for k in selected:
        im.set_array(arrays["damage"][k]);ax.set_title(rf"B3 plate: $t={times[k]*1e6:.1f}\,\mu$s")
        fig.canvas.draw()
        images.append(Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:,:,:3].copy()))
    path=Path(output_dir)/"crack_propagation.gif"
    images[0].save(path,save_all=True,append_images=images[1:],duration=100,loop=0)
    plt.close(fig)
    return path


def _worker(out):
    import torch
    sys.path.insert(0,str(ROOT/"vendor/PhAST/src"))
    from phast.solvers.damage_solver import PhaseFieldDamageSolver
    from phast.solvers.staggered_solver import StaggeredSolver
    from phast.config.run_config import main
    torch.set_num_threads(1)
    old_solve=PhaseFieldDamageSolver.solve;old_step=StaggeredSolver.step_full
    diagnostics=[];samples=[];holder={};minimum=0.;bc_error=0.;finite=True

    def damage(self,H,lower,*args,**kwargs):
        h=H.detach().clone();lb=lower.detach().clone()
        d=old_solve(self,H,lower,*args,**kwargs)
        R=self.compute_residual(h,d).clone();R0=self.compute_residual(h,lb).clone()
        b=-self.compute_residual(h,torch.zeros_like(d)).clone()
        active=((d<=lb+1e-14)&(R>=0))|((d>=1-1e-14)&(R<=0))
        projected=R.clone();projected[active]=0
        scale=max(float(torch.linalg.vector_norm(b)),float(torch.linalg.vector_norm(R0)),1e-30)
        rel=float(torch.linalg.vector_norm(projected))/scale
        diagnostics.append({"step":len(diagnostics),"projected_relative_residual":rel,
                            "tolerance":self.tol,"converged":bool(np.isfinite(rel) and rel<=self.tol),
                            "iterations":self.last_iter})
        return d

    def sample(solver,step):
        samples.append((step,max(step-1,0)*solver.dt,solver.d.detach().numpy().copy(),solver.u.detach().numpy().copy()))

    def step(self):
        nonlocal minimum,bc_error,finite
        holder["solver"]=self
        if not samples:sample(self,0)
        previous=self.d.clone();result=old_step(self)
        minimum=min(minimum,float((self.d-previous).min()))
        mask,values=self.bcs.get_masks_and_values()
        bc_error=max(bc_error,float((self.u[mask]-values[mask]).abs().max()))
        finite=finite and all(bool(torch.isfinite(v).all()) for v in (self.u,self.v,self.d,self.H_elem))
        if self._step_count%40==0:sample(self,self._step_count)
        return result

    PhaseFieldDamageSolver.solve=damage;StaggeredSolver.step_full=step
    config,_mesh=case_files()
    sys.argv=["phast run",str(config),"--device","cpu","--output_dir",str(out/"cli_output")]
    main();solver=holder["solver"]
    if samples[-1][0]!=solver._step_count:sample(solver,solver._step_count)
    nodes=solver.mesh.nodes.numpy();elements=solver.mesh.elements.numpy()
    np.savez_compressed(out/"trajectory.npz",nodes=nodes,elements=elements,
                        step=np.array([v[0] for v in samples]),time=np.array([v[1] for v in samples]),
                        damage=np.array([v[2] for v in samples]),displacement=np.array([v[3] for v in samples]))
    with (out/"diagnostics.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(diagnostics[0]));writer.writeheader();writer.writerows(diagnostics)
    strip=(nodes[:,0]>20)&(np.abs(nodes[:,1]-20)<=1)
    response=[]
    for step_id,t,d,u in samples:
        response.append({"step":step_id,"time_us":t*1e6,"maximum_damage":float(d.max()),
                         "extent_d095_mm":float(nodes[strip&(d>=.95),0].max(initial=20)-20),
                         "maximum_displacement_mm":float(np.abs(u).max())})
    with (out/"results.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(response[0]));writer.writeheader();writer.writerows(response)
    energies=np.genfromtxt(out/"cli_output/energy.csv",delimiter=",",names=True)
    finite_energy=all(bool(np.isfinite(energies[k]).all()) for k in energies.dtype.names)
    summary={"nodes":len(nodes),"elements":len(elements),"steps":solver._step_count,
             "sampled_states":len(samples),"dt_seconds":solver.dt,"damage_updates":len(diagnostics),
             "max_projected_relative_residual":max(v["projected_relative_residual"] for v in diagnostics),
             "all_damage_updates_converged":all(v["converged"] for v in diagnostics),
             "finite_states":finite,"finite_energy_components":finite_energy,
             "minimum_damage_increment":minimum,"maximum_boundary_error":bc_error,
             "final_extent_d095_mm":response[-1]["extent_d095_mm"],
             "damage_bounds":[float(solver.d.min()),float(solver.d.max())],
             "mesh_sha256":MESH_SHA,
             "scope":"Qualitative public B3 plate; fixed-mesh temporal sensitivity checked separately",
             "residual":"||projected(A*d-b)|| / max(||b||,||R(previous)||,1e-30), bound_atol=1e-14",
             "time_convention":"Initial state0; recorded state k uses public CLI label (k-1)*dt"}
    summary["all_checks_pass"]=bool(finite and finite_energy and minimum>=-1e-12 and bc_error<=1e-12
        and summary["all_damage_updates_converged"] and solver.d.min()>=0 and solver.d.max()<=1)
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--worker",type=Path,required=True)
    _worker(parser.parse_args().worker)
