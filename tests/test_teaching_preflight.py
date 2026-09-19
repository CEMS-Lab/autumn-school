"""Source-identity checks run without installing or importing PhAST."""
import base64
import hashlib
from importlib.metadata import PackagePath
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

from scripts import teaching_preflight as preflight


@pytest.fixture
def installation(tmp_path):
    entries = []
    for name in ("__init__.py", "bar.py", "line_mesh.py"):
        path = tmp_path / "phast" / name
        path.parent.mkdir(exist_ok=True)
        path.write_text("# minimal metadata fixture\n")
        digest = base64.urlsafe_b64encode(hashlib.sha256(path.read_bytes()).digest()).decode().rstrip("=")
        entry = PackagePath("phast/" + name)
        entry.hash = SimpleNamespace(mode="sha256", value=digest)
        entries.append(entry)
    direct = {
        "url": preflight.PHAST_REPOSITORY,
        "vcs_info": {"vcs": "git", "commit_id": preflight.PHAST_REVISION},
    }
    dist = SimpleNamespace(
        version="test", files=entries,
        locate_file=lambda name: tmp_path / str(name),
        read_text=lambda name: json.dumps(direct),
    )
    return dist, direct, tmp_path / "phast" / "__init__.py"


def test_verified_vcs_record(installation):
    dist, _, origin = installation
    result = preflight.verify_installation(dist, origin)
    assert result["revision"] == preflight.PHAST_REVISION
    assert result["checked_python_sources"] == 3


@pytest.mark.parametrize("change", ["repository", "revision", "editable", "missing", "malformed"])
def test_rejects_unverified_identity(installation, change):
    dist, direct, origin = installation
    if change == "repository":
        direct["url"] = "https://example.org/phast.git"
    elif change == "revision":
        direct["vcs_info"]["commit_id"] = "0" * 40
    elif change == "editable":
        direct["dir_info"] = {"editable": True}
    elif change == "missing":
        dist.read_text = lambda name: None
    else:
        dist.read_text = lambda name: "{"
    with pytest.raises(preflight.PreflightError):
        preflight.verify_installation(dist, origin)


def test_rejects_shadowed_import(installation, tmp_path):
    dist, _, _ = installation
    with pytest.raises(preflight.PreflightError, match="shadows"):
        preflight.verify_installation(dist, tmp_path / "other" / "__init__.py")


@pytest.mark.parametrize("change", ["modified", "missing", "unrecorded", "unhashed", "incomplete"])
def test_rejects_source_changes(installation, change):
    dist, _, origin = installation
    if change == "modified":
        origin.write_text("# modified after installation\n")
    elif change == "missing":
        origin.unlink()
    elif change == "unrecorded":
        (origin.parent / "unexpected.py").write_text("# unrecorded\n")
    elif change == "unhashed":
        dist.files[0].hash = None
    else:
        dist.files = []
    with pytest.raises(preflight.PreflightError):
        preflight.verify_installation(dist, origin)


def test_requires_fresh_interpreter(monkeypatch):
    monkeypatch.setitem(sys.modules, "phast", SimpleNamespace())
    with pytest.raises(preflight.PreflightError, match="fresh interpreter"):
        preflight.verify_phast_environment()


def test_requirement_matches_verified_revision():
    requirement = (Path(__file__).resolve().parents[1] /
                   "source/requirements-teaching-preflight.txt").read_text()
    assert f"phast @ git+{preflight.PHAST_REPOSITORY}@{preflight.PHAST_REVISION}" in requirement


def test_reports_compiled_backend_error(monkeypatch):
    def broken_backend(name):
        raise ImportError("test binary could not load")
    monkeypatch.setattr(preflight.importlib, "import_module", broken_backend)
    with pytest.raises(preflight.PreflightError, match="test binary could not load"):
        preflight._check_sparse_backend()
