"""Check the three-lab curation, retained outputs and classroom readability."""
import hashlib
import json
from pathlib import Path
import re
import runpy

import nbformat
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SUPPORT = runpy.run_path(str(ROOT / "source/book/scripts/build_lab_pages.py"))
NAMES = ("01_simulate_fracture", "02_gradients_and_recovery", "03_learning_and_hybrid")
report = {"scope": "source, retained-output, static HTML and result-array checks", "notebooks": []}
pointer_path = ROOT / "evidence/classroom_current.json"
pointer = json.loads(pointer_path.read_text()) if pointer_path.exists() else None
evidence_dir = ROOT / (pointer["evidence_dir"] if pointer else "evidence/classroom_runs_20260910")
if pointer:
    assert set(pointer["notebooks"]) == set(NAMES)
    assert hashlib.sha256((evidence_dir / "curation.json").read_bytes()).hexdigest() == pointer["curation_sha256"]

for name in NAMES:
    path = ROOT / "notebooks/classroom" / (name + ".ipynb")
    canonical = nbformat.read(path, 4)
    nbformat.validate(canonical)
    code = [c for c in canonical.cells if c.cell_type == "code"]
    visible = [c for c in code if "hide-input" not in c.metadata.get("tags", [])]
    max_lines = max(sum(bool(l.strip()) for l in c.source.splitlines()) for c in visible)
    assert max_lines <= 12, name
    assert sum(c.metadata.get("classroom_role") == "setup" for c in code) == 1
    setup = next(c for c in code if c.metadata.get("classroom_role") == "setup")
    assert "import google.colab" in setup.source and "git" in setup.source
    assert setup.metadata["cellView"] == "form" and setup.metadata["jupyter"]["source_hidden"]
    all_code = "\n".join(c.source for c in code)
    assert "assert session_seconds" not in all_code and "assert computation_seconds" not in all_code
    images = sum("image/png" in o.get("data", {}) for c in code for o in c.get("outputs", []))
    assert images >= 2, name
    for c in canonical.cells:
        if c.cell_type == "code":
            compile(c.source, name, "exec")
            assert not any(o.output_type == "error" for o in c.get("outputs", []))
        else:
            prose = re.sub(r"```[\s\S]*?```|`[^`]*`", "", c.source)
            assert len(re.findall(r"(?<!\\)\$", prose)) % 2 == 0, (name, c.id)
    fingerprint = SUPPORT["computational_fingerprint"](canonical)
    for folder in ("source/book/classroom", "notebooks/study/classroom", "notebooks/solutions/classroom"):
        variant = nbformat.read(ROOT / folder / path.name, 4)
        assert SUPPORT["computational_fingerprint"](variant) == fingerprint, folder
        prose = "\n".join(c.source for c in variant.cells if c.cell_type == "markdown")
        assert prose.count("## Key takeaways") == 1
        assert "### Exercise 1" in prose and "### Exercise 2" in prose
        if "/study/" in folder:
            assert all("solution" not in e and "hint" not in e for e in variant.metadata.classroom.exercises)
    receipt_path = evidence_dir / (name + ".json")
    receipt = json.loads(receipt_path.read_text())
    if pointer:
        assert hashlib.sha256(receipt_path.read_bytes()).hexdigest() == pointer["notebooks"][name]["receipt_sha256"]
        assert receipt["retained_sha256"] == pointer["notebooks"][name]["retained_sha256"]
    assert receipt["status"] == "passed" and 0 <= receipt["whole_process_seconds"] < 120
    assert receipt.get("under_120_seconds", True) is True
    assert hashlib.sha256(path.read_bytes()).hexdigest() == receipt["retained_sha256"]
    for relative, digest in receipt["support_sha256"].items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == digest
    html = (ROOT / "book/classroom" / (name + ".html")).read_text()
    assert "course-hint" in html and "course-solution" in html
    assert "hide-input" in html or "cell tag_hide-input" in html
    report["notebooks"].append({"name": name, "visible_code_cells": len(visible),
        "folded_code_cells": len(code) - len(visible), "maximum_visible_nonblank_lines": max_lines,
        "retained_figures": images, "whole_process_seconds": receipt["whole_process_seconds"],
        "under_120_seconds": True, "limit_seconds": 120})

# Reorganising the PhAST practical preserves its reference numerical fields.
for stem in ("tiny_notched_tension", "tiny_notched_tension_half_load"):
    before = ROOT / "assets/day2_forward" / (stem + "_fields.npz")
    after = ROOT / "assets/day2_forward/classroom/01" / before.name
    with np.load(before, allow_pickle=False) as old, np.load(after, allow_pickle=False) as new:
        assert set(old.files) == set(new.files)
        for key in old.files:
            np.testing.assert_array_equal(old[key], new[key])

register = (ROOT / "source/planning/PLACEHOLDER_REGISTER.md").read_text()
registered = set(re.findall(r"^## ([LP][1-3]-[ARW]\d{2})", register, re.M))
presented = set()
for guide in (ROOT / "source/book/lectures").glob("*.md"):
    presented.update(re.findall(r"\b[LP][1-3]-[ARW]\d{2}\b", guide.read_text()))
for name in NAMES:
    notebook = nbformat.read(ROOT / "notebooks/classroom" / (name + ".ipynb"), 4)
    for c in notebook.cells:
        if c.cell_type == "markdown":
            presented.update(re.findall(r"\b[LP][1-3]-[ARW]\d{2}\b", c.source))
assert presented == registered and len(registered) == 21
report.update(placeholder_slots=21, preserved_reference_arrays="exact match", result="passed")
print(json.dumps(report, indent=2))
