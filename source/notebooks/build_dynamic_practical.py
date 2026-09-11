"""Author the separate short B3 propagation practical; existing labs stay intact."""
from pathlib import Path
import hashlib
import json
import textwrap

ROOT=Path(__file__).resolve().parents[2]
NAME="01_dynamic_plate_crossing"
cells=[]


def add(kind,source,fold=False):
    source=textwrap.dedent(source).strip()
    if kind=="code" and not fold:
        assert len([v for v in source.splitlines() if v.strip()])<=12
    metadata={}
    if fold:metadata={"tags":["hide-input"],"jupyter":{"source_hidden":True},"cellView":"form"}
    cell={"cell_type":kind,"id":hashlib.sha256(f"{len(cells)}:{source}".encode()).hexdigest()[:16],
          "metadata":metadata,"source":source.splitlines(keepends=True)}
    if kind=="code":cell.update(execution_count=None,outputs=[])
    cells.append(cell)


add("markdown",r"""
# A crack crossing a plate: a short PhAST simulation

**Learning objective:** Import a notched-plate mesh, understand its supports and loading, run a dynamic phase-field calculation, and interpret the computed crack evolution and energy components.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/extensions/01_dynamic_plate_crossing.ipynb)

[Download notebook with exercises and worked solutions](https://cems-lab.github.io/autumn-school/notebooks/extensions/01_dynamic_plate_crossing.ipynb) · [Environment Setup](https://cems-lab.github.io/autumn-school/SETUP.md)

**Predict first:** Under vertical tension, in which direction will the crack grow from the horizontal notch? When a crack opens, how might the stored elastic energy change?

Prepared by Allamaprabhu Ani and Sathiskumar A. Ponnusami, CEMS-Lab, for the UKACM Autumn School 2026.
""")
add("code",'#@title Set up the course environment { display-mode: "form" }\n'+
    (ROOT/"source/notebooks/colab_bootstrap.py").read_text()+
    '\ncomputation_started=time.perf_counter()\ntorch.set_num_threads(1)\n',True)
add("markdown",r"""
## 1. The specimen and physical model

The 40 mm square glass plate has a 20 mm geometric notch. The notch is already a cut in the imported mesh. The phase-field variable starts at $d=0$ and increases towards $d=1$ as a diffuse crack forms in the remaining ligament.

PhAST solves the discrete balance of momentum with an explicit central-difference update, then an implicit damage update:

$$\mathbf M\ddot{\mathbf u}+\mathbf f_{\mathrm{int}}(\mathbf u,d)=\mathbf f_{\mathrm{ext}},
\qquad d^{n+1}\in[d^n,1].$$

Here $\mathbf M$ is the mass matrix, $\mathbf u$ is displacement and $n$ indexes physical time. The spectral split separates tensile and compressive elastic energies. The AT2 energy is

$$\mathcal E(\mathbf u,d)=\int_\Omega
\left[g(d)\psi^+(\boldsymbol\varepsilon)+\psi^-(\boldsymbol\varepsilon)
+\frac{G_c}{2\ell}d^2+\frac{G_c\ell}{2}|\nabla d|^2\right]\,\mathrm d\Omega,$$

where $g(d)=(1-\eta)(1-d)^2+\eta$, $G_c$ is fracture toughness, $\ell$ is the regularisation length and $\eta$ is residual stiffness. The history of tensile energy supplies the irreversible damage update.

### Open the inputs

The portable YAML file contains the material, supports, loading and numerical settings. Its mesh is the checked public PhAST B3 example. Keeping that mesh fixed makes the calculation reproducible across computers.
""")
add("code","""
from day2_helpers.dynamic_practical import case_files, load_case, setup_figure
config_path, mesh_path = case_files()
config = load_case()
print("Mesh:", mesh_path.name)
print("Material:", config["material"])
print("Solver:", config["solver"])
""")
add("markdown",r"""
### Inspect the mesh, supports and load

The left and right edges have $u_x=0$. The top and bottom move vertically by $+0.002\,s(t)$ mm and $-0.002\,s(t)$ mm. The smooth ramp $s(t)$ rises from zero to one over $20\,\mu$s, then remains constant until $100\,\mu$s. The 0.5 mm regularisation length determines the diffuse crack-band scale.
""")
add("code","""
fig = setup_figure()
display_figure(fig, alt="B3 imported triangular mesh, geometric notch, supports and smooth opening ramp")
plt.close(fig)
""")
add("markdown",r"""
## 2. Run the plate calculation

Run one baseline calculation on the CPU. The public solver updates momentum and damage at each time step; the projected damage solve enforces $d^{n+1}\ge d^n$. Numerical checks accompany every update. The calculation exports sampled fields, energy components and a results table into its own output folder.

The helper starts the public PhAST command with the visible configuration. Expand its Python source to inspect the subprocess, residual checks and output routines. The solver subprocess has a 95-second safety cap; the complete uninterrupted practical is tested against a 120-second computation budget after environment setup.
""")
add("code","""
import tempfile
from day2_helpers.dynamic_practical import run_case, load_results
output_dir = Path(os.environ.get("PHAST_DYNAMIC_OUTPUT", tempfile.mkdtemp(prefix="phast-b3-"))) / "results"
output_dir = run_case(output_dir, timeout_seconds=95)
fields, summary = load_results(output_dir)
print({key: summary[key] for key in ["nodes", "elements", "steps", "sampled_states", "all_checks_pass"]})
""")
add("markdown",r"""
## 3. Follow the computed crack

The images use the same damage colour scale throughout. Locate the initial notch, then follow the high-damage band into the remaining 20 mm ligament. The four fields below are selected from the saved calculation.
""")
add("code","""
from day2_helpers.dynamic_practical import result_figure
fig = result_figure(output_dir)
display_figure(fig, alt="Four actual B3 damage states showing initiation and propagation across the ligament")
plt.close(fig)
""")
add("markdown",r"""
### Animate the result

Each frame below is a sampled solver state. Frames emphasise the first $40\,\mu$s, when the crack initiates and traverses the plate, and include the final $100\,\mu$s hold state. Playback speed is selected for viewing.
""")
add("code","""
from day2_helpers.dynamic_practical import make_animation
gif_path = make_animation(output_dir, frames=40)
display(Image(filename=str(gif_path), alt="Computed B3 crack propagation from notch to plate edge"))
""")
add("markdown",r"""
## 4. Interpret the fields and energy

Stored elastic energy changes as the plate is loaded and the crack opens. Fracture energy measures the diffuse crack contribution, and kinetic energy describes motion. These are energies per unit specimen thickness. A complete energy balance additionally requires the work done at the moving boundaries.
""")
add("code","""
from day2_helpers.dynamic_practical import energy_figure
fig = energy_figure(output_dir)
display_figure(fig, alt="Stored elastic, fracture and kinetic energy versus physical time")
plt.close(fig)
""")
add("markdown",r"""
### Read and export a results table

The CSV records the time, maximum damage, displacement and forward extent of nodes with $d\ge0.95$ within a 2 mm strip along the ligament. The extent is a threshold-dependent, mesh-resolved descriptor. The NPZ stores the mesh and sampled displacement/damage fields for further plotting; Zarr stores the public solver's trajectory outputs.
""")
add("code","""
import csv
from IPython.display import HTML
with (output_dir / "results.csv").open() as stream:
    rows = list(csv.DictReader(stream))
selected_rows = [rows[i] for i in np.linspace(0, len(rows)-1, 6, dtype=int)]
head = "<tr><th>Time [µs]</th><th>Maximum d</th><th>Extent [mm]</th></tr>"
body = "".join(f"<tr><td>{float(r['time_us']):.2f}</td><td>{float(r['maximum_damage']):.3f}</td><td>{float(r['extent_d095_mm']):.2f}</td></tr>" for r in selected_rows)
display(HTML("<table>" + head + body + "</table>"))
print("Saved files:", ", ".join(sorted(p.name for p in output_dir.iterdir() if p.is_file())))
""")
add("markdown",r"""
## Key takeaways

- Geometry, material properties, supports and the loading schedule jointly define the fracture problem.
- The phase field resolves a crack as a continuous damage band whose width depends on $\ell$ and mesh resolution.
- The dynamic calculation couples explicit momentum updates with constrained implicit damage updates.
- Field snapshots, an animation, energy curves and numerical tables describe complementary aspects of the same simulation.

## Student exercises

### Exercise 1: resolve the time and length scales

How many numerical updates occur during the $20\,\mu$s ramp? Compare the regularisation length with the plate width. Explain why the smallest mesh element affects explicit computational cost.

<details><summary>Hint</summary>

Read `summary['dt_seconds']` and use $N_\mathrm{ramp}\simeq t_\mathrm{ramp}/\Delta t$. The explicit stability step scales with element size divided by elastic-wave speed.

</details>

<details><summary>Worked Solution</summary>

With $\Delta t\simeq1.6353\times10^{-8}$ s, the ramp spans approximately 1,223 updates. The regularisation length is $0.5/40=0.0125$ of the plate width. A smaller element reduces the stable time step and increases the update count for the same physical duration. Resolution along the entire crack path must also be considered when assessing a mesh.

</details>

### Exercise 2: measure a crack descriptor from saved fields

Use the existing saved fields to compare the forward extent obtained with thresholds $d\ge0.5$ and $d\ge0.95$. At an intermediate time, explain why the two values can differ. This exercise reuses the completed simulation.

<details><summary>Hint</summary>

Select nodes with $x>20$ mm and $|y-20|\le1$ mm, then apply each threshold to one row of `fields['damage']`. Subtract 20 mm from the largest selected x-coordinate.

</details>

<details><summary>Worked Solution</summary>

The lower threshold includes the partially damaged process zone ahead of the highly damaged band, so its extent can be greater. Both are discrete descriptors of a diffuse field. Report the threshold, strip and mesh when presenting either measure as a crack-length estimate.

</details>

## Continue exploring

The example is the lightweight public [PhAST B3 dynamic SENT case](https://github.com/CEMS-Lab/PhAST/tree/f6324f899f0701769810be117f27f1208f7a582e/examples/dynamic/B3_dynamic_sent), with the checked mesh and explicit classroom numerical settings recorded in the YAML. A separate fixed-mesh half-time-step calculation characterises temporal sensitivity. Spatial refinement and larger branching problems form further studies.

For a new geometry, create the mesh with Gmsh, identify boundary sets, then follow the same material → supports → loading → solve → inspect sequence. The current mesh lets this short practical focus on fracture and result interpretation.

### Computation record

The elapsed value below includes pauses when cells are run interactively. The course execution record measures uninterrupted computation separately from installation.
""")
add("code","""
elapsed_seconds = time.perf_counter() - computation_started
print({"elapsed_after_setup_seconds": round(elapsed_seconds, 2),
       "solver_subprocess_seconds": json.loads((output_dir / "runtime.json").read_text())["whole_process_seconds"],
       "environment": setup_receipt["environment"]})
""")

notebook={"nbformat":4,"nbformat_minor":5,"cells":cells,"metadata":{
    "kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
    "language_info":{"name":"python"},"colab":{"name":NAME+".ipynb","provenance":[]},
    "creator":"Allamaprabhu Ani","prepared_by":["Allamaprabhu Ani","Sathiskumar A. Ponnusami"],
    "affiliation":"CEMS-Lab","course":"UKACM Autumn School 2026",
    "authoring_source":"source/notebooks/build_dynamic_practical.py",
    "computation_budget_seconds":120,"solver_subprocess_budget_seconds":95,
    "scientific_scope":"Actual public PhAST dynamic B3, qualitative coarse-mesh practical"}}
path=ROOT/"notebooks/extensions"/(NAME+".ipynb")
path.parent.mkdir(parents=True,exist_ok=True)
path.write_text(json.dumps(notebook,indent=1)+"\n")
print(path)

if __name__ == "__main__":
    import argparse
    import base64
    import os
    import platform
    import shutil
    import signal
    import subprocess
    import sys
    import time
    parser=argparse.ArgumentParser()
    parser.add_argument("--execute",action="store_true")
    parser.add_argument("--evidence-name",default="b3_practical_candidate_01")
    args=parser.parse_args()
    if args.execute:
        evidence=ROOT/"evidence/propagation_20260911"/args.evidence_name
        evidence.mkdir(parents=True,exist_ok=False)
        runner="""import nbformat,sys
from nbclient import NotebookClient
p=sys.argv[1]
n=nbformat.read(p,as_version=4)
try:
 NotebookClient(n,timeout=110,kernel_name='python3',resources={'metadata':{'path':sys.argv[2]}}).execute()
finally:
 nbformat.write(n,p)
"""
        env=dict(os.environ,PHAST_DYNAMIC_OUTPUT=str(evidence),MPLBACKEND="Agg",
                 OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1")
        started=time.perf_counter();timeout=False
        with (evidence/"notebook.log").open("w") as stream:
            proc=subprocess.Popen([sys.executable,"-c",runner,str(path),str(ROOT)],env=env,
                                  stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
            try:code=proc.wait(timeout=120)
            except subprocess.TimeoutExpired:
                timeout=True;os.killpg(proc.pid,signal.SIGKILL);code=proc.wait()
        elapsed=time.perf_counter()-started
        executed=json.loads(path.read_text())
        shutil.copy2(path,evidence/path.name)
        figure_count=0
        for i,cell in enumerate(executed["cells"]):
            for j,output in enumerate(cell.get("outputs",[])):
                for mime,ext in [("image/png","png"),("image/gif","gif")]:
                    if mime in output.get("data",{}):
                        encoded=output["data"][mime]
                        if isinstance(encoded,list):encoded="".join(encoded)
                        (evidence/f"cell_{i:02}_{j}.{ext}").write_bytes(base64.b64decode(encoded))
                        figure_count+=1
        sources=[Path(__file__),ROOT/"notebooks/day2_helpers/dynamic_practical.py",
                 ROOT/"configs/day2_forward/b3_classroom/config.yaml",ROOT/"configs/day2_forward/b3_classroom/mesh.msh"]
        receipt={"whole_process_seconds":elapsed,"hard_cap_seconds":120,"timeout":timeout,
                 "exit_code":code,"figures":figure_count,
                 "code_cells":sum(c["cell_type"]=="code" for c in executed["cells"]),
                 "executed_code_cells":sum(c["cell_type"]=="code" and c.get("execution_count") is not None for c in executed["cells"]),
                 "source_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                 "notebook_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                 "platform":platform.platform(),"python":sys.version,
                 "scope":"Fresh local complete notebook; setup included in process timing; authenticated Colab remains separate"}
        (evidence/"notebook_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
        print(json.dumps(receipt,indent=2))
        if code!=0 or timeout:raise SystemExit(1)
