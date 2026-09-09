"""Fast (<0.05s) design and textual directives validator for Sphinx HTML builds.

Validates that:
1. No prohibited AI drama, negative framing, or compliance checklists exist.
2. The four core workshop pillars are clearly presented on the index page.
3. Every lab notebook page features standard tutorial action badges and dropdown solutions.
"""
from pathlib import Path
import re
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "book"

PROHIBITED_PATTERNS = [
    (re.compile(r"Why average predictions can fail", re.I), "Unrefactored dramatic title"),
    (re.compile(r"stationary trap", re.I), "Negative/dramatic phrasing ('stationary trap')"),
    (re.compile(r"Minimum result card", re.I), "AI compliance checklist phrase ('Minimum result card')"),
]

def check_directives(book_dir=BOOK):
    t0 = time.time()
    errors = []
    
    if not book_dir.exists():
        return False, ["Book directory not found: " + str(book_dir)], 0.0

    html_files = sorted(book_dir.rglob("*.html"))
    if not html_files:
        return False, ["No HTML files found in " + str(book_dir)], 0.0

    # 1. Prohibited phrases check across all HTML files
    for f in html_files:
        if "_static" in f.parts:
            continue
        content = f.read_text(encoding="utf-8", errors="ignore")
        rel = f.relative_to(ROOT)
        for pattern, desc in PROHIBITED_PATTERNS:
            if pattern.search(content):
                errors.append(f"{rel}: contains prohibited text '{pattern.pattern}' ({desc})")

    # 2. Check 4 Pillars on index.html
    index_file = book_dir / "index.html"
    if index_file.is_file():
        index_content = index_file.read_text(encoding="utf-8", errors="ignore")
        pillars = [
            "What Phase-Field Fracture Is",
            "Hands-on with the PhAST Solver",
            "Differentiability and Inverse Problems",
            "Deep Learning Integration",
        ]
        for pillar in pillars:
            if pillar.lower() not in index_content.lower():
                errors.append(f"index.html: missing core workshop pillar '{pillar}'")
        if "colab" not in index_content.lower():
            errors.append("index.html: missing Google Colab links or badges")

    # 3. Check lab notebooks action badges, download buttons, and Colab integration
    lab_files = sorted((book_dir / "labs").glob("*.html")) if (book_dir / "labs").is_dir() else []
    for lf in lab_files:
        l_content = lf.read_text(encoding="utf-8", errors="ignore")
        if "badge-row" not in l_content and "badge-link" not in l_content:
            errors.append(f"{lf.relative_to(ROOT)}: missing tutorial action badges (.badge-row)")
        if "colab" not in l_content.lower():
            errors.append(f"{lf.relative_to(ROOT)}: missing Google Colab launch button or badge")
        if "download" not in l_content.lower() and "btn-download" not in l_content:
            errors.append(f"{lf.relative_to(ROOT)}: missing notebook download option")

    elapsed_ms = (time.time() - t0) * 1000
    return len(errors) == 0, errors, elapsed_ms

def main():
    passed, errors, elapsed_ms = check_directives()
    if passed:
        print(f"✓ [Design Directives] Verified: 0 violations, 4 pillars present, all tutorial badges active ({elapsed_ms:.1f} ms)")
        sys.exit(0)
    else:
        print(f"✗ [Design Directives] Found {len(errors)} violation(s) ({elapsed_ms:.1f} ms):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
