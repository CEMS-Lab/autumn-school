---
orphan: true
---

# Inverse visual laboratory: integration contract

This is an inverse-specific application of the shared design standard. It
does not replace the course leader's theme, typography or release decisions.

- White Matplotlib canvas, STIX mathematics, named axes and physical units.
  Sequential viridis for indicator/loss, inferno for damage, diverging colour
  maps only for signed residuals. Reference and prediction share limits.
- Static PNGs at 240 dpi with vector-PDF counterparts. Labels remain separate
  from rasterized finite-element fields. No textual overlays inside plates.
- Full phase-field damage is shown, including diffuse and boundary responses.
  No threshold masking, fabricated crack smoothing or cropped evidence.
- Pair a 3D parameter landscape with a top-down view. Show where the samples
  actually exist. Geometry-domain axes and parameter-domain axes are distinct.
- The dense geometry-image toy and sparse actual fracture map are separately
  labelled. The latter joins 25 samples; it is not a reconstructed global map.
- Do not project a four-frame optimization onto a single-frame loss surface.
  Every animation uses states from one specified observation/parameter contract.
- Videos are opt-in, native-controls MP4, seekable and fullscreen-capable, with
  static figures/posters and download fallbacks. No automatic motion is needed.
- Physical time, observation step and inverse-update index are named explicitly.
  Retained frames advance discretely; no uncomputed fracture states are added.
- Preserve late loss increases and fixed global colour scales. Displayed errors
  assess synthetic results; they are not used as a claim of independent data.
- Integration checks include actual video decode, playback and seeking, not
  just the presence of an MP4 filename. Inspect desktop and mobile renderings.

Only the inverse source subtree is prepared here. Shared conf.py, _static/, the
common design standard, public main and manuscripts are outside this change.
