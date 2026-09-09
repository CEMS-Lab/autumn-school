"""Render-ready notebook chapters from reviewed computations and original solutions.

This authoring step never executes Python cells or changes their code/outputs.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

import nbformat

BOOK = Path(__file__).resolve().parents[1]
ROOT = next(
    (base for base in BOOK.parents
     if (base / "notebooks").is_dir() and (base / "vendor").is_dir()),
    BOOK.parent,
)
NAMES = (
    "00_why_average_predictions_can_fail",
    "01_phast_tiny_evolving_fracture",
    "02_degradation_autograd",
    "03_tiny_derivative_inverse_toy",
    "04_train_save_reload_adapter",
    "05_hybrid_reference_correction",
)


def computational_fingerprint(notebook) -> str:
    payload = [
        {"source": cell.source, "outputs": cell.get("outputs", []),
         "execution_count": cell.get("execution_count")}
        for cell in notebook.cells if cell.cell_type == "code"
    ]
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def exercise_cells(material: dict, answers: bool, myst: bool = True):
    cells = [nbformat.v4.new_markdown_cell(
        "## Exercises\n\nTry each question before opening the hint or worked solution. "
        "Keep the original calculation as your reference."
    )]
    for number, exercise in enumerate(material["exercises"], 1):
        cells.append(nbformat.v4.new_markdown_cell(
            f"### Exercise {number}: {exercise['title']}\n\n{exercise['question']}"
        ))
        if answers:
            for key, label in (("hint", "Hint"), ("solution", "Worked solution")):
                if myst:
                    text = (f"::::{{admonition}} {label} {number}\n"
                            f":class: dropdown course-{key}\n\n{exercise[key]}\n::::")
                else:
                    # Jupyter Markdown does not interpret MyST directives.
                    text = f"#### {label} {number}\n\n{exercise[key]}"
                cells.append(nbformat.v4.new_markdown_cell(text))
    return cells


def main():
    for folder in (BOOK / "labs", ROOT / "notebooks/study", ROOT / "notebooks/solutions"):
        folder.mkdir(parents=True, exist_ok=True)
    runtime_path = ROOT / "reviews/notebook_runtime.json"
    if not runtime_path.exists():
        runtime_path = ROOT / "evidence/notebook_runtime.json"
    runtime = json.loads(runtime_path.read_text())
    measured = {item["id"]: item["aggregate_wall_seconds"] for item in runtime["notebooks"]}
    teaser_path = runtime_path.parent / "teaser_runtime.json"
    teaser = json.loads(teaser_path.read_text())
    measured["00"] = teaser["notebook"]["aggregate_wall_seconds"]
    report = {"execution": "none; preserved reviewed code and outputs", "lessons": []}
    for name in NAMES:
        identifier = name[:2]
        source = ROOT / "notebooks/executed" / (name + ".ipynb")
        if not source.exists():
            source = ROOT / "notebooks" / (name + ".ipynb")
        original = nbformat.read(source, as_version=4)
        nbformat.validate(original)
        if any(out.output_type == "error" for cell in original.cells
               for out in cell.get("outputs", [])):
            raise ValueError("Cannot publish an errored notebook: " + name)
        material = json.loads((BOOK / "solutions" / (identifier + ".json")).read_text())
        material["title"] = re.sub(r"^\d{2}\s*[—-]\s*", "", material["title"])
        if len(material["exercises"]) < 2:
            raise ValueError("Each lesson needs at least two worked exercises")
        for exercise in material["exercises"]:
            for key in ("title", "question", "hint", "solution"):
                if not exercise.get(key, "").strip():
                    raise ValueError("Incomplete exercise: " + name + "/" + key)
        content = copy.deepcopy(original)
        initial = content.cells.pop(0)
        assert initial.cell_type == "markdown"
        introduction = re.sub(r"^# [^\n]+\n+", "", initial.source, count=1)
        heading = (
            f"# {material['title']}\n\n"
            f"**Learning objective.** {material['objective']}\n\n"
            f"**Predict first.** {material['prediction']}\n\n"
            f"**Recorded computation:** {measured[identifier]:.3f} seconds on the "
            "reference local CPU after setup. This is not a fresh Colab timing.\n\n"
            "Read the code and its recorded outputs in order. To change inputs and "
            "run Python, download a notebook and use the course environment. "
            "The static book does not execute these cells in the browser.\n\n"
        )
        book_links = (
            f"[Download practice notebook](../../notebooks/study/{name}.ipynb) · "
            f"[Download with worked solutions](../../notebooks/solutions/{name}.ipynb) · "
            "[Environment setup](../../SETUP.md)\n\n"
        )
        notebook_links = f"[Read this lesson in the book](../../book/labs/{name}.html)\n\n"
        book_notebook = copy.deepcopy(content)
        book_notebook.cells.insert(0, nbformat.v4.new_markdown_cell(heading + book_links + introduction))
        book_notebook.cells += exercise_cells(material, answers=True)
        book_notebook.metadata["mystnb"] = {"execution_mode": "off"}
        # The first code cell is reproducible environment/plot setup.
        first_code = next(cell for cell in book_notebook.cells if cell.cell_type == "code")
        first_code.metadata["tags"] = list(set(first_code.metadata.get("tags", []) + ["hide-input"]))
        for cell in book_notebook.cells:
            if any("image/png" in out.get("data", {}) for out in cell.get("outputs", [])):
                cell.metadata["mystnb"] = {
                    "image": {"alt": f"Recorded figure from {material['title']}"}
                }
        for kind, answers in (("study", False), ("solutions", True)):
            downloadable = copy.deepcopy(content)
            downloadable.cells.insert(0, nbformat.v4.new_markdown_cell(heading + notebook_links + introduction))
            downloadable.cells += exercise_cells(material, answers, myst=False)
            if computational_fingerprint(downloadable) != computational_fingerprint(original):
                raise AssertionError("Download computation changed")
            nbformat.write(downloadable, ROOT / "notebooks" / kind / (name + ".ipynb"))
        if computational_fingerprint(book_notebook) != computational_fingerprint(original):
            raise AssertionError("Published computation changed")
        nbformat.write(book_notebook, BOOK / "labs" / (name + ".ipynb"))
        report["lessons"].append({
            "name": name,
            "code_and_outputs_sha256": computational_fingerprint(original),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "exercises": len(material["exercises"]),
            "code_cells": sum(c.cell_type == "code" for c in original.cells),
            "recorded_seconds": measured[identifier],
            "code_and_output_parity": True,
        })
    (ROOT / "reviews").mkdir(exist_ok=True)
    (ROOT / "reviews/integrated_notebook_parity.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
