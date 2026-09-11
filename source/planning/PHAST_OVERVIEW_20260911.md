# PhAST overview module

Owning issue: [#12](https://github.com/CEMS-Lab/autumn-school/issues/12).
Reference-design issue: [#14](https://github.com/CEMS-Lab/autumn-school/issues/14).

## Purpose and scope

Create six reusable public-source introduction slides using the supplied PICT screenshots and
transcript for the narrative pattern: solver identity, numerical operators,
derivatives, learned components and applications. A seventh local review slide
uses a retained FEM/hybrid animation from the author's ECCOMAS deck.
Use original PhAST branding and retained solid/fracture-mechanics results. The existing 32-slide
lecture and its 45/55/50-minute allocation remain unchanged during review.

## Ownership

The course integrator owns `source/slides/phast-overview/`,
`output/phast-overview-20260911/`, this plan,
`evidence/phast_overview_20260911.*`, a bounded `TODAY.md` entry and manifest
refresh. A separate reviewer checks scientific wording and public asset scope.
Numerical solver code and inverse research remain with their current authors.

## Slide sequence

1. PhAST identity: a two-dimensional phase-field fracture solver in PyTorch.
2. Tensor operators: mechanics, history and bounded damage updates.
3. Reverse accumulation: a terminal loss and a shared parameter used at each step.
4. Experimental learned-damage interface: proposal, checks and classical correction.
5. Optional local conference insert: classical and learned-assisted fields around three holes.
6. Public result: notched-holed fracture field and a response curve redrawn from its CSV.
7. Explore PhAST: impact fracture, repository QR and book links.

The public storyboard has six slides; the combined local storyboard has seven.
MP4s are embedded on the introduction and optional conference slide. Original
GIFs and static PNGs accompany the local media package.

## Design contract

- White 16:9 canvas with the existing Arial type roles and blue/orange highlights.
- Preserve the original PhAST icon in full and at its original aspect ratio.
  Use a larger introduction mark and a fixed upper-right position thereafter.
- Give each slide one visual centre. Align equations and figures on the existing
  two-column grid. Preserve full-domain evidence and colourbars.
- Use LaTeX for mathematics, retain its source and define the derivative notation.
- Keep normal text editable and store sources and physical interpretation in notes.
- Use the screenshots for composition only. PICT logos, fluid-specific capabilities
  and numerical performance comparisons belong to that solver.

## Acceptance

- [x] Six public-source slides and one optional conference insert, with PhAST logo and repository QR.
- [x] Scientific review of the gradient formula, experimental interface and result labels.
- [x] Rendered inspection of all seven slides and consistent font/placement roles.
- [x] Native Keynote save, close, reopen, seven notes and two embedded movies verified.
- [x] Play branching and conference clips in Keynote; retain developed-crack posters.
- [x] Local source, checklist and delivery receipts updated.
- [ ] Approve source-run provenance and publication of the conference comparison.
- [ ] Lecturer selects insertion/replacement points and checks timing.
- [ ] Test the presentation machine and PowerPoint playback.

The completed checks describe this local module. Insertion and rehearsal remain
part of the complete course-delivery review.
