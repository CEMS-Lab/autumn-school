"""Manifest-only packaging tests; all mutations stay inside temporary fixtures."""
from contextlib import redirect_stdout, redirect_stderr
from datetime import date
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).with_name('package_public_edition.py')
spec = importlib.util.spec_from_file_location('course_packaging', SCRIPT)
packaging = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packaging)


class ManifestOnlyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='phast-manifest-test-')
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        contents = {
            '.gitignore': '.build/\nreviews/\n',
            'README.md': 'Course fixture\n',
            'book/index.html': '<h1>Reviewed local book</h1>\n',
            'source/slides/phast_autumn_school_2026.pdf': 'retained source slide sentinel',
            'slides/phast_autumn_school_2026.pdf': 'retained public slide sentinel',
            'slides/phast_latex_sources.zip': 'retained source zip sentinel',
            'output/lecture-20260910/current.key': 'native animated keynote sentinel',
            '.build/slides/phast_autumn_school_2026.pdf': 'obsolete build slide sentinel',
            'source/book/research/retained.md': 'approved public retained evidence',
        }
        for name, content in contents.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        self.original_metadata = {
            'title': 'PhAST fixture', 'version': '0.16.2', 'date': '2026-09-09',
            'runtime_scope': 'Previous local and retained HPC evidence scope',
            'retained_hpc_receipts': {'date': '2026-09-05', 'jobs': ['retained-fixture-job']},
            'files': {},
        }
        (self.root / 'MANIFEST.json').write_text(json.dumps(self.original_metadata))
        subprocess.run(['git', 'add', '.'], cwd=self.root, check=True)
        subprocess.run(['git', '-c', 'user.name=Manifest Test', '-c', 'user.email=test@example.invalid',
                        'commit', '-qm', 'fixture'], cwd=self.root, check=True)

    def tearDown(self):
        self.temp.cleanup()

    def snapshot(self):
        return {path.relative_to(self.root).as_posix(): path.read_bytes()
                for path in self.root.rglob('*') if path.is_file() and '.git' not in path.relative_to(self.root).parts}

    def invoke(self, args):
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            packaging.main(args, root=self.root)
        return json.loads(output.getvalue())

    def test_dry_run_is_completely_read_only(self):
        before = self.snapshot()
        report = self.invoke(['--manifest-only', '--dry-run'])
        self.assertEqual(before, self.snapshot())
        self.assertEqual(report['version'], '0.16.2')
        self.assertEqual(report['manifest'], 'dry-run; unchanged')

    def test_only_manifest_changes_and_prior_evidence_survives(self):
        before = self.snapshot()
        report = self.invoke(['--manifest-only'])
        after = self.snapshot()
        self.assertEqual(set(before), set(after))
        self.assertEqual([name for name in before if before[name] != after[name]], ['MANIFEST.json'])
        manifest = json.loads(after['MANIFEST.json'])
        self.assertEqual(manifest['version'], '0.16.2')
        self.assertEqual(manifest['published_version'], '0.16.2')
        self.assertEqual(manifest['date'], date.today().isoformat())
        self.assertEqual(manifest['delivery_status'], 'local reviewed candidate; publication pending')
        expected_revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=self.root, text=True).strip()
        self.assertEqual(manifest['base_git_revision'], expected_revision)
        self.assertEqual(manifest['retained_hpc_receipts'], self.original_metadata['retained_hpc_receipts'])
        self.assertEqual(manifest['retained_evidence_metadata']['prior_runtime_scope'], self.original_metadata['runtime_scope'])
        self.assertNotIn('MANIFEST.json', manifest['files'])
        self.assertNotIn('.build/slides/phast_autumn_school_2026.pdf', manifest['files'])
        self.assertIn('output/lecture-20260910/current.key', manifest['files'])
        self.assertEqual(report['verification'], 'inventory and all SHA-256 hashes match')
        before_check = self.snapshot()
        self.invoke(['--check-only'])
        self.assertEqual(before_check, self.snapshot())

    def test_explicit_candidate_version_preserves_published_version(self):
        self.invoke(['--manifest-only', '--version', '0.17.0-candidate'])
        manifest = json.loads((self.root / 'MANIFEST.json').read_text())
        self.assertEqual(manifest['version'], '0.17.0-candidate')
        self.assertEqual(manifest['published_version'], '0.16.2')
        self.invoke(['--manifest-only'])
        self.assertEqual(json.loads((self.root / 'MANIFEST.json').read_text())['version'], '0.16.2')

    def test_changed_hash_is_rejected_without_writes(self):
        self.invoke(['--manifest-only'])
        (self.root / 'README.md').write_text('changed payload')
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            self.invoke(['--check-only'])
        self.assertEqual(before, self.snapshot())

    def test_added_and_missing_inventory_are_rejected(self):
        self.invoke(['--manifest-only'])
        extra = self.root / 'new.txt'
        extra.write_text('new public payload')
        with self.assertRaisesRegex(ValueError, 'inventory differs'):
            self.invoke(['--check-only'])
        extra.unlink()
        (self.root / 'README.md').unlink()
        with self.assertRaisesRegex(ValueError, 'inventory differs'):
            self.invoke(['--check-only'])

    def test_forbidden_and_nonlocal_paths_are_rejected(self):
        for name in ('../outside.txt', '/outside.txt', 'MANIFEST.json', '.build/private.txt',
                     '_attachments/private.txt', 'reviews/draft.txt', 'research/private.txt'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                packaging.validate_public_path(self.root, name)
        symlink = self.root / 'linked.txt'
        symlink.symlink_to(self.root / 'README.md')
        with self.assertRaisesRegex(ValueError, 'Non-local payload'):
            packaging.public_inventory(self.root)
        symlink.unlink()
        linked_directory = self.root / 'linked'
        linked_directory.symlink_to(self.root / 'book', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Non-local payload'):
            packaging.validate_public_path(self.root, 'linked/index.html')

    def test_forbidden_declared_manifest_path_is_rejected(self):
        manifest = packaging.candidate_manifest(self.root)
        manifest['files']['../outside.txt'] = '0' * 64
        with self.assertRaises(ValueError):
            packaging.verify_manifest(self.root, manifest)

    def test_mutating_flag_combinations_are_rejected_before_work(self):
        before = self.snapshot()
        for args in (['--manifest-only', '--output', str(self.root / 'edition')],
                     ['--check-only', '--version', '1.0'], ['--dry-run'], []):
            with self.subTest(args=args), self.assertRaises(SystemExit):
                self.invoke(args)
        self.assertEqual(before, self.snapshot())


if __name__ == '__main__':
    unittest.main(verbosity=2)
