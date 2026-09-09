"""Refresh teaching prose and rendered media while preserving retained FEM data.

The original rendering receipt is kept within the updated manifest. The
refreshed panel reuses its existing numerical payload byte for byte.
"""
import argparse
import base64
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / "interactive"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--rendered", type=Path, required=True,
                    help="New output directory from render_forward_cycle.py")
args = parser.parse_args()
manifest_path = PANEL / "history_plate_manifest.json"
previous = json.loads(manifest_path.read_text())
existing = (PANEL / "history_plate.html").read_text()
match = re.search(r'(<script id="panel-data" type="application/json">)(.*?)(</script>)',
                  existing, re.S)
if match is None:
    raise ValueError("The retained panel payload is missing.")
payload = match.group(2)
json.loads(payload)
rendered = sorted(args.rendered.iterdir())
expected = {"forward_cycle.mp4", "forward_cycle.png", "forward_cycle_manifest.json"}
expected.update(f"cycle_scene_{i}.png" for i in range(1, 9))
if {p.name for p in rendered} != expected:
    raise ValueError("The new animation must contain its movie, poster, eight scenes and receipt.")
template = (PANEL / "history_plate.template.html").read_text()
for marker in ("__PAYLOAD__", "__WALKTHROUGH__", "__CYCLE_MOVIE__", "__CYCLE_POSTER__"):
    if template.count(marker) != 1:
        raise ValueError(f"Expected one template marker: {marker}")
revised = template.replace("__PAYLOAD__", payload).replace(
    "__WALKTHROUGH__", (PANEL / "history_walkthrough.html").read_text())
for marker, name, mime in (
    ("__CYCLE_MOVIE__", "forward_cycle.mp4", "video/mp4"),
    ("__CYCLE_POSTER__", "forward_cycle.png", "image/png"),
):
    revised = revised.replace(marker, "data:" + mime + ";base64," +
                              base64.b64encode((args.rendered / name).read_bytes()).decode())
for source in rendered:
    shutil.copy2(source, PANEL / source.name)
(PANEL / "history_plate.html").write_text(revised)
current = deepcopy(previous)
current["prior_render_receipt"] = previous
current["editorial_refresh"] = {
    "date": "2026-09-09",
    "scope": "Academic prose and animation captions; retained numerical payload unchanged",
    "payload_sha256": hashlib.sha256(payload.encode()).hexdigest(),
    "numerical_execution": False,
    "renderer_input": "history_plate_arrays.npz",
}
for name in current["source_hashes"]:
    folder = ROOT / "code" if name.endswith(".py") else PANEL
    current["source_hashes"][name] = sha(folder / name)
current["source_hashes"][Path(__file__).name] = sha(Path(__file__))
current["outputs"] = {name: sha(PANEL / name) for name in previous["outputs"]}
current["cycle_animation"] = json.loads((PANEL / "forward_cycle_manifest.json").read_text())
manifest_path.write_text(json.dumps(current, indent=2) + "\n")
print("Refreshed panel and animation; numerical payload preserved.")
