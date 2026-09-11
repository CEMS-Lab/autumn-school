"""Read-only diagnostics for a local damaged-bar automatic-differentiation lesson.

The caller supplies the two differentiable inputs and their computed gradient.
This scalar constitutive model prescribes displacement and damage. All values
use dimensionless teaching scales; the residual stiffness is zero and damage
is evaluated in the open interval (0, 1).
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BLUE = "#245a81"
ORANGE = "#c96824"
TEAL = "#087f83"
INK = "#17232d"


def verify_primer(q, gradient, directory, *, E=2.0, A=1.0, length=1.0, target=.04):
    """Compare the supplied PyTorch loss gradient with calculus and central FD."""
    point = q.detach().cpu().numpy().copy()
    actual = gradient.detach().cpu().numpy().copy()
    if point.shape != (2,) or not 0 < point[1] < 1:
        raise ValueError("Expected q=(u,d), with 0<d<1.")
    u, damage = point
    stiffness = E*A/length
    force = stiffness*(1-damage)**2*u
    residual = force-target
    force_gradient = np.array([stiffness*(1-damage)**2,
                               -2*stiffness*(1-damage)*u])
    analytic = residual*force_gradient

    def scalar_loss(values):
        displacement, d = values
        return .5*(stiffness*(1-d)**2*displacement-target)**2

    h = 1.e-6
    perturbations = np.eye(2)*h
    finite_difference = np.array([(scalar_loss(point+step)-scalar_loss(point-step))/(2*h)
                                   for step in perturbations])
    np.testing.assert_allclose(actual, analytic, rtol=1.e-12, atol=1.e-14)
    np.testing.assert_allclose(finite_difference, analytic, rtol=1.e-7, atol=1.e-10)
    receipt = {"scope": "Local damaged-bar constitutive teaching model",
               "input_order": ["u", "d"], "q": point.tolist(),
               "E": E, "A": A, "length": length, "residual_stiffness": 0,
               "target_force": target, "force": float(force),
               "loss": float(.5*residual**2), "force_gradient": force_gradient.tolist(),
               "loss_gradient_autograd": actual.tolist(),
               "loss_gradient_analytic": analytic.tolist(),
               "loss_gradient_central_fd": finite_difference.tolist(), "fd_step": h,
               "max_fd_absolute_error": float(np.max(np.abs(finite_difference-analytic)))}
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    (directory/"autodiff_primer_checks.json").write_text(json.dumps(receipt, indent=2)+"\n")
    np.savetxt(directory/"autodiff_primer_gradient_check.csv",
               np.column_stack([actual, analytic, finite_difference]), delimiter=",",
               header="autograd,analytic,central_fd", comments="")
    return receipt


def _save(fig, directory, name):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(directory/(name+".png"), dpi=180, facecolor="white")
    fig.savefig(directory/(name+".svg"), facecolor="white")
    return fig


def force_sensitivities(receipt, directory):
    """Plot the two one-input slices through the same evaluated force law."""
    u, d = receipt["q"]
    stiffness = receipt["E"]*receipt["A"]/receipt["length"]
    force = receipt["force"]
    du_force, dd_force = receipt["force_gradient"]
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.titlesize": 12, "axes.labelsize": 11,
                         "legend.fontsize": 10, "lines.linewidth": 1.8,
                         "axes.spines.top": False, "axes.spines.right": False}):
        fig, axes = plt.subplots(1, 2, figsize=(10, 3.9), layout="constrained")
        displacement = np.linspace(.02, .18, 160)
        damage = np.linspace(.1, .9, 160)
        axes[0].plot(displacement, stiffness*(1-d)**2*displacement, color=BLUE,
                     label=rf"Force at fixed $d={d:g}$")
        axes[0].plot([u], [force], "o", color=ORANGE, label="Evaluation point")
        axes[0].set(xlabel="Displacement $u$", ylabel="Force $F$",
                    title=rf"More extension: $\partial F/\partial u={du_force:g}$")
        axes[1].plot(damage, stiffness*(1-damage)**2*u, color=BLUE,
                     label=rf"Force at fixed $u={u:g}$")
        local = np.array([d-.17, d+.17])
        axes[1].plot(local, force+dd_force*(local-d), "--", color=TEAL,
                     label="Local tangent")
        axes[1].plot([d], [force], "o", color=ORANGE, label="Evaluation point")
        axes[1].set(xlabel="Damage $d$", ylabel="Force $F$",
                    title=rf"More damage: $\partial F/\partial d={dd_force:g}$")
        for index, ax in enumerate(axes):
            ax.axhline(receipt["target_force"], color=".45", linestyle=":", label="Target force")
            ax.grid(alpha=.25, linestyle="--")
            ax.legend(loc="upper left" if index == 0 else "upper right")
        fig.suptitle("A local damaged bar · dimensionless teaching scales", fontsize=13)
        return _save(fig, directory, "autodiff_force_sensitivities")


def forward_reverse_graph(receipt, directory):
    """Show actual forward values and chain-rule factors for the two inputs."""
    u, d = receipt["q"]
    force = receipt["force"]
    residual = force-receipt["target_force"]
    gradient = receipt["loss_gradient_autograd"]
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 12}):
        fig, axes = plt.subplots(2, 1, figsize=(10.6, 5.8), layout="constrained")
        for ax in axes:
            ax.set(xlim=(0, 1), ylim=(0, 1))
            ax.axis("off")
        boxes = dict(boxstyle="round,pad=.5", facecolor="#f4f8fb", edgecolor=BLUE)
        forward = [(0.09, rf"$u={u:g}$"+"\n"+rf"$d={d:g}$"),
                   (.35, rf"$g=(1-d)^2={((1-d)**2):g}$"),
                   (.62, rf"$F=(EA/L_b)gu={force:g}$"),
                   (.89, rf"$\mathcal{{L}}=\frac{{1}}{{2}}(F-F^\star)^2$"+"\n"+
                    rf"$={receipt['loss']:.5f}$")]
        for x, label in forward:
            axes[0].text(x, .5, label, ha="center", va="center", bbox=boxes, color=INK)
        for begin, end in ((.15, .24), (.47, .53), (.73, .80)):
            axes[0].annotate("", xy=(end, .5), xytext=(begin, .5),
                             arrowprops=dict(arrowstyle="->", color=BLUE, linewidth=1.8))
        axes[0].annotate("", xy=(.62, .72), xytext=(.09, .75),
                         arrowprops=dict(arrowstyle="->", color=BLUE, linewidth=1.8,
                                         connectionstyle="arc3,rad=-.16"))
        axes[0].text(.35, .98, "$u$ enters the force directly", ha="center", color=BLUE, fontsize=11)
        axes[0].text(.20, .58, "$d$", ha="center", color=BLUE)
        axes[0].set_title("Forward: evaluate the force and its mismatch", loc="left", fontsize=14)
        axes[0].text(.62, .13, rf"$E={receipt['E']:g},\ A={receipt['A']:g},\ L_b={receipt['length']:g}$"
                     +rf"; target $F^\star={receipt['target_force']:g}$", ha="center", color=".3")
        axes[1].set_title("Reverse: multiply the loss seed by each local sensitivity", loc="left", fontsize=14)
        axes[1].text(.79, .52, rf"$\frac{{\partial\mathcal{{L}}}}{{\partial F}}=F-F^\star={residual:g}$",
                     ha="center", va="center", bbox=boxes, color=INK)
        axes[1].text(.27, .75, rf"$\frac{{\partial\mathcal{{L}}}}{{\partial u}}={residual:g}\times{receipt['force_gradient'][0]:g}={gradient[0]:g}$",
                     ha="center", va="center", color=BLUE)
        axes[1].text(.27, .30, rf"$\frac{{\partial\mathcal{{L}}}}{{\partial d}}={residual:g}\times({receipt['force_gradient'][1]:g})={gradient[1]:g}$",
                     ha="center", va="center", color=TEAL)
        for y in (.75, .30):
            axes[1].annotate("", xy=(.51, y), xytext=(.64, .52),
                             arrowprops=dict(arrowstyle="->", color=ORANGE, linewidth=1.8))
        return _save(fig, directory, "autodiff_forward_reverse")
