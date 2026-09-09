"""Build the original diagrams used by the PhAST UKACM course book.

The figures are deliberately schematic: they teach relationships between
models, fields, and computational steps without reproducing a published
result.  Run from the book directory with the course Python environment.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
import numpy as np


OUT = Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(parents=True, exist_ok=True)

INK = "#17233c"
NAVY = "#244c77"
BLUE = "#5f9ed1"
TEAL = "#3c9d9b"
GOLD = "#d69e2e"
CORAL = "#d4645c"
PALE = "#eef4f9"
GREY = "#687383"


def canvas(width: float = 10.5, height: float = 5.8):
    fig, ax = plt.subplots(figsize=(width, height), constrained_layout=True)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    return fig, ax


def box(ax, xy, width, height, title, body, color=BLUE, *, fontsize=10):
    x, y = xy
    ax.add_patch(
        FancyBboxPatch(
            (x, y), width, height,
            boxstyle="round,pad=0.08,rounding_size=0.12",
            linewidth=1.5, edgecolor=color, facecolor="white",
        )
    )
    ax.text(x + 0.15, y + height - 0.28, title, color=INK, fontsize=fontsize + 1,
            weight="bold", va="top")
    ax.text(x + 0.15, y + height - 0.72, body, color=GREY, fontsize=fontsize,
            va="top", linespacing=1.35)


def arrow(ax, start, end, color=NAVY, *, label=None, label_offset=(0, 0.14)):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14,
                                 linewidth=1.6, color=color))
    if label:
        mx = (start[0] + end[0]) / 2 + label_offset[0]
        my = (start[1] + end[1]) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", color=GREY, fontsize=9)


def save(fig, name):
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def course_map():
    fig, ax = canvas(10.8, 5.5)
    ax.text(0.2, 5.7, "One day: from a crack description to a reproducible computation",
            fontsize=16, weight="bold", color=INK)
    labels = [
        ("Represent", "sharp, cohesive,\nor diffuse crack", BLUE),
        ("Regularise", "energy, length scale,\nand constraints", TEAL),
        ("Discretise", "mesh, quadrature,\nand unknown fields", GOLD),
        ("Differentiate", "tensors, AD,\nand inverse tasks", CORAL),
    ]
    for i, (head, body, color) in enumerate(labels):
        x = 0.35 + 2.42 * i
        box(ax, (x, 2.15), 1.93, 1.65, head, body, color, fontsize=9)
        if i < len(labels) - 1:
            arrow(ax, (x + 1.98, 2.96), (x + 2.36, 2.96))
    ax.text(5.0, 0.90,
            "Every chapter returns to the same question: what is represented,\n"
            "what is approximated, and what is checked?",
            ha="center", va="center", fontsize=12, color=NAVY,
            bbox=dict(boxstyle="round,pad=0.45", fc=PALE, ec="none"))
    save(fig, "00_course_map.png")


def methods_map():
    fig, ax = canvas(11.0, 6.2)
    ax.text(0.2, 5.75, "Keep the modelling choices separate", fontsize=16,
            weight="bold", color=INK)
    box(ax, (0.35, 3.25), 2.25, 1.45, "Fracture formulation",
        "What energy or traction law\nrepresents separation?", TEAL)
    box(ax, (3.75, 3.25), 2.25, 1.45, "Spatial discretisation",
        "How are fields represented\non a mesh?", BLUE)
    box(ax, (7.15, 3.25), 2.25, 1.45, "Nonlinear solution",
        "How are equilibrium and\nirreversibility solved?", GOLD)
    arrow(ax, (2.65, 3.98), (3.65, 3.98), label="then approximate")
    arrow(ax, (6.05, 3.98), (7.05, 3.98), label="then solve")
    ax.text(1.48, 2.65, "Griffith / phase field\ncohesive-zone law", ha="center",
            fontsize=10, color=INK, weight="bold")
    ax.text(4.88, 2.65, "standard FEM / XFEM\nmesh refinement", ha="center",
            fontsize=10, color=INK, weight="bold")
    ax.text(8.28, 2.65, "staggered / Newton\nquasi-Newton", ha="center",
            fontsize=10, color=INK, weight="bold")
    ax.text(5.0, 1.35,
            "Phase field is a regularised fracture formulation.  XFEM enriches a\n"
            "discretisation.  A cohesive-zone model prescribes an interface law.\n"
            "Quasi-Newton names an optimisation strategy, not a crack model.",
            ha="center", va="center", fontsize=11, color=NAVY,
            bbox=dict(boxstyle="round,pad=0.55", fc="#fff8e8", ec="#f0c45e"))
    save(fig, "01_methods_map.png")


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


def staggered_loop():
    fig, ax = canvas(10.8, 5.8)
    ax.text(0.2, 5.45, "A staggered update reuses two smaller problems", fontsize=16,
            weight="bold", color=INK)
    box(ax, (0.45, 2.4), 2.0, 1.55, "Load increment $n$",
        "known $d_{n-1}$ and\nboundary/loading data", NAVY)
    box(ax, (3.25, 3.55), 2.15, 1.4, "Mechanics step",
        "solve for displacement $u$\nwith damage held fixed", BLUE)
    box(ax, (3.25, 1.20), 2.15, 1.4, "Damage step",
        "solve for $d$ with $u$ fixed\nand enforce $d\geq d_{n-1}$", TEAL)
    box(ax, (7.05, 2.40), 2.35, 1.55, "Accept or repeat",
        "check residual/change;\nadvance the load only when ready", GOLD)
    arrow(ax, (2.55, 3.2), (3.12, 4.15))
    arrow(ax, (5.48, 4.0), (6.92, 3.35), label="stored tensile driving force")
    arrow(ax, (7.02, 2.75), (5.48, 1.9), label="not converged", label_offset=(0, -0.28))
    arrow(ax, (5.48, 1.85), (6.92, 2.75), label="updated damage", label_offset=(0, 0.18))
    arrow(ax, (9.47, 3.15), (10.05, 3.15), label="next increment")
    ax.text(5.0, 0.42,
            "The diffusion analogy helps explain the gradient term, but fracture has\n"
            "a one-way history constraint and is coupled to elastic equilibrium.",
            ha="center", fontsize=10.5, color=GREY)
    save(fig, "03_staggered_loop.png")


def fem_pipeline():
    fig, ax = canvas(11.1, 5.9)
    ax.text(0.2, 5.50, "The same finite-element idea can be written as tensors", fontsize=16,
            weight="bold", color=INK)
    stages = [
        ("Geometry", "points, notch,\nmaterial regions", BLUE),
        ("Mesh", "cells, facets,\nquadrature", TEAL),
        ("Fields", "$u$ and $d$ at\nnodal degrees of freedom", GOLD),
        ("Operators", "strain, stress,\nresidual, action", CORAL),
        ("Results", "reaction, energy,\nfield plots", NAVY),
    ]
    for i, (title, body, color) in enumerate(stages):
        x = 0.25 + 1.96 * i
        box(ax, (x, 2.75), 1.66, 1.45, title, body, color, fontsize=8.7)
        if i < len(stages) - 1:
            arrow(ax, (x + 1.72, 3.47), (x + 1.88, 3.47))
    ax.text(2.7, 1.35,
            "assembled route\nform a sparse matrix $K$\nand solve $Kx=b$",
            ha="center", va="center", fontsize=10.5, color=INK,
            bbox=dict(boxstyle="round,pad=0.40", fc=PALE, ec=BLUE))
    ax.text(7.25, 1.35,
            "matrix-free route\nprovide the action $v\mapsto K v$\nto an iterative solver",
            ha="center", va="center", fontsize=10.5, color=INK,
            bbox=dict(boxstyle="round,pad=0.40", fc="#eef8f7", ec=TEAL))
    arrow(ax, (4.15, 2.70), (3.05, 1.90), color=BLUE)
    arrow(ax, (5.80, 2.70), (6.85, 1.90), color=TEAL)
    ax.text(5.0, 0.28, "Matrix-free means avoiding an explicitly stored global matrix; it does not remove the need for a valid residual or boundary conditions.",
            ha="center", fontsize=9.2, color=GREY)
    save(fig, "04_fem_pipeline.png")


def autograd_inverse():
    fig, ax = canvas(10.8, 5.9)
    ax.text(0.2, 5.45, "Differentiate a defined computation, then test the derivative", fontsize=16,
            weight="bold", color=INK)
    box(ax, (0.4, 2.55), 1.75, 1.42, "Parameter $p$",
        "for example a bounded\nmaterial multiplier", GOLD)
    box(ax, (3.0, 2.55), 1.95, 1.42, "Forward map",
        "geometry + fields +\nsolver operations", BLUE)
    box(ax, (5.85, 2.55), 1.75, 1.42, "Loss $J$",
        "compare a stated\nobservable", TEAL)
    box(ax, (8.45, 2.55), 1.18, 1.42, "Update",
        r"$p\leftarrow p-\alpha\nabla_p J$", CORAL, fontsize=8.5)
    arrow(ax, (2.22, 3.25), (2.90, 3.25))
    arrow(ax, (5.05, 3.25), (5.75, 3.25))
    arrow(ax, (7.70, 3.25), (8.35, 3.25))
    arrow(ax, (9.04, 2.45), (1.28, 2.10), color=CORAL,
          label="repeat after a bounded update", label_offset=(0, -0.22))
    ax.text(5.0, 1.08,
            r"Directional check: $\frac{J(p+hq)-J(p-hq)}{2h}\;\approx\;\nabla_pJ(p)\cdot q$",
            ha="center", va="center", fontsize=15, color=NAVY,
            bbox=dict(boxstyle="round,pad=0.42", fc=PALE, ec="none"))
    ax.text(5.0, 0.35,
            "A small directional discrepancy checks one local derivative; it is not evidence that an inverse problem is globally identifiable.",
            ha="center", fontsize=9.4, color=GREY)
    save(fig, "05_autograd_inverse.png")


def learning_cycle():
    fig, ax = canvas(11.0, 6.1)
    ax.text(0.2, 5.60, "A learned proposal remains part of a checked mechanics workflow", fontsize=16,
            weight="bold", color=INK)
    box(ax, (0.35, 3.15), 2.0, 1.42, "Reference records",
        "inputs, fields, metadata,\nand split definition", BLUE)
    box(ax, (3.05, 3.15), 1.75, 1.42, "Train",
        "fit on training cases;\nkeep validation separate", TEAL)
    box(ax, (5.50, 3.15), 1.75, 1.42, "Save + reload",
        "state, normalisation,\nversion, and device", GOLD)
    box(ax, (7.95, 3.15), 1.75, 1.42, "Proposal",
        "suggest a field or\ninitialisation", CORAL)
    for x in [2.45, 4.90, 7.35]:
        arrow(ax, (x, 3.85), (x + 0.48, 3.85))
    box(ax, (3.05, 0.95), 2.1, 1.35, "Physics check",
        "constraints, residuals,\nand a reference comparison", NAVY)
    box(ax, (6.10, 0.95), 2.1, 1.35, "Adapt / collect",
        "record difficult cases\nwithout relabelling them", TEAL)
    arrow(ax, (8.82, 3.05), (7.22, 2.38), color=CORAL, label="audit first")
    arrow(ax, (6.1, 1.62), (5.25, 1.62))
    arrow(ax, (3.0, 1.62), (1.35, 3.02), color=TEAL,
          label="optional DAgger-style data loop", label_offset=(0.1, -0.25))
    ax.text(5.0, 0.30,
            "An adapter changes the interface between representations; it is not a certificate that a proposal is physically correct.",
            ha="center", fontsize=9.7, color=GREY)
    save(fig, "06_learning_cycle.png")


def main():
    course_map()
    methods_map()
    energy_profiles()
    staggered_loop()
    fem_pipeline()
    autograd_inverse()
    learning_cycle()


if __name__ == "__main__":
    main()
