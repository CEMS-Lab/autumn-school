"""Build the original diagrams used by the PhAST UKACM course book.

The figures are deliberately schematic: they teach relationships between
models, fields, and computational steps without reproducing a published
result. Run with the course Python environment. Use --flowcharts-only to
preserve the separate scientific energy plot byte for byte.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np

from embed_svg_fonts import embed_svg_fonts


OUT = Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#17233c"
TEAL = "#3c9d9b"
GOLD = "#d69e2e"
CORAL = "#d4645c"


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def energy_profiles():
    fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.4), constrained_layout=True)
    x = np.linspace(-3.0, 3.0, 500)
    at2 = np.exp(-np.abs(x))
    at1 = np.maximum(1.0 - np.abs(x) / 2.0, 0.0) ** 2
    axes[0].plot(x, at2, lw=3, color=TEAL, label="AT2 idealised profile")
    axes[0].plot(x, at1, lw=3, color=GOLD, label="AT1 idealised profile")
    axes[0].axhline(0, color=INK, lw=0.8)
    axes[0].axvline(0, color=INK, lw=0.8)
    axes[0].set_xlabel(r"distance from crack centre, $x/\ell$")
    axes[0].set_ylabel(r"damage field, $d$")
    axes[0].set_ylim(-0.04, 1.08)
    axes[0].set_title("The regularisation length sets a diffuse band")
    axes[0].legend(frameon=False, fontsize=9, loc="upper right")
    d = np.linspace(0, 1, 300)
    g = (1 - d) ** 2
    axes[1].plot(d, d**2, lw=3, color=TEAL, label=r"AT2: $w(d)=d^2$")
    axes[1].plot(d, d, lw=3, color=GOLD, label=r"AT1: $w(d)=d$")
    axes[1].plot(d, g, lw=2.5, color=CORAL, ls="--", label=r"$g(d)=(1-d)^2$")
    axes[1].set_xlabel(r"damage variable, $d$ (0 intact; 1 broken)")
    axes[1].set_ylabel("local function value")
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(-0.04, 1.08)
    axes[1].set_title("Crack-density and stiffness-degradation choices")
    axes[1].legend(frameon=False, fontsize=9)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.20)
    save(fig, "02_energy_profiles.png")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--flowcharts-only", action="store_true",
        help="Rebuild the six diagrams without touching the scientific energy plot.",
    )
    args = parser.parse_args()
    course_map()
    methods_map()
    if not args.flowcharts_only:
        energy_profiles()
    staggered_loop()
    fem_pipeline()
    autograd_inverse()
    learning_cycle()


# The energy plot above retains its original palette and generation path.
# The six diagram builders below use a separate, local style so a cosmetic
# flowchart revision cannot alter scientific plots or numerical results.
FLOW_INK = "#17212B"
FLOW_BLUE = "#245A81"
FLOW_TEAL = "#087F82"
FLOW_ORANGE = "#B85C20"
FLOW_GREY = "#58636D"
FLOW_LINE = "#D4DADE"


def flow_canvas(title, height=7.3):
    fig, ax = plt.subplots(figsize=(9.2, height))
    fig.subplots_adjust(left=0.012, right=0.988, bottom=0.018, top=0.982)
    ax.set(xlim=(0, 9.2), ylim=(0, height))
    ax.axis("off")
    ax.text(0.18, height - 0.18, title, fontsize=22, weight="bold",
            color=FLOW_INK, va="top", linespacing=1.15)
    return fig, ax


def flow_text(ax, x, y, text, size=14, color=FLOW_INK, **kwargs):
    return ax.text(x, y, text, fontsize=size, color=color,
                   linespacing=1.3, **kwargs)


def flow_node(ax, x, y, width, height, title, body="", *, color=FLOW_BLUE,
              title_size=17, body_size=14):
    """A flat process rectangle; colour denotes role rather than decoration."""
    ax.add_patch(Rectangle((x, y), width, height, facecolor="white",
                           edgecolor=FLOW_LINE, linewidth=0.9))
    ax.plot([x, x + width], [y + height, y + height], color=color, lw=2.6,
            solid_capstyle="butt")
    flow_text(ax, x + 0.15, y + height - 0.17, title, title_size,
              color, weight="bold", va="top")
    if body:
        flow_text(ax, x + 0.15, y + height - 0.59, body, body_size,
                  va="top")


def flow_arrow(ax, points, *, color=FLOW_BLUE, dashed=False, label=None,
               label_at=None, label_size=14, align="center"):
    """Orthogonal connectors avoid ambiguous crossings and duplicate edges."""
    style = (0, (4, 3)) if dashed else "solid"
    if len(points) > 2:
        xs, ys = zip(*points[:-1])
        ax.plot(xs, ys, color=color, linewidth=1.7, linestyle=style,
                solid_capstyle="butt", dash_capstyle="butt")
    ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle="-|>",
                                 mutation_scale=15, linewidth=1.7,
                                 color=color, linestyle=style,
                                 shrinkA=0, shrinkB=1.5))
    if label:
        flow_text(ax, *label_at, label, label_size, color, ha=align,
                  va="center", bbox=dict(fc="white", ec="none", pad=1.6))


def flow_save(fig, name):
    # Keep SVG labels editable/searchable; PDF embeds TrueType text. These
    # settings are scoped to this export, not to the pre-existing energy plot.
    with plt.rc_context({"svg.fonttype": "none", "pdf.fonttype": 42,
                         "font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans"}):
        for suffix in ("png", "svg", "pdf"):
            fig.savefig(OUT / f"{name}.{suffix}", dpi=220,
                        bbox_inches="tight", pad_inches=0.08,
                        facecolor="white")
            if suffix == "svg":
                embed_svg_fonts(OUT / f"{name}.svg")
    plt.close(fig)


def course_map():
    fig, ax = flow_canvas("Six hours: understand, compute, then learn", 7.1)
    flow_text(ax, 0.2, 6.37,
              "Three 120-minute sessions, each including a 10-minute break.",
              color=FLOW_GREY)
    rows = [
        ("A", 5.96, "Model & numerical method", FLOW_BLUE,
         "Crack representations → energy & damage → FEM",
         "Explain what the model represents and what the method approximates.",
         "Notebook 00  ·  Opening prediction (algebraic teaser)"),
        ("B", 4.08, "Computation & derivatives", FLOW_BLUE,
         "Geometry & loads → PhAST result → checked gradient",
         "Run a small case, interpret its fields, and test a local sensitivity.",
         "Notebooks 01–03  ·  PhAST, degradation, elastic-bar inverse toy"),
        ("C", 2.20, "Learning & model interfaces", FLOW_TEAL,
         "Train & reload → compatible proposal → physics check",
         "Evaluate a learned component and explain when correction is needed.",
         "Notebooks 04–05  ·  Toy field training and checked fallback"),
    ]
    for index, top, title, colour, route, outcome, notebooks in rows:
        flow_text(ax, 0.22, top - 0.05, index, 24, colour,
                  weight="bold", va="top")
        flow_text(ax, 0.95, top, title, 18, colour,
                  weight="bold", va="top")
        flow_text(ax, 8.82, top - 0.03, "120 min", 15, FLOW_GREY,
                  ha="right", va="top")
        flow_text(ax, 0.95, top - 0.48, route, 15, va="top")
        flow_text(ax, 0.95, top - 0.89, outcome, 14, va="top")
        flow_text(ax, 0.95, top - 1.30, notebooks, 14, FLOW_GREY, va="top")
        ax.plot([0.95, 8.93], [top - 1.64, top - 1.64],
                color=FLOW_LINE, lw=0.8)
    for top in (5.96, 4.08):
        flow_arrow(ax, [(0.38, top - 0.61), (0.38, top - 1.68)],
                   color=FLOW_GREY)
    flow_save(fig, "00_course_map")


def methods_map():
    fig, ax = flow_canvas("Three choices, three different questions", 7.4)
    stages = [
        (5.23, "1", "Fracture formulation", "What represents separation?",
         "A phase-field energy or a cohesive traction–separation law.", FLOW_TEAL),
        (3.20, "2", "Spatial discretisation", "How are the fields approximated?",
         "Standard finite elements, XFEM enrichment, mesh resolution.", FLOW_BLUE),
        (1.17, "3", "Solution algorithm", "How is the discrete problem solved?",
         "Staggered or monolithic updates; Newton or quasi-Newton.", FLOW_BLUE),
    ]
    for y, number, title, question, examples, colour in stages:
        flow_text(ax, 0.23, y + 1.07, number, 25, colour, weight="bold")
        flow_node(ax, 0.98, y, 7.91, 1.42, title, question,
                  color=colour, body_size=15)
        flow_text(ax, 1.13, y + 0.25, examples, 14, color=FLOW_GREY)
    flow_arrow(ax, [(4.92, 5.22), (4.92, 4.65)],
               label="discretise the chosen equations", label_at=(5.21, 4.93), align="left")
    flow_arrow(ax, [(4.92, 3.19), (4.92, 2.62)],
               label="solve the discrete equations", label_at=(5.21, 2.90), align="left")
    flow_text(ax, 0.98, 0.43,
              "Quasi-Newton is not a fracture model; XFEM is not a traction law.",
              14, FLOW_GREY)
    flow_save(fig, "01_methods_map")


def staggered_loop():
    fig, ax = flow_canvas("Alternate fields at one load level", 8.0)
    flow_text(ax, 0.75, 7.12,
              r"Load increment $n$: initialise $d^{(0)}=d_{n-1}$; iteration $k=0$.",
              15, FLOW_GREY)
    flow_node(ax, 0.75, 4.82, 3.57, 1.50, "1  Mechanics",
              "Hold damage fixed.\n" + r"Solve for $u^{(k+1)}$.")
    flow_node(ax, 5.16, 4.82, 3.57, 1.50, "2  Driving quantity",
              "Construct the tensile history\nor stated damage source.")
    flow_node(ax, 5.16, 2.63, 3.57, 1.50, "3  Damage",
              "Hold mechanics fixed.\n" + r"Enforce $d^{(k+1)}\geq d_{n-1}$.",
              color=FLOW_TEAL)
    flow_node(ax, 0.75, 2.63, 3.57, 1.50, "4  Converged?",
              "Check both residuals\nand field changes.")
    flow_node(ax, 0.75, 0.57, 3.57, 1.25, "Accept increment",
              "Advance the load: " + r"$n\leftarrow n+1$.", color=FLOW_TEAL)
    flow_arrow(ax, [(2.54, 6.86), (2.54, 6.34)])
    flow_arrow(ax, [(4.33, 5.57), (5.14, 5.57)],
               label=r"$u^{(k+1)}$", label_at=(4.74, 5.93))
    flow_arrow(ax, [(6.95, 4.80), (6.95, 4.15)],
               label=r"$H$ or $\psi^+$", label_at=(7.81, 4.48))
    flow_arrow(ax, [(5.14, 3.38), (4.34, 3.38)],
               label=r"$d^{(k+1)}$", label_at=(4.74, 3.74))
    flow_arrow(ax, [(2.54, 2.61), (2.54, 1.84)], color=FLOW_TEAL,
               label="yes", label_at=(2.95, 2.24))
    flow_arrow(ax, [(0.73, 3.37), (0.28, 3.37), (0.28, 5.57), (0.73, 5.57)],
               color=FLOW_ORANGE)
    flow_text(ax, 0.81, 4.47, r"no: repeat with $k\leftarrow k+1$", 14,
              FLOW_ORANGE, ha="left", va="center")
    flow_text(ax, 5.17, 1.43, "Repeat at the same load.\n"
              "A history construction and a\n"
              "direct irreversibility constraint\n"
              "are distinct modelling choices.", 14, FLOW_GREY, va="center")
    flow_save(fig, "03_staggered_loop")


def fem_pipeline():
    fig, ax = flow_canvas("One FEM model, two operator routes", 8.2)
    for x, title, body in [
        (0.22, "Domain & mesh", "Coordinates, cells,\nquadrature."),
        (3.36, "Material & state", r"Properties, $u$, $d$," + "\ninitial conditions."),
        (6.50, "Loads & BCs", "Forces, prescribed\nvalues, boundaries."),
    ]:
        flow_node(ax, x, 5.87, 2.50, 1.47, title, body, title_size=16)
    # Three inputs meet before the element operations; neither linear-solver
    # branch is permitted to bypass geometry, material data, or constraints.
    for centre in (1.47, 4.61, 7.75):
        flow_arrow(ax, [(centre, 5.85), (centre, 5.46), (4.61, 5.46), (4.61, 5.03)])
    flow_node(ax, 2.04, 3.53, 5.15, 1.48, "Element tensor operations",
              r"$u_e\;\longrightarrow\;\varepsilon_q\;\longrightarrow\;\sigma_q\;\longrightarrow\;r_e$",
              body_size=18)
    flow_text(ax, 4.61, 3.70, "Gather → evaluate → scatter", 14,
              FLOW_GREY, ha="center")
    flow_node(ax, 0.39, 1.48, 3.75, 1.34, "Assembled route",
              r"Store $K$; solve $Kx=b$.", body_size=15)
    flow_node(ax, 5.07, 1.48, 3.75, 1.34, "Matrix-free route",
              r"Apply $v\mapsto Kv$ in Krylov." + "\nNo stored global matrix.",
              color=FLOW_BLUE, body_size=14)
    flow_arrow(ax, [(3.01, 3.51), (3.01, 3.18), (2.27, 3.18), (2.27, 2.84)])
    flow_arrow(ax, [(6.21, 3.51), (6.21, 3.18), (6.95, 3.18), (6.95, 2.84)])
    flow_arrow(ax, [(2.27, 1.46), (2.27, 1.03), (4.61, 1.03), (4.61, 0.69)])
    flow_arrow(ax, [(6.95, 1.46), (6.95, 1.03), (4.61, 1.03), (4.61, 0.69)])
    flow_text(ax, 4.61, 0.42, "Inspect fields, reactions and residuals", 17,
              FLOW_TEAL, ha="center", va="center", weight="bold")
    flow_save(fig, "04_fem_pipeline")


def autograd_inverse():
    fig, ax = flow_canvas("A gradient is not an optimisation step", 8.1)
    flow_text(ax, 0.25, 7.22, "FORWARD  ·  evaluate the stated computation", 14,
              FLOW_BLUE, weight="bold")
    for x, width, title, body in [
        (0.25, 2.33, "Parameter", r"Chosen input $p$" + "\nOther inputs fixed."),
        (3.39, 2.43, "Forward map", r"$z=S(p)$" + "\n" + r"Observable $y=Cz$"),
        (6.64, 2.33, "Scalar loss", r"$J=\frac{1}{2}\|y-y^\star\|^2$"),
    ]:
        flow_node(ax, x, 5.41, width, 1.48, title, body, body_size=14)
    flow_arrow(ax, [(2.60, 6.15), (3.37, 6.15)],
               label=r"$p$", label_at=(2.98, 6.48))
    flow_arrow(ax, [(5.84, 6.15), (6.62, 6.15)],
               label=r"$y$", label_at=(6.23, 6.48))
    flow_text(ax, 0.25, 4.93, "REVERSE  ·  accumulate vector–Jacobian products", 14,
              FLOW_ORANGE, weight="bold")
    flow_node(ax, 0.25, 3.10, 2.33, 1.48, "Input sensitivity",
              r"$\nabla_p J$", color=FLOW_ORANGE, body_size=20, title_size=16)
    flow_node(ax, 3.39, 3.10, 2.43, 1.48, "Reverse pass",
              r"$(\partial y/\partial p)^T$" + "\nApply; do not invert.",
              color=FLOW_ORANGE, body_size=14, title_size=16)
    flow_node(ax, 6.64, 3.10, 2.33, 1.48, "Loss sensitivity",
              r"$\nabla_yJ=y-y^\star$", color=FLOW_ORANGE, body_size=16, title_size=16)
    flow_arrow(ax, [(7.805, 5.39), (7.805, 4.60)], color=FLOW_ORANGE)
    flow_arrow(ax, [(6.62, 3.84), (5.84, 3.84)], color=FLOW_ORANGE)
    flow_arrow(ax, [(3.37, 3.84), (2.60, 3.84)], color=FLOW_ORANGE)
    flow_text(ax, 4.61, 2.54,
              r"$\nabla_pJ=(\partial y/\partial p)^T\nabla_yJ$",
              20, FLOW_ORANGE, ha="center", va="center")
    ax.plot([0.25, 8.97], [2.12, 2.12], color=FLOW_LINE, lw=0.8)
    flow_text(ax, 0.25, 1.72, "CHECK", 14, FLOW_INK, weight="bold")
    flow_text(ax, 2.01, 1.75,
              r"$\frac{J(p+hq)-J(p-hq)}{2h}\;\approx\;(\nabla_pJ)^Tq$",
              18, FLOW_INK, va="center")
    flow_text(ax, 0.25, 0.95, "OPTIONAL", 14, FLOW_TEAL, weight="bold")
    flow_text(ax, 2.01, 0.98, r"Optimise: $p_{\mathrm{new}}=p-\alpha\nabla_pJ$",
              18, FLOW_TEAL, va="center")
    flow_text(ax, 0.25, 0.34,
              "A local derivative check does not establish a unique inverse solution.",
              14, FLOW_GREY)
    flow_save(fig, "05_autograd_inverse")


def learning_cycle():
    fig, ax = flow_canvas("Learn a proposal; retain a checked solution", 9.3)
    flow_text(ax, 0.25, 8.47, "OFFLINE  ·  fit and preserve the model contract", 14,
              FLOW_TEAL, weight="bold")
    for x, title, body in [
        (0.25, "Reference data", "Inputs, targets,\nheld-out split."),
        (3.39, "Train", r"Fit $f_\theta$; evaluate" + "\non unseen cases."),
        (6.53, "Save & reload", "Weights, scaling,\nshapes, metadata."),
    ]:
        flow_node(ax, x, 6.70, 2.43, 1.45, title, body,
                  color=FLOW_TEAL, title_size=16)
    flow_arrow(ax, [(2.70, 7.43), (3.37, 7.43)], color=FLOW_TEAL)
    flow_arrow(ax, [(5.84, 7.43), (6.51, 7.43)], color=FLOW_TEAL)
    flow_arrow(ax, [(7.745, 6.68), (7.745, 6.16), (1.465, 6.16), (1.465, 5.30)],
               color=FLOW_TEAL, label="deploy model + preprocessing",
               label_at=(4.64, 6.16))
    flow_text(ax, 2.07, 5.65, "ONLINE  ·  assess each proposed state", 14,
              FLOW_BLUE, weight="bold")
    flow_node(ax, 0.25, 3.81, 2.43, 1.47, "Proposal",
              r"$\widehat z=f_\theta(x)$" + "\nDeclared interface.")
    flow_node(ax, 3.39, 3.81, 2.43, 1.47, "Checks pass?",
              "Bounds, history,\nstated residual.")
    flow_node(ax, 6.53, 3.81, 2.43, 1.47, "Accept state",
              "Record diagnostics\nand total cost.", color=FLOW_TEAL, title_size=16)
    flow_arrow(ax, [(2.70, 4.55), (3.37, 4.55)])
    flow_arrow(ax, [(5.84, 4.55), (6.51, 4.55)], color=FLOW_TEAL,
               label="yes", label_at=(6.175, 4.93))
    flow_node(ax, 3.39, 1.56, 2.43, 1.47, "Correct / fallback",
              "Use the reference\nprocedure; recheck.", color=FLOW_ORANGE, title_size=15)
    flow_arrow(ax, [(4.605, 3.79), (4.605, 3.05)], color=FLOW_ORANGE,
               label="no", label_at=(5.02, 3.42))
    flow_arrow(ax, [(5.84, 2.30), (7.745, 2.30), (7.745, 3.79)],
               color=FLOW_BLUE, label="if checks pass",
               label_at=(6.73, 3.42))
    flow_node(ax, 0.25, 1.56, 2.43, 1.47, "Reference labels",
              "Visited inputs +\ntrusted targets.", color=FLOW_GREY, title_size=16)
    flow_arrow(ax, [(3.37, 2.30), (2.70, 2.30)], color=FLOW_ORANGE, dashed=True)
    # Deliberately dashed: this is the optional conceptual aggregation loop,
    # not a claim that the current toy notebooks perform full DAgger training.
    flow_arrow(ax, [(1.465, 1.54), (1.465, 1.20), (0.08, 1.20),
                   (0.08, 7.42), (0.23, 7.42)], color=FLOW_ORANGE, dashed=True)
    flow_text(ax, 0.25, 0.77,
              "Dashed loop: aggregate reference-labelled visited states and retrain.",
              14, FLOW_ORANGE)
    flow_text(ax, 0.25, 0.30,
              "A conceptual DAgger extension; notebooks 04–05 demonstrate toy components.",
              14, FLOW_GREY)
    flow_save(fig, "06_learning_cycle")


if __name__ == "__main__":
    main()
