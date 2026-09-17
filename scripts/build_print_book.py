"""Prepare a print edition from lecture sources and saved notebook outputs.

No solver is executed. The JSON report records every output retained or omitted.
Build after build_classroom_pages.py. Run Sphinx and latexmk on the staging tree.
"""
from pathlib import Path
import base64
import io
import json
import re
import shutil
import textwrap
from urllib.parse import urljoin

import nbformat
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / 'tmp/pdfs/source'
BASE = 'https://cems-lab.github.io/autumn-school/book/'
LECTURES = ['lectures/01_fracture_and_phast',
            'lectures/02_differentiability_and_inverse',
            'lectures/03_hybrid_learning']
NOTEBOOKS = ['classroom/01_simulate_fracture',
             'classroom/02_gradients_and_recovery',
             'classroom/03_learning_and_hybrid']
REFERENCE = ['01_crack_representations', '02_phase_field_energy',
             '03_staggered_solution', '04_fem_to_tensors',
             '05_differentiation_and_inverse', '05a_backpropagation_step_by_step',
             '06_learning_adapter', '07_practice_references']


def clean_markdown(s, doc):
    s = re.sub(r'<div class="badge-row">.*?</div>', '', s, flags=re.S)
    s = re.sub(r'<summary>(.*?)</summary>', r'\n\n**\1**\n\n', s, flags=re.S)
    s = re.sub(r'</?(?:details|p|div)(?:\s[^>]*)?>', '\n\n', s)
    s = re.sub(r'```\{raw\} html\n.*?```', '', s, flags=re.S)
    def doclink(m):
        label, target = (m[1].rsplit(' <', 1) if ' <' in m[1]
                         else (m[1].replace('_', ' '), m[1]))
        return f'[{label}]({urljoin(BASE + doc + ".html", target.rstrip(">") + ".html")})'
    s = re.sub(r'\{doc\}`([^`]+)`', doclink, s)
    s = re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)',
               lambda m: f'[{m[1]}]({urljoin(BASE+doc+".html",m[2])})'
               if not m[2].startswith(('http', '#', 'mailto:')) else m[0], s)
    # Preserve maths and code; only remove empty answer placeholders.
    s = re.sub(r'\*\*Your (?:answer|observations):\*\*\s*_(?:Write here\.|Write your answer here\.)_',
               '*Exercise for independent work.*', s)
    # Five-column comparison tables become readable labelled entries in print.
    def wide_table(m):
        rows = [[v.strip() for v in l.strip().strip('|').split('|')]
                for l in m[0].strip().splitlines()]
        if len(rows[0]) < 5: return m[0]
        return '\n\n'+'\n\n'.join('**'+r[0].strip('*')+'**\n\n'+
            '\n'.join('- **'+h+':** '+v for h,v in zip(rows[0][1:],r[1:]))
            for r in rows[2:])+'\n\n'
    s = re.sub(r'(?:^\|[^\n]+\|\s*\n){3,}', wide_table, s, flags=re.M)
    s = s.replace('| Field | Symbol | Why this is the right view |',
                  '```{tabularcolumns} '+r'\X{3}{10}\X{1}{10}\X{6}{10}'+'\n```\n\n| Field | Symbol | Why this is the right view |')
    return re.sub(r'\n{4,}', '\n\n\n', s).strip()


def figure(path, caption):
    return f'\n\n:::{{figure}} /{path.relative_to(STAGE).as_posix()}\n:width: 100%\n\n{caption}\n:::\n\n'


def animation_panel(frames, path):
    count = len(frames)
    indices = sorted(set([0, (count-1)//2, count-1]))
    selected = [frames[i].convert('RGB') for i in indices]
    width = 660
    height = max(round(im.height * width / im.width) for im in selected)
    stacked = selected[0].width / selected[0].height > 2.0
    canvas = Image.new('RGB', (width if stacked else width * len(selected),
                              (height + 45) * len(selected) if stacked else height + 45), 'white')
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 22)
    for col, (idx, im) in enumerate(zip(indices, selected)):
        im.thumbnail((width, height))
        x = 0 if stacked else col * width
        y = col * (height + 45) if stacked else 0
        canvas.paste(im, (x+(width-im.width)//2, y+40))
        draw.text((x+16, y+8), f'Frame {idx+1} of {count}', font=font, fill='#333333')
    canvas.save(path)
    return count


def html_output(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    if table:
        rows = [[c.get_text(' ', strip=True).replace('|', '/')
                 for c in tr.find_all(['th','td'])] for tr in table.find_all('tr')]
        rows = [r for r in rows if r]
        if rows:
            return '\n'.join(['| '+' | '.join(rows[0])+' |',
                              '| '+' | '.join(['---']*len(rows[0]))+' |'] +
                             ['| '+' | '.join(r)+' |' for r in rows[1:]])
    for t in soup(['style','script']): t.decompose()
    return soup.get_text('\n', strip=True)


def notebook(doc, report):
    source = ROOT / 'source/book' / (doc + '.ipynb')
    nb = nbformat.read(source, 4)
    parts = []
    assets = STAGE / 'print_assets' / Path(doc).name
    assets.mkdir(parents=True, exist_ok=True)
    for index, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown':
            parts.append(clean_markdown(cell.source, doc))
            continue
        if cell.cell_type != 'code': continue
        parts.append(f'**Code cell {index+1}**\n\n```ipython\n{cell.source}\n```')
        for j, out in enumerate(cell.get('outputs', [])):
            entry = dict(notebook=doc, cell=index+1, output=j+1)
            data = out.get('data', {})
            path = assets / f'cell-{index+1:03}-{j+1}.png'
            if 'image/png' in data:
                path.write_bytes(base64.b64decode(data['image/png']))
                parts.append(figure(path, f'Saved output from code cell {index+1}.'))
                entry['action'] = 'saved PNG'
            elif 'image/gif' in data:
                gif = Image.open(io.BytesIO(base64.b64decode(data['image/gif'])))
                frames = []
                for k in range(gif.n_frames):
                    gif.seek(k); frames.append(gif.convert('RGB').copy())
                count = animation_panel(frames, path)
                parts.append(figure(path, f'Three stages from the saved animation ({count} frames). '
                                    f'[Play the animation online]({BASE+doc}.html).'))
                entry.update(action='GIF frames', frames=count)
            elif 'text/html' in data:
                html = data['text/html']
                encoded = re.findall(r'data:image/(png|gif);base64,([^"\']+)', html)
                if encoded:
                    frames = []
                    for kind, encoded_image in encoded:
                        im = Image.open(io.BytesIO(base64.b64decode(
                            re.sub(r'\\\s*', '', encoded_image))))
                        for k in range(getattr(im, 'n_frames', 1)):
                            im.seek(k); frames.append(im.convert('RGB').copy())
                    count = animation_panel(frames, path)
                    parts.append(figure(path, f'Three stages from the saved animation ({count} frames). '
                                        f'[Play the animation online]({BASE+doc}.html).'))
                    entry.update(action='HTML animation frames', frames=count)
                else:
                    parts.append(html_output(html)); entry['action'] = 'HTML text/table'
            elif 'text/markdown' in data:
                parts.append(data['text/markdown']); entry['action'] = 'Markdown output'
            elif 'application/javascript' in data or 'application/vnd.jupyter.widget-view+json' in data:
                entry['action'] = 'browser download/progress control omitted'
            elif out.get('output_type') == 'stream' or 'text/plain' in data:
                s = out.get('text', data.get('text/plain', ''))
                s = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', s).replace('\r', '\n')
                lines = s.splitlines()
                if len(lines)>45:
                    s = '[Long console log abbreviated; see the online notebook for the full output.]\n'+'\n'.join(lines[-18:])
                    entry['action'] = 'abbreviated console output'
                else:
                    entry['action'] = 'console output'
                s = '\n'.join(textwrap.fill(l, 94, replace_whitespace=False,
                                           drop_whitespace=False) if len(l)>94 else l for l in s.splitlines())
                if s.strip(): parts.append('```text\n'+s.strip()+'\n```')
            elif out.get('output_type') == 'error':
                parts.append('**Saved execution error:** '+out.get('ename','')+': '+out.get('evalue',''))
                entry['action'] = 'saved error'
            else:
                entry['action'] = 'empty output'
            report.append(entry)
    target = STAGE / (doc + '.md')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('\n\n'.join(parts)+'\n')


def main():
    STAGE.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT/'source/book/figures', STAGE/'figures', dirs_exist_ok=True)
    for doc in LECTURES + REFERENCE:
        target = STAGE/(doc+'.md'); target.parent.mkdir(parents=True, exist_ok=True)
        text = (ROOT/'source/book'/(doc+'.md')).read_text()
        target.write_text(clean_markdown(text, doc)+'\n')
    report=[]
    for doc in NOTEBOOKS: notebook(doc, report)
    toc = '\n'.join(x for pair in zip(LECTURES,NOTEBOOKS) for x in pair)
    (STAGE/'preface.md').write_text('''# About this edition

**UKACM Autumn School 2026 · Day 3 · 16 September 2026**

Prepared by **Allamaprabhu Ani and Sathiskumar A. Ponnusami**, CEMS-Lab,
City St George's, University of London; Queen Mary University of London.

This book brings together three lecture guides, the worked practical notebooks
and supporting mathematical chapters. Begin with a lecture and then follow its
notebook. The reference chapters develop the equations in greater detail and
can be consulted as needed.

The practicals progress from dynamic fracture simulation to recovery of a
bar's Young's modulus and direct learned replacement of a damage update.
The bar is linear elastic and contains no damage. The hybrid example uses a
different specimen and constitutive model from the dynamic plate.

## Reading code and results

Code listings and numerical figures are taken from the supplied notebooks.
The saved outputs are reproduced, not newly executed for this edition. They
document particular runs, not guaranteed outcomes on every computer. Parameters,
software revisions, physical assumptions and comparison scope accompany the
examples. Additional exercises remain exercises unless a result is shown.

Animations appear as selected frames in print. Their links open the complete
HTML notebooks, where the animations can be played and code downloaded.
Long installation and progress logs are abbreviated; numerical plots and
result tables are retained. Expandable hints and conceptual answers are printed.

The notation uses $d=0$ for intact material and $d=1$ for fully damaged material.
Numerical time increments describe the model; measured wall-clock times in the
hybrid example describe computational cost. They are different quantities.

[Online book and notebook downloads](https://cems-lab.github.io/autumn-school/book/index.html#day-3-phast)
''')
    (STAGE/'index.md').write_text('''# Fracture, Differentiability and PhAST

```{toctree}
:maxdepth: 2

preface

'''+toc+'''
```

```{toctree}
:maxdepth: 2

'''+ '\n'.join(REFERENCE)+ '\n```\n')
    (STAGE/'conf.py').write_text(r'''project = "Fracture, Differentiability and PhAST"
author = "Allamaprabhu Ani and Sathiskumar A. Ponnusami"
copyright = "2026, CEMS-Lab"
extensions = ["myst_parser"]
myst_enable_extensions = ["amsmath", "colon_fence", "deflist", "dollarmath"]
myst_dmath_double_inline = True
master_doc = "index"
numfig = True
latex_engine = "xelatex"
latex_documents = [("index", "phast-autumn-school.tex", project,
    author+r"\\[0.5em]{\large UKACM Autumn School 2026 · Day 3}", "manual")]
latex_elements = {
 "papersize": "a4paper", "pointsize": "10pt",
 "extraclassoptions": "openany,oneside",
 "fontpkg": r"""
\setmainfont{STIX Two Text}
\setsansfont{Helvetica Neue}
\setmonofont[Scale=0.88]{DejaVu Sans Mono for Powerline}
\usepackage{unicode-math}
\setmathfont{STIX Two Math}
""",
 "sphinxsetup": "verbatimwithframe=false,verbatimwrapslines=true,VerbatimColor={RGB}{248,248,248},TitleColor={RGB}{30,30,30},InnerLinkColor={RGB}{35,85,120},OuterLinkColor={RGB}{35,85,120}",
 "preamble": r"""
\usepackage{booktabs}
\usepackage{needspace}
\usepackage{etoolbox}
\usepackage{newunicodechar}
\newunicodechar{→}{\ensuremath{\rightarrow}}
\setlength{\parskip}{0.3em}
\setcounter{tocdepth}{1}
\setcounter{secnumdepth}{0}
\BeforeBeginEnvironment{sphinxadmonition}{\Needspace{6\baselineskip}}
\AtBeginDocument{\hypersetup{pdfauthor={Allamaprabhu Ani and Sathiskumar A. Ponnusami},pdfsubject={UKACM Autumn School 2026: lectures and worked PhAST notebooks}}}
""",
 "maketitle": r"""
\hypersetup{pageanchor=false}
\begin{titlepage}
\centering
\vspace*{20mm}
{\sffamily\large UKACM AUTUMN SCHOOL 2026\par}
\vspace{20mm}
{\sffamily\bfseries\fontsize{29}{36}\selectfont Fracture, Differentiability\\and PhAST\par}
\vspace{10mm}
{\Large Lecture notes and worked notebooks\par}
\vspace{8mm}
{\large Day 3 · 16 September 2026\par}
\vfill
{\large Allamaprabhu Ani\\Sathiskumar A. Ponnusami\par}
\vspace{8mm}
CEMS-Lab\\City St George's, University of London\\Queen Mary University of London
\vspace{16mm}
\par Print edition · 17 September 2026
\end{titlepage}
\hypersetup{pageanchor=true}
""",
}
''')
    (ROOT/'tmp/pdfs/output_manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'Prepared {len(LECTURES)} lectures, {len(NOTEBOOKS)} notebooks and {len(REFERENCE)} references.')
    print(f'Accounted for {len(report)} saved outputs in tmp/pdfs/output_manifest.json')


if __name__ == '__main__':
    main()
