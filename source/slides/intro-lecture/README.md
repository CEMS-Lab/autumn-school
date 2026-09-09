# Introductory lecture deck

Presented by Sathiskumar A. Ponnusami, Queen Mary University of London ·
CEMS-Lab, for the UKACM Autumn School 2026. Creator attribution is retained in
standard document metadata and presenter notes.

## Current files

The latest generated revision is in `output/intro-lecture-20260909/`:

- `phast_lecture_introduction_v7.pptx`: 18 slides with editable text and diagrams.
- `phast_lecture_introduction_v7.key`: the native Keynote edition.
- `phast_lecture_introduction_v7.pdf`: the rendered introductory handout.

This introduction continues the four-slide original, preserving its Helvetica
Neue typography and colour direction. The separate 44-slide lecture resource
covers the broader six-hour subject sequence. The original presenter file is
preserved.

## Editing and building

`build_deck.mjs` imports the presenter's PowerPoint export and generates the
continuation with the configured JavaScript presentation library. Set
`COURSE_ROOT`, `PRESENTATION_SKILL_DIR`, `RUNTIME_PYTHON` and
`RUNTIME_NODE_MODULES`. Set `SOURCE_PPTX` to an absolute path to your supplied
PowerPoint export; the default authoring location is
`.build/intro-lecture-20260909/source/keynote-original.pptx`.

`build_equations.py` contains editable LaTeX strings and original scientific
figures. SVG sources and high-resolution PNGs are retained. The deck embeds
PNG equations for tested Keynote compatibility; edit their source to change
the mathematics. Body text, diagram boxes and connectors are editable.

`normalise_template_media.py` converts the three inherited backgrounds to
8-bit sRGB PNGs while preserving all 19 scientific images. Use a fresh
validation receipt after changes, import in Keynote, export PDF and inspect
the rendered pages. `stamp_metadata.py` retains ordinary creator metadata,
which remains editable through normal document tools.

## Verification

The current PowerPoint passes package, geometry and font checks: 18 slides,
16:9 dimensions, Helvetica Neue and all 19 scientific images. The 18 Keynote
PDF pages match the previously reviewed v6 pages pixel-for-pixel at 1600 × 900.
Revision v7 improves the presenter notes.

The native file opens successfully from a local disk copy. Opening the OneDrive
path encountered a stalled download prompt during verification; allow syncing
to complete or use a locally downloaded copy before presenting. See
[COMPATIBILITY_QA.md](COMPATIBILITY_QA.md) for the exact scope and file hashes.
Validation covers the PowerPoint package and native Keynote/PDF rendering;
include PowerPoint playback in the presentation-machine rehearsal.

The lesson identifies the isotropic AT2 model, quasistatic sparse-direct
forward practical, schematic tensor/matrix-free operations and standalone
diffusion sensitivity example. The course delivery checklist tracks the full
timed rehearsal and authenticated Colab run.
