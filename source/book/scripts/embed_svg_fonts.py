"""Embed subset fonts in Matplotlib SVGs without converting labels to paths.

Each SVG remains a standalone, offline image with live text. Font subsets use
distinct PHAST Diagram family names; this avoids operating-system substitution
and respects the reserved-name conditions of the bundled font licences.

Usage: python source/book/scripts/embed_svg_fonts.py source/book/figures/*.svg
Requires fontTools and Brotli in the authoring environment, not in the browser.
"""

from __future__ import annotations

import argparse
import base64
from collections import defaultdict
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from fontTools import subset
from fontTools.ttLib import TTFont
import matplotlib
from matplotlib.font_manager import FontProperties, findfont


SVG = "http://www.w3.org/2000/svg"
ALIASES = {
    "DejaVu Sans": "PHAST Diagram Sans",
    "DejaVu Sans Display": "PHAST Diagram Sans Display",
    "STIXSizeOneSym": "PHAST Diagram Math Size One",
    "STIXSizeTwoSym": "PHAST Diagram Math Size Two",
}
CANONICAL = {alias: family for family, alias in ALIASES.items()}
EMBEDDED_IDS = {"phast-embedded-fonts", "phast-font-licences", "phast-font-provenance"}


def _style(value: str) -> dict[str, str]:
    return dict(part.strip().split(":", 1) for part in value.split(";") if ":" in part)


def _family(value: str) -> str:
    family = value.split(",")[0].strip().strip("'\"")
    return CANONICAL.get(family, family)


def _font_subset(family: str, style: str, weight: str, characters: set[str]):
    font_path = Path(findfont(FontProperties(family=[family], style=style, weight=weight),
                              fallback_to_default=False))
    font = TTFont(font_path, recalcTimestamp=False)
    source_version = font["name"].getDebugName(5)
    codepoints = {ord(char) for char in characters}
    missing = codepoints - set(font.getBestCmap())
    if missing:
        raise ValueError(f"{font_path.name} lacks required glyphs: {sorted(missing)}")
    options = subset.Options()
    options.name_IDs = ["*"]
    options.name_legacy = True
    options.name_languages = ["*"]
    options.recalc_timestamp = False
    # The old FontForge table is irrelevant to browser shaping and otherwise
    # produces an unnecessary warning for every independently embedded face.
    options.drop_tables += ["FFTM"]
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=codepoints)
    subsetter.subset(font)
    alias = ALIASES[family]
    variant = ("Bold " if weight in {"700", "bold"} else "") + (
        "Oblique" if style in {"oblique", "italic"} else "Regular")
    variant = variant.replace("Bold Regular", "Bold")
    names = {1: alias, 2: variant, 3: f"{alias} {variant} subset", 4: f"{alias} {variant}",
             6: re.sub(r"[^A-Za-z0-9-]", "", f"{alias}-{variant}"), 16: alias, 17: variant}
    for record in list(font["name"].names):
        if record.nameID in names:
            font["name"].setName(names[record.nameID], record.nameID,
                                 record.platformID, record.platEncID, record.langID)
    font.flavor = "woff2"
    output = BytesIO()
    font.save(output)
    binary = output.getvalue()
    css = ("@font-face {"
           f"font-family:'{alias}';font-style:{style};font-weight:{weight};"
           f"src:url(data:font/woff2;base64,{base64.b64encode(binary).decode('ascii')}) format('woff2');"
           "font-display:block;}\n")
    return css, {
        "family": alias, "source_family": family, "style": style, "weight": weight,
        "source_font": font_path.name, "source_version": source_version,
        "source_sha256": hashlib.sha256(font_path.read_bytes()).hexdigest(),
        "subset_sha256": hashlib.sha256(binary).hexdigest(),
        "codepoints": sorted(codepoints), "subset_bytes": len(binary),
    }


def embed_svg_fonts(svg_path: Path) -> list[dict]:
    """Embed every actually used face and glyph; safe to run more than once."""
    svg_path = Path(svg_path)
    for prefix, uri in [("", SVG), ("xlink", "http://www.w3.org/1999/xlink"),
                        ("dc", "http://purl.org/dc/elements/1.1/"),
                        ("cc", "http://creativecommons.org/ns#"),
                        ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")]:
        ET.register_namespace(prefix, uri)
    root = ET.fromstring(svg_path.read_text(encoding="utf-8"))
    for parent in root.iter():
        for child in list(parent):
            if child.get("id") in EMBEDDED_IDS:
                parent.remove(child)
    glyphs = defaultdict(set)

    def visit(element, inherited):
        own = _style(element.get("style", ""))
        style = {**inherited, **{key: value.strip() for key, value in own.items()}}
        tag = element.tag.rsplit("}", 1)[-1]
        # Matplotlib pretty-prints one tspan per mathematical glyph. Remove
        # indentation between those positioned spans: otherwise the browser
        # shapes invisible separator whitespace using the parent default font.
        if tag in {"text", "tspan"} and len(element):
            if element.text and not element.text.strip():
                element.text = None
            for child in element:
                if child.tail and not child.tail.strip():
                    child.tail = None
        if tag in {"text", "tspan"} and element.text:
            family = _family(style.get("font-family", "DejaVu Sans"))
            if family not in ALIASES:
                raise ValueError(f"Unmapped SVG font family: {family}")
            variant = style.get("font-style", "normal")
            weight = style.get("font-weight", "400")
            if weight == "normal":
                weight = "400"
            if weight == "bold":
                weight = "700"
            glyphs[(family, variant, weight)].update(
                char for char in element.text if char not in "\n\r\t")
        if "font-family" in own:
            family = _family(own["font-family"])
            if family not in ALIASES:
                raise ValueError(f"Unmapped SVG font family: {family}")
            own["font-family"] = f"'{ALIASES[family]}'"
            element.set("style", "; ".join(f"{key}: {value.strip()}" for key, value in own.items()))
        for child in element:
            visit(child, style)

    visit(root, {})
    css, records = [], []
    for (family, style, weight), characters in sorted(glyphs.items()):
        rule, record = _font_subset(family, style, weight, characters)
        css.append(rule)
        records.append(record)
    defs = root.find(f"{{{SVG}}}defs")
    if defs is None:
        defs = ET.SubElement(root, f"{{{SVG}}}defs")
    ET.SubElement(defs, f"{{{SVG}}}style", {"id": "phast-embedded-fonts", "type": "text/css"}).text = "\n" + "".join(css)
    font_dir = Path(matplotlib.get_data_path()) / "fonts" / "ttf"
    licences = [font_dir / "LICENSE_DEJAVU"]
    if any(record["source_family"].startswith("STIX") for record in records):
        licences.append(font_dir / "LICENSE_STIX")
    ET.SubElement(root, f"{{{SVG}}}metadata", {"id": "phast-font-licences"}).text = "\n\n".join(
        file.read_text(encoding="utf-8") for file in licences)
    ET.SubElement(root, f"{{{SVG}}}metadata", {"id": "phast-font-provenance"}).text = json.dumps(
        {"matplotlib_version": matplotlib.__version__, "font_subsets": records}, indent=2)
    svg_path.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.svg:
        records = embed_svg_fonts(path)
        print(f"{path.name}: {len(records)} embedded faces, {sum(r['subset_bytes'] for r in records)} font bytes")
