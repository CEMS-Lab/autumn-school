"""Verify the installed source used by the small PhAST teaching tests.

This helper reads installation metadata and source files. Installation remains
an explicit preparation step. PhAST's ``doctor`` supplies broader diagnostics.
"""
from __future__ import annotations

import base64
import hashlib
import importlib
import importlib.metadata as metadata
import importlib.util
import json
from pathlib import Path
import platform
import sys


PHAST_REPOSITORY = "https://github.com/CEMS-Lab/PhAST.git"
PHAST_REVISION = "6d1903e96874ce501f7bd466fdfd9d7b0ea10519"


class PreflightError(RuntimeError):
    """The active interpreter cannot verify the approved PhAST installation."""


def verify_installation(distribution, module_origin):
    """Check a non-editable pip VCS installation before importing PhAST.

    Pip's PEP 610 record supplies the repository and resolved commit; wheel
    RECORD hashes detect subsequent edits to installed Python sources. This
    verifies installation consistency, rather than a signed supply-chain claim.
    """
    try:
        direct = json.loads(distribution.read_text("direct_url.json") or "null")
    except (ValueError, TypeError) as exc:
        raise PreflightError("PhAST direct_url.json is invalid; reinstall the pinned requirement.") from exc
    if not isinstance(direct, dict):
        raise PreflightError("PhAST has no VCS installation record; install the pinned requirement.")
    vcs = direct.get("vcs_info", {})
    directory = direct.get("dir_info", {})
    if (direct.get("url") != PHAST_REPOSITORY
            or not isinstance(vcs, dict)
            or vcs.get("vcs") != "git"
            or vcs.get("commit_id") != PHAST_REVISION
            or not isinstance(directory, dict)
            or directory.get("editable")):
        raise PreflightError("PhAST source identity differs from the approved repository/revision.")

    package = Path(distribution.locate_file("phast")).resolve()
    expected_origin = package / "__init__.py"
    if module_origin is None or Path(module_origin).resolve() != expected_origin:
        raise PreflightError("Another phast module shadows the installed package; use a fresh kernel.")
    sources = {}
    for entry in distribution.files or ():
        name = str(entry).replace("\\", "/")
        if not name.startswith("phast/") or not name.endswith(".py"):
            continue
        installed = Path(distribution.locate_file(entry)).resolve()
        if not installed.is_relative_to(package):
            raise PreflightError(f"Source path lies outside the installed package: {name}")
        if entry.hash is None or entry.hash.mode != "sha256":
            raise PreflightError(f"Missing SHA256 in installed source record: {name}")
        try:
            digest = hashlib.sha256(installed.read_bytes()).digest()
        except OSError as exc:
            raise PreflightError(f"Cannot read installed source: {name}") from exc
        encoded = base64.urlsafe_b64encode(digest).decode().rstrip("=")
        if encoded != entry.hash.value:
            raise PreflightError(f"Installed source changed after installation: {name}")
        sources[name] = digest.hex()
    required = {"phast/__init__.py", "phast/bar.py", "phast/line_mesh.py"}
    if not required <= sources.keys():
        raise PreflightError("The installed source record is incomplete for the bar example.")
    # An extra .py can override a recorded module or add a stale submodule.
    present = {p.relative_to(package.parent).as_posix() for p in package.rglob("*.py")}
    if present != sources.keys():
        raise PreflightError("The PhAST directory contains unrecorded or missing Python sources.")
    return {
        "repository": PHAST_REPOSITORY,
        "revision": PHAST_REVISION,
        "distribution_version": distribution.version,
        "module_path": str(expected_origin),
        "checked_python_sources": len(sources),
        "source_sha256": sources,
    }


def _check_sparse_backend():
    """Load the compiled backend needed by solve_bar, without running a solve."""
    try:
        importlib.import_module("scipy.sparse.linalg")
    except (ImportError, OSError) as exc:
        raise PreflightError(
            "SciPy sparse backend could not load. Install the declared teaching "
            f"requirements in a fresh environment. Original error: {exc}"
        ) from exc


def verify_phast_environment():
    """Return source identity and environment details for a fresh interpreter.

    Call before any PhAST import. A cached module can retain old code even
    after the package on disk has been replaced; restarting resolves that case.
    """
    if sys.version_info < (3, 10):
        raise PreflightError("This teaching example requires Python 3.10 or newer.")
    if any(name == "phast" or name.startswith("phast.") for name in sys.modules):
        raise PreflightError("PhAST is already imported; run preflight first in a fresh interpreter.")
    try:
        distribution = metadata.distribution("phast")
    except metadata.PackageNotFoundError as exc:
        raise PreflightError("Install source/requirements-teaching-preflight.txt in this environment.") from exc
    spec = importlib.util.find_spec("phast")
    report = verify_installation(distribution, None if spec is None else spec.origin)
    phast = importlib.import_module("phast")
    if Path(phast.__file__).resolve() != Path(report["module_path"]):
        raise PreflightError("Imported PhAST differs from the checked installation.")
    for name in ("line_mesh", "solve_bar"):
        if not callable(getattr(phast, name, None)):
            raise PreflightError(f"The verified installation does not expose phast.{name}.")
    _check_sparse_backend()
    report["environment"] = {
        "python": platform.python_version(),
        "executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "test_device": "cpu",
        "test_dtype": "torch.float64",
        "sparse_backend_import": "passed",
        "packages": {name: metadata.version(name) for name in
                     ("torch", "numpy", "scipy", "matplotlib", "gmsh", "meshio", "zarr")},
    }
    return report


if __name__ == "__main__":
    try:
        print(json.dumps(verify_phast_environment(), indent=2, sort_keys=True))
    except PreflightError as exc:
        raise SystemExit(f"Teaching preflight: {exc}") from exc
