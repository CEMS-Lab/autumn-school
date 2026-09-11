"""Render-ready notebook chapters from reviewed computations and original solutions.

This authoring step never executes Python cells or changes their code/outputs.

Course material prepared by Allamaprabhu Ani and Sathiskumar A. Ponnusami,
CEMS-Lab, UKACM Autumn School 2026. Attribution does not replace bundled licences.
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
COURSE_ATTRIBUTION = {
    "creator": "Allamaprabhu Ani",
    "prepared_by": ["Allamaprabhu Ani", "Sathiskumar A. Ponnusami"],
    "affiliation": "CEMS-Lab",
    "course": "UKACM Autumn School 2026",
}


def computational_fingerprint(notebook) -> str:
    payload = [
        {"source": cell.source, "outputs": cell.get("outputs", []),
         "execution_count": cell.get("execution_count")}
        for cell in notebook.cells if cell.cell_type == "code"
    ]
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def stable_cell_ids(notebook, name: str, surface: str):
    for index, cell in enumerate(notebook.cells):
        cell.id = hashlib.sha256(f"{name}:{surface}:{index}:{cell.source}".encode()).hexdigest()[:16]


def exercise_cells(material: dict, answers: bool, myst: bool = True, solutions_url: str | None = None):
    if answers:
        introduction = "Try each question before opening the hint or worked solution."
    elif solutions_url:
        introduction = f"Try each question, then use the [notebook with worked solutions]({solutions_url}) for hints and worked answers."
    else:
        introduction = "Try each question, then use the worked-solutions download at the top of this notebook for hints and worked answers."
    cells = [nbformat.v4.new_markdown_cell(
        "## Exercises\n\n" + introduction + " Keep the original calculation as your reference."
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
                    text = (f"<details><summary>{label} {number}</summary>\n\n"
                            f"{exercise[key]}\n\n</details>")
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
    current_path = ROOT / "evidence/notebook_runtime_current.json"
    current_runs = {}
    if current_path.exists():
        current_runs = {item["id"]: item for item in json.loads(current_path.read_text())["notebooks"]}
    report = {"execution": "none; preserved reviewed code and outputs", "lessons": []}
    for name in NAMES:
        identifier = name[:2]
        authored_path = ROOT / "notebooks" / (name + ".ipynb")
        authored = nbformat.read(authored_path, as_version=4)
        nbformat.validate(authored)
        if identifier in current_runs:
            code = [cell.source for cell in authored.cells if cell.cell_type == "code"]
            digest = hashlib.sha256(json.dumps(code).encode()).hexdigest()
            if digest != current_runs[identifier]["code_sha256"]:
                raise ValueError("Runtime receipt differs from authored code: " + name)
            measured[identifier] = current_runs[identifier]["aggregate_wall_seconds"]
        source = ROOT / "notebooks/executed" / (name + ".ipynb")
        if not source.exists():
            source = authored_path
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
        # Use the current authored explanation alongside retained computations.
        # A changed code cell requires a new execution before these can be paired.
        if [cell.cell_type for cell in content.cells] != [
            cell.cell_type for cell in authored.cells
        ]:
            raise ValueError("Authored/executed cell layout differs: " + name)
        for cell, authored_cell in zip(content.cells, authored.cells):
            if cell.cell_type == "code" and cell.source != authored_cell.source:
                raise ValueError("Authored/executed code differs; rerun notebook: " + name)
            if cell.cell_type == "markdown":
                cell.source = authored_cell.source
        # Standard notebook metadata stays out of the rendered lesson body.
        content.metadata.pop("presenter", None)
        content.metadata.update(COURSE_ATTRIBUTION)
        initial = content.cells.pop(0)
        assert initial.cell_type == "markdown"
        introduction = re.sub(r"^# [^\n]+\n+", "", initial.source, count=1)
        # Action links and objectives are generated consistently for each surface.
        introduction = re.sub(r"^\*\*Learning [Oo]bjective[.:]?\*\*[^\n]*\n+", "", introduction, flags=re.M)
        introduction = re.sub(r"^\[!?\[?.*(?:[Oo]pen [Ii]n Colab|[Dd]ownload practice|[Dd]ownload with worked|[Ee]nvironment [Ss]etup|[Rr]ead this lesson).*\n*", "", introduction, flags=re.M)
        heading = (
            f"# {material['title']}\n\n"
            f"**Learning objective.** {material['objective']}\n\n"
            f"**Predict first.** {material['prediction']}\n\n"
            "Follow the worked calculation, then use the downloadable notebook "
            "to explore the exercises.\n\n"
        )
        colab = f"https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/{name}.ipynb"
        book_links = (
            '<div class="badge-row">\n'
            f'<a class="badge-colab" href="{colab}"><img src="../_static/colab-badge.svg" alt="Open in Colab"/></a>\n'
            f'<a class="badge-link" href="../../notebooks/study/{name}.ipynb">Download Practice Notebook</a>\n'
            f'<a class="badge-link" href="../../notebooks/solutions/{name}.ipynb">Download with Worked Solutions</a>\n'
            '<a class="badge-link" href="../../SETUP.md">Environment Setup</a>\n'
            '</div>\n\n'
        )
        public = "https://cems-lab.github.io/autumn-school"
        notebook_links = (
            f"[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab})\n\n"
            f"[Download practice notebook]({public}/notebooks/study/{name}.ipynb) · "
            f"[Download with worked solutions]({public}/notebooks/solutions/{name}.ipynb) · "
            f"[Environment setup]({public}/SETUP.md) · "
            f"[Read this lesson in the book]({public}/book/labs/{name}.html)\n\n"
        )
        takeaways = material.get("takeaways", [])
        if not 3 <= len(takeaways) <= 4:
            raise ValueError("Each lesson needs three or four key takeaways: " + name)
        content.cells = [cell for cell in content.cells
                         if not (cell.cell_type == "markdown" and
                                 cell.source.startswith("## Key takeaways"))]
        content.cells.append(nbformat.v4.new_markdown_cell(
            "## Key takeaways\n\n" + "\n".join("- " + item for item in takeaways)))
        book_notebook = copy.deepcopy(content)
        book_notebook.cells.insert(0, nbformat.v4.new_markdown_cell(heading + book_links + introduction))
        book_notebook.cells += exercise_cells(material, answers=True)
        book_notebook.metadata["mystnb"] = {"execution_mode": "off"}
        # The first code cell is reproducible environment/plot setup.
        first_code = next(cell for cell in book_notebook.cells if cell.cell_type == "code")
        first_code.metadata["tags"] = sorted(set(first_code.metadata.get("tags", []) + ["hide-input"]))
        for cell in book_notebook.cells:
            if any("image/png" in out.get("data", {}) for out in cell.get("outputs", [])):
                cell.metadata["mystnb"] = {
                    "image": {"alt": f"Figure from {material['title']}"}
                }
        for kind, answers in (("study", False), ("solutions", True)):
            downloadable = copy.deepcopy(content)
            downloadable.cells.insert(0, nbformat.v4.new_markdown_cell(heading + notebook_links + introduction))
            downloadable.cells += exercise_cells(material, answers, myst=False)
            if computational_fingerprint(downloadable) != computational_fingerprint(original):
                raise AssertionError("Download computation changed")
            stable_cell_ids(downloadable, name, kind)
            nbformat.write(downloadable, ROOT / "notebooks" / kind / (name + ".ipynb"))
        if computational_fingerprint(book_notebook) != computational_fingerprint(original):
            raise AssertionError("Published computation changed")
        stable_cell_ids(book_notebook, name, "book")
        nbformat.write(book_notebook, BOOK / "labs" / (name + ".ipynb"))
        report["lessons"].append({
            "name": name,
            "code_and_outputs_sha256": computational_fingerprint(original),
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "prose_source_sha256": hashlib.sha256(authored_path.read_bytes()).hexdigest(),
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
