"""Retain successful exact-source classroom executions and their provenance."""
import copy
import hashlib
import json
import platform
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parents[1]

def code_hash(notebook):
    code = [cell.source for cell in notebook.cells if cell.cell_type == "code"]
    return hashlib.sha256(json.dumps(code).encode()).hexdigest()

def main():
    (ROOT / "notebooks/executed").mkdir(parents=True, exist_ok=True)
    report = {"scope": "fresh local whole-notebook processes after setup; Colab rehearsal separate",
              "platform": platform.platform(), "python": platform.python_version(), "notebooks": []}
    for source in sorted((ROOT / "notebooks").glob("0[0-5]*.ipynb")):
        folder = ROOT / "runs" / source.stem
        receipt = json.loads((folder / "runtime.json").read_text())
        if receipt["status"] != "passed" or receipt["seconds"] >= 300:
            raise ValueError("A successful under-300-second run is required: " + source.name)
        authored = nbformat.read(source, 4)
        executed = nbformat.read(folder / source.name, 4)
        if code_hash(authored) != code_hash(executed):
            raise ValueError("Code changed since execution: " + source.name)
        if [c.cell_type for c in authored.cells] != [c.cell_type for c in executed.cells]:
            raise ValueError("Cell layout changed since execution: " + source.name)
        if any(out.output_type == "error" for cell in executed.cells for out in cell.get("outputs", [])):
            raise ValueError("Errored output: " + source.name)
        retained = copy.deepcopy(executed)
        for cell, prose in zip(retained.cells, authored.cells):
            if cell.cell_type == "markdown":
                cell.source = prose.source
        retained.metadata.update(authored.metadata)
        nbformat.write(retained, ROOT / "notebooks/executed" / source.name)
        nbformat.write(retained, source)
        report["notebooks"].append({
            "id": source.name[:2], "notebook": source.name,
            "aggregate_wall_seconds": receipt["seconds"],
            "code_sha256": code_hash(retained),
            "retained_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "status": receipt["status"], "limit_seconds": 300,
        })
    target = ROOT / "evidence/notebook_runtime_current.json"
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
