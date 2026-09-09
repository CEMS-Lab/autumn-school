"""Original schematic animations for the PhAST Autumn School.

Render from the repository root (Manim Community 0.19.1):
    python -m manim --renderer cairo -r 1280,720 --fps 30 \
      --media_dir .build/animations/learning --disable_caching \
      source/animations/learning_scenes.py ReverseAccumulation CheckedLearnedProposal

These scenes explain a computational graph and a checked proposal interface.
The mathematical graph assumes differentiable update maps, a fixed initial
state and a scalar loss depending on the terminal state. The
book gives the additional direct-loss and initial-state terms in the general
case. The checked-proposal animation requires architecture compatibility,
admissibility and the declared residual/constraint check before acceptance.

Visual structure follows DESIGN_STANDARD.md; all artwork here is original.
"""

from manim import (
    DOWN, LEFT, RIGHT, UP, WHITE,
    Arrow, Circle, Create, FadeIn, Indicate,
    Line, MathTex, Polygon, Rectangle, Scene,
    Text, Transform, VGroup,
)
from manim.renderer.cairo_renderer import CairoRenderer
from manim.scene.scene_file_writer import SceneFileWriter


INK = "#20262B"
MUTED = "#52616C"
FORWARD = "#245A81"
REVERSE = "#B85C20"
PARAMETER = "#087F82"
PALE_BLUE = "#EEF4F8"
PALE_TEAL = "#E9F5F3"
PALE_ORANGE = "#FAF0E9"


def prose(text, size=24, color=INK):
    return Text(text, font="Arial", font_size=size, color=color,
                line_spacing=0.9)


def maths(tex, size=31, color=INK):
    return MathTex(tex, font_size=size, color=color)


def arrow(start, end, color=FORWARD, **kwargs):
    return Arrow(start, end, color=color, buff=0.08, stroke_width=3,
                 max_tip_length_to_length_ratio=0.12, **kwargs)


def box(label, position, width=2.0, height=0.94, color=FORWARD, fill=WHITE,
        size=24, equation=False):
    frame = Rectangle(width=width, height=height, stroke_width=2,
                      color=color, fill_color=fill, fill_opacity=1)
    content = maths(label, size) if equation else prose(label, size)
    if content.width > width - 0.2:
        content.scale_to_fit_width(width - 0.2)
    return VGroup(frame, content).move_to(position)


def state(label, position, color=FORWARD):
    return VGroup(Circle(radius=0.38, color=color, stroke_width=2.5,
                         fill_color=WHITE, fill_opacity=1),
                  maths(label, 32)).move_to(position)


def decision(position):
    shape = Polygon(0.84 * LEFT, 0.63 * UP, 0.84 * RIGHT, 0.63 * DOWN,
                    stroke_color=FORWARD, stroke_width=2,
                    fill_color=WHITE, fill_opacity=1)
    return VGroup(shape, prose("Checks\npass?", 21)).move_to(position)


class QuoteSafeWriter(SceneFileWriter):
    """Escape apostrophes in Manim 0.19.1's FFmpeg concat manifest only.

    This is local to these scenes, not a patch of the installed Manim package.
    FFmpeg's concat syntax closes a quote, escapes the apostrophe, then reopens
    the quote. The actual source files and output paths remain unchanged.
    """

    def combine_files(self, input_files, output_file, *args, **kwargs):
        safe_paths = [str(path).replace("'", "'\\''") for path in input_files]
        return super().combine_files(safe_paths, output_file, *args, **kwargs)


class LectureScene(Scene):
    def __init__(self, renderer=None, **kwargs):
        if renderer is None:
            renderer = CairoRenderer(file_writer_class=QuoteSafeWriter)
        super().__init__(renderer=renderer, **kwargs)

    def setup(self):
        self.camera.background_color = WHITE

    def heading(self, title, subtitle):
        h = prose(title, 35).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.45)
        sub = prose(subtitle, 21, MUTED).next_to(h, DOWN, buff=0.17).align_to(h, LEFT)
        self.play(FadeIn(h), FadeIn(sub), run_time=0.8)
        return h, sub


class ReverseAccumulation(LectureScene):
    """Two update maps; every local use of theta contributes to dL/dtheta."""

    def construct(self):
        _, subtitle = self.heading(
            "One shared parameter, several contributions",
            "Forward evaluation first; reverse accumulation second.",
        )
        xs = [-5.2, -1.85, 1.5]
        y = 0.65
        states = [state(rf"x_{i}", [x, y, 0]) for i, x in enumerate(xs)]
        loss = box(r"L=\ell(x_2)", [5.0, y, 0], 2.0, 0.83,
                   equation=True, size=32)
        forward = [arrow(states[i].get_right(), states[i + 1].get_left())
                   for i in range(2)]
        maps = [maths(rf"S_{i}", 28, FORWARD).next_to(a, UP, buff=0.12)
                for i, a in enumerate(forward)]
        loss_arrow = arrow(states[2].get_right(), loss.get_left())
        theta = maths(r"\theta", 35, PARAMETER).move_to([-1.85, 2.0, 0])
        buses = VGroup(
            Line([-3.525, 1.83, 0], [-0.175, 1.83, 0], color=PARAMETER,
                 stroke_width=2),
            arrow([-3.525, 1.83, 0], [-3.525, 1.28, 0], PARAMETER),
            arrow([-0.175, 1.83, 0], [-0.175, 1.28, 0], PARAMETER),
        )
        assumption = VGroup(
            prose("Differentiable update maps", 20, MUTED),
            maths(r"x_{n+1}=S_n(x_n,\theta)", 26),
            maths(r"x_0\ \mathrm{fixed},\quad L=\ell(x_2)", 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.35, 1.98, 0])
        self.play(FadeIn(states[0]), FadeIn(theta), FadeIn(assumption), run_time=0.8)
        self.wait(1.1)
        self.play(Create(buses), run_time=0.8)
        for a, s, label in zip(forward, states[1:], maps):
            self.play(Create(a), FadeIn(label), FadeIn(s), run_time=1.0)
            self.wait(0.5)
        self.play(Create(loss_arrow), FadeIn(loss), run_time=0.9)
        self.wait(1.4)

        reverse_y = -0.97
        adjoints = [state(rf"\lambda_{i}", [x, reverse_y, 0], REVERSE)
                    for i, x in enumerate(xs)]
        seed = arrow([4.0, 0.35, 0], adjoints[2].get_right(), REVERSE)
        seed_label = maths(r"\lambda_2=\nabla_{x_2}L", 28, REVERSE).move_to([4.65, -0.9, 0])
        reverse = [arrow(adjoints[i + 1].get_left(), adjoints[i].get_right(), REVERSE)
                   for i in range(2)]
        reverse_labels = [maths(rf"A_{i}^{{\mathsf{{T}}}}", 27, REVERSE)
                          .next_to(a, UP, buff=0.10) for i, a in enumerate(reverse)]
        self.play(Create(seed), FadeIn(seed_label), FadeIn(adjoints[2]), run_time=1.0)
        self.wait(1.2)
        for i in [1, 0]:
            self.play(Create(reverse[i]), FadeIn(reverse_labels[i]),
                      FadeIn(adjoints[i]), run_time=1.0)
            self.wait(0.6)
        definitions = maths(
            r"A_n=\frac{\partial x_{n+1}}{\partial x_n},\qquad "
            r"B_n=\frac{\partial x_{n+1}}{\partial\theta},\qquad "
            r"\lambda_n=A_n^{\mathsf T}\lambda_{n+1}", 30,
        ).move_to([0, -2.0, 0])
        self.play(FadeIn(definitions), run_time=0.7)
        self.wait(2.0)
        gradient = MathTex(
            r"\frac{dL}{d\theta}=", r"B_0^{\mathsf T}\lambda_1",
            "+", r"B_1^{\mathsf T}\lambda_2",
            font_size=38, color=PARAMETER,
        ).move_to([0, -2.87, 0])
        # Reveal the complete equality: never display a partial sum as dL/dtheta.
        self.play(FadeIn(gradient), run_time=1.0)
        self.wait(1.2)
        self.play(Indicate(gradient[3], color=PARAMETER),
                  Indicate(maps[1], color=PARAMETER), run_time=1.0)
        self.play(Indicate(gradient[1], color=PARAMETER),
                  Indicate(maps[0], color=PARAMETER), run_time=1.0)
        self.wait(1.8)
        note = prose("This is a gradient — an optimiser chooses a separate update.",
                     22, MUTED).move_to([0, -3.6, 0])
        self.play(FadeIn(note), run_time=0.8)
        self.wait(4.0)


class CheckedLearnedProposal(LectureScene):
    """A learned candidate must pass checks; corrected candidates are rechecked."""

    def construct(self):
        _, subtitle = self.heading(
            "Assess a learned proposal before accepting the state",
            "Schematic interface: model architecture must match the declared inputs and output.",
        )
        y = 1.15
        features = box("Feature\ncontract", [-5.55, y, 0], 1.75, 1.03)
        model = box("Radius GNO\nor GNN", [-2.85, y, 0], 2.03, 1.03,
                    color=PARAMETER, fill=PALE_TEAL, size=23)
        proposal = box(r"\widehat d", [-0.25, y, 0], 1.2, 1.03,
                       equation=True, size=39)
        gate = decision([2.15, y, 0])
        accept = box("Accept\nchecked state", [5.3, y, 0], 2.04, 1.03,
                     color=PARAMETER, fill=PALE_TEAL, size=23)
        correction = box("Reference\ncorrection", [2.15, -1.1, 0], 2.05, 1.00,
                         color=REVERSE, fill=PALE_ORANGE, size=23)
        recheck = decision([5.3, -1.1, 0])
        stop = box("Stop / report\nnonconvergence", [5.3, -2.99, 0], 2.6, 0.90,
                   color=REVERSE, fill=PALE_ORANGE, size=21)
        steps = [arrow(features.get_right(), model.get_left()),
                 arrow(model.get_right(), proposal.get_left()),
                 arrow(proposal.get_right(), gate.get_left())]
        yes = arrow(gate.get_right(), accept.get_left(), PARAMETER)
        yes_label = prose("yes", 20, PARAMETER).next_to(yes, UP, buff=0.1)
        no = arrow(gate.get_bottom(), correction.get_top(), REVERSE)
        no_label = prose("no", 20, REVERSE).next_to(no, LEFT, buff=0.12)
        correct_arrow = arrow(correction.get_right(), recheck.get_left(), REVERSE)
        again_yes = arrow(recheck.get_top(), accept.get_bottom(), PARAMETER)
        again_yes_label = prose("yes", 20, PARAMETER).next_to(again_yes, RIGHT, buff=0.10)
        again_no = arrow(recheck.get_bottom(), stop.get_top(), REVERSE)
        again_no_label = prose("no", 20, REVERSE).next_to(again_no, LEFT, buff=0.10)

        interface = VGroup(
            prose("Declare the interface", 24, FORWARD),
            prose("Mesh / graph • node order • units", 22),
            prose("Field channels • normalisation", 22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-3.38, -0.5, 0])
        checks = VGroup(
            prose("Check the proposed state", 24, FORWARD),
            maths(r"0\leq d_{\mathrm{prev}}\leq\widehat d\leq1", 29),
            prose("Declared residual / constraint tolerance", 21),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-3.05, -2.17, 0])
        footer = prose("Assess field quality and the complete computational cost.", 21, MUTED)
        footer.move_to([0, -3.65, 0])
        self.play(FadeIn(features), FadeIn(interface), FadeIn(footer), run_time=0.8)
        self.wait(1.4)
        self.play(Create(steps[0]), FadeIn(model), run_time=0.9)
        self.wait(1.0)
        self.play(Create(steps[1]), FadeIn(proposal), run_time=0.9)
        self.wait(0.8)
        self.play(Create(steps[2]), FadeIn(gate), FadeIn(checks), run_time=0.9)
        self.wait(2.3)
        self.play(Create(yes), FadeIn(yes_label), FadeIn(accept), run_time=0.9)
        self.wait(1.7)
        self.play(Create(no), FadeIn(no_label), FadeIn(correction), run_time=0.9)
        self.wait(1.7)
        self.play(Create(correct_arrow), FadeIn(recheck), run_time=0.9)
        self.wait(1.7)
        self.play(Create(again_yes), FadeIn(again_yes_label),
                  Indicate(accept, color=PARAMETER), run_time=0.9)
        self.wait(1.3)
        self.play(Create(again_no), FadeIn(again_no_label), FadeIn(stop), run_time=0.9)
        self.wait(2.0)
        timing = prose("Time the full route: predict + convert + check + correct.", 21, MUTED)
        timing.move_to(footer)
        self.play(Transform(footer, timing), run_time=0.8)
        self.wait(3.0)


def export_assets(render_seconds):
    """Publish only the two existing local renders and inspection thumbnails.

    Example, after the render command above:
        python source/animations/learning_scenes.py --export-assets \
          --render-seconds 12.25
    """
    import hashlib
    import json
    import platform
    import shutil
    import subprocess
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    destination = root / "assets/animations/learning"
    destination.mkdir(parents=True, exist_ok=True)
    ffmpeg = shutil.which("ffmpeg")
    ffprobe = shutil.which("ffprobe")
    if not ffmpeg or not ffprobe:
        raise RuntimeError("ffmpeg and ffprobe must already be installed")
    media = root / ".build/animations/learning/videos/learning_scenes/720p30"
    records = []
    for scene, stem in [
        ("ReverseAccumulation", "reverse_accumulation"),
        ("CheckedLearnedProposal", "checked_learned_proposal"),
    ]:
        movie = destination / f"{stem}.mp4"
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                        "-i", str(media / f"{scene}.mp4"), "-c", "copy",
                        "-movflags", "+faststart", str(movie)], check=True)
        probe = json.loads(subprocess.check_output([
            ffprobe, "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=codec_name,pix_fmt,width,height,r_frame_rate",
            "-show_entries", "format=duration", "-of", "json", str(movie),
        ]))
        stream = probe["streams"][0]
        assert stream == {"codec_name": "h264", "width": 1280,
                          "height": 720, "pix_fmt": "yuv420p",
                          "r_frame_rate": "30/1"}, stream
        assert 20 < float(probe["format"]["duration"]) < 35
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                        "-ss", "26", "-i", str(movie), "-frames:v", "1",
                        str(destination / f"{stem}.png")], check=True)
        # Six panels in row-major time order: 2, 8, 14, 19, 22 and 26 seconds.
        subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                        "-i", str(movie), "-vf",
                        "select='eq(n,60)+eq(n,240)+eq(n,420)+eq(n,570)+"
                        "eq(n,660)+eq(n,780)',scale=640:360,"
                        "tile=2x3:padding=12:margin=12:color=white",
                        "-frames:v", "1",
                        str(destination / f"{stem}_contact.png")], check=True)
        records.append({
            "scene": scene, "video": f"assets/animations/learning/{movie.name}",
            "sha256": hashlib.sha256(movie.read_bytes()).hexdigest(),
            "duration_seconds": float(probe["format"]["duration"]),
            "video_stream": stream,
        })
    receipt = {
        "scope": "Original schematic animations; no solver or model training executed",
        "authoring_render_seconds": render_seconds,
        "authoring_environment": {"system": platform.system(),
                                  "machine": platform.machine(),
                                  "python": platform.python_version(),
                                  "manim": "0.19.1"},
        "source": "source/animations/learning_scenes.py",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "records": records,
        "limitations": [
            "Not a fracture calculation, full-path derivative test or accelerator benchmark",
            "No fresh Google Colab or PowerPoint playback validation",
            "Reverse graph assumes differentiable maps, fixed x0 and L = ell(x2)",
            "Corrected proposals must pass the stated checks before acceptance",
        ],
    }
    (destination / "render_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export-assets", action="store_true")
    parser.add_argument("--render-seconds", type=float, required=True)
    args = parser.parse_args()
    if not args.export_assets:
        parser.error("Use Manim to render; this entry point requires --export-assets")
    export_assets(args.render_seconds)
