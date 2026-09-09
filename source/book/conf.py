"""Sphinx configuration for the PhAST UKACM course companion."""

project = "PhAST: Phase-field fracture with differentiable FEM"
author = "UKACM Autumn School"
copyright = "2026, UKACM Autumn School"
release = "2026"

extensions = [
    "myst_nb",
    "sphinx_copybutton",
    "sphinx_immaterial",
]

myst_enable_extensions = ["amsmath", "colon_fence", "deflist", "dollarmath"]
myst_heading_anchors = 3
myst_dmath_double_inline = True
myst_all_links_external = True
nb_execution_mode = "off"
nb_output_stderr = "warn"
nb_ipywidgets_js = {}

master_doc = "index"
exclude_patterns = ["_build", "README.md", "solutions", "Thumbs.db", ".DS_Store",
                    "research/_build", "research/README.md", "research/REVIEW_STATUS.md",
                    "research/notebooks/inverse_experiments_source.ipynb"]
numfig = True
numfig_format = {"figure": "Figure %s"}

html_theme = "sphinx_immaterial"
html_title = project
html_static_path = ["_static"]
html_css_files = ["mobile_math.css", "learning_book.css"]
html_js_files = ["learning_book.js"]
mathjax_path = "mathjax/tex-mml-chtml.js"


def setup(app):
    """Load the Sphinx options object before the copy-button extension."""
    app.add_js_file("documentation_options.js", priority=100)
    # Reuse the extension's attachment handling; retain the course theme/controls.
    from pathlib import Path
    import runpy
    support = runpy.run_path(str(Path(__file__).parent / "research" / "conf.py"))
    app.connect("source-read", support["expand_notebook_attachments"])

latex_engine = "xelatex"
latex_documents = [
    (master_doc, "phast-ukacm-course.tex", project, author, "manual"),
]
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "10pt",
    "extraclassoptions": "openany,oneside",
    "preamble": r"""
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\setlength{\parskip}{0.35em}
""",
}
