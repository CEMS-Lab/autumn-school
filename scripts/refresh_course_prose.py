"""Apply the September print-edition prose corrections; preserve numerical cells."""
from pathlib import Path
import re
import nbformat

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = ROOT / 'source/book/lectures/01_fracture_and_phast.md'
    s = p.read_text().replace('**45 minutes.** ', '')
    s = re.sub(r' · \d+–\d+ minutes', '', s)
    p.write_text(s)
    replacements = {
        '01_simulate_fracture': {
            'This notebook shows dynamic fracture simulation. We start from defining geometry to animated\nresults using the Open Source PhAST solver.\nas a set of reusable functions for the exercises at the end.':
                'This notebook develops a dynamic fracture simulation with PhAST, from\ngeometry and material data to animated results. Reusable functions support\nthe parameter studies at the end.',
            'libraries, so one `apt` package is installed first on Colab. The whole cell\ntakes one to three minutes on a fresh runtime.':
                'libraries, so one `apt` package is installed first on Colab.',
            'A CPU runtime is sufficient. The reference configuration completes in roughly\nhalf a minute to two minutes depending on the machine.':
                'A CPU runtime is sufficient. Execution time depends on the machine, mesh\nand selected output settings.',
            '`stride` selects every nth stored snapshot. A stride of 4 gives a smooth\nanimation from the reference run and keeps the whole section under half a minute\non a Colab CPU runtime. Set `SAVE_GIFS = True` if you also want GIF files in the\nworking directory for a report or for offline viewing; writing them roughly\ntriples the time.':
                '`stride` selects every nth stored snapshot. A stride of 4 reduces the\nnumber of frames while retaining the main stages of crack propagation. Set\n`SAVE_GIFS = True` to save GIF files for a report or offline viewing.',
            'which is\nwhat makes each one cheap and well behaved.':
                'which allows different numerical methods for the two subproblems.\nTheir convergence and stability still require separate checks.',
            '`step_solve_damage()` is the one to remember. **The third laboratory replaces\nexactly that call with a trained network, and changes nothing else.**':
                'In NB3, the analogous damage-solve operation is replaced by a trained\nnetwork. Its FEM and GNN routes share the same mechanics, geometry and loading.\nNB3 itself uses a different specimen, constitutive law and quasi-static solver\nfrom this dynamic plate example.',
            'Everything below the solver is post-processing. The `RunViewer` class collects':
                '`RunViewer` is a helper class defined in this notebook, not a public\nPhAST class. It uses PhAST result and field interfaces and collects',
        },
        '03_learning_and_hybrid': {
            'fix horizontal displacement and increase vertical displacement to 0.04 mm over\n500 increments.':
                'fix horizontal displacement and increase vertical displacement to 0.04 mm\nover `N_STEPS` increments.',
            'The 500 increments describe the loading schedule; they are not dynamic time\nsteps.':
                'The load increments describe the loading schedule; they are not dynamic\ntime steps. The supplied code selects 60 increments with `QUICK_TEST=True`\nand 500 with `QUICK_TEST=False`, unless `PHAST_DEMO_STEPS` overrides the count.\nUse the same count for both routes. A coarser schedule is not evidence of\nload-increment convergence.',
            'benchmark label. Retain the default 500 increments for the first comparison.':
                'benchmark label. Record `N_STEPS` with the results so comparisons use\nthe same loading schedule.',
        },
    }
    for stem, changes in replacements.items():
        path = ROOT / 'notebooks/classroom' / (stem + '.ipynb')
        nb = nbformat.read(path, 4)
        before = [(c.source, c.get('outputs'), c.get('execution_count'))
                  for c in nb.cells if c.cell_type == 'code']
        for old, new in changes.items():
            matched = False
            for c in nb.cells:
                if c.cell_type == 'markdown' and old in c.source:
                    c.source = c.source.replace(old, new)
                    matched = True
            if not matched and not any(new in c.source for c in nb.cells):
                raise ValueError(f'Expected passage missing in {stem}: {old[:70]}')
        after = [(c.source, c.get('outputs'), c.get('execution_count'))
                 for c in nb.cells if c.cell_type == 'code']
        assert before == after
        nbformat.write(nb, path)
    print('Prose refreshed; numerical cells and saved outputs unchanged.')


if __name__ == '__main__':
    main()
