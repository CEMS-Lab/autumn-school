"""Refresh a public-only manifest and optionally copy a new, immutable edition.

Run only after source/build/render review. This packages this public repository,
not an upstream solver worktree, and never publishes to GitHub.
"""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', required=True)
    parser.add_argument('--output', type=Path, help='New folder, must not exist')
    args = parser.parse_args()
    if args.output and (args.output.exists() or Path(str(args.output)+'.zip').exists()):
        raise FileExistsError('Choose a new edition path; existing editions are immutable')
    for src, dst in [('.build/slides/phast_autumn_school_2026.pdf','slides/phast_autumn_school_2026.pdf'),
                     ('.build/slides/phast_autumn_school_2026.pdf','source/slides/phast_autumn_school_2026.pdf')]:
        shutil.copy2(ROOT/src, ROOT/dst)
    names = ['00_course_map','01_methods_map','03_staggered_loop','04_fem_pipeline',
             '05_autograd_inverse','05a_backpropagation','06_learning_cycle']
    for name in names:
        # Retain old PNG URLs with the current drawing; HTML selects vector SVG.
        shutil.copy2(ROOT/'source/book/figures'/f'{name}.png',ROOT/'book/_images'/f'{name}.png')
    slides = ROOT/'source/slides'
    with zipfile.ZipFile(ROOT/'slides/phast_latex_sources.zip','w',zipfile.ZIP_DEFLATED) as archive:
        sources = [slides/p for p in ['phast_autumn_school_2026.tex','phast_autumn_school_2026.pdf',
            'build_beamer_figures.py','render_beamer.py','README.md',
            'beamer_speaker_notes.md','beamer_slide_manifest.json']]
        sources += sorted((slides/'latex_figures').iterdir())
        for src in sources:
            if src.is_file(): archive.write(src, src.relative_to(slides))
    raw = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT)
    files = sorted(set(s.decode() for s in raw.split(b'\0') if s))
    files = [f for f in files if f != 'MANIFEST.json' and (ROOT/f).is_file()]
    for f in files:
        approved_extension = f.startswith(('source/book/research/', 'book/research/', 'book/_sources/research/'))
        forbidden = {'.git','.build','reviews','jupyter_execute','_attachments'}
        if any(part in forbidden for part in Path(f).parts) or ('research' in Path(f).parts and not approved_extension):
            raise ValueError(f'Non-public build or draft path: {f}')
        if (ROOT/f).is_symlink() or not (ROOT/f).resolve().is_relative_to(ROOT):
            raise ValueError(f'Non-local payload: {f}')
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    manifest.update(version=args.version, date=date.today().isoformat(),
                    change_scope='PhAST dark theme, integrated inverse and history lessons, academic prose, revised animations and current teaching slides',
                    runtime_scope='Exact-source local rehearsal of six classroom notebooks, local diffusion run and retained HPC inverse receipts; authenticated Colab rehearsal tracked in delivery plan',
                    delivery_formats=['HTML book', 'Jupyter notebooks', 'editable PowerPoint', 'native Keynote', 'slide PDFs', 'animation assets'],
                    printable_book='archived by maintainer request')
    manifest['files'] = {f:sha(ROOT/f) for f in files}
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if args.output:
        destination = args.output.resolve()
        destination.mkdir(parents=True,exist_ok=False)
        for f in files+['MANIFEST.json']:
            dst = destination/f
            dst.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/f,dst)
        zip_path = Path(str(destination)+'.zip')
        with zipfile.ZipFile(zip_path,'x',zipfile.ZIP_DEFLATED) as archive:
            for f in files+['MANIFEST.json']:
                archive.write(destination/f,Path(destination.name)/f)
        for f, digest in manifest['files'].items():
            assert sha(destination/f)==digest
        print(json.dumps({'version':args.version,'files':len(files)+1,
                          'zip_sha256':sha(zip_path)},indent=2))
    else:
        print(json.dumps({'version':args.version,'files':len(files)+1,'manifest':'refreshed'}))


if __name__ == '__main__':
    main()
