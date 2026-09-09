"""Render the built book for visual review; no notebook execution.

Requires pypdf, Pillow and Poppler. Run from the repository root.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw
from pypdf import PdfReader


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('--output', type=Path, default=Path('reviews/book_pdf'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    reader = PdfReader(args.pdf)
    subprocess.run(['pdftoppm', '-scale-to', '1300', '-png', str(args.pdf),
                    str(args.output / 'page')], check=True)
    images = sorted(args.output.glob('page-*.png'))
    assert len(images) == len(reader.pages)
    texts = [page.extract_text() or '' for page in reader.pages]
    figure_pages = {key: [i + 1 for i, text in enumerate(texts) if key in text]
                    for key in ['Figure 1', 'Figure 2.1', 'Figure 4.1', 'Figure 5.1',
                                'Figure 6.1', 'Figure 6.2', 'Figure 7.1']}
    for start in range(0, len(images), 6):
        sheet = Image.new('RGB', (1500, 1880), '#e7ebee')
        draw = ImageDraw.Draw(sheet)
        for j, path in enumerate(images[start:start+6]):
            im = Image.open(path)
            im.thumbnail((720, 575))
            x, y = 15 + (j % 2)*750, 32 + (j//2)*620
            sheet.paste(im, (x+(720-im.width)//2, y))
            draw.text((x, y-20), f'PDF page {start+j+1}', fill='#182633')
        sheet.save(args.output / f'contact-{start//6+1:02}.png')
    report = {'pages': len(reader.pages), 'rendered': len(images),
              'all_pages_have_text': all(text.strip() for text in texts),
              'figure_page_candidates': figure_pages,
              'pdf_sha256': hashlib.sha256(args.pdf.read_bytes()).hexdigest(),
              'scope': 'Rendering and structural checks, not a scientific validation'}
    (args.output/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
