# Short animations for the fracture course

Open assets/animations/index.html from the complete repository or animation
kit. The adjacent animation_gallery.ipynb has player cells, questions, worked
answers and text descriptions. MP4 files are silent, H.264/yuv420p, 1280×720
at 30 fps; every clip is shorter than 35 seconds.

Insert a local MP4 into PowerPoint or Keynote as a video and choose
click-to-play. Preserve the caption that states its analytic/schematic
scope. Use the supplied PNG poster for print and alternative reading.
Rehearse playback in your chosen presentation software or notebook environment.

Students use a video player to view the clips. Scene authoring uses Python
3.10.18, Manim 0.19.1, a LaTeX installation and FFmpeg.

## Rebuild the editable scenes

From the repository root:

```bash
python -m manim render --renderer cairo --format mp4 --fps 30 \
  --disable_caching --verbosity WARNING --progress_bar none \
  -r 1280,720 --media_dir .build/animations/mechanics \
  source/animations/mechanics_scenes.py PhaseFieldBand ExplicitImplicitStep
python -m manim render --renderer cairo --format mp4 --fps 30 \
  --disable_caching --verbosity WARNING --progress_bar none \
  -r 1280,720 --media_dir .build/animations/learning \
  source/animations/learning_scenes.py ReverseAccumulation CheckedLearnedProposal
```

The mechanics scene files are in
.build/animations/mechanics/videos/mechanics_scenes/720p30/.
The learning scene files follow the equivalent learning directory.
Copy the rendered videos to their documented asset names using FFmpeg with
H.264/yuv420p and faststart. The learning module has an export entry point:

```bash
python source/animations/learning_scenes.py --export-assets --render-seconds MEASURED_SECONDS
python source/animations/build_gallery.py
```

Replace MEASURED_SECONDS with the measured authoring render duration.
That duration measures animation authoring. Review posters, intermediate
frames and captions after any change. The gallery builder checks durations,
codec and full video decoding and generates its own media manifest.

The current three-clip caption revision is recorded in
assets/animations/caption_render_receipt.json, with source and media hashes,
authoring times, frame-review locations and local player checks.

Each scene has a local adapter for Manim's path-quoting bug with apostrophes.
The adapter is local to the scene source. The diagrams are original and follow
DESIGN_STANDARD.md in the full course repository.

## Teaching scope

- PhaseFieldBand varies the regularisation length of an analytic isolated AT2
  damage profile around a fixed crack centre.
- ExplicitImplicitStep explains one partitioned dynamic update and its
  acceptance checks. The PhAST practical uses quasistatic mechanics.
- ReverseAccumulation assumes differentiable maps, a fixed initial state and
  a scalar loss depending on the terminal state.
- CheckedLearnedProposal states a compatible interface, admissibility and
  residual/constraint checks, reference correction, rechecking and failure.
  Field quality and complete computational cost guide assessment of a chosen model.

DIFFERENTIABLE_SOLVER_TEACHING_NOTES.md at the repository/kit root supplies
the equations and scientific references. Use the clips alongside the book's
derivations and the corresponding lecture diagrams.
