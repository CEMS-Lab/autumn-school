"""Validate retained inverse evidence within the combined September course edition."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "source/book/research"
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--refresh-manifest", action="store_true")
args = parser.parse_args()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
private = re.compile(r"/(?:Users|users|home|mnt/scratch)/|sharedscratch|codex://|"
                     r"-----BEGIN .*PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}")
texts = 0
for p in BASE.rglob("*"):
    if not p.is_file() or any(x in {"_build","__pycache__","_attachments"} for x in p.parts):
        continue
    if p.suffix in {".md",".py",".js",".cjs",".css",".json",".ipynb",".tex",".txt",".html"}:
        if private.search(p.read_text()):
            raise ValueError(f"Private path or credential marker: {p.relative_to(ROOT)}")
        texts += 1

visuals = BASE / "visuals"
inputs = json.loads((visuals/"input_manifest.json").read_text())["files"]
with zipfile.ZipFile(visuals/"retained_inputs.zip") as archive:
    assert set(archive.namelist()) == {"inputs/"+name for name in inputs}
    for name, digest in inputs.items():
        data = archive.read("inputs/"+name)
        assert hashlib.sha256(data).hexdigest() == digest, name
        if name.endswith(".json"):
            parsed = json.loads(data)
            assert not private.search(json.dumps(parsed)), name
verified = 0
for receipt_name in ("manifest.json","history_manifest.json"):
    receipt = json.loads((visuals/receipt_name).read_text())
    artifact_hashes = receipt["artifacts"] if "artifacts" in receipt else receipt["artifact_sha256"]
    for name,digest in artifact_hashes.items():
        assert sha(visuals/name) == digest, name
        verified += 1
history = json.loads((visuals/"history_manifest.json").read_text())
for name,digest in history["sources"].items():
    assert sha(BASE/"code"/name) == digest, name
assert all(history["checks"].values())
panel_dir = BASE / "interactive"
panel = json.loads((panel_dir/"history_plate_manifest.json").read_text())
panel_verified = 0
for name,digest in {**panel["source_hashes"],**panel["outputs"]}.items():
    folder = BASE/"code" if name.endswith(".py") else panel_dir
    assert sha(folder/name) == digest, name
    panel_verified += 1
assert panel["frames"] == 12 and panel["selected_frame_difference"] == 0
assert panel["float32_maximum_error"] < 3e-8
assert panel["cycle_animation"]["duration_seconds"] == 40
assert not panel["cycle_animation"]["new_forward_solve"]
notebook = json.loads((BASE/"notebooks/inverse_experiments.ipynb").read_text())
cells = [c for c in notebook["cells"] if c["cell_type"]=="code"]
assert len(cells)==16 and all(c.get("execution_count") is not None for c in cells)
assert not any(o.get("output_type")=="error" for c in cells for o in c.get("outputs",[]))
editorial = json.loads((BASE/"notebooks/prose_refresh_20260909.json").read_text())
for name, record in editorial["notebooks"].items():
    path = BASE/"notebooks"/name
    assert sha(path) == record["after_sha256"], name
    content = json.loads(path.read_text())
    for cell in content["cells"]:
        if cell["cell_type"] == "markdown":
            assert not re.search(r"(?m)^myst:|^\s*all_links_external:", "".join(cell["source"])), name
    retained = [cell for cell in content["cells"] if cell["cell_type"] == "code"]
    assert hashlib.sha256(json.dumps(retained, sort_keys=True).encode()).hexdigest() == record["retained_code_cells_sha256"], name
assert sha(BASE/"code/build_notebook.py") == editorial["generator_sha256"]
assert sha(panel_dir/"history_plate_arrays.npz") == panel["prior_render_receipt"]["outputs"]["history_plate_arrays.npz"]
report = {"scope":"Combined September web course: theme, course and inverse prose, current slides, and retained inverse numerical evidence",
          "date":"2026-09-09","retained_inverse_source_commit":"4c79cd6",
          "publication_base_commit":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
          "text_files_scanned":texts,"archive_inputs_verified":len(inputs),
          "visual_artifact_hashes_verified":verified,
          "history_primitive_checks":len(history["checks"]),
          "retained_interactive_source_commit":"bafb35e",
          "interactive_source_and_output_hashes_verified":panel_verified,
          "retained_plate_frames":panel["frames"],
          "algorithm_animation_seconds":40,
          "retained_notebook_cells":len(cells),
          "audit_runs_numerics":False,
          "inverse_numerical_execution":False,
          "inverse_code_and_outputs_preserved":True,
          "classroom_notebook_prose_updated":True,
          "slides_updated":True,
          "printable_book_delivery":"archived",
          "full_fracture_issue_7_closed":False,
          "private_paths_or_credential_markers_found":False}
(ROOT/"evidence/inverse_publication.json").write_text(json.dumps(report,indent=2)+"\n")
if args.refresh_manifest:
    raw = subprocess.check_output(["git","ls-files","--cached","--others","--exclude-standard","-z"],cwd=ROOT)
    names = sorted(set(n.decode() for n in raw.split(b"\0") if n))
    names = [n for n in names if n!="MANIFEST.json" and (ROOT/n).is_file()]
    for name in names:
        p=ROOT/name
        assert not p.is_symlink() and p.resolve().is_relative_to(ROOT), name
        assert not any(x in {".git",".build","reviews","jupyter_execute","_attachments"} for x in Path(name).parts), name
    manifest = json.loads((ROOT/"MANIFEST.json").read_text())
    manifest.update(version="main-20260909-combined-course",date="2026-09-09",
                    change_scope="Combined web course theme, academic prose, inverse extension, current slides and standalone differentiation lesson",
                    runtime_scope="Per-artifact local classroom and diffusion receipts, plus retained HPC inverse receipts; setup and execution evidence remain separate")
    manifest["files"]={name:sha(ROOT/name) for name in names}
    (ROOT/"MANIFEST.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(report,indent=2))
