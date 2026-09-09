# Keynote compatibility check — 9 September 2026

Current delivery: `phast_lecture_introduction_v7` in PowerPoint, Keynote and PDF.

## Verified observations

- High-resolution PNG equations and diagrams preserve the scientific media in
  the tested native Keynote PDF export.
- Three inherited background images use 8-bit sRGB PNGs. The package contains
  19 scientific images and uses native editable text and diagram connectors.
- Keynote reports 18 slides at 1920 × 1080 points. Scientific image counts by
  slide are `0,0,0,0,0,3,3,0,0,4,3,1,1,2,1,1,0,0`.
- All 18 v7 PDF pages are pixel-identical to the visually reviewed v6 export
  at 1600 × 900. Revision v7 changes presenter-note prose.
- The original Keynote is preserved. Superseded generated introductory
  versions are recoverable in the local Trash.
- The saved v7 file opens successfully from a local disk copy, showing the
  complete 18-slide document. Reopening its OneDrive location encountered a
  stalled download prompt and an AppleEvent timeout. Local-copy verification
  distinguishes document readability from cloud hydration.
- The earlier user-reported popup remains a separate diagnostic question:
  capture its exact message if it recurs. These checks cover the observed
  Keynote import/render and local native-file opening.

## Current hashes (SHA-256)

| File | Hash |
| --- | --- |
| PowerPoint | `58f9726cf7d78c745e7dfcb3e06f437faab19daa0aa6703c2a6bb1820979e8bf` |
| Keynote | `ec3fb2e0fc4559fc2f5eb90089acf12e81c7e8231fca4eb374c4387705f419d4` |
| PDF | `a86f41cc4561455916030b8e20f1a8d3d893cf4cbfa34edbae6931ed090f0698` |

Private authoring receipts and review renders are retained under
`.build/intro-lecture-20260909/`. Include native PowerPoint playback and the
full teaching rehearsal in the presentation-machine checks. Ordinary metadata
provides editable creator attribution.
