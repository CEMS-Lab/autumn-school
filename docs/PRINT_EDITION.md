# Day 3 print edition

The print edition combines three lecture guides, three worked classroom
notebooks and the mathematical reference chapters. It uses the saved notebook
outputs; building it does not execute the numerical calculations. Open exercises
are labelled separately from worked results.

## Build

Requirements: the book's Python dependencies, Pillow, BeautifulSoup, pypdf,
XeLaTeX, latexmk, Poppler, STIX Two Text/Math, Helvetica Neue and DejaVu Sans Mono
for Powerline. The current typesetting configuration uses these installed fonts.

From the repository root:

```sh
python source/book/scripts/build_classroom_pages.py
python scripts/build_print_book.py
python -m sphinx -b latex -E tmp/pdfs/source tmp/pdfs/latex -W --keep-going
latexmk -cd -xelatex -interaction=nonstopmode -halt-on-error tmp/pdfs/latex/phast-autumn-school.tex
python scripts/mark_internal_pdf.py tmp/pdfs/latex/phast-autumn-school.pdf output/pdf/PhAST_Autumn_School_2026_Day3.pdf
python scripts/review_book_pdf.py output/pdf/PhAST_Autumn_School_2026_Day3.pdf --output tmp/pdfs/review
```

Review the rendered pages before publishing. Copy the checked PDF to
`downloads/PhAST_Autumn_School_2026_Day3.pdf`, then rebuild the website and run
`python scripts/check_book_theme.py`.

Every published page carries an internal-document notice, a faint watermark and
a copyright statement. The notice requests restricted distribution; the public
website download is not access-controlled. Third-party rights remain unchanged.

## Treatment of notebook output

All code cells are included. Saved figures are retained. Each animation becomes
a sequence of selected frames with a link to the online notebook. Long setup
and progress logs are shortened with an explicit note; measured results remain.
Browser-only controls are omitted. The conversion records every output decision
in `tmp/pdfs/output_manifest.json`.

This is a publication check, not a new numerical validation. The saved examples
use different physical models and solver settings; their assumptions and
comparison limitations must remain visible.
