"""Render all Beamer pages, collect their notes, and report structural checks.

Requires pypdf, Pillow and Poppler's pdftoppm. Does not execute course notebooks.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--build-dir',type=Path,default=ROOT,help='Directory containing the compiled PDF and log')
parser.add_argument('--output',type=Path,default=ROOT/'latex_qa',help='Private review output directory')
options=parser.parse_args()
OUT=options.output.resolve();OUT.mkdir(parents=True,exist_ok=True)
TEX=ROOT/'phast_autumn_school_2026.tex'
PDF=options.build_dir.resolve()/'phast_autumn_school_2026.pdf'
text=TEX.read_text()
body=text.split(r'\begin{document}',1)[1]

def group(src,pos):
    while src[pos].isspace():pos+=1
    assert src[pos]=='{',(pos,src[pos:pos+60])
    start=pos+1;depth=1;pos+=1
    while depth:
        if src[pos]=='{' and src[pos-1]!='\\':depth+=1
        elif src[pos]=='}' and src[pos-1]!='\\':depth-=1
        pos+=1
    return src[start:pos-1],pos

manifest=[]
for match in re.finditer(r'\\begin\{frame\}(?:\[[^\]]*\])?|\\session(?=\{)',body):
    pos=match.end()
    if match.group().startswith(r'\session'):
        args=[]
        for _ in range(4):value,pos=group(body,pos);args.append(value)
        title,timing,_,notes=args
    else:
        if body[pos:pos+1]=='{':title,pos=group(body,pos)
        else:title='From cracks to computation'
        end=body.index(r'\end{frame}',pos)
        content=body[pos:end]
        tm=re.search(r'\\timing(?=\{)',content)
        if tm:
            timing,p=group(content,tm.end());notes,p=group(content,p)
        else:timing,notes='',''
        for prompt in re.finditer(r'\\question(?=\{)',content):
            question,_=group(content,prompt.end())
            notes+=' Discussion prompt: '+question
    manifest.append({'slide':len(manifest)+1,'title':title,'timing':timing,'notes':notes})

reader=PdfReader(PDF)
subprocess.run(['pdftoppm','-scale-to','1500','-png',str(PDF),str(OUT/'slide')],check=True)
rendered=[]
for i in range(len(reader.pages)):
    target=OUT/f'slide-{i+1:02}.png';assert target.is_file();rendered.append(target)
for first in range(0,len(rendered),6):
    sheet=Image.new('RGB',(1640,1500),'#DCE3E7');draw=ImageDraw.Draw(sheet)
    for j,target in enumerate(rendered[first:first+6]):
        im=Image.open(target);im.thumbnail((800,450))
        x,y=10+(j%2)*820,32+(j//2)*500
        sheet.paste(im,(x,y));draw.text((x,y-20),f'Slide {first+j+1:02}',fill='#20364D')
    sheet.save(OUT/f'contact-{first//6+1:02}.png')
texts=[p.extract_text() or '' for p in reader.pages]
log=(options.build_dir.resolve()/'phast_autumn_school_2026.log').read_text()
report={
    'format':'LaTeX Beamer, 16:9','renderer':'Poppler pdftoppm','source_frames':len(manifest),
    'pdf_pages':len(reader.pages),'rendered_pages':len(rendered),
    'frames_with_notes':sum(bool(m['notes']) for m in manifest),
    'all_pages_have_text':all(bool(t.strip()) for t in texts),
    'overfull_boxes':re.findall(r'Overfull[^\n]*',log),
    'missing_glyph_warnings':re.findall(r'Missing character[^\n]*',log),
    'placeholder_hits':[i+1 for i,t in enumerate(texts) if re.search(r'lorem ipsum|\[insert|TODO|XXX',t,re.I)],
    'pdf_sha256':hashlib.sha256(PDF.read_bytes()).hexdigest(),
    'source_sha256':hashlib.sha256(TEX.read_bytes()).hexdigest(),
}
expected_figure_pages=[1,4,8,9,10,11,12,19,22,23,29,33,34]
report['missing_expected_figure_resources']=[
    i for i in expected_figure_pages
    if not reader.pages[i-1]['/Resources'].get('/XObject')]
(OUT/'structural_review.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'beamer_slide_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
notes=['# Instructor notes — PhAST six-hour course',
    'Primary source: `phast_autumn_school_2026.tex`. These are the same notes embedded in the Beamer source.',
    'Three 120-minute sections; each contains 110 minutes of instruction/activity and one 10-minute break. Timings describe relative teaching allocations; notebook execution has separate runtime receipts.']
for m in manifest:
    notes.extend([f"## {m['slide']}. {m['title']}",f"Timing: {m['timing']}",m['notes']])
(ROOT/'beamer_speaker_notes.md').write_text('\n\n'.join(notes)+'\n')
print(json.dumps(report,indent=2))
assert len(manifest)==len(reader.pages)==44
assert report['frames_with_notes']==44
assert not report['overfull_boxes']
assert not report['missing_glyph_warnings']
assert not report['placeholder_hits']
assert not report['missing_expected_figure_resources']
