"""Refresh a public-only manifest and optionally copy a new, immutable edition.

Run only after source/build/render review. This packages this public repository,
not an upstream solver worktree, and never publishes to GitHub.
"""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_public_path(root, name):
    """Apply the same public-payload boundary to inventory and declared paths."""
    root = Path(root).resolve()
    if not isinstance(name, str):
        raise ValueError('Manifest paths must be strings')
    relative = Path(name)
    if relative.is_absolute() or '..' in relative.parts or relative.as_posix() != name:
        raise ValueError(f'Invalid public relative path: {name}')
    if name in ('', '.', 'MANIFEST.json'):
        raise ValueError(f'Excluded manifest path: {name}')
    approved_extension = name.startswith(('source/book/research/', 'book/research/', 'book/_sources/research/'))
    forbidden = {'.git', '.build', 'reviews', 'jupyter_execute', '_attachments'}
    if any(part in forbidden for part in relative.parts) or ('research' in relative.parts and not approved_extension):
        raise ValueError(f'Non-public build or draft path: {name}')
    payload = root / relative
    # A symlinked directory can hide behind a regular-looking final component.
    if any((root / Path(*relative.parts[:i])).is_symlink() for i in range(1, len(relative.parts) + 1)):
        raise ValueError(f'Non-local payload: {name}')
    if not payload.resolve().is_relative_to(root):
        raise ValueError(f'Non-local payload: {name}')
    return payload


def public_inventory(root):
    """Read Git's tracked/public-untracked inventory; exclude the manifest itself."""
    root = Path(root).resolve()
    raw = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=root)
    names = sorted(set(item.decode() for item in raw.split(b'\0') if item))
    files = []
    for name in names:
        if name == 'MANIFEST.json':
            continue
        path = validate_public_path(root, name)
        if path.is_file():
            files.append(name)
    return files


def candidate_manifest(root, version=None):
    """Build a local-candidate manifest in memory without copying any artifact."""
    root = Path(root).resolve()
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    prior_version = manifest.get('published_version', manifest.get('version', '0.16.2'))
    prior_runtime_scope = manifest.get('runtime_scope')
    manifest.setdefault('published_version', prior_version)
    retained = manifest.setdefault('retained_evidence_metadata', {})
    if not isinstance(retained, dict):
        raise ValueError('retained_evidence_metadata must be an object')
    if prior_runtime_scope:
        retained.setdefault('prior_runtime_scope', prior_runtime_scope)
    retained.setdefault('hpc_inverse_status', 'Previously retained HPC inverse receipts retain their original provenance; this packaging step executes no HPC work.')
    manifest.update(
        version=version if version is not None else prior_version,
        date=date.today().isoformat(),
        base_git_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
        delivery_status='local reviewed candidate; publication pending',
        change_scope='Three curated classroom notebooks, three lecture guides and a 32-slide native Keynote companion with explicit example/animation outlines; original detailed notebooks, editable slides and media retained',
        runtime_scope='Current classroom receipts cover three complete local notebook processes after setup. Six detailed-source receipts and older HPC inverse evidence preserve their original dates and scope. Fresh Colab rehearsal remains a separate gate.',
        delivery_formats=['HTML book', 'Jupyter notebooks', 'editable PowerPoint', 'native Keynote', 'slide PDFs', 'animation assets'],
        printable_book='archived by maintainer request',
        files={name: sha(root / name) for name in public_inventory(root)},
    )
    return manifest


def verify_manifest(root, manifest=None):
    """Verify current public inventory and every declared hash without writes."""
    root = Path(root).resolve()
    if manifest is None:
        manifest = json.loads((root / 'MANIFEST.json').read_text())
    declared = manifest.get('files')
    if not isinstance(declared, dict):
        raise ValueError('Manifest files must map public relative paths to SHA-256 hashes')
    for name, digest in declared.items():
        validate_public_path(root, name)
        if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError(f'Invalid SHA-256 digest: {name}')
    current = set(public_inventory(root))
    if current != set(declared):
        raise ValueError(f'Manifest inventory differs: unrecorded={sorted(current-set(declared))[:10]}, missing={sorted(set(declared)-current)[:10]}')
    changed = [name for name, digest in declared.items() if sha(root / name) != digest]
    if changed:
        raise ValueError(f'Manifest hash mismatch: {changed[:10]}')
    return {'version': manifest.get('version'), 'files': len(declared), 'verification': 'inventory and all SHA-256 hashes match'}


def main(argv=None, root=ROOT):
    root = Path(root).resolve()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', help='Explicit version override; required for legacy edition packaging')
    parser.add_argument('--output', type=Path, help='New folder, must not exist')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--manifest-only', action='store_true', help='Refresh only the local-candidate manifest; preserve all artifacts and the existing version')
    modes.add_argument('--check-only', action='store_true', help='Verify existing manifest inventory and file hashes without writes')
    parser.add_argument('--dry-run', action='store_true', help='Validate a candidate manifest in memory; use with --manifest-only')
    args = parser.parse_args(argv)
    if args.check_only:
        if args.output or args.version or args.dry_run:
            parser.error('--check-only accepts no output, version override or dry-run')
        print(json.dumps(verify_manifest(root), indent=2))
        return
    if args.manifest_only:
        if args.output:
            parser.error('--manifest-only preserves artifacts and cannot create an edition output')
        manifest = candidate_manifest(root, args.version)
        report = verify_manifest(root, manifest)
        if not args.dry_run:
            (root / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
        report.update(manifest='dry-run; unchanged' if args.dry_run else 'refreshed only',
                      delivery_status=manifest['delivery_status'], base_git_revision=manifest['base_git_revision'])
        print(json.dumps(report, indent=2))
        return
    if args.dry_run:
        parser.error('--dry-run requires --manifest-only')
    if not args.version:
        parser.error('legacy edition packaging requires --version; use --manifest-only for a local candidate')
    if args.output and (args.output.exists() or Path(str(args.output)+'.zip').exists()):
        raise FileExistsError('Choose a new edition path; existing editions are immutable')
    for src, dst in [('.build/slides/phast_autumn_school_2026.pdf','slides/phast_autumn_school_2026.pdf'),
                     ('.build/slides/phast_autumn_school_2026.pdf','source/slides/phast_autumn_school_2026.pdf')]:
        shutil.copy2(root/src, root/dst)
    names = ['00_course_map','01_methods_map','03_staggered_loop','04_fem_pipeline',
             '05_autograd_inverse','05a_backpropagation','06_learning_cycle']
    for name in names:
        # Retain old PNG URLs with the current drawing; HTML selects vector SVG.
        shutil.copy2(root/'source/book/figures'/f'{name}.png',root/'book/_images'/f'{name}.png')
    slides = root/'source/slides'
    with zipfile.ZipFile(root/'slides/phast_latex_sources.zip','w',zipfile.ZIP_DEFLATED) as archive:
        sources = [slides/p for p in ['phast_autumn_school_2026.tex','phast_autumn_school_2026.pdf',
            'build_beamer_figures.py','render_beamer.py','README.md',
            'beamer_speaker_notes.md','beamer_slide_manifest.json']]
        sources += sorted((slides/'latex_figures').iterdir())
        for src in sources:
            if src.is_file(): archive.write(src, src.relative_to(slides))
    files = public_inventory(root)
    manifest = json.loads((root/'MANIFEST.json').read_text())
    manifest.update(version=args.version, date=date.today().isoformat(),
                    change_scope='PhAST dark theme, integrated inverse and history lessons, academic prose, revised animations and current teaching slides',
                    runtime_scope='Exact-source local rehearsal of six classroom notebooks, local diffusion run and retained HPC inverse receipts; authenticated Colab rehearsal tracked in delivery plan',
                    delivery_formats=['HTML book', 'Jupyter notebooks', 'editable PowerPoint', 'native Keynote', 'slide PDFs', 'animation assets'],
                    printable_book='archived by maintainer request')
    manifest['files'] = {f:sha(root/f) for f in files}
    (root/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if args.output:
        destination = args.output.resolve()
        destination.mkdir(parents=True,exist_ok=False)
        for f in files+['MANIFEST.json']:
            dst = destination/f
            dst.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(root/f,dst)
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
