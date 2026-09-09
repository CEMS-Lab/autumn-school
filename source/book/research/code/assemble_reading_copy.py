"""Embed verified retained figures without claiming a fresh notebook execution."""
import ast
import base64
import hashlib
import json
from pathlib import Path
import nbformat

root = Path(__file__).resolve().parents[1]
current = root / 'notebooks/inverse_experiments.ipynb'
if current.exists() and nbformat.read(current, as_version=4).metadata.get('provenance', {}).get('status') == 'HPC executed':
    raise RuntimeError('Preserve the verified HPC notebook; this legacy retained-output assembler is not a replacement.')
source = root / "notebooks/inverse_experiments_source.ipynb"
notebook = nbformat.read(source, as_version=4)
receipt = json.loads((root / "data/rendering_receipt.json").read_text())
assert hashlib.sha256((root / "data/teaching_results.json").read_bytes()).hexdigest() == receipt["data_sha256"]
status = """## Execution status of this reading copy

The seven displayed plots are verified retained outputs from the preceding
HPC teaching calculations and their recorded figure renderer. The complete
notebook's fresh top-to-bottom HPC execution is pending. Blank execution
counts are intentional: the retained images do not certify execution of this
assembled notebook. All numerical and plotting code is included below.
"""
notebook.cells.insert(1, nbformat.v4.new_markdown_cell(status))
count = 0
for cell in notebook.cells:
    if cell.cell_type != "code":
        continue
    for node in ast.parse(cell.source).body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "save":
            name = ast.literal_eval(node.value.args[1])
            image = root / "figures" / (name + ".png")
            sha = hashlib.sha256(image.read_bytes()).hexdigest()
            assert sha == receipt["figure_sha256"][image.name]
            cell.outputs = [nbformat.v4.new_output("display_data",
                data={"image/png": base64.b64encode(image.read_bytes()).decode()},
                metadata={"provenance": {"kind": "retained figure; not fresh cell execution",
                                        "sha256": sha}})]
            count += 1
assert count == 7
notebook.metadata.provenance.update(
    status="retained-output reading copy; fresh whole-notebook execution pending",
    input_notebook_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    retained_data_sha256=receipt["data_sha256"],
    retained_renderer_sha256=receipt["renderer_sha256"])
nbformat.write(notebook, root / "notebooks/inverse_experiments.ipynb")
print("Embedded seven hash-verified retained plots; execution remains pending.")
