"""Build three concise classroom notebooks from the retained public course.

This is an authoring command; it clears outputs and never runs computations.
The detailed notebooks remain the provenance and independent-study route.
Generated notebooks have one shared setup cell, inspectable teaching code,
folded plotting/export detail, and structured exercise metadata for the book.

Course material prepared by Allamaprabhu Ani and Sathiskumar A. Ponnusami,
CEMS-Lab, UKACM Autumn School 2026. Preserve the repository's attribution and
bundled licences when reusing this material.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import textwrap


NAMES = (
    "01_simulate_fracture",
    "02_gradients_and_recovery",
    "03_learning_and_hybrid",
)
DETAILS = (
    "01_phast_tiny_evolving_fracture",
    "02_degradation_autograd",
    "03_tiny_derivative_inverse_toy",
    "04_train_save_reload_adapter",
    "05_hybrid_reference_correction",
)
PUBLIC = "https://cems-lab.github.io/autumn-school"
GITHUB = "https://github.com/CEMS-Lab/autumn-school/blob/main"


def text(cell):
    source = cell["source"]
    return "".join(source) if isinstance(source, list) else source


class Lesson:
    def __init__(self, root, name, title, objective, prediction, sources):
        self.root, self.name, self.cells = root, name, []
        self.info = {
            "title": title, "objective": objective, "prediction": prediction,
            "source_notebooks": [f"notebooks/{source}.ipynb" for source in sources],
            "source_sha256": {
                f"notebooks/{source}.ipynb": hashlib.sha256(
                    (root / f"notebooks/{source}.ipynb").read_bytes()).hexdigest()
                for source in sources
            },
            "authoring_source": "source/notebooks/build_classroom_labs.py",
            "execution": "Run the complete generated notebook to retain new outputs and timing.",
        }
        self.md(f"""# {title}

**Learning objective:** {objective}

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/{name}.ipynb)

[Download Practice Notebook]({PUBLIC}/notebooks/study/classroom/{name}.ipynb) · [Download with Worked Solutions]({PUBLIC}/notebooks/solutions/classroom/{name}.ipynb) · [Environment Setup]({PUBLIC}/SETUP.md)

**Predict first:** {prediction}

Run the cells in order. The setup and figure-formatting cells can be expanded when you want to inspect them. The principal model, derivative and learning operations stay visible.

Prepared by Allamaprabhu Ani and Sathiskumar A. Ponnusami, CEMS-Lab, for the UKACM Autumn School 2026.
""")
        bootstrap = (root / "source/notebooks/colab_bootstrap.py").read_text()
        self.code('#@title Set up the course environment { display-mode: "form" }\n' + bootstrap +
                  '\nsession_started = time.perf_counter()\n'
                  'torch.set_num_threads(1)\n', folded=True, role="setup")

    def md(self, source, **metadata):
        self.add("markdown", source, metadata)

    def code(self, source, folded=False, role="teaching"):
        source = textwrap.dedent(source).strip()
        if not folded and len([line for line in source.splitlines() if line.strip()]) > 12:
            raise ValueError(f"Visible code exceeds 12 lines: {self.name}: {source[:100]}")
        metadata = {"classroom_role": role}
        if folded:
            metadata.update(tags=["hide-input"], cellView="form",
                            jupyter={"source_hidden": True})
        self.add("code", source, metadata)

    def add(self, kind, source, metadata):
        source = textwrap.dedent(source).strip()
        identifier = hashlib.sha256(f"{self.name}:{len(self.cells)}:{source}".encode()).hexdigest()[:16]
        cell = {"id": identifier, "cell_type": kind, "metadata": metadata,
                "source": source.splitlines(keepends=True)}
        if kind == "code":
            cell.update(execution_count=None, outputs=[])
        self.cells.append(cell)

    def finish(self, takeaways, exercises):
        self.info.update(takeaways=takeaways, exercises=copy.deepcopy(exercises))
        self.md("## Key takeaways\n\n" + "\n".join(f"- {item}" for item in takeaways))
        self.md("## Student exercises\n\nWork through both questions, then open the hints and worked answers.",
                classroom_exercise=True)
        for number, exercise in enumerate(exercises, 1):
            exercise.setdefault("id", f"{self.name[:2]}-{number}")
            self.info["exercises"][number - 1]["id"] = exercise["id"]
            self.md(f"### Exercise {number}: {exercise['title']}\n\n{exercise['question']}",
                    classroom_exercise=True, exercise_id=exercise["id"])
            for key, label in (("hint", "Hint"), ("solution", "Worked Solution")):
                self.md(f"<details><summary>{label}</summary>\n\n{exercise[key]}\n\n</details>",
                        classroom_exercise=True, exercise_id=exercise["id"], answer_kind=key)
        links = " · ".join(f"[Detailed notebook {name[:2]}]({GITHUB}/notebooks/{name}.ipynb)"
                           for name in (Path(path).stem for path in self.info["source_notebooks"]))
        self.md("## Continue studying\n\n" + links +
                f"\n\nThe complete source, attribution and bundled licences remain in the [course repository]({GITHUB}/ATTRIBUTION.md).")
        self.md("### Session timing\n\nElapsed session time includes reading and pauses between cells. The course runner measures uninterrupted computation separately from installation.")
        self.code('''
            session_seconds = time.perf_counter() - session_started
            print({"setup_seconds": setup_receipt["setup_seconds"],
                   "elapsed_session_seconds": round(session_seconds, 2),
                   "environment": setup_receipt["environment"], "torch": torch.__version__})
        ''')
        return {
            "cells": self.cells, "nbformat": 4, "nbformat_minor": 5,
            "metadata": {
                "classroom": self.info,
                "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                "language_info": {"name": "python"},
                "colab": {"name": self.name + ".ipynb", "provenance": []},
                "creator": "Allamaprabhu Ani",
                "prepared_by": ["Allamaprabhu Ani", "Sathiskumar A. Ponnusami"],
                "affiliation": "CEMS-Lab", "course": "UKACM Autumn School 2026",
            },
        }


def read_details(root):
    return {name: json.loads((root / f"notebooks/{name}.ipynb").read_text()) for name in DETAILS}


def solutions(root, number):
    material = json.loads((root / f"source/book/solutions/{number:02}.json").read_text())
    for index, exercise in enumerate(material["exercises"], 1):
        exercise["source"] = f"source/book/solutions/{number:02}.json, exercise {index}"
    return material


def build_quasistatic_reference(root, detailed):
    original = detailed[DETAILS[0]]["cells"]
    old = lambda index: text(original[index])
    material = solutions(root, 1)
    lab = Lesson(root, NAMES[0], "Practical 1: Simulate and interpret diffuse fracture damage",
                 "Build a small public PhAST calculation, apply symmetric tension, and inspect displacement, damage and reaction. Compare two imposed separations using saved numerical results.",
                 "Where will damage increase, and how should halving the separation affect the elastic energy?", [DETAILS[0]])
    lab.md(r"""## Physical motivation and model

Pulling the top and bottom of a specimen apart stores elastic energy. A phase-field model balances that energy with the cost of a diffuse damaged region. We use a $4\times2$ rectangle with an initially damaged centreline of nominal length $0.8$.

This actual PhAST example uses quasistatic AT2, isotropic energy degradation, plane strain and assembled sparse-direct mechanics. Its loading produces diffuse damage evolution. All quantities use consistent dimensionless teaching scales.

The damage variable is $d=0$ in intact material and $d=1$ on the initial notch. The regularisation length $\ell=0.15$ sets the scale over which damage varies. The energy takes the AT2 form

$$\mathcal E(\mathbf u,d)=\int_\Omega g(d)\,\psi_0(\boldsymbol\varepsilon(\mathbf u))\,\mathrm d\Omega + \frac{G_c}{2}\int_\Omega\left(\frac{d^2}{\ell}+\ell|\nabla d|^2\right)\mathrm d\Omega.$$

Here $\mathbf u$ is displacement, $\boldsymbol\varepsilon$ is small strain, $\psi_0$ is elastic energy density, $g$ degrades stiffness, and $G_c$ is fracture energy per unit crack area. Prescribed boundary motion supplies the loading.

## Step-by-step calculation

### Choose the public case

The single configuration supplies the geometry, mesh, material and loading. Source verification selects the public PhAST version bundled with this course.
""")
    lab.code('''
        import copy
        import matplotlib.tri as mtri
        from day2_helpers import import_public_phast, load_forward_config
        from day2_helpers.forward_workflow import prepare_course_mesh, solver_configuration
        from day2_helpers.forward_workflow import solve_prepared_case, save_results, load_results
        from day2_helpers.forward_workflow import digest_file, notebook_source_hash
        config = load_forward_config()
        phast_info = import_public_phast(config["public_source"]["revision"])
        torch.manual_seed(config["seed"])
        torch.set_num_threads(min(4, os.cpu_count() or 1))
    ''')
    lab.md("The geometry sketch shows the imposed vertical motion and the lateral restraints. Its plotting details are expandable.")
    lab.code('''
        practical_dir = assets_dir() / "classroom" / "01"
        practical_dir.mkdir(parents=True, exist_ok=True)
        geometry, mesh_cfg = config["geometry"], config["mesh"]
        width, height, notch_length = (geometry[key] for key in ("width", "height", "notch_length"))
        print({"geometry": geometry, "mesh": mesh_cfg, "loading": config["loading"]})
        def show_figure(fig, name, alt):
            fig.savefig(practical_dir / name, dpi=150, bbox_inches="tight")
            display_figure(fig, alt=alt)
            plt.close(fig)
    ''', folded=True, role="plotting")
    lab.code(old(3)[old(3).index("fig, ax ="):], folded=True, role="plotting")
    lab.md(r"""### Create the mesh

The course helper `prepare_course_mesh` creates the rectangular three-node triangular mesh, saves and reopens its arrays, checks the round trip, and returns the mesh used below. Coordinates have shape `(nodes, 2)`; connectivity has shape `(triangles, 3)`. The named boundary sets identify exterior nodes. [Inspect the helper source](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/day2_helpers/forward_workflow.py).
""")
    lab.code('''
        prepared_mesh_path = practical_dir / "prepared_mesh.npz"
        mesh = prepare_course_mesh(config, prepared_mesh_path)
        print({"nodes": mesh.n_nodes, "T3_elements": mesh.n_elems,
               "boundary_sets": sorted(mesh.node_sets)})
    ''')
    lab.md(r"""### Set the initial notch and boundary conditions

The Boolean mask selects centreline nodes up to the nominal notch endpoint. Hold them at $d=1$. The boundary helper prescribes $u_y=+\delta/2$ at the top, $u_y=-\delta/2$ at the bottom and $u_x=0$ on every exterior edge. Here $\delta$ denotes the total separation.
""")
    lab.code('''
        from phast.physics.boundary_conditions import symmetric_tension_bcs
        from phast.physics.material import Material
        from phast.solvers.staggered_solver import StaggeredSolver
        nodes = mesh.nodes
        precrack = ((nodes[:, 1] - height / 2).abs() < 1.e-12)
        precrack &= nodes[:, 0] <= notch_length + 1.e-12
        bcs = symmetric_tension_bcs(mesh, disp=config["loading"]["total_symmetric_vertical_displacement"])
        bcs.add_pf_dirichlet(torch.where(precrack)[0], value=1.0)
    ''')
    lab.md(r"""### Construct the material and solver

The material uses $E=1$, $\nu=0.3$, $G_c=0.0005$ and $\ell=0.15$. `StaggeredSolver` receives the mesh, material and boundary objects we just created. Seed its initial damage using the same notch mask.
""")
    lab.code('''
        material = Material(**config["material"])
        assert material.plane_stress is False
        solver = StaggeredSolver(mesh, material, bcs, solver_configuration(config))
        solver.d[precrack] = 1.0
        assert solver.mesh is mesh and solver.bcs is bcs and solver.material is material
        print({"locked_precrack_nodes": int(precrack.sum()), "kinematics": "plane strain"})
    ''')
    lab.md("Locate the prescribed boundaries and the initial notch in these full-domain views. Expand the cell to inspect the plotting commands.")
    lab.code(old(9), folded=True, role="plotting")
    lab.md(r"""### Apply the load and solve

The 60 load factors advance a sequence of quasistatic equilibria. At each increment, PhAST alternates mechanics, driving history and damage until the relative $L^2$ changes in both fields are below $10^{-5}$.

`solve_prepared_case` advances the existing `solver`. Its loop sets `bcs.load_factor`, calls `solver.step_full()`, records the fields, and checks displacement constraints, damage bounds, irreversibility and convergence at every increment. [Open that short workflow and its checks](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/day2_helpers/forward_workflow.py).
""")
    lab.code(old(11).replace('precrack, phast_info)', 'precrack, phast_info, retain_history=True)'))
    lab.md("### Save and reopen the fields\n\nThe original NPZ stores the named fields and four selected snapshots. A separate history NPZ stores the seeded state and every accepted displacement/damage state. JSON records the case, source revision, response trace and file hashes. Reopening checks file integrity and reproduces every array. These files support independent post-processing.")
    lab.code('''
        result["metadata"]["source_hashes"] = {
            name: digest_file(COURSE_ROOT / name) for name in (
                "notebooks/day2_helpers/forward_workflow.py",
                "notebooks/day2_helpers/classroom_visuals.py",
                "configs/day2_forward/tiny_notched_tension.json")}
        notebook_path = "notebooks/classroom/01_simulate_fracture.ipynb"
        result["metadata"]["notebook_source"] = {
            "path": notebook_path,
            "cell_source_sha256": notebook_source_hash(COURSE_ROOT / notebook_path)}
    ''', folded=True, role="provenance")
    lab.code('''
        field_path, metadata_path = save_results(result, practical_dir)
        saved, record = load_results(field_path, metadata_path)
        for name, array in result["arrays"].items():
            np.testing.assert_array_equal(saved[name], array)
        assert record["config"] == config
        print({"fields_file": field_path.name, "case_file": metadata_path.name,
               "displacement_shape": saved["final_displacement"].shape})
    ''')
    lab.md("## Interpret the computed fields\n\nThe vertical displacement and magnified boundary outline show the imposed motion. Initial, first-increment and final damage use a common colour scale. The additional increment plot isolates damage accumulated after the first equilibrium step. All views use the reopened arrays.")
    plotting = old(15)
    markers = ("\nfig, axes = plt.subplots(1, 3", "\nfig, ax = plt.subplots(figsize=(7")
    split1, split2 = (plotting.index(marker) for marker in markers)
    lab.code(plotting[:split1], folded=True, role="plotting")
    lab.md("Compare damage across the complete specimen before loading, after the first increment and at the final separation.")
    lab.code(plotting[split1:split2], folded=True, role="plotting")
    lab.md("This increment separates the initial damaged centreline from subsequent diffuse evolution. The current example illustrates damage accumulation under the stated loading and restraints.")
    lab.code(plotting[split2:], folded=True, role="plotting")
    lab.md("The top reaction sums the internal vertical forces at prescribed top nodes. Read this curve alongside the fields. The nodal damage sum depends on mesh density; the iteration count describes coupling effort.")
    lab.code(old(17), folded=True, role="plotting")
    lab.md("### Follow the accepted states\n\nThe animation shows the seeded notch followed by all 60 accepted quasistatic increments, with damage fixed to the same 0–1 colour scale. Each frame corresponds to saved numerical arrays; the reaction marker identifies its load. Playback speed is a viewing choice. The static full-domain figures above remain available for comparison. This case shows diffuse damage accumulation under the stated loading.")
    lab.code('''
        from IPython.display import HTML
        from day2_helpers.forward_workflow import load_history
        from day2_helpers.classroom_visuals import fracture_evolution, response_table
        retained_history = load_history(metadata_path, saved, record)
        animation_path = fracture_evolution(saved, record, practical_dir / "tiny_notched_tension_evolution.gif", history=retained_history)
        display(Image(filename=str(animation_path), format="gif",
                      alt="Seeded notch and 60 accepted PhAST damage states with their reaction history."))
        response_csv, response_html = response_table(record, practical_dir)
        display(HTML(response_html))
        print({"animation": animation_path.name, "all_increment_results": response_csv.name,
               "original_fields": field_path.name})
    ''')
    lab.md(r"""### Compare a smaller separation

For a fixed damage field, halving displacement halves strain and reduces elastic energy to one quarter. The coupled damage response also changes. Copy the case, halve its maximum separation, and create a fresh solver on the same mesh.
""")
    lab.code('''
        smaller_config = copy.deepcopy(config)
        smaller_config["loading"]["total_symmetric_vertical_displacement"] *= .5
        smaller_bcs = symmetric_tension_bcs(mesh, disp=smaller_config["loading"]["total_symmetric_vertical_displacement"])
        smaller_bcs.add_pf_dirichlet(torch.where(precrack)[0], value=1.0)
        smaller_material = Material(**smaller_config["material"])
        smaller_solver = StaggeredSolver(mesh, smaller_material, smaller_bcs, solver_configuration(smaller_config))
        smaller_precrack = precrack.clone()
        smaller_solver.d[smaller_precrack] = 1.0
    ''')
    lab.md("Execute the same load factors and reopen the second case. Both cases keep the same coordinates, triangles and material values.")
    comparison = old(19)
    solve_part = comparison[comparison.index("smaller_result ="):comparison.index("\nfig, axes")]
    lab.code(solve_part.replace('save_results(smaller_result, assets_dir(),', 'save_results(smaller_result, practical_dir,')
             .replace('smaller_precrack, phast_info)', 'smaller_precrack, phast_info, retain_history=True)'))
    lab.md("Inspect both final fields on the same scale. The assertion checks the lower nodal damage sum for this particular smaller-load calculation; the full fields show where that difference occurs.")
    lab.code(comparison[comparison.index("fig, axes"):], folded=True, role="plotting")
    lab.md("The comparison table uses each run's final accepted increment. Separate history NPZ files include every accepted displacement and damage state; each CSV contains all 60 response rows at full precision. The nodal damage sum is a mesh-dependent descriptor.")
    lab.code('''
        from day2_helpers.classroom_visuals import numeric_table_html, save_table
        smaller_history = load_history(smaller_json, smaller_saved, smaller_record)
        half_csv, _ = response_table(smaller_record, practical_dir, "tiny_notched_tension_half_load")
        comparison_rows = [dict(case=label, **case["trace"][-1]) for label, case in
                           (("Full separation", record), ("Half separation", smaller_record))]
        columns = [("case", "Case"), ("applied_separation", "Final separation"),
                   ("reaction_top_y", "Top reaction"), ("damage_outside_sum", "Nodal damage sum outside notch")]
        save_table(comparison_rows, practical_dir / "tiny_notched_tension_comparison.csv")
        display(HTML(numeric_table_html(comparison_rows, columns, "Final states on the same mesh and scales")))
    ''')
    lab.md("""### Example outline · P1-R01 · A short propagating crack

**Learning question:** How does a resolved crack front advance as loading continues?

**Planned content.** Compare full-domain displacement and damage fields with the reaction history from a selected public PhAST propagation example.

### Animation storyboard · P1-A01 · Geometry to damage

**Current notebook visual.** The accepted-state GIF above shows the seeded notch followed by all 60 computed damage states with their response history. The geometry and mesh figures supply the preceding static views. A presenter-controlled composition can combine those stages using the retained outputs.
""")
    return lab.finish(material["takeaways"], material["exercises"])


def build_simulation(root, detailed):
    """Primary P1: one short dynamic run, using the checked public B3 mesh.

    The preserved quasistatic generator and exact executed archive retain the
    former two-run teaching reference. This function only authors P1.
    """
    candidate_path = root / "notebooks/extensions/01_dynamic_plate_crossing.ipynb"
    candidate = json.loads(candidate_path.read_text())
    lab = Lesson(root, NAMES[0], "Practical 1: Simulate a crack crossing a plate",
                 "Import a notched-plate mesh, understand its supports and loading, run a short dynamic PhAST calculation, and interpret the crack evolution and energy components.",
                 "Under vertical tension, where will the crack grow from a horizontal notch, and how might its opening change the stored elastic energy?",
                 ["extensions/01_dynamic_plate_crossing"])
    lab.info.update(
        authoring_source="source/notebooks/build_classroom_labs.py, build_simulation",
        dynamic_authoring_source="source/notebooks/build_dynamic_practical.py",
        physical_case="Public PhAST B3 dynamic SENT, plane-strain spectral AT2",
        solver_subprocess_budget_seconds=95,
        computation_budget_seconds=120,
        previous_reference="notebooks/extensions/reference_quasistatic_diffuse_damage_20260911.ipynb",
        source_config="configs/day2_forward/b3_classroom/config.yaml",
        source_mesh="configs/day2_forward/b3_classroom/mesh.msh")
    # Keep the extension's inspected model -> setup -> solve -> plots sequence.
    # Shared Lesson supplies classroom badges, setup, exercises and timing.
    for cell in candidate["cells"][2:16]:
        source = text(cell)
        if cell["cell_type"] == "markdown":
            lab.md(source)
        else:
            if "output_dir = Path(os.environ.get(" in source:
                source = source.replace(
                    'output_dir = Path(os.environ.get("PHAST_DYNAMIC_OUTPUT", tempfile.mkdtemp(prefix="phast-b3-"))) / "results"',
                    'practical_dir = assets_dir() / "classroom" / "01_dynamic"\n'
                    'practical_dir.mkdir(parents=True, exist_ok=True)\n'
                    'output_dir = Path(tempfile.mkdtemp(prefix="b3-", dir=practical_dir)) / "results"')
            lab.code(source)
    lab.md("""### Worked example · P1-R01 · A short propagating crack

The computed fields above follow initiation at the geometric notch and growth through the remaining ligament. Read the field sequence together with the elastic, fracture and kinetic energy curves. The fixed-mesh half-time-step comparison records temporal sensitivity; spatial refinement is a further study.

### Animation · P1-A01 · Geometry to damage

The mesh and support diagram introduces the specimen. The 40-frame GIF selects actual saved states through initiation and propagation, then includes the final hold state. The static snapshots and numerical CSV remain available for independent interpretation.

For a new geometry, create the mesh with Gmsh, identify boundary sets, then follow the same material → supports → loading → solve → inspect sequence. The supplied public mesh makes this first practical short and reproducible.
""")
    notebook = lab.finish([
        "Geometry, material properties, supports and loading jointly define the fracture problem.",
        "The phase field resolves a continuous damage band whose width depends on regularisation and mesh resolution.",
        "The dynamic calculation couples explicit momentum updates with constrained implicit damage updates.",
        "Fields, animation, energy curves and numerical tables describe complementary aspects of one simulation.",
    ], [
        {
            "id": "01-1", "kind": "conceptual", "title": "Resolve the time and length scales",
            "source": "source/notebooks/build_dynamic_practical.py, exercise 1",
            "question": r"How many numerical updates occur during the $20\,\mu$s ramp? Compare the regularisation length with the plate width. Explain why the smallest mesh element affects explicit computational cost.",
            "hint": r"Read `summary['dt_seconds']` and use $N_{\mathrm{ramp}}\simeq t_{\mathrm{ramp}}/\Delta t$. The explicit stability step scales with element size divided by elastic-wave speed.",
            "solution": r"With $\Delta t\simeq1.6353\times10^{-8}$ s, the ramp spans approximately 1,223 updates. The regularisation length is $0.5/40=0.0125$ of the plate width. A smaller element reduces the stable time step and increases the update count for the same physical duration. Resolution along the whole crack path must also be considered when assessing a mesh.",
        },
        {
            "id": "01-2", "kind": "practical", "title": "Measure a crack descriptor from saved fields",
            "source": "source/notebooks/build_dynamic_practical.py, exercise 2",
            "question": r"Use the saved fields to compare the forward extent obtained with thresholds $d\ge0.5$ and $d\ge0.95$. At an intermediate time, explain why the two values can differ. Reuse the completed simulation.",
            "hint": r"Select nodes with $x>20$ mm and $|y-20|\le1$ mm, then apply each threshold to one row of `fields['damage']`. Subtract 20 mm from the largest selected x-coordinate.",
            "solution": "The lower threshold includes the partially damaged process zone ahead of the highly damaged band, so its extent can be greater. Both values are discrete descriptors of a diffuse field. Report the threshold, strip and mesh when presenting either measure as a crack-length estimate.",
        },
    ])
    for cell in notebook["cells"]:
        source = text(cell).replace(
            f"{GITHUB}/notebooks/01_dynamic_plate_crossing.ipynb",
            f"{GITHUB}/notebooks/extensions/01_dynamic_plate_crossing.ipynb")
        cell["source"] = source.splitlines(keepends=True)
    return notebook


def build_gradients(root, detailed):
    degradation = detailed[DETAILS[1]]["cells"]
    inverse = detailed[DETAILS[2]]["cells"]
    lab = Lesson(root, NAMES[1], "Practical 2: Gradients and material recovery",
                 "Trace a force-to-loss gradient by hand and with PyTorch, check a material-law derivative, then differentiate an elastic-bar solve and recover its modulus.",
                 "For a stretched, damaged bar, how will a little more extension or a little more damage change its force?", DETAILS[1:3])
    lab.md(r"""## Physical motivation and equations

A derivative quantifies how a chosen output changes when one input changes. We begin with a local damaged bar whose extension and damage are prescribed. Then we connect that chain rule to a public material law and an equilibrium solve.

### Begin with a damaged bar

For a bar with Young's modulus $E$, cross-sectional area $A$, reference length $L_b$, extension $u$ and uniform damage $d$, the axial force is

$$g(d)=(1-d)^2,\qquad F(u,d)=\frac{EA}{L_b}\,g(d)\,u.$$

All quantities use dimensionless teaching scales. This local constitutive example takes $E=2$, $A=L_b=1$, zero residual stiffness ($\kappa=0$), and $0<d<1$. The two inputs are collected in $\mathbf q=(u,d)=(0.1,0.5)$. Increasing $u$ stretches the bar further; increasing $d$ reduces its stiffness. Hold the other input fixed when reasoning about each change.

Suppose the target force is $F^\star=0.04$. Define the residual $r=F-F^\star$ and the scalar squared-mismatch loss $\mathcal L=\tfrac12r^2$. Damage is a prescribed input in this first calculation. The later equilibrium example introduces a solved displacement field.

### Compute the forward values

`requires_grad=True` asks PyTorch to record how subsequent tensor operations depend on $\mathbf q$. Unpacking its entries preserves that connection. Follow the values from inputs to degradation, force, residual and loss.
""")
    lab.code('''
        q = torch.tensor([.1, .5], dtype=torch.float64, requires_grad=True)
        u, damage = q.unbind()
        E, A, L_b, target_force = 2., 1., 1., .04
        degradation = (1. - damage) ** 2
        force = (E * A / L_b) * degradation * u
        residual = force - target_force
        primer_loss = .5 * residual ** 2
        print({"degradation": float(degradation.detach()), "force": float(force.detach()),
               "residual": float(residual.detach()), "loss": float(primer_loss.detach())})
    ''')
    lab.md(r"""The forward values are $g=0.25$, $F=0.05$, $r=0.01$ and $\mathcal L=5\times10^{-5}$. The force is slightly above its target.

### Work backwards with the chain rule

Start with the loss sensitivity to force, $\partial\mathcal L/\partial F=r=0.01$. The two local force sensitivities are

$$\frac{\partial F}{\partial u}=\frac{EA}{L_b}(1-d)^2=0.5,
\qquad
\frac{\partial F}{\partial d}=-2\frac{EA}{L_b}(1-d)u=-0.2.$$

Multiply each by the same loss seed:

$$\frac{\partial\mathcal L}{\partial u}=0.01(0.5)=0.005,
\qquad
\frac{\partial\mathcal L}{\partial d}=0.01(-0.2)=-0.002.$$

These signs describe this evaluation point: a small increase in extension raises the loss; a small increase in damage lowers it. They follow from both the material response and the current force mismatch.

### Ask PyTorch for the same derivatives

`primer_loss.backward()` applies that chain rule to the recorded operations. `q.grad` contains $\nabla_{\mathbf q}\mathcal L$ in the order `[u, damage]`. Re-run the forward cell before repeating this backward cell to create a fresh graph. An optimisation step would subsequently choose how to change the inputs using this gradient.
""")
    lab.code('''
        primer_loss.backward()
        print("[d(loss)/du, d(loss)/dd] =", q.grad.tolist())
        manual_gradient = residual.detach() * torch.stack([
            (E * A / L_b) * (1 - damage.detach()) ** 2,
            -2 * (E * A / L_b) * (1 - damage.detach()) * u.detach()])
        torch.testing.assert_close(q.grad, manual_gradient)
    ''')
    lab.md(r"""### Check the gradient and inspect its meaning

The check below independently evaluates central differences, $[\mathcal L(\mathbf q+h\mathbf e_i)-\mathcal L(\mathbf q-h\mathbf e_i)]/(2h)$, with $h=10^{-6}$. Here $\mathbf e_i$ changes only input $i$. The helper records the analytic, autograd and finite-difference results in a CSV and a JSON file. The two force curves vary one input at a time around the same evaluation point.
""")
    lab.code('''
        from day2_helpers.autodiff_primer import verify_primer
        from day2_helpers.autodiff_primer import force_sensitivities, forward_reverse_graph
        practical_dir = assets_dir() / "classroom" / "02"
        primer_check = verify_primer(q, q.grad, practical_dir)
        for method in ("autograd", "analytic", "central_fd"):
            print(method, primer_check["loss_gradient_" + method])
    ''')
    lab.code('''
        fig = force_sensitivities(primer_check, practical_dir)
        display_figure(fig, alt="Force increases with extension and decreases with prescribed damage; the evaluation point, target force and local damage tangent are marked.")
        plt.close(fig)
        fig = forward_reverse_graph(primer_check, practical_dir)
        display_figure(fig, alt="Forward values from prescribed displacement and damage to force and loss, then the loss seed multiplied by each local force derivative.")
        plt.close(fig)
    ''', folded=True, role="plotting")
    lab.md(r"""### Predict and check: move each input separately

Keeping the target force fixed, predict what happens to the force and loss when (a) $u$ changes from $0.1$ to $0.101$, and (b) $d$ changes from $0.5$ to $0.501$. Change only one input at a time. Use $\Delta\mathcal L\approx(\partial\mathcal L/\partial q_i)\Delta q_i$ for your first estimate, then check the exact values below.

<details><summary>Hint</summary>

At the starting point, $\Delta\mathcal L\approx0.005\Delta u-0.002\Delta d$. Compare the new force with $F^\star=0.04$.

</details>
""")
    lab.code('''
        with torch.no_grad():
            for label, delta in (("More extension", [.001, 0.]), ("More damage", [0., .001])):
                changed = q.detach() + torch.tensor(delta, dtype=q.dtype)
                trial_force = (E * A / L_b) * (1 - changed[1]) ** 2 * changed[0]
                trial_loss = .5 * (trial_force - target_force) ** 2
                print(label, {"force": float(trial_force), "loss": float(trial_loss),
                              "loss_change": float(trial_loss - primer_loss.detach())})
    ''')
    lab.md(r"""<details><summary>Worked Solution</summary>

With $u=0.101$ and $d=0.5$, the force rises to $0.0505$ and the loss rises to $0.000055125$: $\Delta\mathcal L=0.000005125$, close to the first-order estimate $0.000005$.

With $u=0.1$ and $d=0.501$, the force falls to $0.0498002$ and the loss falls to about $0.00004802196$: $\Delta\mathcal L\approx-0.00000197804$, close to $-0.000002$. The gradient is a local linear approximation; finite changes also contain higher-order terms.

</details>

### Connect local derivatives to equilibrium

The damaged-bar calculation makes a scalar forward and backward pass explicit. We now inspect PhAST's degradation law, then differentiate a small mechanics graph in which a material parameter changes a solved response:

$$E\ \longrightarrow\ K(E)\ \longrightarrow\ \mathbf u\ \longrightarrow\ \mathcal L\ \longrightarrow\ \frac{\partial\mathcal L}{\partial E}.$$

Here $K(E)$ is the assembled stiffness matrix, $\mathbf u$ contains nodal displacements, and $\mathcal L$ measures displacement mismatch. The recovery example is a **one-dimensional linear-elastic bar** with a fixed left end, length $L=1$, area $A=1$ and tip force $F$. It uses 40 finite elements and dimensionless teaching scales. Its response is $u_{\mathrm{tip}}=FL/(EA)$. Under a fixed positive force, predict how increasing $E$ changes the tip displacement. Fracture evolution introduces additional coupled and history-dependent operations.

## Step-by-step calculation

### A local derivative: stiffness degradation

The normalised law $g(d)=(1-\eta)(1-d)^2+\eta$ reduces stiffness with damage $d$, retaining residual stiffness $\eta=10^{-7}$. Its slope is $g'(d)=-2(1-\eta)(1-d)$. Compare the public implementation, calculus and central differences.
""")
    lab.code('''
        from day2_helpers import import_public_phast
        phast_info = import_public_phast()
        from phast.physics.material import Material
        eta = 1.e-7
        material = Material(E=1., nu=.3, Gc=1., l0=.1, rho=1., eta_residual=eta)
        def g_analytic(d):
            return (1.0 - eta) * (1.0 - d) ** 2 + eta
        def gp_analytic(d):
            return -2.0 * (1.0 - eta) * (1.0 - d)
    ''')
    lab.md("`requires_grad=True` marks the chosen input. `torch.autograd.grad` differentiates the scalar output along the recorded tensor operations. Detaching the input lets us evaluate an independent finite-difference comparison.")
    lab.code('''
        d = torch.tensor(.25, requires_grad=True)
        g_phast = material.degradation(d)
        (g_ad,) = torch.autograd.grad(g_phast, d)
        h = 1.e-6
        g_fd = (g_analytic(d.detach() + h) - g_analytic(d.detach() - h)) / (2 * h)
        expected = gp_analytic(d.detach())
        print({"autograd": float(g_ad), "finite_difference": float(g_fd),
               "analytic": float(expected)})
    ''')
    lab.md("The endpoint checks confirm the meaning of intact and fully damaged material. The derivative checks compare this scalar material operation in float64.")
    lab.code(text(degradation[3]))
    lab.md("The degradation curve connects the numerical derivative to its physical meaning: the stiffness contribution decreases as damage grows.")
    lab.code('practical_dir = assets_dir() / "classroom" / "02"\npractical_dir.mkdir(parents=True, exist_ok=True)\n' +
             text(degradation[4]).replace('assets_dir() / "degradation_autograd.png"', 'practical_dir / "degradation_autograd.png"')
             .replace('axes[0].legend()', 'axes[0].text(.48, .82, r"$g(1)=\\eta=10^{-7}$" + "\\nEndpoint appears zero at this scale", transform=axes[0].transAxes, fontsize=9)\naxes[0].legend()'),
             folded=True, role="plotting")
    lab.md(r"""### Assemble a one-dimensional bar

Each element has stiffness $(EA/h)\begin{bmatrix}1&-1\\-1&1\end{bmatrix}$, where $h=L/40$. Assemble `K0` with unit modulus, so the differentiable scalar $E$ multiplies the complete matrix. Node zero is the fixed left end.
""")
    lab.code('''
        torch.manual_seed(20260909)
        n_elements, length, area = 40, 1.0, 1.0
        h = length / n_elements
        K0 = torch.zeros((n_elements + 1, n_elements + 1))
        local = torch.tensor([[1., -1.], [-1., 1.]]) * area / h
        for e in range(n_elements):
            K0[e:e+2, e:e+2] += local
        print({"stiffness_shape": tuple(K0.shape), "free_displacements": n_elements})
    ''')
    lab.md("Remove the fixed degree of freedom, apply the tip force at the final node, then solve equilibrium. The returned tip displacement remains connected to `E` through `torch.linalg.solve`.")
    lab.code('''
        def tip_displacement(E, load):
            K_free = (E * K0)[1:, 1:]
            force = torch.zeros(n_elements)
            force[-1] = load
            return torch.linalg.solve(K_free, force)[-1]
    ''')
    lab.md("Locate the fixed node, free nodes and applied force before differentiating equilibrium. The diagram uses the same 40-element topology as the assembled matrix.")
    lab.code('''
        from day2_helpers.classroom_visuals import bar_setup, bar_sensitivity, bar_initial_observations
        fig = bar_setup(n_elements, length, area, practical_dir)
        display_figure(fig, alt="One-dimensional 40-element bar, fixed left end and tip force at the right.")
        plt.close(fig)
    ''', folded=True, role="plotting")
    lab.md(r"""### Differentiate through equilibrium

For the uniform bar, $\partial u_{\mathrm{tip}}/\partial E=-u_{\mathrm{tip}}/E$. Check the sign and magnitude against the finite-element graph and a central difference.
""")
    probe = text(inverse[2]); probe = probe[probe.index("E_probe ="):]
    lab.code(probe)
    lab.md("All three sensitivity estimates are negative: a larger modulus reduces the extension under a fixed force. The step-size sweep shows how finite-difference agreement depends on the perturbation, using the same equilibrium function. The CSV retains every diagnostic value.")
    lab.code('''
        fig = bar_sensitivity(tip_displacement, E_probe, 1.1, du_dE_ad, du_dE_fd, du_dE_exact, practical_dir)
        display_figure(fig, alt="Negative bar sensitivity from autograd, finite differences and calculus, with finite-difference error versus step size.")
        plt.close(fig)
    ''', folded=True, role="plotting")
    lab.md("### Create synthetic observations\n\nThe known modulus generates displacement observations at separate training, validation and held-out loads. Detaching observations treats them as fixed measurements during recovery.")
    initial = text(inverse[3])
    lab.code(initial[:initial.index("log_E =")])
    lab.md("Plot the observations before fitting. The starting modulus 0.9 gives a steeper displacement–load response than the target modulus 2.4. Training, validation and held-out loads are marked separately.")
    lab.code('''
        fig = bar_initial_observations(tip_displacement, .9, E_true, train_loads, observed_train,
                                       validation_load, observed_validation, heldout_load, observed_heldout, practical_dir)
        display_figure(fig, alt="Starting and target elastic-bar responses with distinct training, validation and held-out observation loads.")
        plt.close(fig)
    ''', folded=True, role="plotting")
    lab.md(r"""### Recover a positive modulus

Represent stiffness as $E=\exp(z)$, with the trainable scalar `log_E` storing $z$. This gives positive stiffness. Minimise the mean squared displacement mismatch $\mathcal L=M^{-1}\sum_{i=1}^M(u_i(E)-u_i^{\mathrm{obs}})^2$, where $M=4$ training loads.
""")
    lab.code('''
        log_E = torch.nn.Parameter(torch.log(torch.tensor(.9)))
        optimiser = torch.optim.Adam([log_E], lr=.08)
        history = []
    ''')
    lab.md("Each iteration clears the previous gradients, evaluates the four equilibrium responses, differentiates the scalar loss and updates the log modulus. Validation observes an additional load without contributing to the training gradient.")
    lab.code('''
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
                    fitted = float(torch.exp(log_E))
                history.append((iteration + 1, fitted, float(loss.detach()), float(val_error)))
    ''')
    lab.md("## Interpret the recovered response\n\nCompare the recovered modulus and the held-out tip displacement, then inspect both the load-response curve and optimisation history. All observations here come from the same linear-elastic bar model.")
    lab.code(initial[initial.index("E_fit ="):])
    lab.md("Agreement at an additional positive load checks the fitted compliance. Both history curves show root-mean-square displacement error at the same recorded, updated modulus. Training uses four loads; validation uses one load, for which RMSE equals absolute displacement error. New geometries, nonlinear material laws and noisy observations would require their own evaluations.")
    history_plot = text(inverse[4]).replace('assets_dir() / "tiny_inverse_bar.png"', 'practical_dir / "tiny_inverse_bar.png"')
    # Re-evaluate only the plotted training metric at each recorded post-update
    # modulus. The recovery loop, optimizer, loss and fitted values are unchanged.
    history_plot = history_plot.replace(
        'history_array = np.array(history)',
        '''history_array = np.array(history)
training_rmse = []
with torch.no_grad():
    for fitted_modulus in history_array[:, 1]:
        responses = torch.stack([tip_displacement(torch.tensor(fitted_modulus), load) for load in train_loads])
        training_rmse.append(float((responses - observed_train).square().mean().sqrt()))''')
    history_plot = history_plot.replace('history_array[:, 2], label="training loss"',
                                        'training_rmse, label="training RMSE (4 loads)"')
    history_plot = history_plot.replace('label="validation absolute error"',
                                        'label="validation RMSE (1 load)"')
    history_plot = history_plot.replace('ylabel="error", title="Optimisation history"',
                                        'ylabel="Displacement RMSE [dimensionless]", title="Optimisation history"')
    history_plot = history_plot.replace('plt.subplots(1, 2, figsize=(10, 3.5)',
                                        'plt.subplots(1, 3, figsize=(14, 3.5)')
    history_plot = history_plot.replace('fig.savefig(', '''axes[2].plot(history_array[:, 0], history_array[:, 1], "o-", label="Recorded updated modulus")
axes[2].axhline(float(E_true), color="#d46b27", linestyle="--", label="Target modulus")
axes[2].set(xlabel="Iteration", ylabel="Modulus E [dimensionless]", title="Parameter recovery")
axes[2].legend(fontsize=9)
from day2_helpers.classroom_visuals import save_table
save_table([{"iteration": int(row[0]), "updated_modulus": float(row[1]),
             "pre_update_training_mse": float(row[2]), "training_rmse": rmse,
             "validation_rmse": float(row[3])} for row, rmse in zip(history_array, training_rmse)],
           practical_dir / "bar_recovery_history.csv")
np.savez_compressed(practical_dir / "bar_recovery_results.npz", loads=response_loads.numpy(),
                    target_response=true_response, recovered_response=fit_response,
                    recorded_history=history_array, matched_training_rmse=np.array(training_rmse),
                    E_true=float(E_true), E_fit=float(E_fit))
fig.savefig(''')
    history_plot = history_plot.replace('Toy elastic-bar response recovery and optimisation history.',
                                        'Elastic-bar response, matched training/validation displacement RMSE, and updated modulus across recovery.')
    lab.code(history_plot, folded=True, role="plotting")
    lab.md("""### Example outline · P2-R01 · Fracture inverse recovery

**Learning question:** Which fracture parameters can be recovered from specified observations?

**Planned content.** Extend the parameter–observation–loss sequence to a small fracture problem, with recovery histories and held-out observations. The elastic bar above supplies the current executable exercise.

### Animation storyboard · P2-A01 · Forward values and backward sensitivities

**Planned content.** Follow $E$, the stiffness matrix, tip displacement and scalar mismatch forwards, then follow the derivative backwards. Show the optimisation update as a separate final step.
""")
    exercise1 = {
        "id": "02-1", "title": "Derive two sensitivities", "kind": "conceptual",
        "question": r"For $g(d)=(1-\eta)(1-d)^2+\eta$, derive its slope and explain its sign. For the fixed-left bar, derive $u_{\mathrm{tip}}$ and $\partial u_{\mathrm{tip}}/\partial E$. How do these two gradients enter different computational graphs?",
        "hint": r"Differentiate the square in $g$. For the bar, use axial force balance and $u_{\mathrm{tip}}=FL/(EA)$.",
        "solution": r"The degradation slope is $g'(d)=-2(1-\eta)(1-d)$, which is negative for $d<1$ when $0\le\eta<1$: increased damage reduces stiffness. The bar has $u_{\mathrm{tip}}=FL/(EA)$ and $\partial u_{\mathrm{tip}}/\partial E=-FL/(AE^2)$: increased modulus reduces extension under a fixed load. The first derivative is local to a material law. The second passes through the assembled equilibrium solve. A coupled fracture sensitivity additionally includes the damage/history operations that connect the chosen parameter to the observable.",
        "source": "Adapted from source/book/solutions/02.json exercise 1 and 03.json exercise 1",
    }
    exercise2 = solutions(root, 3)["exercises"][1]
    exercise2.update(id="02-2", kind="practical")
    return lab.finish([
        "A scalar loss supplies a reverse seed; the chain rule converts local force sensitivities into input gradients.",
        "The degradation slope describes how local stiffness changes with damage.",
        "Autograd differentiates the finite-element solve connecting the modulus to tip displacement.",
        "Positive modulus recovery and a held-out load check the fitted linear-bar compliance.",
    ], [exercise1, exercise2])


def build_learning(root, detailed):
    learning = detailed[DETAILS[3]]["cells"]
    hybrid = detailed[DETAILS[4]]["cells"]
    lab = Lesson(root, NAMES[2], "Practical 3: Learn a field and assess its proposal",
                 "Train, save and reload a small field model, then assess its output against a discrete equation and apply a reference correction when needed.",
                 "How will tightening a residual tolerance affect the selected field and use of reference corrections?", DETAILS[3:5])
    lab.md(r"""## Physical motivation and model

A learned model can propose a field from coordinates and loading. A discrete equation then provides a second way to inspect that proposal. We practise this relationship using the course-owned **ToyHelmholtzProblem**, a smooth scalar-field model on a $25\times13$ grid:

$$d-\ell^2\nabla^2d=s(x,y,\lambda),\qquad d=0\text{ on the boundary}.$$

Here $d$ is a dimensionless scalar field, $\ell$ is its smoothing length, $s$ is a prescribed source and $\lambda$ is a load factor. Its discrete equation is $A\mathbf d=\mathbf b(\lambda)$. The helper exposes the matrix, source, reference solve and residual. These synthetic fields support teaching model interfaces and correction; applying a learned damage component to fracture requires the fracture-specific inputs, history and coupled residuals.

The workflow is **reference fields → training → saved model → proposal → residual check → selected field**.

## Step-by-step calculation

### Generate whole-load datasets

Each node supplies the row `[x/L, y/H, load_factor]` and one target field value. Keep complete load cases together when dividing training, validation and test data. [Inspect the existing toy and model helpers](https://github.com/CEMS-Lab/autumn-school/blob/main/notebooks/day2_helpers/course_tools.py).
""")
    lab.code('''
        from day2_helpers.course_tools import FEATURE_ORDER, TOY_INTERFACE_VERSION
        from day2_helpers.course_tools import TinyDamageMLP, ToyHelmholtzProblem, ToyDamageAdapter
        from day2_helpers.course_tools import load_toy_model, normalise_features
        torch.manual_seed(20260909)
        problem = ToyHelmholtzProblem()
        split_loads = {"train": tuple(np.linspace(.12, .76, 12)),
                       "validation": (.82, .88), "test": (.94, 1.00)}
        train_x, train_y = problem.case_tensor(split_loads["train"])
        val_x, val_y = problem.case_tensor(split_loads["validation"])
        test_x, test_y = problem.case_tensor(split_loads["test"])
        print({"features": tuple(train_x.shape), "targets": tuple(train_y.shape)})
    ''')
    lab.md("Inspect complete sample fields from the whole-load splits. Load changes the source amplitude in this teaching equation. Every panel uses the same 0–1 field scale; the NPZ retains the coordinates, split names, loads and shown fields.")
    lab.code('''
        from day2_helpers.classroom_visuals import toy_reference_samples, toy_initial_prediction
        from day2_helpers.classroom_visuals import training_snapshot, toy_training_history
        practical_dir = assets_dir() / "classroom" / "03"
        practical_dir.mkdir(parents=True, exist_ok=True)
        fig = toy_reference_samples(problem, split_loads, practical_dir)
        display_figure(fig, alt="Full toy reference fields at two training loads, a validation load and a test load on a common colour scale.")
        plt.close(fig)
    ''', folded=True, role="plotting")
    lab.md("### Define the neural model\n\nCompute the feature mean and scale from the training inputs. Reuse that transform for every split. `TinyDamageMLP` has two hidden layers of width 32 with SiLU activations and a scalar sigmoid output; print its structure to inspect the model.")
    lab.code('''
        mean = train_x.mean(dim=0)
        scale = train_x.std(dim=0).clamp_min(1.e-12)
        model = TinyDamageMLP(width=32).to(dtype=torch.float64)
        optimiser = torch.optim.Adam(model.parameters(), lr=1.5e-2)
        history = []
        print(model)
    ''')
    lab.md("Before training, compare the initial model prediction with one training reference field. The model and the source equation produce visibly different spatial patterns at this stage.")
    lab.code('''
        fig = toy_initial_prediction(problem, model, mean, scale, split_loads["train"][-1], practical_dir)
        display_figure(fig, alt="Training reference field and initial neural prediction at the same load and colour scale.")
        plt.close(fig)
    ''', folded=True, role="plotting")
    lab.md(r"""### Train with an inspectable gradient loop

The mean squared error is $\mathcal L=M^{-1}\sum_i(\widehat d_i-d_i)^2$ over the $M$ training rows. `loss.backward()` accumulates gradients of this scalar loss with respect to network weights; Adam updates them. Four snapshots record the training and validation losses. This is the existing 400-epoch teaching calculation.
""")
    lab.code('''
        training_started = time.perf_counter()
        for epoch in range(400):
            optimiser.zero_grad(set_to_none=True)
            prediction = model(normalise_features(train_x, mean, scale))
            loss = torch.mean((prediction - train_y) ** 2)
            loss.backward()
            optimiser.step()
            if epoch in {0, 24, 99, 399}:
                history.append(training_snapshot(epoch, loss, model, train_x, train_y, val_x, val_y, mean, scale))
        training_seconds = time.perf_counter() - training_started
    ''')
    lab.md("Read the four recorded snapshots at epochs 1, 25, 100 and 400. Both plotted errors use the same updated model weights. The CSV also retains the original pre-update training loss used by the optimiser; connected markers guide the eye between the four recorded points.")
    lab.code('''
        fig = toy_training_history(history, practical_dir)
        display_figure(fig, alt="Four matched post-update training and validation mean-squared field-error snapshots.")
        plt.close(fig)
    ''', folded=True, role="plotting")
    lab.md("Evaluate the held-out data after training. Separate test error, training time and validation history describe different parts of the calculation.")
    lab.code('''
        model.eval()
        with torch.no_grad():
            test_prediction = model(normalise_features(test_x, mean, scale))
            test_rmse = float(torch.sqrt(torch.mean((test_prediction - test_y) ** 2)))
        print({"test_rmse": test_rmse, "training_seconds": round(training_seconds, 2),
               "history": history})
    ''')
    lab.md("### Save the model with its input conventions\n\nA usable checkpoint stores architecture, weights, feature order, normalisation and data provenance. Expand the packaging cell to inspect every field. The training and prediction operations above remain unchanged by saving.")
    lab.code('''
        practical_dir = assets_dir() / "classroom" / "03"
        practical_dir.mkdir(parents=True, exist_ok=True)
        checkpoint_path = practical_dir / "tiny_damage_mlp.pt"
        metadata = {
            "interface_version": TOY_INTERFACE_VERSION, "architecture": "TinyDamageMLP",
            "width": model.width, "feature_order": list(FEATURE_ORDER),
            "feature_location": "node",
            "feature_units": ["dimensionless x/L", "dimensionless y/H", "dimensionless"],
            "output": "toy_damage_proposal at nodes; d=0 intact-like, d=1 saturated",
            "dtype": "float64", "device": "cpu", "mesh_signature": list(problem.mesh_signature),
            "normalisation_mean": mean.tolist(), "normalisation_scale": scale.tolist(),
            "splits": {key: [float(value) for value in values] for key, values in split_loads.items()},
            "data_provenance": "course-owned synthetic fields from the discrete ToyHelmholtzProblem",
            "seed": 20260909, "epochs": 400,
        }
        checkpoint = {"state_dict": model.state_dict(), "metadata": metadata, "history": history,
                      "metrics": {"test_rmse": test_rmse, "training_seconds": training_seconds}}
        torch.save(checkpoint, checkpoint_path)
        checkpoint_path.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2))
    ''', folded=True, role="export")
    lab.md("Reload a fresh model instance and compare predictions at load 1.00. Equal predictions check reconstruction from the checkpoint; reference-field error assesses approximation quality.")
    lab.code('''
        reloaded, reloaded_metadata = load_toy_model(checkpoint_path)
        heldout_load = 1.00
        heldout_features = problem.features(heldout_load)
        heldout_reference = problem.reference_field(heldout_load)
        with torch.no_grad():
            prediction_before = model(normalise_features(heldout_features, mean, scale)).squeeze(1)
            prediction_after = reloaded(normalise_features(heldout_features, mean, scale)).squeeze(1)
        reload_difference = float((prediction_before - prediction_after).abs().max())
        heldout_rmse = float((prediction_after - heldout_reference).square().mean().sqrt())
        assert reload_difference < 1.e-12 and heldout_rmse < .07
        print({"reload_difference": reload_difference, "heldout_rmse": heldout_rmse})
    ''')
    lab.md("Reload agreement checks the saved model; reference error measures its approximation. Keep those two questions separate in this compact table.")
    lab.code('''
        from IPython.display import HTML
        from day2_helpers.classroom_visuals import numeric_table_html, save_table
        reload_rows = [{"comparison": "Original vs reloaded: maximum difference", "value": reload_difference},
                       {"comparison": "Reloaded vs reference: held-out RMSE", "value": heldout_rmse}]
        save_table(reload_rows, practical_dir / "toy_reload_checks.csv")
        display(HTML(numeric_table_html(reload_rows, [("comparison", "Question"), ("value", "Field difference")],
                                       "Model reconstruction and held-out field quality")))
    ''')
    lab.md("### Additional comparison: a radial-basis predictor\n\nThe retained reference notebook also compares a radial-basis average using the same nodewise features. Run the following cell as part of the sequence; its prediction is used in the next figure. Its prediction and assumptions remain separate from the neural model.")
    lab.code(text(learning[4]), folded=True, role="advanced")
    lab.md("## Interpret the fields and correction\n\nInspect the complete reference, MLP and radial-basis fields together with the signed MLP error. Common field scales make their spatial differences visible.")
    lab.code(text(learning[5]).replace('assets_dir() / "tiny_mlp_heldout_field.png"', 'practical_dir / "tiny_mlp_heldout_field.png"'), folded=True, role="plotting")
    lab.md(r"""### Assess a compatible proposal

`ToyDamageAdapter` checks feature order, grid signature, input shape and finite values. Its proposal also respects the scalar bounds, boundary values and supplied previous state. The relative residual is

$$\rho=\frac{\|A\widehat{\mathbf d}-\mathbf b\|_2}{\|\mathbf b\|_2+10^{-15}}.$$

The gate accepts when $\rho\le0.30$. Otherwise it computes the direct toy reference correction. Here the previous state is the reference field at the lower load 0.82.
""")
    lab.code('''
        adapter = ToyDamageAdapter(reloaded, metadata, problem)
        load_factor = .94
        d_previous = problem.reference_field(.82)
        proposal = adapter.propose(problem.features(load_factor), d_previous=d_previous)
        assessment = adapter.assess(proposal, load_factor, residual_limit=.30)
        reference = problem.reference_field(load_factor)
        corrected = proposal if assessment["accepted"] else adapter.fallback(load_factor, d_previous)
        print({"assessment": assessment, "proposal_rmse": float((proposal-reference).square().mean().sqrt())})
        assert assessment["accepted"], assessment
    ''')
    lab.md("### Observe the reference-correction branch\n\nA controlled spatial perturbation provides a second proposal for the same equation and tolerance. Compare its residual with the reference correction's residual. This demonstration keeps the data, model and load fixed.")
    lab.code('''
        corrupted = torch.where(problem.boundary_mask, torch.zeros_like(proposal),
                                (proposal + .30 * torch.sin(12 * problem.coordinates[:, 0])).clamp(0, 1))
        rejected = adapter.assess(corrupted, load_factor, residual_limit=.30)
        fallback = adapter.fallback(load_factor, d_previous)
        fallback_residual = problem.relative_residual(fallback, load_factor)
        assert not rejected["accepted"], rejected
        assert fallback_residual < 1.e-10
        print({"perturbed_assessment": rejected, "fallback_residual": fallback_residual})
    ''')
    lab.md("Expand the optional interface checks to see how the adapter responds to permuted feature names and a non-finite input.")
    lab.code(text(hybrid[4]), folded=True, role="advanced")
    lab.md("Read the complete fields alongside the residuals. A proposal can look smooth and still differ from the discrete reference; the equation check adds information about that difference.")
    lab.code(text(hybrid[5]).replace('assets_dir() / "toy_adapter_fallback.png"', 'practical_dir / "toy_adapter_fallback.png"')
             .replace('label="toy field d"', 'label="field error" if ax is axes[3] else "toy field d"'),
             folded=True, role="plotting")
    lab.md("The result table links each field to its residual and selected action. In the saved NPZ, `proposal` is the model prediction, `selected` is the field returned by the acceptance check, and `fallback` is the reference solution used after rejection.")
    lab.code('''
        gate_rows = [{"case": "Compatible proposal", "residual": assessment["toy_relative_residual"], "action": "Accept"},
                     {"case": "Perturbed proposal", "residual": rejected["toy_relative_residual"], "action": "Reference correction"},
                     {"case": "Reference fallback", "residual": fallback_residual, "action": "Use reference solution"}]
        save_table(gate_rows, practical_dir / "toy_gate_results.csv")
        display(HTML(numeric_table_html(gate_rows, [("case", "Field"), ("residual", "Relative equation residual"),
                                                   ("action", "Selected action")], "Residual limit = 0.30")))
    ''')
    lab.code('''
        np.savez_compressed(practical_dir / "toy_review_fields.npz", coordinates=problem.coordinates.numpy(),
                            heldout_load=heldout_load, heldout_reference=heldout_reference.numpy(),
                            prediction_before=prediction_before.numpy(), prediction_after=prediction_after.numpy(),
                            rbf_prediction=rbf_prediction.detach().numpy(), proposal_load=load_factor,
                            previous=d_previous.numpy(), proposal=proposal.numpy(), reference=reference.numpy(),
                            perturbed=corrupted.numpy(), selected=corrected.numpy(), fallback=fallback.numpy())
    ''', folded=True, role="export")
    lab.md("The optional export records the two decisions. A later data-aggregation activity would additionally retain the model-visited inputs and reference target arrays, retrain, and evaluate a held-out rollout.")
    lab.code(text(hybrid[6]).replace('assets_dir() / "toy_adapter_replay_record.json"', 'practical_dir / "toy_adapter_replay_record.json"'), folded=True, role="export")
    lab.md("""### Example outline · P3-R01 · A fracture-compatible hybrid

**Learning question:** Which proposed fracture state can be accepted, and when is a coupled correction needed?

**Planned content.** Follow a learned damage proposal through a coupled fracture calculation, with its history inputs and corrected fields. The Helmholtz calculation above supplies the current executable demonstration.

### Animation storyboard · P3-A01 · Proposal, check and correction

**Planned content.** Show a model proposal, its residual assessment and the accepted or corrected field. Link this sequence to Lecture 3's conceptual data-aggregation loop, with reference labelling, retraining and held-out evaluation.
""")
    exercise1 = solutions(root, 4)["exercises"][0]
    exercise1["solution"] = exercise1["solution"].replace("The notebook's training helper computes", "The visible training loop computes")
    exercise1["solution"] += r" Here $z_i$ denotes the normalised feature row for training sample $i$, containing position and load."
    exercise1.update(id="03-1", kind="conceptual")
    exercise2 = solutions(root, 5)["exercises"][1]
    exercise2.update(id="03-2", kind="practical")
    return lab.finish([
        "Whole-load splits and training-only normalisation define the learning experiment.",
        "The visible loss and backward pass connect field mismatch to every trainable weight.",
        "Saved weights and input conventions reconstruct the same model prediction.",
        "The discrete toy residual guides proposal acceptance and checked reference correction.",
    ], [exercise1, exercise2])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output-root", type=Path, help="Destination repository root; defaults to --repo-root")
    args = parser.parse_args()
    root = args.repo_root.resolve()
    destination = (args.output_root or root).resolve() / "notebooks/classroom"
    detailed = read_details(root)
    notebooks = (build_simulation(root, detailed), build_gradients(root, detailed), build_learning(root, detailed))
    destination.mkdir(parents=True, exist_ok=True)
    for name, notebook in zip(NAMES, notebooks):
        path = destination / f"{name}.ipynb"
        path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
