"""Publish the supplied Day 2 notebooks without claiming a new execution.

Canonical notebooks are in notebooks/classroom. This builds reading and download
copies, retaining all code and outputs, and adds course navigation and guidance.
"""
from pathlib import Path
import copy
import hashlib
import json
import nbformat
import re

ROOT = Path(__file__).resolve().parents[3]
NAMES = ('01_simulate_fracture', '02_gradients_and_recovery', '03_learning_and_hybrid')
EDITION_NOTES = (
    'Run the notebook to generate its plots and animations; this edition includes the code without retained run outputs. Complete the reference before trying the additional parameter studies.',
    'Figures and animation are retained from the supplied notebook. This book update preserves those outputs. The calculation uses SGD with momentum 0.5; the lecture deck also illustrates plain SGD, which has a different optimisation history.',
    'Obtain the instructor-supplied mesh_graph_net.pt before starting; Colab requests an upload. Run the notebook to generate the three comparisons and their plots. Fresh whole-notebook timing remains to be recorded.',
)
TAKEAWAYS = (
    ['Named mesh regions connect geometry to boundary conditions.', 'Dynamic mechanics retains inertia and requires a stable time step.', 'Fixed colour scales make evolving fields comparable.'],
    ['The force remains 4000 N throughout the inverse loop.', 'Autograd differentiates the current forward solve and scalar loss.', 'The optimiser selects the next modulus; each update requires another forward evaluation.'],
    ['Mechanics remains in PhAST for every damage route.', 'A learned initial guess is corrected by the classical damage solve.', 'Direct replacement is checked and may use classical fallback; compare complete cost and field accuracy.'],
)
QUESTIONS = (
    ('Why does refining the mesh increase dynamic computation time?', 'Consider the smallest element and the wave speed.', 'The explicit stability limit scales with the smallest element dimension divided by wave speed. A smaller element reduces the stable time step and increases the number of updates over the same physical duration.'),
    ('What happens to the tip displacement when E doubles at the same force?', 'Use u(L) = F L / (E A).', 'For this uniform linear-elastic bar, the displacement halves. The analytical relation also provides an independent check of the PhAST result.'),
    ('What evidence is needed to assess a direct damage replacement?', 'Compare the damage equation, constraints and the reference field.', 'Compare projected residuals, damage bounds, irreversibility and field differences with the classical reference. Measure complete runtime, including prediction, checks and fallback.'),
)


def fingerprint(nb):
    return [(c.source, c.get('outputs', []), c.get('execution_count'))
            for c in nb.cells if c.cell_type == 'code']


def main():
    report = []
    for i, name in enumerate(NAMES):
        path = ROOT / 'notebooks/classroom' / (name + '.ipynb')
        original = nbformat.read(path, as_version=4)
        status = EDITION_NOTES[i]
        for surface in ('book', 'study', 'solutions'):
            nb = copy.deepcopy(original)
            # Keep a valid heading hierarchy without changing numerical cells.
            nb.cells[0].source = nb.cells[0].source.replace('\n### ', '\n## ')
            nb.metadata.setdefault('language_info', {})['pygments_lexer'] = 'ipython3'
            url = 'https://colab.research.google.com/github/CEMS-Lab/autumn-school/blob/main/notebooks/study/classroom/' + name + '.ipynb'
            download_root = '../../' if surface == 'book' else 'https://cems-lab.github.io/autumn-school/'
            badges = ('\n\n<div class="badge-row">\n'
                      f'<a class="badge-colab" href="{url}">Open in Colab (published edition)</a> · '
                      f'<a class="badge-link" href="{download_root}notebooks/study/classroom/{name}.ipynb">Download notebook</a> · '
                      f'<a class="badge-link" href="{download_root}notebooks/solutions/classroom/{name}.ipynb">Download with recap answer</a> · '
                      f'<a class="badge-link" href="{download_root}SETUP.md">Environment setup</a>\n</div>\n')
            nb.cells[0].source += badges
            nb.cells.insert(1, nbformat.v4.new_markdown_cell('**Day 3 · PhAST practical. Updated 15 September 2026.** ' + status))
            q, hint, answer = QUESTIONS[i]
            recap = '## Key takeaways\n\n' + '\n'.join('- ' + t for t in TAKEAWAYS[i])
            recap += '\n\n### Consolidation\n\n' + q
            recap += f'\n\n<details class="course-hint"><summary>Hint</summary><p>{hint}</p></details>'
            if surface != 'study':
                recap += f'\n\n<details class="course-solution"><summary>Conceptual answer</summary><p>{answer}</p></details>'
            exercise_index = next(j for j, cell in enumerate(nb.cells)
                                  if cell.cell_type == 'markdown'
                                  and re.search(r'^#{2,3}\s+(?:\d+\.\s+)?Exercises\b',
                                                cell.source, flags=re.M | re.I))
            nb.cells.insert(exercise_index, nbformat.v4.new_markdown_cell(recap))
            if surface == 'book':
                # Display the retained PyTorch sparse-invariant warning in full.
                nb.metadata['mystnb'] = {'execution_mode': 'off', 'output_stderr': 'show'}
                folder = ROOT / 'source/book/classroom'
            else:
                folder = ROOT / 'notebooks' / surface / 'classroom'
            for j, cell in enumerate(nb.cells):
                cell['id'] = f'day2-{i+1}-{j:03d}'
            assert fingerprint(nb) == fingerprint(original), name
            nbformat.validate(nb)
            folder.mkdir(parents=True, exist_ok=True)
            nbformat.write(nb, folder / path.name)
        report.append({'notebook': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'code_cells': len(fingerprint(original)), 'fresh_execution': False,
                       'outputs_retained': sum(len(c.get('outputs', [])) for c in original.cells)})
    (ROOT / 'evidence/day2_book_import.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
