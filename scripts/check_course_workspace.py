"""Verify the consolidated local package without rerunning a calculation."""
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

OUT = Path(os.environ.get("UKACM_COURSE_PACKAGE", str(Path.home() / "Documents/UKACM Autumn School 2026")))


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    manifest = json.loads((OUT / "MANIFEST.json").read_text())
    mismatches = []
    for item in manifest["copied_files"]:
        target = OUT / item["destination"]
        if not target.is_file() or sha(target) != item["sha256"]:
            mismatches.append(item["destination"])
    pages = ["index.html", "Visual_Results/index.html", "Visual_Results/Fracture_Examples/index.html", "Media_Library/index.html"]
    checked, broken = 0, []
    for name in pages:
        path = OUT / name
        soup = BeautifulSoup(path.read_text(), "html.parser")
        for tag in soup.find_all(["a", "img", "source", "video", "script", "link"]):
            for attribute in ("href", "src", "poster"):
                value = tag.get(attribute)
                if not value:
                    continue
                parsed = urlsplit(value)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                checked += 1
                target = (path.parent / unquote(parsed.path)).resolve()
                if not target.exists():
                    broken.append({"page": name, "target": value})
    primary = [r for r in manifest["execution_summary"]["notebooks"] if r["kind"] == "classroom"]
    assert len(primary) == 3
    assert all(r["status"] == "passed" and r["whole_process_seconds"] < 120 for r in primary)
    report = {"copied_hashes_checked": len(manifest["copied_files"]), "entry_page_links_checked": checked,
              "mismatches": mismatches, "broken_links": broken,
              "primary_seconds": {r["name"]: r["whole_process_seconds"] for r in primary},
              "authenticated_colab": False, "status": "passed" if not mismatches and not broken else "failed"}
    print(json.dumps(report, indent=2))
    assert not mismatches and not broken


if __name__ == "__main__":
    main()
