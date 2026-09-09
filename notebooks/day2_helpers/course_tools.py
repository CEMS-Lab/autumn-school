"""Reproducible helpers for the UKACM day-two teaching notebooks.

There are two deliberately different scopes in this module:

* ``run_notched_tension`` imports the pinned *public* PhAST source and runs a
  small AT2 phase-field calculation.
* ``ToyHelmholtzProblem`` and the MLP/adapter utilities are original,
  course-owned tensor examples.  They are not PhAST fracture data, a PhAST
  learned-damage checkpoint, or a paper workflow.

Keeping these boundaries in one place makes the notebooks safe to reuse and
easy to audit.
"""

from __future__ import annotations

import importlib
import hashlib
import json
import os
import subprocess
import sys
import time
import warnings
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import torch
from torch import nn


EXPECTED_PHAST_REVISION = "f6324f899f0701769810be117f27f1208f7a582e"
EXPECTED_PHAST_VERSION = "0.16.2"
FEATURE_ORDER = ("x_over_L", "y_over_H", "load_factor")
TOY_INTERFACE_VERSION = "ukacm-toy-damage-v1"


def course_root() -> Path:
    """Return the course directory without relying on the current directory."""
    return Path(__file__).resolve().parents[2]


def assets_dir() -> Path:
    path = course_root() / "assets" / "day2_forward"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _candidate_public_sources() -> Iterable[Path]:
    # A course bundle is self-contained and takes precedence over a sibling
    # checkout.  Its manifest is verified below when Git metadata is absent.
    yield course_root() / "vendor" / "PhAST" / "src"

    explicit = os.environ.get("PHAST_PUBLIC_SRC")
    if explicit:
        yield Path(explicit).expanduser()

    # The checked course worktree is nested below ``neural_operator``.  Search
    # ancestors so the notebooks can also run from a copied course directory
    # when PHAST_PUBLIC_SRC is set explicitly.
    for base in (Path.cwd(), *Path.cwd().parents, course_root(), *course_root().parents):
        yield base / "PhAST" / "src"


def public_phast_source() -> Path:
    """Locate a public source tree with a usable ``phast`` package."""
    checked: list[str] = []
    for candidate in _candidate_public_sources():
        candidate = candidate.resolve()
        checked.append(candidate.name)
        if (candidate / "phast" / "__init__.py").is_file():
            return candidate
    raise FileNotFoundError(
        "Could not locate public PhAST source. Set PHAST_PUBLIC_SRC to the "
        "repository's src directory or unpack vendor/PhAST. Checked source "
        "directory names: " + "; ".join(checked)
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _verify_vendor_manifest(repository: Path, expected_revision: str) -> str:
    """Verify the bundled public tree when it has no Git metadata.

    ``COURSE_SOURCE_MANIFEST.json`` is intentionally a flat, portable contract:
    ``{"revision": "...", "files": {"src/phast/...": "sha256"}}``.
    Every regular source-tree file must be represented and hash-identical before
    the interpreter imports it.
    """
    manifest_path = repository / "COURSE_SOURCE_MANIFEST.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(
            "Vendored PhAST source has no .git directory and no "
            "COURSE_SOURCE_MANIFEST.json verification record."
        )
    with manifest_path.open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    revision = manifest.get("revision")
    if revision != expected_revision:
        raise RuntimeError(
            "Vendored PhAST manifest revision differs from the teaching pin: "
            f"got {revision!r}, expected {expected_revision!r}."
        )
    declared = manifest.get("files")
    if not isinstance(declared, dict):
        raise ValueError("Vendored PhAST manifest must map relative paths to SHA-256 hashes.")
    actual_paths = {
        path.relative_to(repository).as_posix()
        for path in (repository / "src").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    declared_paths = {path for path in declared if path.startswith("src/")}
    if actual_paths != declared_paths:
        missing = sorted(actual_paths - declared_paths)
        extra = sorted(declared_paths - actual_paths)
        raise RuntimeError(
            "Vendored PhAST source files do not match the manifest "
            f"(missing={missing[:3]}, extra={extra[:3]})."
        )
    for relative_path in sorted(actual_paths):
        expected_hash = declared[relative_path]
        actual_hash = _sha256(repository / relative_path)
        if actual_hash != expected_hash:
            raise RuntimeError(
                "Vendored PhAST source hash mismatch for "
                f"{relative_path}; refuse to import an unverified source tree."
            )
    return revision


def _public_route_label(source: Path) -> str:
    vendor_source = (course_root() / "vendor" / "PhAST" / "src").resolve()
    if source == vendor_source:
        return "vendor/PhAST/src (manifest-verified when vendored)"
    return "<external-public-PhAST>/src (Git revision verified)"


def import_public_phast(expected_revision: str = EXPECTED_PHAST_REVISION) -> dict[str, str]:
    """Put the public source first on ``sys.path`` and verify its revision.

    This is intentionally stricter than a plain ``import phast`` because this
    course worktree sits beside a private development checkout which may also
    be importable in the same Python environment.
    """
    source = public_phast_source()
    source_text = str(source)
    if source_text in sys.path:
        sys.path.remove(source_text)
    sys.path.insert(0, source_text)
    for name in tuple(sys.modules):
        if name == "phast" or name.startswith("phast."):
            del sys.modules[name]
    importlib.invalidate_caches()
    phast = importlib.import_module("phast")
    imported_file = Path(phast.__file__).resolve()
    if source not in imported_file.parents:
        raise RuntimeError(
            "The import did not resolve to the requested public source: "
            f"{imported_file} (expected below {source})."
        )

    repository = source.parent
    if (repository / ".git").exists():
        revision = subprocess.check_output(
            ["git", "-C", str(repository), "rev-parse", "HEAD"], text=True
        ).strip()
        verification = "Git revision verified"
    elif source == (course_root() / "vendor" / "PhAST" / "src").resolve():
        revision = _verify_vendor_manifest(repository, expected_revision)
        verification = "COURSE_SOURCE_MANIFEST.json hashes verified"
    else:
        raise RuntimeError(
            "A non-vendored PhAST source without Git metadata cannot be pinned. "
            "Use the course bundle or a public Git checkout."
        )
    if expected_revision and revision != expected_revision:
        raise RuntimeError(
            "Public PhAST revision differs from the teaching pin: "
            f"got {revision}, expected {expected_revision}."
        )
    return {
        "source": _public_route_label(source),
        "module_file": "phast/__init__.py",
        "revision": revision,
        "version": EXPECTED_PHAST_VERSION,
        "import_route": "PYTHONPATH=<public-PhAST>/src",
        "verification": verification,
    }


def load_forward_config() -> dict[str, Any]:
    path = course_root() / "configs" / "day2_forward" / "tiny_notched_tension.json"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _structured_triangles(nx: int, ny: int) -> torch.Tensor:
    elements: list[tuple[int, int, int]] = []
    for j in range(ny):
        for i in range(nx):
            lower_left = j * (nx + 1) + i
            elements.extend(
                (
                    (lower_left, lower_left + 1, lower_left + nx + 2),
                    (lower_left, lower_left + nx + 2, lower_left + nx + 1),
                )
            )
    return torch.tensor(elements, dtype=torch.long)


def run_notched_tension(
    config: dict[str, Any] | None = None,
    *,
    artifact_dir: Path | None = None,
    write_artifacts: bool = True,
) -> dict[str, Any]:
    """Run the selected public PhAST quasi-static AT2 teaching calculation.

    The ``load_factor`` is set before each ``step_full`` call.  Consequently
    this calculation advances a quasi-static load history; it does not claim
    physical dynamic time integration.
    """
    config = load_forward_config() if config is None else config
    phast_info = import_public_phast(config["public_source"]["revision"])
    from phast.core.mesh import FEMMesh
    from phast.physics.boundary_conditions import symmetric_tension_bcs
    from phast.physics.material import Material
    from phast.solvers.staggered_solver import SolverConfig, StaggeredSolver

    torch.manual_seed(int(config["seed"]))
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    geometry = config["geometry"]
    mesh_cfg = config["mesh"]
    material_cfg = config["material"]
    loading = config["loading"]
    solver_cfg = config["solver"]
    dtype = torch.float64
    width, height = float(geometry["width"]), float(geometry["height"])
    nx, ny = int(mesh_cfg["nx"]), int(mesh_cfg["ny"])
    if ny % 2:
        raise ValueError("ny must be even so the centreline is represented exactly.")

    setup_start = time.perf_counter()
    x = torch.linspace(0.0, width, nx + 1, dtype=dtype)
    y = torch.linspace(0.0, height, ny + 1, dtype=dtype)
    xx, yy = torch.meshgrid(x, y, indexing="xy")
    nodes = torch.stack((xx.reshape(-1), yy.reshape(-1)), dim=1)
    mesh = FEMMesh.from_tensors(
        nodes, _structured_triangles(nx, ny), device="cpu", dtype=dtype
    )
    mesh.identify_boundaries()
    bcs = symmetric_tension_bcs(
        mesh, disp=float(loading["total_symmetric_vertical_displacement"])
    )
    centreline = (nodes[:, 1] - height / 2).abs() < 1.0e-12
    precrack = centreline & (nodes[:, 0] <= float(geometry["notch_length"]) + 1.0e-12)
    precrack_nodes = torch.where(precrack)[0]
    bcs.add_pf_dirichlet(precrack_nodes, value=1.0)
    material = Material(
        E=float(material_cfg["E"]),
        nu=float(material_cfg["nu"]),
        Gc=float(material_cfg["Gc"]),
        l0=float(material_cfg["l0"]),
        rho=float(material_cfg["rho"]),
        eta_residual=float(material_cfg["eta_residual"]),
        energy_split=material_cfg["energy_split"],
        pf_model=material_cfg["pf_model"],
    )
    solver = StaggeredSolver(
        mesh,
        material,
        bcs,
        SolverConfig(
            solver_type=solver_cfg["solver_type"],
            backend=solver_cfg["mechanics_backend"],
            preconditioner=solver_cfg["damage_preconditioner"],
            use_multigrid=bool(solver_cfg["use_multigrid"]),
            static_tol=float(solver_cfg["static_tol"]),
            static_max_iter=int(solver_cfg["static_max_iter"]),
            damage_tol=float(solver_cfg["damage_tol"]),
            damage_max_iter=int(solver_cfg["damage_max_iter"]),
            stagger_tol=float(solver_cfg["stagger_tol"]),
            max_stagger=int(solver_cfg["max_stagger"]),
            fail_on_mechanics_nonconvergence=bool(
                solver_cfg["fail_on_mechanics_nonconvergence"]
            ),
            fail_on_stagger_nonconvergence=bool(
                solver_cfg["fail_on_stagger_nonconvergence"]
            ),
        ),
    )
    # Make the initial locked crack visible before the first staggered solve.
    solver.d[precrack_nodes] = 1.0
    seeded_damage = solver.d.detach().clone()
    setup_seconds = time.perf_counter() - setup_start

    n_steps = int(loading["n_load_steps"])
    load_factors = torch.linspace(
        float(loading["first_load_factor"]),
        float(loading["last_load_factor"]),
        n_steps,
        dtype=dtype,
    )
    outside_precrack = ~precrack
    top_nodes = mesh.node_sets["top"]
    snapshots: dict[int, torch.Tensor] = {0: seeded_damage}
    trace: list[dict[str, float]] = []
    captured_warnings: list[str] = []
    solve_start = time.perf_counter()
    for step, load_factor in enumerate(load_factors, start=1):
        step_start = time.perf_counter()
        bcs.load_factor = float(load_factor)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            solver.step_full()
        captured_warnings.extend(str(item.message) for item in caught)
        internal_force = solver.fem.internal_force(solver.u, solver.d)
        damage_outside = solver.d[outside_precrack]
        trace.append(
            {
                "step": float(step),
                "load_factor": float(load_factor),
                "reaction_top_y": float(internal_force[top_nodes, 1].sum()),
                "damage_outside_sum": float(damage_outside.sum()),
                "damage_outside_max": float(damage_outside.max()),
                "max_displacement": float(solver.u.abs().max()),
                "stagger_iterations": float(solver._last_stagger_iter),
                "stagger_residual": float(solver._last_residual),
                "step_seconds": time.perf_counter() - step_start,
            }
        )
        if step in {1, n_steps // 2, n_steps}:
            snapshots[step] = solver.d.detach().clone()
    solve_seconds = time.perf_counter() - solve_start
    first_damage = snapshots[1]
    final_damage = snapshots[n_steps]
    incremental_damage = (final_damage - first_damage).clamp_min(0.0)
    result = {
        "config": config,
        "phast": phast_info,
        "mesh": mesh,
        "solver": solver,
        "nodes": nodes,
        "elements": mesh.elements,
        "precrack": precrack,
        "outside_precrack": outside_precrack,
        "seeded_damage": seeded_damage,
        "first_damage": first_damage,
        "final_damage": final_damage,
        "incremental_damage": incremental_damage,
        "trace": trace,
        "snapshots": snapshots,
        "setup_seconds": setup_seconds,
        "solve_seconds": solve_seconds,
        "warnings": captured_warnings,
        "summary": {
            "nodes": int(mesh.n_nodes),
            "elements": int(mesh.n_elems),
            "load_steps": n_steps,
            "dtype": str(dtype).replace("torch.", ""),
            "setup_seconds": setup_seconds,
            "solve_seconds": solve_seconds,
            "damage_outside_initial_sum": float(first_damage[outside_precrack].sum()),
            "damage_outside_final_sum": float(final_damage[outside_precrack].sum()),
            "incremental_damage_outside_sum": float(
                incremental_damage[outside_precrack].sum()
            ),
            "incremental_damage_outside_max": float(
                incremental_damage[outside_precrack].max()
            ),
            "final_damage_outside_max": float(final_damage[outside_precrack].max()),
            "all_steps_returned_with_failure_flags_enabled": True,
            "warnings": captured_warnings,
        },
    }
    if write_artifacts:
        artifact_dir = assets_dir() if artifact_dir is None else artifact_dir
        artifact_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = artifact_dir / "tiny_notched_tension_summary.json"
        with artifact_path.open("w", encoding="utf-8") as handle:
            json.dump(result["summary"] | {"phast": phast_info, "trace": trace}, handle, indent=2)
        np.savez_compressed(
            artifact_dir / "tiny_notched_tension_fields.npz",
            nodes=nodes.detach().cpu().numpy(),
            elements=mesh.elements.detach().cpu().numpy(),
            precrack=precrack.detach().cpu().numpy(),
            seeded_damage=seeded_damage.detach().cpu().numpy(),
            first_damage=first_damage.detach().cpu().numpy(),
            final_damage=final_damage.detach().cpu().numpy(),
            incremental_damage=incremental_damage.detach().cpu().numpy(),
        )
    return result


class ToyHelmholtzProblem:
    """Course-owned linear field problem for the inverse/model notebooks.

    It is a tiny finite-difference Helmholtz-like field equation with a
    load-scaled source.  It is intentionally *not* an AT2 fracture equation;
    its role is to provide fast, inspectable data and a genuine discrete
    residual for the adapter/fallback lesson.
    """

    def __init__(self, nx: int = 25, ny: int = 13, length_scale: float = 0.09):
        self.nx, self.ny = int(nx), int(ny)
        self.length_scale = float(length_scale)
        self.dtype = torch.float64
        self.x = torch.linspace(0.0, 1.0, self.nx, dtype=self.dtype)
        self.y = torch.linspace(0.0, 1.0, self.ny, dtype=self.dtype)
        xx, yy = torch.meshgrid(self.x, self.y, indexing="xy")
        self.coordinates = torch.stack((xx.reshape(-1), yy.reshape(-1)), dim=1)
        self.n_nodes = self.coordinates.shape[0]
        self.boundary_mask = (
            (self.coordinates[:, 0] == 0.0)
            | (self.coordinates[:, 0] == 1.0)
            | (self.coordinates[:, 1] == 0.0)
            | (self.coordinates[:, 1] == 1.0)
        )
        self.matrix = self._matrix()

    @property
    def mesh_signature(self) -> tuple[int, int]:
        return (self.nx, self.ny)

    def _index(self, i: int, j: int) -> int:
        return j * self.nx + i

    def _matrix(self) -> torch.Tensor:
        # The grid is rectangular (25 by 13 by default), so its horizontal
        # and vertical spacings must remain separate.  A single ``h`` would
        # silently turn the intended isotropic physical length scale into an
        # anisotropic discrete operator.
        hx = 1.0 / (self.nx - 1)
        hy = 1.0 / (self.ny - 1)
        alpha_x = (self.length_scale / hx) ** 2
        alpha_y = (self.length_scale / hy) ** 2
        matrix = torch.zeros((self.n_nodes, self.n_nodes), dtype=self.dtype)
        for j in range(self.ny):
            for i in range(self.nx):
                index = self._index(i, j)
                if i in {0, self.nx - 1} or j in {0, self.ny - 1}:
                    matrix[index, index] = 1.0
                else:
                    matrix[index, index] = 1.0 + 2.0 * alpha_x + 2.0 * alpha_y
                    matrix[index, self._index(i - 1, j)] = -alpha_x
                    matrix[index, self._index(i + 1, j)] = -alpha_x
                    matrix[index, self._index(i, j - 1)] = -alpha_y
                    matrix[index, self._index(i, j + 1)] = -alpha_y
        return matrix

    def source(self, load_factor: float | torch.Tensor) -> torch.Tensor:
        load = torch.as_tensor(load_factor, dtype=self.dtype)
        x, y = self.coordinates[:, 0], self.coordinates[:, 1]
        notch = torch.exp(-((x - 0.22) / 0.13) ** 2 - ((y - 0.5) / 0.18) ** 2)
        wing = 0.35 * torch.exp(-((x - 0.48) / 0.30) ** 2 - ((y - 0.5) / 0.38) ** 2)
        # The amplitude keeps the exact linear solve inside [0, 1] over the
        # teaching load range, so its reported residual is not distorted by a
        # post-solve clamp.
        source = 1.4 * load * (notch + wing)
        return torch.where(self.boundary_mask, torch.zeros_like(source), source)

    def reference_field(self, load_factor: float | torch.Tensor) -> torch.Tensor:
        field = torch.linalg.solve(self.matrix, self.source(load_factor))
        return field.clamp(0.0, 1.0)

    def features(self, load_factor: float | torch.Tensor) -> torch.Tensor:
        load = torch.full((self.n_nodes, 1), float(load_factor), dtype=self.dtype)
        return torch.cat((self.coordinates, load), dim=1)

    def relative_residual(self, field: torch.Tensor, load_factor: float) -> float:
        field = field.to(dtype=self.dtype).reshape(-1)
        residual = self.matrix @ field - self.source(load_factor)
        return float(residual.norm() / (self.source(load_factor).norm() + 1.0e-15))

    def case_tensor(self, load_factors: Iterable[float]) -> tuple[torch.Tensor, torch.Tensor]:
        features, targets = [], []
        for load in load_factors:
            features.append(self.features(float(load)))
            targets.append(self.reference_field(float(load)).unsqueeze(1))
        return torch.cat(features), torch.cat(targets)


class TinyDamageMLP(nn.Module):
    """The one trainable architecture used in the course-owned toy."""

    def __init__(self, width: int = 32):
        super().__init__()
        self.width = int(width)
        self.network = nn.Sequential(
            nn.Linear(3, self.width),
            nn.SiLU(),
            nn.Linear(self.width, self.width),
            nn.SiLU(),
            nn.Linear(self.width, 1),
            nn.Sigmoid(),
        )

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.network(features)


def _normalisation(features: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    mean = features.mean(dim=0)
    scale = features.std(dim=0).clamp_min(1.0e-12)
    return mean, scale


def normalise_features(features: torch.Tensor, mean: torch.Tensor, scale: torch.Tensor) -> torch.Tensor:
    return (features - mean) / scale


def make_toy_checkpoint(
    checkpoint_path: Path | None = None,
    *,
    epochs: int = 400,
    seed: int = 20260909,
    force: bool = True,
) -> dict[str, Any]:
    """Train and save the small course-owned MLP with whole-case splits."""
    checkpoint_path = checkpoint_path or assets_dir() / "models" / "tiny_damage_mlp.pt"
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    if checkpoint_path.exists() and not force:
        return torch.load(checkpoint_path, map_location="cpu", weights_only=True)

    torch.manual_seed(seed)
    # This tiny full-batch training task gains no practical speed from parallel
    # reductions; one thread also makes its teaching receipt repeatable.
    torch.set_num_threads(1)
    problem = ToyHelmholtzProblem()
    split_loads = {
        "train": tuple(np.linspace(0.12, 0.76, 12)),
        "validation": (0.82, 0.88),
        "test": (0.94, 1.00),
    }
    train_x, train_y = problem.case_tensor(split_loads["train"])
    val_x, val_y = problem.case_tensor(split_loads["validation"])
    test_x, test_y = problem.case_tensor(split_loads["test"])
    mean, scale = _normalisation(train_x)
    model = TinyDamageMLP(width=32).to(dtype=torch.float64)
    optimizer = torch.optim.Adam(model.parameters(), lr=1.5e-2)
    history: list[dict[str, float]] = []
    start = time.perf_counter()
    for epoch in range(int(epochs)):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        prediction = model(normalise_features(train_x, mean, scale))
        loss = torch.mean((prediction - train_y) ** 2)
        loss.backward()
        optimizer.step()
        if epoch in {0, 24, 99, int(epochs) - 1}:
            model.eval()
            with torch.no_grad():
                validation_loss = torch.mean(
                    (model(normalise_features(val_x, mean, scale)) - val_y) ** 2
                )
            history.append(
                {
                    "epoch": float(epoch + 1),
                    "train_mse": float(loss.detach()),
                    "validation_mse": float(validation_loss),
                }
            )
    train_seconds = time.perf_counter() - start
    model.eval()
    with torch.no_grad():
        test_prediction = model(normalise_features(test_x, mean, scale))
        test_rmse = float(torch.sqrt(torch.mean((test_prediction - test_y) ** 2)))
    metadata = {
        "interface_version": TOY_INTERFACE_VERSION,
        "architecture": "TinyDamageMLP",
        "width": model.width,
        "feature_order": list(FEATURE_ORDER),
        "feature_location": "node",
        "feature_units": ["dimensionless x/L", "dimensionless y/H", "dimensionless"],
        "output": "toy_damage_proposal at nodes; d=0 intact-like, d=1 saturated",
        "dtype": "float64",
        "device": "cpu",
        "mesh_signature": list(problem.mesh_signature),
        "normalisation_mean": mean.tolist(),
        "normalisation_scale": scale.tolist(),
        "splits": {name: [float(value) for value in values] for name, values in split_loads.items()},
        "data_provenance": "course-owned ToyHelmholtzProblem; not PhAST or research data",
        "seed": seed,
        "epochs": int(epochs),
    }
    checkpoint = {
        "state_dict": model.state_dict(),
        "metadata": metadata,
        "history": history,
        "metrics": {"test_rmse": test_rmse, "training_seconds": train_seconds},
    }
    torch.save(checkpoint, checkpoint_path)
    with checkpoint_path.with_suffix(".metadata.json").open("w", encoding="utf-8") as handle:
        json.dump(metadata | checkpoint["metrics"], handle, indent=2)
    return checkpoint


def load_toy_model(checkpoint_path: Path | None = None) -> tuple[TinyDamageMLP, dict[str, Any]]:
    checkpoint_path = checkpoint_path or assets_dir() / "models" / "tiny_damage_mlp.pt"
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    metadata = checkpoint["metadata"]
    if metadata.get("interface_version") != TOY_INTERFACE_VERSION:
        raise ValueError("Unsupported teaching-model interface version.")
    model = TinyDamageMLP(width=int(metadata["width"])).to(dtype=torch.float64)
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    return model, metadata


class ToyDamageAdapter:
    """A teaching adapter: compatibility, projection, residual, fallback.

    It mirrors the *shape* of an adapter boundary—rather than claiming that a
    trained checkpoint is automatically portable to PhAST.  The residual is
    for ``ToyHelmholtzProblem`` only.
    """

    def __init__(self, model: TinyDamageMLP, metadata: dict[str, Any], problem: ToyHelmholtzProblem):
        self.model = model.eval()
        self.metadata = metadata
        self.problem = problem
        self.mean = torch.tensor(metadata["normalisation_mean"], dtype=torch.float64)
        self.scale = torch.tensor(metadata["normalisation_scale"], dtype=torch.float64)

    def _check(self, feature_order: Iterable[str], mesh_signature: Iterable[int], features: torch.Tensor) -> None:
        if not torch.isfinite(features).all():
            raise ValueError("Incompatible feature tensor: all adapter inputs must be finite.")
        if tuple(feature_order) != tuple(self.metadata["feature_order"]):
            raise ValueError(
                "Incompatible feature order. Expected "
                f"{self.metadata['feature_order']}, got {list(feature_order)}."
            )
        if tuple(mesh_signature) != tuple(self.metadata["mesh_signature"]):
            raise ValueError(
                "Incompatible mesh signature. Expected "
                f"{self.metadata['mesh_signature']}, got {list(mesh_signature)}."
            )
        if tuple(features.shape) != (self.problem.n_nodes, len(FEATURE_ORDER)):
            raise ValueError(
                "Incompatible feature tensor shape. Expected "
                f"({self.problem.n_nodes}, {len(FEATURE_ORDER)}), got {tuple(features.shape)}."
            )

    def propose(
        self,
        features: torch.Tensor,
        *,
        feature_order: Iterable[str] = FEATURE_ORDER,
        mesh_signature: Iterable[int] | None = None,
        d_previous: torch.Tensor | None = None,
    ) -> torch.Tensor:
        mesh_signature = self.problem.mesh_signature if mesh_signature is None else mesh_signature
        self._check(feature_order, mesh_signature, features)
        with torch.no_grad():
            proposal = self.model(normalise_features(features.to(torch.float64), self.mean, self.scale)).squeeze(1)
        proposal = proposal.clamp(0.0, 1.0)
        if d_previous is not None:
            proposal = torch.maximum(proposal, d_previous.to(torch.float64))
        return torch.where(self.problem.boundary_mask, torch.zeros_like(proposal), proposal)

    def assess(self, proposal: torch.Tensor, load_factor: float, *, residual_limit: float = 0.12) -> dict[str, Any]:
        residual = self.problem.relative_residual(proposal, load_factor)
        return {
            "toy_relative_residual": residual,
            "residual_limit": float(residual_limit),
            "accepted": bool(residual <= residual_limit),
            "scope": "ToyHelmholtzProblem residual only; not a PhAST AT2 residual",
        }

    def fallback(self, load_factor: float, d_previous: torch.Tensor | None = None) -> torch.Tensor:
        corrected = self.problem.reference_field(load_factor)
        if d_previous is not None:
            corrected = torch.maximum(corrected, d_previous.to(torch.float64))
        return corrected
