"""Inline the maintained setup cell into canonical notebooks before execution."""
from pathlib import Path
import nbformat

ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP = Path(__file__).with_name("colab_bootstrap.py").read_text()
TEASER_SETUP = '''
import platform
from torch import nn
from torch.nn import functional as F
torch.manual_seed(20260909)
torch.set_num_threads(1)
# Preserve the original model-initialisation convention; calculations use float64.
torch.set_default_dtype(torch.float32)
dtype = torch.float64
ASSETS = COURSE_ROOT / "assets/teaser"
ASSETS.mkdir(parents=True, exist_ok=True)
'''

def sync(identifiers=("00", "02", "03", "04", "05")):
    for identifier in identifiers:
        if identifier == "01":
            raise ValueError("Regenerate lesson 01 with build_forward_practical.py to retain its forward-specific setup.")
        path = next((ROOT / "notebooks").glob(identifier + "*.ipynb"))
        notebook = nbformat.read(path, 4)
        cell = next(cell for cell in notebook.cells if cell.cell_type == "code")
        source = BOOTSTRAP + (TEASER_SETUP if identifier == "00" else "")
        if cell.source != source:
            cell.source = source
            for computational_cell in notebook.cells:
                if computational_cell.cell_type == "code":
                    computational_cell.outputs = []
                    computational_cell.execution_count = None
            nbformat.write(notebook, path)
            print("Updated setup; fresh execution required:", path.name)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lessons", nargs="+", default=["00", "02", "03", "04", "05"])
    sync(parser.parse_args().lessons)
