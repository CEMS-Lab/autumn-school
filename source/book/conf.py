"""Sphinx configuration for the PhAST UKACM course companion."""

from pathlib import Path
from shutil import copytree

project = "PhAST: Phase-field fracture with differentiable FEM"
author = "Allamaprabhu Ani"
presenter = "Sathiskumar A. Ponnusami"
presenter_affiliation = "Queen Mary University of London · CEMS-Lab"
copyright = "2026, CEMS-Lab"
release = "2026"

extensions = [
    "myst_nb",
    "sphinx_copybutton",
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
                    "research/VISUAL_CONTRACT.md",
                    "research/notebooks/inverse_experiments_source.ipynb"]
numfig = True
numfig_format = {"figure": "Figure %s"}

html_theme = "sphinx_book_theme"
html_title = project
html_context = {
    "default_mode": "dark",
    "course_presenter": presenter,
    "course_presenter_affiliation": presenter_affiliation,
}
html_theme_options = {
    "home_page_in_toc": True,
    "show_navbar_depth": 1,
    "show_toc_level": 1,
    "repository_url": "https://github.com/CEMS-Lab/autumn-school",
    "use_repository_button": True,
    # Lessons already link complete practice/solution notebooks and companions.
    "use_download_button": False,
    "footer_content_items": ["phast-credit.html", "phast-discoveries.html"],
}
templates_path = ["_templates"]
html_static_path = ["_static"]
html_css_files = ["mobile_math.css", "learning_book.css"]
html_js_files = ["learning_book.js"]
# The public repository retains this licensed local MathJax distribution.
mathjax_path = "mathjax/tex-mml-chtml.js"


def _copy_local_mathjax(app, exception):
    """Reuse the licensed distribution for normal and fresh HTML builds."""
    if exception is not None or app.builder.format != "html":
        return
    source = Path(__file__).resolve().parents[2] / "book/_static/mathjax"
    target = Path(app.outdir) / "_static/mathjax"
    if not (source / "tex-mml-chtml.js").is_file():
        raise FileNotFoundError("Retain the tracked book/_static/mathjax distribution.")
    if source.resolve() != target.resolve():
        copytree(source, target, dirs_exist_ok=True)


def _verify_design_directives(app, exception):
    """Validate design directives and pedagogical standards upon HTML finalization."""
    if exception is not None or app.builder.format != "html":
        return
    import runpy
    import sys
    checker_path = Path(__file__).resolve().parents[2] / "scripts/check_design_directives.py"
    if checker_path.is_file():
        support = runpy.run_path(str(checker_path))
        passed, errors, elapsed_ms = support["check_directives"](Path(app.outdir))
        if passed:
            print(f"\n✓ [Design Directives] Verified: 0 violations, 4 pillars present, all tutorial badges active ({elapsed_ms:.1f} ms)")
        else:
            print(f"\n⚠ [Design Directives] Found {len(errors)} violation(s):", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)


def setup(app):
    app.connect("build-finished", _copy_local_mathjax)
    app.connect("build-finished", _verify_design_directives)
    # Expand retained notebook attachments for the optional inverse laboratory.
    import runpy
    support = runpy.run_path(str(Path(__file__).parent / "research" / "conf.py"))
    app.connect("source-read", support["expand_notebook_attachments"])

latex_engine = "xelatex"
presenter_latex = presenter + r"\\[0.35em]{\large Queen Mary University of London · CEMS-Lab}"
latex_documents = [
    (master_doc, "phast-ukacm-course.tex", project, presenter_latex, "manual"),
]
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "10pt",
    "extraclassoptions": "openany,oneside",
    "preamble": r"""
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{needspace}
\usepackage{etoolbox}
% Keep an admonition title with the opening lines of its worked explanation.
\BeforeBeginEnvironment{sphinxadmonition}{\Needspace{6\baselineskip}}
\setlength{\parskip}{0.35em}
\AtBeginDocument{\hypersetup{pdfauthor={Allamaprabhu Ani},pdfsubject={Presented by Sathiskumar A. Ponnusami, Queen Mary University of London, CEMS-Lab; UKACM Autumn School 2026}}}
""",
}
