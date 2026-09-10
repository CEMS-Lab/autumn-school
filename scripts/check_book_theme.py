"""Static theme smoke check; does not execute notebooks or test a browser."""
from html.parser import HTMLParser
import argparse
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--book", type=Path, default=ROOT / "book")
BOOK = parser.parse_args().book.resolve()


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.links = []
        self.ids = set()
        self.classes = set()
        self.dark_default = False
        source = path.read_text()
        self.source = source
        self.credit_present = (
            'name="author" content="Allamaprabhu Ani and Sathiskumar A. Ponnusami"' in source
            and "Prepared by <span>Allamaprabhu Ani and Sathiskumar A. Ponnusami</span>" in source
            and 'name="prepared-by" content="Allamaprabhu Ani and Sathiskumar A. Ponnusami"' in source
            and "Presented by <span>" not in source
            and "CEMS-Lab" in source and "UKACM Autumn School 2026" in source
        )
        self.details = {}
        # The upstream theme creates its mode control via document.write.
        # This checks inclusion of the template, not runtime interaction.
        self.theme_switch_template = "theme-switch-button" in source
        self.feed(source)

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "details" and attrs.get("id"):
            self.details[attrs["id"]] = "open" in attrs
        self.classes.update(attrs.get("class", "").split())
        if tag == "body":
            self.dark_default = attrs.get("data-default-mode") == "dark"
        for key in ("src", "href", "poster"):
            if attrs.get(key):
                self.links.append((tag, key, attrs[key]))


pages = {
    p.resolve(): Page(p)
    for p in sorted(BOOK.rglob("*.html"))
    if "_static" not in p.parts
}
errors = []
asset_refs = 0
lesson_count = 0
sphinx_count = 0
standalone_count = 0
standalone_names = {"history_plate.html", "history_plate.template.html", "history_walkthrough.html"}
for path, page in pages.items():
    rel = str(path.relative_to(ROOT))
    standalone = "_downloads" in path.relative_to(BOOK).parts
    if standalone:
        standalone_count += 1
        original = ROOT / "source/book/research/interactive" / path.name
        if path.name not in standalone_names:
            errors.append(f"{rel}: unclassified standalone HTML payload")
        elif not original.is_file() or original.read_bytes() != path.read_bytes():
            errors.append(f"{rel}: standalone payload differs from its authored source")
        if path.name == "history_plate.html":
            required = {"history-panel", "panel-data", "cycle-video", "walkthrough"}
            if not required <= page.ids:
                errors.append(f"{rel}: complete interactive payload missing")
            if any(marker in page.source for marker in ("__PAYLOAD__", "__WALKTHROUGH__", "__CYCLE_MOVIE__", "__CYCLE_POSTER__")):
                errors.append(f"{rel}: unresolved standalone template marker")
    else:
        sphinx_count += 1
        if not page.dark_default:
            errors.append(f"{rel}: dark default missing")
        if not page.credit_present:
            errors.append(f"{rel}: creator, lab or event credit missing")
        if path.name not in {"search.html", "genindex.html"}:
            for discovery in ("phast-gradient-discovery", "phast-backward-discovery"):
                if page.details.get(discovery) is not False:
                    errors.append(f"{rel}: closed native discovery missing: {discovery}")
        content_class = "bd-search-container" if path.name == "search.html" else "bd-article"
        if content_class not in page.classes or not page.theme_switch_template:
            errors.append(f"{rel}: article or theme switch missing")
        if path.parent.name == "labs":
            lesson_count += 1
            if not {"cell_input", "cell_output", "dropdown"} <= page.classes:
                errors.append(f"{rel}: notebook inputs, outputs or solutions missing")
    for tag, key, value in page.links:
        if standalone and path.name == "history_plate.template.html" and value in {"__CYCLE_MOVIE__", "__CYCLE_POSTER__"}:
            continue
        url = urlsplit(value)
        if url.scheme or url.netloc:
            if tag in {"script", "img", "video", "audio", "source", "iframe"} and key in {"src", "poster"} and url.scheme != "data":
                errors.append(f"{rel}: external runtime asset {value}")
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            errors.append(f"{rel}: missing local target {value}")
        elif target.suffix == ".html" and url.fragment:
            linked = pages.get(target)
            ids = set(linked.ids) if linked else set()
            if standalone and path.name == "history_plate.template.html" and target == path:
                # The downloadable authoring template inserts this named fragment.
                walkthrough = Page(ROOT / "source/book/research/interactive/history_walkthrough.html")
                ids.update(walkthrough.ids)
            if linked and unquote(url.fragment) not in ids:
                errors.append(f"{rel}: missing local fragment {value}")
        if tag in {"script", "img", "link"}:
            asset_refs += 1

for relative in [
    "_static/mathjax/tex-mml-chtml.js",
    "_static/licenses/sphinx_book_theme-1.1.4.txt",
    "_static/licenses/pydata_sphinx_theme-0.15.4.txt",
    "searchindex.js",
]:
    if not (BOOK / relative).is_file():
        errors.append(f"Missing required asset: {relative}")

from check_design_directives import check_directives
passed_directives, directive_errors, directive_time = check_directives(BOOK)
errors.extend(directive_errors)

print(json.dumps({
    "scope": "Static HTML/source checks, not browser or numerical validation",
    "html_pages": len(pages),
    "sphinx_pages": sphinx_count,
    "standalone_payloads": standalone_count,
    "notebook_lessons": lesson_count,
    "local_asset_references": asset_refs,
    "design_directives": "passed" if passed_directives else "failed",
    "design_directives_ms": round(directive_time, 1),
    "errors": errors,
}, indent=2))
raise SystemExit(bool(errors))
