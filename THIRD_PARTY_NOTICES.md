# Third-party software, fonts and notices

This publication includes generated browser assets and a pinned public PhAST
source snapshot. Their existing licences and copyright notices remain in force.
**This document does not assign a licence to the original course text,
notebooks, exercises, solutions, diagrams or data.** See [ATTRIBUTION.md](ATTRIBUTION.md)
for that separate boundary. Citing D2L, ADL4P or CWI does not transfer their
licences to this course; their pages, figures and exercise code are not bundled.

## Included components

| Component and identified version | Where used | Preserved licence/notice |
| --- | --- | --- |
| PhAST 0.16.2, revision `f6324f899f0701769810be117f27f1208f7a582e` | `vendor/PhAST/`; public solver source, without Git history | [PhAST MIT licence](vendor/PhAST/LICENSE) and [source manifest](vendor/PhAST/COURSE_SOURCE_MANIFEST.json) |
| Sphinx 7.4.7 | Generated book HTML, base CSS and language data | [Full Sphinx BSD and incorporated-software notices](licenses/sphinx-7.4.7-LICENSE.rst) |
| Sphinx Immaterial 0.13.9 | Book theme, bundled JavaScript/CSS and icons | [Full upstream-distribution licence and third-party notices](licenses/sphinx-immaterial-0.13.9-LICENSE.txt) |
| sphinx-copybutton 0.5.2 | Book copy-button JavaScript/CSS | [MIT](licenses/sphinx-copybutton-0.5.2-LICENSE.txt) |
| clipboard.js 2.0.8 | `book/_static/clipboard.min.js`; version identified from its retained header | [MIT, Zeno Rocha](licenses/clipboard-2.0.8-LICENSE.txt) |
| MyST-NB 1.4.0 | Notebook-derived book pages and styles | [BSD-3-Clause](licenses/myst-nb-1.4.0-LICENSE.txt) |
| nbconvert 7.17.0 | Standalone notebook HTML templates and styles | [BSD-3-Clause](licenses/nbconvert-7.17.0-LICENSE.txt) |
| Pygments 2.20.0 | Generated code highlighting | [BSD](licenses/pygments-2.20.0-LICENSE.txt) |
| jupyterlab-pygments 0.3.0 | Notebook HTML highlighting styles | [BSD-3-Clause](licenses/jupyterlab-pygments-0.3.0-LICENSE.txt) |
| MathJax 3.2.2 | Local equation rendering and its browser font assets | [Apache-2.0](licenses/mathjax-3.2.2-LICENSE.txt); also retained at `book/_static/mathjax/LICENSE` |
| Roboto | Unmodified text fonts under `book/_static/fonts/` | [SIL OFL 1.1; Copyright 2011 The Roboto Project Authors](licenses/roboto-OFL.txt) |
| Roboto Mono | Unmodified monospace fonts under `book/_static/fonts/` | [SIL OFL 1.1; Copyright 2015 The Roboto Mono Project Authors](licenses/roboto-mono-OFL.txt) |
| DejaVu Sans and DejaVu Sans Display, bundled by Matplotlib 3.10.8 | Glyph-subset WOFF2 fonts embedded in the seven course-flowchart SVGs; renamed `PHAST Diagram Sans` families | [Full Bitstream/DejaVu/Arev notices](licenses/dejavu-matplotlib-3.10.8-LICENSE.txt) |
| STIX mathematical size glyphs, bundled by Matplotlib 3.10.8 | Glyph-subset WOFF2 fonts embedded where the flowcharts use mathematical fences; renamed `PHAST Diagram Math Size` families | [Full Matplotlib STIX notice and SIL OFL 1.1](licenses/stix-matplotlib-3.10.8-LICENSE.txt) |

The Sphinx Immaterial notice is preserved in full rather than abridged. It
includes notices for inherited themes, embedded JavaScript dependencies and
icon sets, including the Font Awesome attribution retained in the generated
theme. Its file-specific sections also describe components from the upstream
distribution that are not shipped here (for example, cppreference index data
and Mermaid). Those sections apply to the named upstream files, **not** to this
course's original content. They do not imply that these unbundled components
are present. No icon designs were modified. The diagram fonts are subsets of
Matplotlib's bundled fonts: unused glyphs are removed, family names are changed,
and retained glyph outlines are unchanged. Their original font licences remain
in force and do not license the original course diagrams.

## Provenance and verification

- [Licence provenance and SHA-256 hashes](licenses/provenance.json) identify
  the source and version of every copied notice. The licence files themselves
  are verbatim, including their copyright notices.
- The Sphinx, theme, copy-button, MyST-NB, nbconvert and highlighting licences
  came from the exact installed package distributions used to create the
  reviewed exports. Project links in the provenance record identify upstream
  projects; the copied distribution text and hash are the retained evidence.
- MathJax's version was identified in the bundled JavaScript. Its licence was
  copied byte-for-byte from the generated book's existing licence file.
- Clipboard's licence came from the official `v2.0.8` tag, matching the
  version printed in the bundled standalone script. Any other Clipboard
  version embedded in the theme remains covered by that theme's complete
  third-party notice file.
- The Roboto and Roboto Mono OFL texts came from pinned official upstream
  licence revisions. Their copyright holders and licence identifiers match
  the bundled fonts' name-table metadata. These upstream licence revisions
  identify the notices, not a claim that the font binaries were rebuilt from
  those Git commits.
- [Font inventory](licenses/font_inventory.json) records the 278 bundled
  Roboto/Roboto Mono files, their actual binary version strings, copyright
  metadata and hashes. Preserve the corresponding OFL notice with any
  redistribution of these font files.
- Every flowchart SVG embeds its required font faces as data-URI WOFF2 subsets,
  without remote font requests or a dependency on installed system fonts. Its
  readable XML metadata preserves the complete font notices, source font
  filenames and versions, source/subset SHA-256 hashes, and retained codepoints.
  `source/book/scripts/embed_svg_fonts.py` reproduces these subsets from the
  Matplotlib authoring distribution; text remains selectable in the SVG.

Python runtime dependencies installed during setup (such as PyTorch and
Matplotlib) are not bundled as package binaries here. Their own distributions
provide their licences. The supplied course model checkpoint and numerical
arrays are course-generated teaching artifacts, not third-party model weights
or paper datasets.

Prepared 9 September 2026. Preserve this file, `licenses/`, existing inline
attributions and `vendor/PhAST/LICENSE` when redistributing the supplied assets.
