"""Mark every page of the course PDF without changing its scientific content.

Use the unmarked XeLaTeX build as input. Links and bookmarks are retained.
"""
import argparse
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

NOTICE = "INTERNAL DOCUMENTATION - NOT TO BE DISTRIBUTED"
COPYRIGHT = "Copyright © 2026 Allamaprabhu Ani and Sathiskumar A. Ponnusami."
RIGHTS = "Original course material: all rights reserved. Third-party material retains its existing rights."


def overlay(width, height):
    stream = BytesIO()
    c = canvas.Canvas(stream, pagesize=(width, height))
    c.saveState()
    c.setFillColorRGB(0.35, 0.35, 0.35)
    c.setFillAlpha(0.13)
    c.translate(width / 2, height / 2)
    c.rotate(48)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(0, 14, "INTERNAL DOCUMENTATION")
    c.setFont("Helvetica-Bold", 25)
    c.drawCentredString(0, -22, "NOT TO BE DISTRIBUTED")
    c.restoreState()
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.setFont("Helvetica", 7)
    c.drawCentredString(width / 2, height - 19, NOTICE)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(width / 2, 23, COPYRIGHT)
    c.drawCentredString(width / 2, 14, RIGHTS)
    c.save()
    stream.seek(0)
    return PdfReader(stream).pages[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        raise ValueError("Keep the unmarked source separate from the output.")
    reader = PdfReader(args.source)
    writer = PdfWriter(clone_from=reader)
    for page in writer.pages:
        if NOTICE in (page.extract_text() or ""):
            raise ValueError("Input already contains the internal-document notice.")
        page.merge_page(overlay(float(page.mediabox.width), float(page.mediabox.height)))
        page.compress_content_streams()
    writer.add_metadata({"/Subject": NOTICE, "/Copyright": COPYRIGHT + " " + RIGHTS})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("wb") as stream:
        writer.write(stream)
    checked = PdfReader(args.output)
    assert len(checked.pages) == len(reader.pages)
    assert all(NOTICE in (page.extract_text() or "") for page in checked.pages)
    def annotation_count(pdf):
        return sum(len(p['/Annots'].get_object()) if '/Annots' in p else 0
                   for p in pdf.pages)
    assert annotation_count(checked) == annotation_count(reader)
    print(f"Marked and checked all {len(checked.pages)} pages; annotations retained.")


if __name__ == "__main__":
    main()
