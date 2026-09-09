#!/usr/bin/env python3
"""Validate and draw the original reverse-accumulation teaching example.

The example is intentionally a three-step scalar recurrence, not a call to
PhAST.  It is small enough to check by hand while retaining the important
feature of a shared parameter entering every time step.
"""

from __future__ import annotations

import time

# This starts before the plotting and tensor imports, so the receipt captures
# the practical script cost rather than only the arithmetic section.
PROCESS_START = time.perf_counter()

import hashlib
import json
import platform
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import torch

from embed_svg_fonts import embed_svg_fonts


BOOK = Path(__file__).resolve().parents[1]
ROOT = next(
    (
        base
        for base in BOOK.parents
        if (base / "notebooks").is_dir() and (base / "vendor").is_dir()
    ),
    BOOK.parent,
)

DT = 0.2
P_VALUE = 0.8
FORCING = 1.5
X0 = 0.4
TARGET = 0.9
N_STEPS = 3
FD_STEP = 1.0e-6


def loss_at(parameter: float) -> float:
    """Evaluate J for the scalar, explicitly stepped teaching recurrence."""
    x = X0
    for _ in range(N_STEPS):
        x = (1.0 - DT * parameter) * x + DT * FORCING
    return 0.5 * (x - TARGET) ** 2


def draw_box(ax, x, y, width, height, label, *, face, edge, fontsize=10.5):
    """Add one rounded diagram box in axes coordinates."""
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.035,rounding_size=0.08",
        facecolor=face,
        edgecolor=edge,
        linewidth=1.25,
    )
    ax.add_patch(patch)
    ax.text(
        x + width / 2,
        y + height / 2,
        label,
        ha="center",
        va="center",
        fontsize=fontsize,
        color="#14213d",
        linespacing=1.12,
    )


def arrow(ax, start, stop, *, color="#293241", linewidth=1.4, style="->"):
    """Add a compact directed arrow between diagram elements."""
    ax.annotate(
        "",
        xy=stop,
        xytext=start,
        arrowprops={
            "arrowstyle": style,
            "color": color,
            "linewidth": linewidth,
            "shrinkA": 0,
            "shrinkB": 0,
        },
    )


def build_figure(output_path: Path) -> None:
    """Draw aligned forward, adjoint and shared-parameter accumulation bands.

    This original schematic uses the chapter's three-step notation. Its
    printable vector exports preserve text; it does not execute the example
    or make a new numerical-validation claim.
    """
    from matplotlib.patches import Circle, Rectangle

    blue, orange, teal = "#245A81", "#B85C20", "#087F82"
    ink, muted, rule = "#17252E", "#536571", "#DDE5EA"
    with plt.rc_context(
        {
            "font.family": "DejaVu Sans",
            "mathtext.fontset": "dejavusans",
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "savefig.facecolor": "white",
        }
    ):
        fig, ax = plt.subplots(figsize=(9, 7.2))
        fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        fig.patch.set_facecolor("white")
        ax.set(xlim=(0, 9), ylim=(0, 7.2), aspect="equal")
        ax.axis("off")

        def text(x, y, label, *, size=16, color=ink, weight="normal", align="left"):
            return ax.text(
                x, y, label, fontsize=size, color=color, fontweight=weight,
                ha=align, va="center",
            )

        def node(x, y, label, color, fill):
            ax.add_patch(Circle((x, y), 0.29, facecolor=fill, edgecolor=color, lw=1.4))
            text(x, y, label, size=20, color=color, align="center")

        def directed(start, stop, color, width=1.65):
            ax.annotate(
                "", xy=stop, xytext=start,
                arrowprops={"arrowstyle": "-|>", "color": color,
                            "lw": width, "mutation_scale": 12,
                            "shrinkA": 0, "shrinkB": 0},
            )

        def rectangular(x, y, width, height, label, color, fill, size=16):
            ax.add_patch(Rectangle((x, y), width, height,
                                   facecolor=fill, edgecolor=color, lw=1.3))
            text(x + width / 2, y + height / 2, label,
                 size=size, color=color, align="center")

        text(0.38, 6.91, "Backpropagation through three updates", size=22, weight="bold")

        # The state and adjoint columns line up: only the direction changes.
        states = [0.80, 2.55, 4.30, 6.05]
        operators = [(left + right) / 2 for left, right in zip(states, states[1:])]
        forward_y, reverse_y = 5.15, 3.36

        text(0.38, 6.40, "1   Evolve the state", color=blue, weight="bold")
        text(8.62, 6.40, r"$z_{n+1}=S_n(z_n,p)$", size=17, color=blue, align="right")
        text(0.42, 5.96, "shared $p$", size=14, color=teal)
        ax.plot([1.47, operators[-1]], [5.96, 5.96], color=teal, lw=1.4)
        for xpos in operators:
            directed((xpos, 5.96), (xpos, 5.66), teal, width=1.3)
        for index, xpos in enumerate(states):
            node(xpos, forward_y, rf"$z_{index}$", blue, "#EDF4F8")
        for index, xpos in enumerate(operators):
            directed((states[index] + 0.33, forward_y),
                     (states[index + 1] - 0.33, forward_y), blue)
            text(xpos, 5.48, rf"$S_{index}$", size=18, color=blue, align="center")
        rectangular(6.79, 4.86, 1.85, 0.58, r"$J=\ell(Cz_3,p)$", blue, "#EDF4F8", size=17)
        directed((6.38, forward_y), (6.74, forward_y), blue)
        text(7.715, 5.66, "scalar objective", size=14, color=muted, align="center")

        # The right-hand turn seeds the reverse sweep from the final scalar.
        ax.plot([0.38, 6.61], [4.52, 4.52], color=rule, lw=1)
        text(0.38, 4.23, "2   Pass adjoints backwards", color=orange, weight="bold")
        rectangular(6.79, 3.07, 1.85, 0.58, r"$C^\mathsf{T}\nabla_y\ell$",
                    orange, "#FCF2E9", size=18)
        directed((7.715, 4.79), (7.715, 3.70), orange)
        text(8.03, 4.13, "seed", size=14, color=orange)
        directed((6.74, reverse_y), (6.38, reverse_y), orange)
        for index, xpos in enumerate(states):
            node(xpos, reverse_y, rf"$\lambda_{index}$", orange, "#FCF2E9")
        for index, xpos in enumerate(operators):
            directed((states[index + 1] - 0.33, reverse_y),
                     (states[index] + 0.33, reverse_y), orange)
            text(xpos, 3.74, rf"$A_{index}^\mathsf{{T}}$", size=17,
                 color=orange, align="center")
        text(0.44, 2.84, r"$A_n=\partial S_n/\partial z_n$", size=15, color=orange)
        text(4.47, 2.84, r"$B_n=\partial S_n/\partial p$", size=15, color=teal)

        # The sum includes every use of p; direct and initial terms are retained.
        ax.plot([0.38, 8.62], [2.57, 2.57], color=rule, lw=1)
        text(0.38, 2.27, "3   Add every parameter contribution", color=teal, weight="bold")
        text(0.43, 1.80, "from updates", size=14, color=muted)
        text(4.90, 1.80,
             r"$B_0^\mathsf{T}\lambda_1\; +\; B_1^\mathsf{T}\lambda_2\; +\; B_2^\mathsf{T}\lambda_3$",
             size=19, color=teal, align="center")
        directed((4.85, 1.55), (4.85, 1.37), teal, width=1.4)

        # Separate text spans give each term a readable caption without using
        # coloured equation screenshots or shrinking a long all-in-one formula.
        term_y = 1.03
        text(0.52, term_y, r"$\frac{dJ}{dp}\;=$", size=21)
        text(2.12, term_y, r"$\frac{\partial\ell}{\partial p}$", size=21, align="center")
        text(2.97, term_y, "+", size=21, align="center")
        text(4.44, term_y, r"$\sum_{n=0}^{2} B_n^\mathsf{T}\lambda_{n+1}$",
             size=21, color=teal, align="center")
        text(5.94, term_y, "+", size=21, align="center")
        text(7.36, term_y, r"$\left(\frac{\partial z_0}{\partial p}\right)^\mathsf{T}\lambda_0$",
             size=21, align="center")
        text(2.12, 0.43, "direct loss", size=14, color=muted, align="center")
        text(4.44, 0.43, "all three updates", size=14, color=teal, align="center")
        text(7.36, 0.43, "initial state", size=14, color=muted, align="center")
        text(0.43, 0.12, "The gradient is an input to a separate optimisation step.",
             size=14, color=muted)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_path, dpi=220, facecolor="white")
        fig.savefig(output_path.with_suffix(".svg"), facecolor="white")
        embed_svg_fonts(output_path.with_suffix(".svg"))
        fig.savefig(output_path.with_suffix(".pdf"), facecolor="white")
        plt.close(fig)


def main() -> None:
    """Run hand, reverse-mode, AD, and finite-difference checks; save receipt."""
    start = PROCESS_START
    if not (P_VALUE > 0.0 and 0.0 < DT * P_VALUE < 1.0):
        raise AssertionError("the selected scalar relaxation must satisfy 0 < dt*p < 1")

    a = 1.0 - DT * P_VALUE
    states = [X0]
    for _ in range(N_STEPS):
        states.append(a * states[-1] + DT * FORCING)

    lambdas = [0.0] * (N_STEPS + 1)
    lambdas[-1] = states[-1] - TARGET
    for step in range(N_STEPS - 1, -1, -1):
        lambdas[step] = a * lambdas[step + 1]

    records = []
    reverse_gradient = 0.0
    forward_tangent = 0.0
    for step in range(N_STEPS):
        b = -DT * states[step]
        contribution = b * lambdas[step + 1]
        reverse_gradient += contribution
        forward_tangent = a * forward_tangent + b
        records.append(
            {
                "step": step,
                "x_n": states[step],
                "x_next": states[step + 1],
                "A_n_dxnext_dx": a,
                "B_n_dxnext_dp": b,
                "lambda_next": lambdas[step + 1],
                "B_transpose_lambda_next": contribution,
            }
        )

    loss = loss_at(P_VALUE)
    forward_gradient = (states[-1] - TARGET) * forward_tangent

    p = torch.tensor(P_VALUE, dtype=torch.float64, requires_grad=True)
    x = torch.tensor(X0, dtype=torch.float64)
    for _ in range(N_STEPS):
        x = (1.0 - DT * p) * x + DT * FORCING
    torch_loss = 0.5 * (x - TARGET) ** 2
    torch_loss.backward()
    autograd_gradient = float(p.grad.item())

    finite_difference = (loss_at(P_VALUE + FD_STEP) - loss_at(P_VALUE - FD_STEP)) / (
        2.0 * FD_STEP
    )
    reverse_ad_error = abs(reverse_gradient - autograd_gradient)
    reverse_fd_error = abs(reverse_gradient - finite_difference)
    reverse_forward_error = abs(reverse_gradient - forward_gradient)

    assertions = {
        "stable_scalar_relaxation_0_lt_dt_p_lt_1": 0.0 < DT * P_VALUE < 1.0,
        "reverse_matches_forward_tangent": reverse_forward_error < 1.0e-14,
        "reverse_matches_torch_autograd": reverse_ad_error < 1.0e-14,
        "reverse_matches_central_difference": reverse_fd_error < 1.0e-9,
    }
    if not all(assertions.values()):
        raise AssertionError(f"validation failed: {assertions}")

    figure_path = BOOK / "figures" / "05a_backpropagation.png"
    receipt_path = ROOT / "reviews" / "backprop_example.json"
    build_figure(figure_path)
    elapsed_s = time.perf_counter() - start
    if elapsed_s >= 300.0:
        raise AssertionError(f"example exceeded the 300-second course cap: {elapsed_s:.3f} s")

    receipt = {
        "schema_version": 1,
        "title": "Three-step reverse accumulation teaching example",
        "execution": {
            "aggregate_wall_seconds": elapsed_s,
            "device": "cpu",
            "python": platform.python_version(),
            "torch": torch.__version__,
            "matplotlib": matplotlib.__version__,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "timeout_contract_seconds": 300.0,
        },
        "recurrence": {
            "equation": "x_next = (1 - dt*p)*x + dt*f",
            "n_steps": N_STEPS,
            "dt": DT,
            "p": P_VALUE,
            "f": FORCING,
            "x0": X0,
            "target": TARGET,
            "stability_condition_checked": "0 < dt*p < 1",
            "states": states,
            "loss": loss,
        },
        "reverse_table": records,
        "gradients": {
            "reverse_accumulation": reverse_gradient,
            "forward_tangent": forward_gradient,
            "torch_autograd": autograd_gradient,
            "central_difference": finite_difference,
            "central_difference_step": FD_STEP,
            "reverse_vs_forward_abs_error": reverse_forward_error,
            "reverse_vs_autograd_abs_error": reverse_ad_error,
            "reverse_vs_central_difference_abs_error": reverse_fd_error,
            "direct_loss_partial_p": 0.0,
            "initial_state_partial_p": 0.0,
        },
        "assertions": assertions,
        "artifacts": {
            "figure": "book/figures/05a_backpropagation.png",
            "figure_sha256": hashlib.sha256(figure_path.read_bytes()).hexdigest(),
            "script": "book/scripts/build_backprop_example.py",
        },
        "scope": {
            "is": "original scalar explicit-relaxation teaching example",
            "is_not": [
                "a PhAST fracture solve",
                "an AT2 or full finite-element residual execution",
                "a solver-in-the-loop differentiability claim",
                "a universal stability result",
            ],
        },
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--figure-only", action="store_true",
        help="Redraw PNG/SVG/PDF without executing the example or writing a receipt.",
    )
    args = parser.parse_args()
    if args.figure_only:
        build_figure(BOOK / "figures" / "05a_backpropagation.png")
        print("Redrew 05a_backpropagation.{png,svg,pdf}; numerical receipts unchanged.")
    else:
        sys.exit(main())
