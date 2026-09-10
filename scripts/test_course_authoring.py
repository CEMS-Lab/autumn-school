"""Regression tests for preserved notebook anatomy and enforced design checks."""
import hashlib
import json
import re
from pathlib import Path
import runpy
import tempfile
from types import SimpleNamespace
import unittest

import nbformat
from sphinx.errors import SphinxError

ROOT = Path(__file__).resolve().parents[1]
SUPPORT = runpy.run_path(str(ROOT / "source/book/scripts/build_lab_pages.py"))
CHECK = runpy.run_path(str(ROOT / "scripts/check_design_directives.py"))["check_directives"]

class AuthoringTests(unittest.TestCase):
    def test_source_math_delimiters(self):
        def check(text, label):
            # Code examples may contain literal dollars; prose uses paired math delimiters.
            prose = re.sub(r"```[\s\S]*?```", "", text)
            prose = re.sub(r"`[^`]*`", "", prose)
            dollars = re.findall(r"(?<!\\)\$", prose)
            self.assertEqual(len(dollars) % 2, 0, label)
            self.assertNotIn("569Xa", prose, label)

        for name in SUPPORT["NAMES"]:
            notebook = nbformat.read(ROOT / "notebooks" / (name + ".ipynb"), 4)
            for index, cell in enumerate(notebook.cells):
                if cell.cell_type == "markdown":
                    check(cell.source, f"{name}: markdown cell {index}")
            data = json.loads((ROOT / "source/book/solutions" / (name[:2] + ".json")).read_text())
            for index, exercise in enumerate(data["exercises"]):
                for field, text in exercise.items():
                    check(text, f"{name}: exercise {index + 1}, {field}")
            for field in ("title", "objective", "prediction"):
                check(data[field], f"{name}: {field}")
            for text in data["takeaways"]:
                check(text, f"{name}: takeaway")

    def test_downloads_preserve_computation_and_anatomy(self):
        for name in SUPPORT["NAMES"]:
            canonical = nbformat.read(ROOT / "notebooks" / (name + ".ipynb"), 4)
            fingerprint = SUPPORT["computational_fingerprint"](canonical)
            for directory in ("source/book/labs", "notebooks/study", "notebooks/solutions"):
                notebook = nbformat.read(ROOT / directory / (name + ".ipynb"), 4)
                self.assertEqual(SUPPORT["computational_fingerprint"](notebook), fingerprint)
                prose = "\n".join(c.source for c in notebook.cells if c.cell_type == "markdown")
                self.assertEqual(prose.count("## Key takeaways"), 1)
                for phrase in ("Learning objective", "colab.research.google.com", "Environment", "### Exercise 1", "### Exercise 2"):
                    self.assertIn(phrase.lower(), prose.lower())
                self.assertIn("assets_dir", next(c.source for c in notebook.cells if c.cell_type == "code"))

    def test_cell_ids_are_stable(self):
        notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell("## Example")])
        SUPPORT["stable_cell_ids"](notebook, "example", "book")
        first = notebook.cells[0].id
        SUPPORT["stable_cell_ids"](notebook, "example", "book")
        self.assertEqual(first, notebook.cells[0].id)

    def test_empty_book_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertFalse(CHECK(Path(folder))[0])

    def test_missing_tutorials_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            (path / "index.html").write_text("<h1>Example</h1>")
            passed, errors, _ = CHECK(path)
            self.assertFalse(passed)
            self.assertTrue(any("six core tutorials" in error for error in errors))

    def test_sphinx_hook_stops_invalid_build(self):
        conf = runpy.run_path(str(ROOT / "source/book/conf.py"))
        with tempfile.TemporaryDirectory() as folder:
            app = SimpleNamespace(outdir=folder, builder=SimpleNamespace(format="html"))
            with self.assertRaises(SphinxError):
                conf["_verify_design_directives"](app, None)

if __name__ == "__main__":
    unittest.main()
