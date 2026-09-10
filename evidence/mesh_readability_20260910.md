# Mesh readability and documentation continuity

Date: 10 September 2026. Local follow-up to published course revision
`6254c050f1af34efd10ddf1df7c5e80aa8302d40`.
Tracking: course issues #5 and #19, with PhAST documentation issue #4.

## Change and numerical equivalence

The first practical's visible mesh cell now contains three lines: choose the
archive path, call the documented course helper, and inspect node/element counts
and boundary names. `prepare_course_mesh` retains the original coordinate and
connectivity construction, NPZ save/reload, exact array checks and boundary
identification. Solver construction and mesh/initial-damage plotting occupy
separate adjacent cells. A clearly labelled optional example explains import of
an existing compatible `.msh` file through `FEMMesh`.

The generated mesh is exactly the previous 8,385-node, 16,384-T3 mesh. Every
boundary array agrees with the pre-refactor result. Independent 2-by-2-grid,
precision, archive-reload and corruption tests pass. The notebook's physical
configuration and vendored solver remain unchanged. Both newly computed result
NPZ archives and all field/response PNGs are byte-identical to the published
baseline. JSON changes record current timing and source provenance.

## Execution

```bash
python source/notebooks/build_forward_practical.py
python scripts/run_course.py --notebook 1
python scripts/check_forward_practical.py
python scripts/retain_course_runs.py
python source/book/scripts/build_lab_pages.py
python -m sphinx -b html -E -a source/book book -W --keep-going
python scripts/test_course_authoring.py
python scripts/check_book_theme.py
```

The complete changed notebook passed in **92.2464 seconds** after setup,
including both 60-increment calculations, exports/reloads and all figures.
The internal computation timer recorded 88.0289 seconds; reference and half-load
solves took 59.8896 and 25.2751 seconds. Environment: existing Python 3.10.18,
macOS ARM, PyTorch 2.8.0, CPU float64 and four PyTorch threads. This is local
execution evidence; fresh authenticated Colab remains a separate check.

Both runs retain zero warnings, finite states, damage bounds and irreversibility,
exact prescribed boundary values and the previous staggered iterate-change
criterion. The full result-contract checker, including malformed-archive cases,
passed. Six authoring regression tests passed. The strict Sphinx build and
33-page static theme check passed with zero errors.

The current [runtime receipt](notebook_runtime_current.json) identifies the
changed code hash. The unchanged physical configuration SHA-256 is
`31f808405a43c6d9aa88b54041ca8b51fde8f6991c3c149a3d03d23473627aa2`;
the mesh helper file SHA-256 is
`52c41173cf828a0fc3b77f7037ff2540f644d741b587a00a82c729f6ee80d551`.

## Teaching and rendered review

The practice/reference chapter now connects the course quasistatic activity,
the upstream Gmsh/SENT setup and retained B3 dynamic SENT results. It states
the physical question for each and links directly to the official documentation
and versioned public B3 source. The original setup URL was corrected to the
verified `tutorial/notebook_setup.html` endpoint during link checking.

Browser checks passed at 1440- and 390-pixel widths for Lab 01 and the reference
chapter: mathematical rendering, images, page-width containment, upstream links
and the short mesh cell. Desktop/mobile captures were visually inspected; code
blocks retain horizontal scrolling on narrow screens. See the
[browser receipt](mesh_readability_browser_20260910.json).

## Continuing numerical work

This readability refactor preserves the current diffuse-damage response. The
separate canonical-example review assesses actual propagation from existing
public PhAST material. Promotion to a student-run propagation lesson additionally
requires source/configuration alignment, numerical and visual checks, a complete
runtime receipt and the classroom environment test. The book changes passed
review and were authorised for publication on 10 September. Published source
revisions and deployment checks are recorded in course issue #19.
