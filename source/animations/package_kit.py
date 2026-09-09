"""Package only the animation assets, editable source and teaching notes."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    destination = args.output.resolve()
    if destination.exists():
        raise FileExistsError("Refusing to replace an existing animation kit")
    files = sorted(p for p in (ROOT / "assets/animations").rglob("*") if p.is_file())
    files += sorted((ROOT / "source/animations").glob("*.py"))
    files += [ROOT / "source/animations/README.md", ROOT / "DIFFERENTIABLE_SOLVER_TEACHING_NOTES.md"]
    mapping = {}
    for p in files:
        if p.is_symlink() or not p.resolve().is_relative_to(ROOT):
            raise ValueError("Unexpected asset outside this worktree")
        mapping[p.relative_to(ROOT).as_posix()] = p.read_bytes()
    mapping["README.md"] = (ROOT / "source/animations/README.md").read_bytes()
    manifest = {"scope": "Original course animation kit with editable source and teaching notes",
                "files": {name: sha(data) for name, data in sorted(mapping.items())}}
    mapping["KIT_MANIFEST.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    with zipfile.ZipFile(destination, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(mapping.items()):
            archive.writestr("PhAST_Animation_Kit/" + name, data)
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        for name, expected in manifest["files"].items():
            assert sha(archive.read("PhAST_Animation_Kit/" + name)) == expected
    print(json.dumps({"output":str(destination), "files":len(mapping),
                      "bytes":destination.stat().st_size,
                      "sha256":sha(destination.read_bytes()), "verified":True}, indent=2))

if __name__ == "__main__":
    main()
