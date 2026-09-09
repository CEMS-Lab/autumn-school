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
    """Draw a full-width forward/reverse VJP schematic on a white canvas."""
    navy = "#dce9f6"
    navy_edge = "#2f5d8a"
    green = "#dff2e4"
    green_edge = "#2d7a46"
    gold = "#fff0cf"
    gold_edge = "#a76500"
    violet = "#eee6f8"
    violet_edge = "#6b4c9a"
    grey = "#f5f6f8"
    grey_edge = "#697386"

    fig, ax = plt.subplots(figsize=(14.6, 7.15), constrained_layout=True)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis("off")

    ax.text(
        0.35,
        9.63,
        "Forward states and one shared parameter",
        fontsize=15,
        fontweight="bold",
        color="#14213d",
    )
    ax.text(
        0.35,
        5.64,
        "Reverse accumulation: vector--Jacobian products, not full Jacobians",
        fontsize=14,
        fontweight="bold",
        color="#14213d",
    )
    ax.text(
        0.35,
        1.70,
        "Parameter contributions are added once for every use of $p$",
        fontsize=13.5,
        fontweight="bold",
        color="#14213d",
    )

    # Forward row.
    state_y, op_y, h = 7.30, 7.30, 0.78
    state_w, op_w = 0.84, 1.10
    x_state = [0.45, 3.10, 5.75, 8.40]
    x_op = [1.57, 4.22, 6.87]
    for index, xpos in enumerate(x_state):
        draw_box(
            ax,
            xpos,
            state_y,
            state_w,
            h,
            rf"$z_{index}$",
            face=navy,
            edge=navy_edge,
            fontsize=12,
        )
    for index, xpos in enumerate(x_op):
        draw_box(
            ax,
            xpos,
            op_y,
            op_w,
            h,
            rf"$S_{index}$",
            face=green,
            edge=green_edge,
            fontsize=12,
        )
        arrow(ax, (x_state[index] + state_w, state_y + h / 2), (xpos, op_y + h / 2))
        arrow(ax, (xpos + op_w, op_y + h / 2), (x_state[index + 1], state_y + h / 2))

    draw_box(
        ax,
        10.25,
        7.20,
        2.35,
        0.98,
        r"$y=Cz_N$" "\n" r"$J=\ell(y,p)$",
        face=grey,
        edge=grey_edge,
        fontsize=11,
    )
    arrow(ax, (x_state[-1] + state_w, state_y + h / 2), (10.25, 7.69))
    draw_box(
        ax,
        13.10,
        7.30,
        1.25,
        h,
        "$J$",
        face=grey,
        edge=grey_edge,
        fontsize=13,
    )
    arrow(ax, (12.60, 7.69), (13.10, 7.69))

    draw_box(
        ax,
        5.37,
        8.72,
        1.08,
        0.62,
        "shared $p$",
        face=green,
        edge=green_edge,
        fontsize=10.4,
    )
    for xpos in x_op:
        ax.plot(
            [5.91, xpos + op_w / 2],
            [8.72, op_y + h],
            color=green_edge,
            linewidth=1.1,
            linestyle=(0, (3, 3)),
            zorder=0,
        )

    # Backward row.  Arrows run from the terminal seed towards the initial state.
    backward_y = 3.50
    lambda_positions = x_state
    adjoint_positions = x_op
    for index, xpos in enumerate(lambda_positions):
        draw_box(
            ax,
            xpos,
            backward_y,
            state_w,
            h,
            rf"$\lambda_{index}$",
            face=gold,
            edge=gold_edge,
            fontsize=12,
        )
    for index, xpos in enumerate(adjoint_positions):
        draw_box(
            ax,
            xpos,
            backward_y,
            op_w,
            h,
            rf"$A_{index}^\mathsf{{T}}$",
            face=gold,
            edge=gold_edge,
            fontsize=11.5,
        )
        arrow(
            ax,
            (lambda_positions[index + 1], backward_y + h / 2),
            (xpos + op_w, backward_y + h / 2),
            color=gold_edge,
        )
        arrow(
            ax,
            (xpos, backward_y + h / 2),
            (lambda_positions[index] + state_w, backward_y + h / 2),
            color=gold_edge,
        )
    arrow(ax, (11.43, 7.20), (8.82, backward_y + h), color=gold_edge)
    ax.text(
        10.02,
        5.74,
        r"terminal seed $\lambda_N=C^\mathsf{T}\nabla_y\ell$",
        ha="center",
        va="center",
        color=gold_edge,
        fontsize=10.2,
    )

    # Contribution row.
    card_y, card_w, card_h = 0.35, 2.00, 0.79
    contribution_x = [0.35, 2.75, 5.15]
    labels = [
        r"$B_0^\mathsf{T}\lambda_1$",
        r"$B_1^\mathsf{T}\lambda_2$",
        r"$B_2^\mathsf{T}\lambda_3$",
    ]
    for xpos, label in zip(contribution_x, labels):
        draw_box(
            ax,
            xpos,
            card_y,
            card_w,
            card_h,
            label,
            face=violet,
            edge=violet_edge,
            fontsize=11.4,
        )
    draw_box(
        ax,
        7.55,
        card_y,
        2.35,
        card_h,
        r"direct: $\partial_p\ell$" "\n" r"initial: $(\partial_p z_0)^\mathsf{T}\lambda_0$",
        face=violet,
        edge=violet_edge,
        fontsize=9.8,
    )
    draw_box(
        ax,
        10.22,
        card_y,
        0.65,
        card_h,
        r"$\sum$",
        face=violet,
        edge=violet_edge,
        fontsize=15,
    )
    draw_box(
        ax,
        11.17,
        card_y,
        1.38,
        card_h,
        "$dJ/dp$",
        face=violet,
        edge=violet_edge,
        fontsize=11.8,
    )
    draw_box(
        ax,
        12.85,
        card_y,
        1.80,
        card_h,
        r"$p_{\rm new}$" "\n" r"$=p-\alpha\,dJ/dp$",
        face=grey,
        edge=grey_edge,
        fontsize=9.7,
    )
    for xpos in (2.55, 4.95, 7.35):
        ax.text(
            xpos,
            card_y + card_h / 2,
            "+",
            ha="center",
            va="center",
            color=violet_edge,
            fontsize=15,
            fontweight="bold",
        )
    arrow(ax, (9.90, card_y + card_h / 2), (10.22, card_y + card_h / 2), color=violet_edge)
    arrow(ax, (10.87, card_y + card_h / 2), (11.17, card_y + card_h / 2), color=violet_edge)
    arrow(ax, (12.55, card_y + card_h / 2), (12.85, card_y + card_h / 2))

    ax.text(
        0.35,
        2.47,
        r"$\lambda_n=A_n^\mathsf{T}\lambda_{n+1}$",
        fontsize=11.7,
        color=gold_edge,
    )
    ax.text(
        10.72,
        2.47,
        r"$B_n=\partial S_n/\partial p$",
        fontsize=11.1,
        color=violet_edge,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=190, facecolor="white")
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
    sys.exit(main())
