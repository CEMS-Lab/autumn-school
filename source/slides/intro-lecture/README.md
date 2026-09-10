# Introductory lecture deck

Presented by Sathiskumar A. Ponnusami, Queen Mary University of London ·
CEMS-Lab, for the UKACM Autumn School 2026. Creator attribution is retained in
standard document metadata and presenter notes.

## Current files

The 10 September animated candidate is in `output/lecture-20260910/`:

- `phast_lecture_animated.pptx`: a 23-slide editable lecture spine with five
  embedded H.264 movies, native static posters and presenter pause questions.
- `phast_lecture_animated.key`: the native Keynote candidate, imported and
  saved locally after successful playback of all five animations.
- `speaker_notes.md`, `media_manifest.json` and `package_checks.json`: teaching
  notes, original-media provenance and reproducible package checks.
- `media/`: the five portable movies and their PNG posters.

See [the lecture mapping](ANIMATED_LECTURE_MAP.md) for the placement of these
slides within the three lecture hours and the three practical hours. Keynote
import and playback are verified locally; the remaining presentation-machine
checks are listed below.

Build and check this candidate from the repository root:

```bash
python source/slides/intro-lecture/build_animated_deck.py
python source/slides/intro-lecture/verify_animated_deck.py
```

The previously validated fallback remains in `output/intro-lecture-20260909/`:

- `phast_lecture_introduction_v7.pptx`: 18 slides with editable text and diagrams.
- `phast_lecture_introduction_v7.key`: the native Keynote edition.
- `phast_lecture_introduction_v7.pdf`: the rendered introductory handout.

The v7 introduction continues the four-slide original, preserving its Helvetica
Neue typography and colour direction. The separate 44-slide lecture resource
covers the broader six-hour subject sequence. The original presenter file is
preserved.

## Editing and building

`build_animated_deck.py` reads v7 without modifying it, preserves its eighteen
slides, and inserts five original course animations in lecture order. Native
text uses Arial for consistent rendering, white backgrounds and the PhAST
orange/blue accents. Equations retain their original PNG and LaTeX sources.
Each movie has an embedded poster and a separate native picture beneath it so
static exports remain readable. The history movie is converted from 0.5 to
30 frames per second while retaining each original two-second state.

`build_deck.mjs` imports the presenter's PowerPoint export and generates the v7
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

### Current animated candidate

The 23-slide PowerPoint passes OOXML and package checks. All slides were
rendered and visually inspected, including the five scientific posters.
Native Keynote imported the fully downloaded local PowerPoint without a
warning. All five animation slides—4, 7, 13, 15 and 21—played with advancing
scientific frames. The saved `.key` contains the same five MP4s as the `.pptx`,
verified by their hashes. See [the evidence record](../../../evidence/slides_20260910.md).

Keynote initially selects the movie's opening frame over the complete embedded
poster. A clearer preplay frame remains a cosmetic improvement. Explicit
pausing, seeking/replay, native PowerPoint playback, offline portability on the
presentation machine and the full timed lecture rehearsal remain to check.
The forward-practical mesh, fields and loading configuration remain consistent
with the retained 8,385-node/16,384-triangle baseline.

### Preserved v7 fallback

The v7 PowerPoint passes package, geometry and font checks: 18 slides,
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
