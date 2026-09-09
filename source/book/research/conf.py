"""Isolated authoring preview. The main course owns its publication config."""

project = "PhAST inverse experiments: research teaching extension"
author = "CEMS-Lab"
extensions = ["myst_nb", "sphinx_immaterial"]
myst_enable_extensions = ["amsmath", "colon_fence", "deflist", "dollarmath"]
nb_execution_mode = "off"
master_doc = "index"
exclude_patterns = ["_build", "README.md", "REVIEW_STATUS.md", "notebooks/inverse_experiments_source.ipynb"]
html_theme = "sphinx_immaterial"
html_title = project
html_static_path = ["../../../book/_static", "_static"]
html_css_files = ["research.css"]
html_js_files = ["answers.js"]
mathjax_path = "mathjax/tex-mml-chtml.js"
html_theme_options = {"features": ["navigation.sections", "navigation.top"]}


def expand_notebook_attachments(app, docname, source):
    """Keep downloads self-contained while resolving images for this HTML build."""
    if docname not in {"notebooks/inverse_experiments", "research/notebooks/inverse_experiments"}:
        return
    import base64
    import hashlib
    import json
    import re
    from pathlib import Path
    notebook = json.loads(source[0])
    base = Path(app.srcdir) / ("research" if docname.startswith("research/") else "")
    folder = base / "notebooks/_attachments"
    folder.mkdir(exist_ok=True)
    for index, cell in enumerate(notebook["cells"]):
        if index > 0 and cell["cell_type"] == "markdown":
            cell["source"] = re.sub(r"^(#{1,5}) ", r"\1# ", "".join(cell["source"]), flags=re.M)
        for name, media in cell.get("attachments", {}).items():
            if "image/png" not in media:
                continue
            blob = base64.b64decode(media["image/png"])
            filename = hashlib.sha256(blob).hexdigest()[:20] + ".png"
            (folder / filename).write_bytes(blob)
            text = "".join(cell["source"])
            cell["source"] = text.replace("attachment:" + name, "_attachments/" + filename)
    source[0] = json.dumps(notebook)


def setup(app):
    app.connect("source-read", expand_notebook_attachments)
