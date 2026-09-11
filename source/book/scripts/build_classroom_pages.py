"""Publish retained executions of the three curated classroom notebooks.

This command checks code and helper provenance and creates reading/download
variants. It performs no numerical execution and preserves every code output.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import runpy

import nbformat

ROOT = Path(__file__).resolve().parents[3]
SUPPORT = runpy.run_path(str(ROOT / "source/book/scripts/build_lab_pages.py"))
NAMES = ("01_simulate_fracture", "02_gradients_and_recovery", "03_learning_and_hybrid")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-dir", type=Path, help="Directory containing the three checked receipts and executed/ copies")
    args = parser.parse_args()
    pointer_path = ROOT / "evidence/classroom_current.json"
    selected = args.evidence_dir
    if selected is None and pointer_path.exists():
        selected = Path(json.loads(pointer_path.read_text())["evidence_dir"])
    evidence_dir = (ROOT / selected).resolve() if selected is not None else ROOT / "evidence/classroom_runs_20260910"
    destination = evidence_dir / "executed" if selected is not None else ROOT / "notebooks/executed/classroom"
    report = {"scope": "three classroom notebooks; retained local executions",
              "notebooks": []}
    for name in NAMES:
        source_path = ROOT / "notebooks/classroom" / (name + ".ipynb")
        executed_path = destination / source_path.name
        if not executed_path.exists():
            executed_path = source_path
        receipt_path = evidence_dir / (name + ".json")
        authored = nbformat.read(source_path, 4)
        executed = nbformat.read(executed_path, 4)
        receipt = json.loads(receipt_path.read_text())
        code = [c.source for c in authored.cells if c.cell_type == "code"]
        if (receipt["status"] != "passed" or not 0 <= receipt["whole_process_seconds"] < 120
                or receipt.get("under_120_seconds", True) is not True):
            raise ValueError("A passing complete execution below 120 seconds is required: " + name)
        if hashlib.sha256(json.dumps(code).encode()).hexdigest() != receipt["code_sha256"]:
            raise ValueError("Execution receipt has different code: " + name)
        if [c.source for c in executed.cells if c.cell_type == "code"] != code:
            raise ValueError("Executed code differs: " + name)
        expected_execution = receipt["retained_sha256"] if executed_path == source_path else receipt["executed_sha256"]
        if digest(executed_path) != expected_execution:
            raise ValueError("Executed outputs differ from receipt: " + name)
        for relative, expected in receipt["support_sha256"].items():
            if digest(ROOT / relative) != expected:
                raise ValueError("Supporting source changed after execution: " + relative)
        if len(authored.cells) != len(executed.cells):
            raise ValueError("Cell layout differs: " + name)
        content = copy.deepcopy(executed)
        for cell, original in zip(content.cells, authored.cells):
            if cell.cell_type != original.cell_type:
                raise ValueError("Cell type differs: " + name)
            cell.metadata = copy.deepcopy(original.metadata)
            if cell.cell_type == "markdown":
                cell.source = original.source
        info = authored.metadata.classroom
        if len(info.exercises) != 2 or not 3 <= len(info.takeaways) <= 4:
            raise ValueError("Each classroom lab needs two exercises and 3–4 takeaways")
        for cell in content.cells:
            if cell.cell_type == "code" and "hide-input" not in cell.metadata.get("tags", []):
                if len([line for line in cell.source.splitlines() if line.strip()]) > 12:
                    raise ValueError("Visible cell exceeds 12 lines: " + name)
        content.cells = [c for c in content.cells if not c.metadata.get("classroom_exercise")]
        fingerprint = SUPPORT["computational_fingerprint"](executed)
        for surface, answers, book in (("book", True, True), ("study", False, False),
                                       ("solutions", True, False)):
            variant = copy.deepcopy(content)
            if book:
                colab = ("https://colab.research.google.com/github/CEMS-Lab/autumn-school/"
                         "blob/main/notebooks/study/classroom/" + name + ".ipynb")
                variant.cells[0].source = (
                    f"# {info.title}\n\n**Learning objective.** {info.objective}\n\n"
                    f"**Predict first.** {info.prediction}\n\n"
                    '<div class="badge-row">\n'
                    f'<a class="badge-colab" href="{colab}"><img src="../_static/colab-badge.svg" alt="Open in Colab"/></a>\n'
                    f'<a class="badge-link" href="../../notebooks/study/classroom/{name}.ipynb">Download Practice Notebook</a>\n'
                    f'<a class="badge-link" href="../../notebooks/solutions/classroom/{name}.ipynb">Download with Worked Solutions</a>\n'
                    '<a class="badge-link" href="../../SETUP.md">Environment Setup</a>\n</div>\n\n'
                    'Work through the cells in order. Expand setup and figure details when you want to inspect the complete implementation.\n'
                )
                variant.metadata["mystnb"] = {"execution_mode": "off"}
                folder = ROOT / "source/book/classroom"
            else:
                folder = ROOT / "notebooks" / surface / "classroom"
                if not answers:
                    variant.metadata.classroom.exercises = [
                        {key: value for key, value in ex.items() if key not in {"hint", "solution"}}
                        for ex in info.exercises
                    ]
            # Put exercises before the further-study and runtime notes.
            insertion = next((i for i, c in enumerate(variant.cells)
                              if c.cell_type == "markdown" and c.source.startswith("## Continue studying")),
                             len(variant.cells))
            solutions_url = f"https://cems-lab.github.io/autumn-school/notebooks/solutions/classroom/{name}.ipynb"
            variant.cells[insertion:insertion] = SUPPORT["exercise_cells"](info, answers, myst=book, solutions_url=solutions_url)
            for cell in variant.cells:
                if any(any(mime in out.get("data", {}) for mime in ("image/png", "image/gif"))
                       for out in cell.get("outputs", [])):
                    cell.metadata["mystnb"] = {"image": {"alt": "Computed field or curve from " + info.title}}
            if SUPPORT["computational_fingerprint"](variant) != fingerprint:
                raise ValueError("A publication variant changed code or outputs: " + name)
            SUPPORT["stable_cell_ids"](variant, "classroom/" + name, surface)
            nbformat.validate(variant)
            folder.mkdir(parents=True, exist_ok=True)
            nbformat.write(variant, folder / source_path.name)
        report["notebooks"].append({
            "name": name, "whole_process_seconds": receipt["whole_process_seconds"],
            "under_120_seconds": True, "limit_seconds": 120,
            "source_sha256": digest(source_path), "code_sha256": receipt["code_sha256"],
            "code_and_outputs_sha256": fingerprint, "download_parity": True,
            "visible_cell_limit": 12, "execution_receipt": str(receipt_path.relative_to(ROOT)),
        })
    report_path = evidence_dir / "curation.json" if selected is not None else ROOT / "evidence/classroom_curation_20260910.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    if selected is not None:
        # Promote only a complete, hash-checked three-notebook edition.
        pointer = {"evidence_dir": str(evidence_dir.relative_to(ROOT)),
                   "curation_sha256": digest(report_path), "notebooks": {}}
        for name in NAMES:
            receipt_path = evidence_dir / (name + ".json")
            receipt = json.loads(receipt_path.read_text())
            source_path = ROOT / "notebooks/classroom" / (name + ".ipynb")
            if digest(source_path) != receipt["retained_sha256"]:
                raise ValueError("Canonical outputs must be retained before promoting this edition: " + name)
            pointer["notebooks"][name] = {"retained_sha256": receipt["retained_sha256"],
                                           "receipt_sha256": digest(receipt_path)}
        pointer_path.write_text(json.dumps(pointer, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
