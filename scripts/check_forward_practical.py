"""Check the retained Practical 1 result contract and its tamper safeguards."""
import copy
import json
from pathlib import Path
import sys
import tempfile

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "notebooks"))
from day2_helpers.forward_workflow import load_results, digest_file, notebook_source_hash


def rejects(function):
    try:
        function()
    except (AssertionError, ValueError, KeyError):
        return
    raise AssertionError("A malformed result was accepted")


def main():
    folder = ROOT / "assets/day2_forward"
    archives = []
    for stem in ("tiny_notched_tension", "tiny_notched_tension_half_load"):
        fields = folder / f"{stem}_fields.npz"
        metadata = folder / f"{stem}_summary.json"
        arrays, record = load_results(fields, metadata)
        archives.append((arrays, record))
        assert arrays["nodes"].shape == (8385, 2)
        assert arrays["elements"].shape == (16384, 3)
        assert arrays["precrack"].sum() == 26
        assert np.all(arrays["seeded_damage"][arrays["precrack"]] == 1)
        assert np.all(arrays["seeded_damage"][~arrays["precrack"]] == 0)
        assert np.all(np.diff(arrays["damage_snapshots"], axis=0) >= -1.e-10)
        assert np.array_equal(arrays["snapshot_steps"], [0, 1, 30, 60])
        assert len(record["trace"]) == 60
        assert max(row["stagger_residual"] for row in record["trace"]) <= record["config"]["solver"]["stagger_tol"]
        assert max(row["boundary_value_error"] for row in record["trace"]) <= 1.e-10
        assert record["checks"]["warning_count"] == 0
        assert record["checks"]["strict_mechanics_and_stagger_flags"]
        assert record["resolved_model"]["plane_stress"] is False
        assert record["resolved_model"]["kinematics"] == "plane strain"
        assert record["resolved_solver"]["stagger_criterion"] == "relative"
        assert record["resolved_solver"]["stagger_norm"] == "l2"

        with tempfile.TemporaryDirectory(prefix="phast-forward-contract-") as tmp:
            tmp = Path(tmp)
            # An edited configuration must invalidate the original hash.
            changed = copy.deepcopy(record)
            changed["config"]["geometry"]["width"] += 1
            changed_metadata = tmp / "changed.json"
            changed_metadata.write_text(json.dumps(changed))
            rejects(lambda: load_results(fields, changed_metadata))
            # Shape checks remain effective even for a correctly hashed archive.
            changed_arrays = dict(arrays)
            changed_arrays["final_displacement"] = arrays["final_displacement"][:-1]
            changed_fields = tmp / "wrong-shape.npz"
            np.savez_compressed(changed_fields, **changed_arrays)
            changed = copy.deepcopy(record)
            changed["fields_sha256"] = digest_file(changed_fields)
            changed_metadata.write_text(json.dumps(changed))
            rejects(lambda: load_results(changed_fields, changed_metadata))
            # Boundary arrays are required by the post-processing notebook.
            malformed = []
            for boundary_name in ("left", "right", "top", "bottom"):
                missing = dict(arrays)
                del missing[f"boundary_{boundary_name}"]
                malformed.append(missing)
            for invalid_indices in (np.array([0., 1.]), np.array([-1, 0]),
                                    np.array([0, 8385]), np.array([0, 0]),
                                    np.array([], dtype=int), np.array([[0, 1]])):
                malformed.append(dict(arrays, boundary_left=invalid_indices))
            for invalid_steps in (np.array([0., 1., 30., 60.]), np.array([0, 1, 1, 60]),
                                  np.array([0, 30, 1, 60]), np.array([0, 1, 30, 61]),
                                  np.array([-1, 1, 30, 60]), np.array([1, 2, 30, 60]),
                                  np.array([0, 1, 30, 59])):
                malformed.append(dict(arrays, snapshot_steps=invalid_steps))
            for name, index in (("damage_snapshots", 0), ("damage_snapshots", 1),
                                ("damage_snapshots", -1), ("displacement_snapshots", -1)):
                changed_snapshot = arrays[name].copy()
                changed_snapshot[index].flat[0] += .1
                malformed.append(dict(arrays, **{name: changed_snapshot}))
            # Direct ordering comparisons also cover unsigned integer IDs.
            unsigned_reordered = dict(arrays, snapshot_steps=np.array([0, 1, 30, 20, 60], dtype=np.uint64))
            for name in ("damage_snapshots", "displacement_snapshots"):
                unsigned_reordered[name] = arrays[name][[0, 1, 2, 2, 3]]
            malformed.append(unsigned_reordered)
            for changed_arrays in malformed:
                np.savez_compressed(changed_fields, **changed_arrays)
                changed = copy.deepcopy(record)
                changed["fields_sha256"] = digest_file(changed_fields)
                changed_metadata.write_text(json.dumps(changed))
                rejects(lambda: load_results(changed_fields, changed_metadata))
    full, half = archives
    np.testing.assert_array_equal(full[0]["nodes"], half[0]["nodes"])
    np.testing.assert_array_equal(full[0]["elements"], half[0]["elements"])
    original_config, changed_config = copy.deepcopy(full[1]["config"]), copy.deepcopy(half[1]["config"])
    original_config["loading"]["total_symmetric_vertical_displacement"] *= .5
    assert original_config == changed_config
    assert half[0]["final_damage"][~half[0]["precrack"]].sum() < full[0]["final_damage"][~full[0]["precrack"]].sum()
    receipt = json.loads((folder / "tiny_notched_tension_notebook_receipt.json").read_text())
    assert receipt["computation_seconds"] < 300
    for name, recorded_hash in receipt["source_hashes"].items():
        assert digest_file(ROOT / name) == recorded_hash, name
    notebook = receipt["notebook_source"]
    assert notebook_source_hash(ROOT / notebook["path"]) == notebook["cell_source_sha256"]
    with tempfile.TemporaryDirectory(prefix="phast-notebook-source-") as tmp:
        altered = json.loads((ROOT / notebook["path"]).read_text())
        first_code = next(cell for cell in altered["cells"] if cell["cell_type"] == "code")
        first_code.update(outputs=[{"output_type": "stream", "name": "stdout", "text": "retained output"}], execution_count=7)
        altered_path = Path(tmp) / "retained.ipynb"
        altered_path.write_text(json.dumps(altered))
        assert notebook_source_hash(altered_path) == notebook["cell_source_sha256"]
        first_code["source"] = "changed computation"
        altered_path.write_text(json.dumps(altered))
        assert notebook_source_hash(altered_path) != notebook["cell_source_sha256"]
    print("Forward practical: both 60-step cases, portable schema, source hashes, reload integrity, physical-state checks and malformed-file rejection passed.")


if __name__ == "__main__":
    main()
