"""Observational figures and portable data for the three classroom lessons.

These helpers copy or evaluate outputs for teaching; they do not update a
solver, change parameters, train a model, or consume random numbers.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
import torch


def save_table(rows, path):
    """Write every numeric row with its original precision and column names."""
    rows = list(rows)
    if not rows:
        raise ValueError("A results table needs at least one row.")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path


def numeric_table_html(rows, columns, caption):
    """A compact, dependency-free notebook table; CSV keeps full precision."""
    heads = "".join(f"<th>{html.escape(label)}</th>" for _, label in columns)
    body = []
    for row in rows:
        cells = []
        for key, _ in columns:
            value = row[key]
            value = f"{value:.5g}" if isinstance(value, (float, np.floating)) else str(value)
            cells.append(f"<td>{html.escape(value)}</td>")
        body.append("<tr>" + "".join(cells) + "</tr>")
    return (f"<table><caption>{html.escape(caption)}</caption><thead><tr>{heads}</tr></thead>"
            f"<tbody>{''.join(body)}</tbody></table>")


def response_table(record, directory, stem="tiny_notched_tension"):
    """Export all accepted increments and preview the first, then every tenth."""
    rows = record["trace"]
    path = save_table(rows, Path(directory) / f"{stem}_response.csv")
    selected = [row for row in rows if row["step"] == 1 or row["step"] % 10 == 0
                or row["step"] == rows[-1]["step"]]
    columns = [("step", "Accepted increment"), ("applied_separation", "Separation"),
               ("reaction_top_y", "Top reaction"), ("damage_outside_sum", "Nodal damage sum outside notch"),
               ("stagger_iterations", "Coupling iterations"), ("stagger_residual", "Relative iterate change")]
    table = numeric_table_html(selected, columns,
                               "Selected increments; dimensionless teaching scales. CSV contains every increment.")
    return path, table


def fracture_evolution(arrays, record, path, *, history, fps=4):
    """Animate genuine retained states with fixed damage limits and no tweening.

    Frame zero is the seeded initial state. Subsequent frames are accepted
    quasistatic increments, not physical-time samples. Gouraud shading renders
    nodal fields on the T3 mesh; no extra temporal states are manufactured.
    """
    from matplotlib.animation import FuncAnimation, PillowWriter

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    steps = history["history_steps"]
    n_steps = record["summary"]["load_steps"]
    np.testing.assert_array_equal(steps, np.arange(n_steps + 1))
    damage = history["damage_history"]
    assert damage.shape == (n_steps + 1, len(arrays["nodes"]))
    assert np.isfinite(damage).all() and damage.min() >= -1.e-10 and damage.max() <= 1 + 1.e-10
    np.testing.assert_array_equal(damage[0], arrays["seeded_damage"])
    np.testing.assert_array_equal(damage[-1], arrays["final_damage"])
    assert np.all(np.diff(damage, axis=0) >= -1.e-10)
    trace = record["trace"]
    separation = np.array([row["applied_separation"] for row in trace])
    reaction = np.array([row["reaction_top_y"] for row in trace])
    tri = mtri.Triangulation(*arrays["nodes"].T, triangles=arrays["elements"])
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), layout="constrained",
                             gridspec_kw={"width_ratios": [1.45, 1]})
    field = axes[0].tripcolor(tri, damage[0], cmap="magma", vmin=0, vmax=1, shading="gouraud")
    axes[0].set(xlabel="x [dimensionless]", ylabel="y [dimensionless]", aspect="equal")
    axes[0].grid(False)
    fig.colorbar(field, ax=axes[0], label="Damage d: 0 intact, 1 fully damaged", shrink=.8)
    axes[1].plot(separation, reaction, color="0.85", linewidth=1.2)
    curve, = axes[1].plot([], [], color="#245a81")
    point, = axes[1].plot([], [], "o", color="#d46b27")
    axes[1].set(xlabel="Separation [dimensionless]", ylabel="Top reaction [dimensionless]",
                title="Accepted response history")
    axes[1].set_xlim(0, separation[-1] * 1.03)
    heading = fig.suptitle("", fontsize=12)

    def update(index):
        field.set_array(damage[index])
        curve.set_data(separation[:index], reaction[:index])
        point.set_data(separation[index-1:index], reaction[index-1:index])
        if index == 0:
            heading.set_text("Seeded state · before equilibrium · d = 1 on the initial notch")
        else:
            row = trace[index - 1]
            heading.set_text(f"Accepted increment {index}/{n_steps} · load factor {row['load_factor']:.3f}"
                             f" · separation {row['applied_separation']:.4f}")
        axes[0].set_title("Actual PhAST diffuse damage · fixed colour scale")
        return field, curve, point, heading

    animation = FuncAnimation(fig, update, frames=len(steps), interval=1000/fps, blit=False)
    try:
        animation.save(path, writer=PillowWriter(fps=fps), dpi=90)
    finally:
        plt.close(fig)
    frames = [{"frame": int(step), "state": "seeded" if step == 0 else "accepted increment",
               "load_factor": float(history["history_load_factors"][step]),
               "damage_sha256": hashlib.sha256(damage[step].tobytes()).hexdigest()}
              for step in steps]
    receipt = {"scope": "Actual quasistatic PhAST diffuse damage; temporal interpolation disabled",
               "fields_sha256": record["fields_sha256"],
               "history_sha256": record["retained_history"]["sha256"], "frame_count": len(frames),
               "fps": fps, "duration_seconds": len(frames)/fps, "damage_limits": [0, 1],
               "frames": frames}
    path.with_suffix(".frames.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return path


def _save_figure(fig, directory, name):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    fig.savefig(directory / name, dpi=150, bbox_inches="tight")
    return fig


def bar_setup(n_elements, length, area, directory):
    """Draw the exact one-dimensional topology and its physical constraints."""
    x = np.linspace(0, length, n_elements + 1)
    fig, ax = plt.subplots(figsize=(8, 2.6), layout="constrained")
    ax.plot(x, np.zeros_like(x), "o-", color="#245a81", markersize=3)
    ax.plot([0, 0], [-.18, .18], color="#263746", linewidth=4)
    ax.annotate("", xy=(length * 1.13, 0), xytext=(length, 0),
                arrowprops={"arrowstyle": "->", "color": "#d46b27", "linewidth": 2})
    ax.text(length * .94, .24, "Tip force F", color="#b95514")
    ax.text(0, -.30, "u(0) = 0", ha="center")
    ax.text(length, -.30, r"$u_{\mathrm{tip}}$", ha="center")
    ax.set(xlim=(-.08*length, 1.18*length), ylim=(-.48, .48),
           title=f"Elastic bar · {n_elements} elements · length {length:g} · area {area:g}",
           xlabel="x [dimensionless]")
    ax.set_yticks([])
    for spine in ("left", "right", "top"):
        ax.spines[spine].set_visible(False)
    return _save_figure(fig, directory, "bar_setup.png")


def bar_sensitivity(tip_displacement, modulus, load, ad, finite_difference, exact, directory):
    """Compare the existing probe with an observational finite-difference sweep."""
    e = modulus.detach()
    steps = np.logspace(-2, -8, 13)
    with torch.no_grad():
        fd = np.array([float((tip_displacement(e + h, load) - tip_displacement(e - h, load))/(2*h))
                       for h in steps])
    rows = [{"fd_step": float(h), "finite_difference": float(value), "autograd": float(ad),
             "analytic": float(exact), "absolute_error": abs(float(value-exact))}
            for h, value in zip(steps, fd)]
    save_table(rows, Path(directory) / "bar_sensitivity_check.csv")
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.3), layout="constrained")
    axes[0].bar(["Autograd", "Central FD", "Analytic"], [float(ad), float(finite_difference), float(exact)],
                color=["#245a81", "#d46b27", "#087f83"])
    axes[0].set(ylabel="du_tip/dE [dimensionless]", title=f"Sensitivity at E={float(e):g}, F={float(load):g}")
    axes[1].loglog(steps, np.maximum(np.abs(fd-float(exact)), np.finfo(float).eps), "o-")
    axes[1].set(xlabel="Finite-difference step h", ylabel="Absolute derivative error",
                title="Step size and numerical agreement")
    return _save_figure(fig, directory, "bar_sensitivity_check.png")


def bar_initial_observations(tip_displacement, initial_modulus, true_modulus, train_loads,
                             observed_train, validation_load, observed_validation,
                             heldout_load, observed_heldout, directory):
    loads = torch.linspace(.2, 1.7, 80)
    with torch.no_grad():
        initial = np.array([float(tip_displacement(torch.tensor(initial_modulus), load)) for load in loads])
        target = np.array([float(tip_displacement(true_modulus, load)) for load in loads])
    np.savez_compressed(Path(directory) / "bar_initial_observations.npz", loads=loads.numpy(),
                        initial_response=initial, target_response=target, train_loads=train_loads.numpy(),
                        observed_train=observed_train.numpy(), validation_load=float(validation_load),
                        observed_validation=float(observed_validation), heldout_load=float(heldout_load),
                        observed_heldout=float(observed_heldout))
    fig, ax = plt.subplots(figsize=(7.5, 3.5), layout="constrained")
    ax.plot(loads, target, color="#245a81", label=f"Synthetic target E={float(true_modulus):g}")
    ax.plot(loads, initial, "--", color="#d46b27", label=f"Starting response E={initial_modulus:g}")
    ax.scatter(train_loads, observed_train, label="Training observations", color="#245a81", zorder=3)
    ax.scatter([validation_load], [observed_validation], marker="s", color="#087f83", label="Validation")
    ax.scatter([heldout_load], [observed_heldout], marker="x", color="black", label="Held-out")
    ax.set(xlabel="Tip force F [dimensionless]", ylabel="Tip displacement [dimensionless]",
           title="Starting compliance and synthetic observations")
    ax.legend(fontsize=9)
    return _save_figure(fig, directory, "bar_initial_observations.png")


def _toy_panels(problem, fields, titles, directory, name):
    fig, axes = plt.subplots(1, len(fields), figsize=(3.2*len(fields), 3.4), layout="constrained")
    for ax, field, title in zip(np.atleast_1d(axes), fields, titles):
        image = ax.imshow(field.detach().reshape(problem.ny, problem.nx).numpy(), origin="lower",
                          extent=(0, 1, 0, 1), cmap="magma", vmin=0, vmax=1)
        ax.set(title=title, xlabel="x/L", ylabel="y/H", aspect="equal")
        ax.grid(False)
    fig.colorbar(image, ax=np.atleast_1d(axes).tolist(), shrink=.78, label="Toy scalar field d [dimensionless]")
    return _save_figure(fig, directory, name)


def toy_reference_samples(problem, split_loads, directory):
    chosen = [("Train", split_loads["train"][0]), ("Train", split_loads["train"][-1]),
              ("Validation", split_loads["validation"][-1]), ("Test", split_loads["test"][-1])]
    with torch.no_grad():
        fields = [problem.reference_field(load) for _, load in chosen]
    np.savez_compressed(Path(directory) / "toy_reference_samples.npz", coordinates=problem.coordinates.numpy(),
                        load_factors=np.array([load for _, load in chosen]),
                        fields=torch.stack(fields).numpy(), splits=np.array([split for split, _ in chosen]))
    return _toy_panels(problem, fields, [f"{split}: load {load:.2f}" for split, load in chosen],
                       directory, "toy_reference_samples.png")


def toy_initial_prediction(problem, model, mean, scale, load, directory):
    from .course_tools import normalise_features
    with torch.no_grad():
        target = problem.reference_field(load)
        initial = model(normalise_features(problem.features(load), mean, scale)).squeeze(1)
    np.savez_compressed(Path(directory) / "toy_initial_prediction.npz", coordinates=problem.coordinates.numpy(),
                        load_factor=load, target=target.numpy(), initial_prediction=initial.numpy())
    return _toy_panels(problem, [target, initial], [f"Training reference: load {load:.2f}", "Initial MLP prediction"],
                       directory, "toy_initial_prediction.png")


def training_snapshot(epoch, loss, model, train_x, train_y, val_x, val_y, mean, scale):
    """Retain old metrics and add matched post-update training MSE for plotting."""
    from .course_tools import normalise_features
    with torch.no_grad():
        validation = (model(normalise_features(val_x, mean, scale)) - val_y).square().mean()
        matched_train = (model(normalise_features(train_x, mean, scale)) - train_y).square().mean()
    return {"epoch": epoch + 1, "train_mse": float(loss.detach()), "validation_mse": float(validation),
            "post_update_train_mse": float(matched_train)}


def toy_training_history(history, directory):
    save_table(history, Path(directory) / "toy_training_history.csv")
    fig, ax = plt.subplots(figsize=(7.5, 3.4), layout="constrained")
    for key, label, style in (("post_update_train_mse", "Training: updated weights", "o-"),
                              ("validation_mse", "Validation: same weights", "s--")):
        ax.semilogy([row["epoch"] for row in history], [row[key] for row in history], style, label=label)
    ax.set(xlabel="Epoch", ylabel="Mean squared field error", title="Four recorded training snapshots")
    ax.legend()
    return _save_figure(fig, directory, "toy_training_history.png")
