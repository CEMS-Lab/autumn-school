"""Original, conceptual mechanics animations for the PhAST Autumn School.

Render from the repository root (Manim 0.19.1):
    python -m manim render --renderer cairo --format mp4 --fps 30 \
      -r 1280,720 --media_dir .build/animations/mechanics \
      source/animations/mechanics_scenes.py PhaseFieldBand ExplicitImplicitStep

PhaseFieldBand evaluates the stated one-dimensional isolated AT2 profile.
ExplicitImplicitStep illustrates a partitioned dynamic update and its checks.
The existing book's phase-field-energy and staggered-solution chapters provide
the notation and bibliographic context. All geometry and animation are original.
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib
import numpy as np
from manimpango import register_font
from manim import (
    Arrow, Axes, Circle, Create, DashedLine, DecimalNumber, Dot, DOWN,
    FadeIn, FadeOut, ImageMobject, LaggedStart, LEFT, Line, MathTex,
    ORIGIN, Polygon, Rectangle, ReplacementTransform, RIGHT, Scene,
    SurroundingRectangle, Text, Transform, UP, VGroup, ValueTracker,
    VMobject, WHITE, always_redraw, config, linear,
)

BLUE = "#245A81"
ORANGE = "#B85C20"
TEAL = "#087F82"
INK = "#151A1E"
GREY = "#53616B"
LIGHT = "#E6EDF1"
FONT = "DejaVu Sans"

# Register the existing Matplotlib-supplied face for deterministic Pango text;
# this neither installs fonts globally nor needs a font download.
register_font(str(Path(matplotlib.get_data_path()) / "fonts/ttf/DejaVuSans.ttf"))

config.background_color = WHITE
config.frame_width = 128 / 9
config.frame_height = 8


def label(text: str, size: int = 30, color: str = INK) -> Text:
    return Text(text, font=FONT, font_size=size, color=color, line_spacing=1.1)


def title(scene: Scene, heading: str, subtitle: str) -> None:
    head = label(heading, 39).to_edge(UP, buff=0.48).to_edge(LEFT, buff=0.65)
    sub = label(subtitle, 25, GREY).next_to(head, DOWN, buff=0.22).align_to(head, LEFT)
    scene.play(FadeIn(head), FadeIn(sub), run_time=0.8)


def connector(start: np.ndarray, end: np.ndarray, color: str = BLUE) -> Arrow:
    return Arrow(start, end, color=color, buff=0.06, stroke_width=3,
                 max_tip_length_to_length_ratio=0.14)


class PortableScene(Scene):
    """Keep Manim 0.19.1's concat list safe in paths containing apostrophes.

    Manim writes single-quoted absolute filenames without escaping quotes.
    Here only its final combine operation uses filenames local to that scene's
    partial-movie folder. No installed library is changed, and no extra render
    location or globally installed font is needed.
    """

    def setup(self) -> None:
        writer = self.renderer.file_writer
        original_combine = writer.combine_files

        def combine_local(input_files, output_file, *args, **kwargs):
            directory = writer.partial_movie_directory.resolve()
            names = [str(Path(item).resolve().relative_to(directory))
                     for item in input_files]
            previous = Path.cwd()
            try:
                os.chdir(directory)
                return original_combine(names, output_file, *args, **kwargs)
            finally:
                os.chdir(previous)

        writer.combine_files = combine_local


class PhaseFieldBand(PortableScene):
    """A crack representation and analytic length-scale comparison, 24.8 s."""

    def construct(self) -> None:
        title(self, "A sharp crack becomes a diffuse field",
              "Analytic isolated AT2 damage profile")

        centre = np.array([-3.55, 0.1, 0.0])
        outline = Rectangle(width=5.3, height=3.25, stroke_color=GREY,
                            stroke_width=1.7).move_to(centre)
        crack = Line(centre + DOWN * 1.62, centre + UP * 1.62,
                     color=INK, stroke_width=5)
        domain_title = label("Sharp crack", 29).next_to(outline, UP, buff=0.24)
        self.play(Create(outline), Create(crack), FadeIn(domain_title), run_time=1.1)
        self.wait(1.7)

        ell = ValueTracker(0.35)

        def band() -> ImageMobject:
            x = np.linspace(-2.5, 2.5, 360)
            d = np.exp(-np.abs(x) / ell.get_value())
            ink = np.array([36, 90, 129])
            row = (255 * (1 - d[:, None]) + ink[None, :] * d[:, None])
            rgb = np.repeat(np.uint8(row)[None, :, :], 220, axis=0)
            return ImageMobject(rgb).stretch_to_fit_width(5.28).stretch_to_fit_height(3.23).move_to(centre)

        band_image = always_redraw(band)
        band_image.set_z_index(-1)
        diffuse_title = label("Diffuse damage field", 29).move_to(domain_title)
        self.remove(domain_title)
        self.add(diffuse_title)
        self.play(FadeIn(band_image), FadeOut(crack), run_time=1.5)

        axes = Axes(x_range=[-2.5, 2.5, 1], y_range=[0, 1, 0.5],
                    x_length=5.25, y_length=2.6,
                    axis_config={"color": GREY, "stroke_width": 1.6,
                                 "include_ticks": False, "include_tip": False},
                    tips=False).move_to([3.55, -0.02, 0])
        axes.y_axis.set_opacity(0)
        ordinate = Line(axes.c2p(-2.5, 0), axes.c2p(-2.5, 1),
                        color=GREY, stroke_width=1.6)
        curve = always_redraw(lambda: axes.plot(
            lambda x: np.exp(-abs(x) / ell.get_value()),
            x_range=[-2.5, 2.5, 0.025], color=BLUE, stroke_width=4,
            use_smoothing=False))
        equation = MathTex(r"d(x)=\exp(-|x|/\ell)", font_size=36,
                           color=BLUE).next_to(axes, UP, buff=0.4)
        origin = MathTex("0", font_size=25, color=GREY).next_to(axes.c2p(0, 0), DOWN, buff=0.13)
        one = MathTex("1", font_size=25, color=GREY).next_to(axes.c2p(-2.5, 1), LEFT, buff=0.14)
        x_label = MathTex("x", font_size=30, color=INK).next_to(axes.c2p(2.5, 0), RIGHT, buff=0.12)
        d_label = MathTex("d", font_size=30, color=INK).next_to(axes.c2p(-2.5, 1), UP, buff=0.1)
        centreline = DashedLine(axes.c2p(0, 0), axes.c2p(0, 1), color=GREY,
                                stroke_opacity=0.45, dash_length=0.08)
        self.play(Create(axes), Create(ordinate), FadeIn(equation), FadeIn(origin), FadeIn(one),
                  FadeIn(x_label), FadeIn(d_label), Create(centreline),
                  Create(curve), run_time=1.2)

        intact = label("d = 0: intact", 25, GREY).move_to([-4.95, -2.00, 0])
        broken = label("d = 1: broken", 25, BLUE).move_to([-2.1, -2.00, 0])
        unit_note = label("x and ℓ use the same arbitrary length unit", 22, GREY).move_to([3.5, -2.0, 0])
        ell_name = MathTex(r"\ell =", font_size=34, color=TEAL).move_to([-0.60, -2.6, 0])
        ell_value = DecimalNumber(ell.get_value(), num_decimal_places=2,
                                  font_size=34, color=TEAL).next_to(ell_name, RIGHT)
        ell_value.add_updater(lambda number: number.set_value(ell.get_value()))
        ell_scale = label("regularisation length", 26, TEAL).next_to(ell_value, RIGHT, buff=0.25)
        ell_group = VGroup(ell_name, ell_value, ell_scale)
        ell_group.move_to([0, -2.6, 0])
        self.play(FadeIn(intact), FadeIn(broken), FadeIn(unit_note), FadeIn(ell_group), run_time=0.7)
        message = label("A continuous field represents the crack.", 30).move_to([0, -3.3, 0])
        self.play(FadeIn(message), run_time=0.6)
        self.wait(2.5)

        wide_message = label("Larger ℓ spreads the regularised band.", 30).move_to(message)
        self.play(FadeOut(message), run_time=0.2)
        self.play(FadeIn(wide_message), run_time=0.2)
        self.play(ell.animate.set_value(0.85), run_time=3.2, rate_func=linear)
        self.wait(2.0)
        narrow_message = label("Smaller ℓ requires a finer mesh to resolve the band.", 29).move_to(message)
        self.play(FadeOut(wide_message), run_time=0.2)
        self.play(FadeIn(narrow_message), run_time=0.2)
        self.play(ell.animate.set_value(0.22), run_time=3.2, rate_func=linear)
        self.wait(2.5)
        final_message = label("The regularisation length sets the width of the diffuse damage band.", 26, GREY).move_to(message)
        self.play(FadeOut(narrow_message), run_time=0.2)
        self.play(FadeIn(final_message), run_time=0.2)
        self.wait(2.6)


class ExplicitImplicitStep(PortableScene):
    """An explicit–implicit dynamic splitting schematic, approximately 27 s."""

    def construct(self) -> None:
        title(self, "One explicit–implicit time step",
              "Partitioned dynamics with explicit mechanics and implicit damage")

        accepted = MathTex(r"\text{Accepted at }t_n:\quad (u_n,\,v_{n-1/2},\,d_n,\,H_n)",
                           font_size=32, color=INK).move_to([0, 2.1, 0])
        self.play(FadeIn(accepted), run_time=0.7)
        self.wait(1.4)

        def operation(x: float, heading: str, line1: str, line2: str) -> VGroup:
            frame = Rectangle(width=3.65, height=1.7, stroke_color=BLUE,
                              stroke_width=2).move_to([x, 0.7, 0])
            head = label(heading, 28, BLUE).move_to([x, 1.17, 0])
            a = label(line1, 27).move_to([x, 0.60, 0])
            b = label(line2, 27).move_to([x, 0.15, 0])
            return VGroup(frame, head, a, b)

        mechanics = operation(-4.55, "1. Mechanics", "Explicit update", "Hold dₙ fixed")
        driving = operation(0, "2. Driving field", "Tensile energy", "History update")
        damage = operation(4.55, "3. Damage", "Implicit solve", "Irreversibility")
        first = connector([-4.55, 1.92, 0], [-4.55, 1.58, 0])
        state_link = Line([0, 1.92, 0], [-4.55, 1.92, 0], color=BLUE, stroke_width=2)
        self.play(FadeIn(mechanics), Create(state_link), Create(first), run_time=0.8)
        self.wait(2.6)
        arrow1 = connector(mechanics[0].get_right(), driving[0].get_left())
        self.play(Create(arrow1), FadeIn(driving), run_time=0.8)
        self.wait(2.4)
        arrow2 = connector(driving[0].get_right(), damage[0].get_left())
        self.play(Create(arrow2), FadeIn(damage), run_time=0.8)
        self.wait(2.8)

        gate = Polygon([0, -0.95, 0], [1.65, -1.8, 0], [0, -2.65, 0],
                       [-1.65, -1.8, 0], stroke_color=BLUE, stroke_width=2)
        gate_text = label("Checks\npass?", 27).move_to([0, -1.8, 0])
        check_names = label("Residuals · bounds · irreversibility · energy balance", 25, GREY).move_to([0, -0.65, 0])
        down = Line([4.55, -0.20, 0], [4.55, -1.8, 0], color=BLUE, stroke_width=3)
        to_gate = connector([4.55, -1.8, 0], [1.70, -1.8, 0])
        self.play(Create(down), Create(to_gate), Create(gate),
                  FadeIn(gate_text), FadeIn(check_names), run_time=1.0)
        self.wait(2.7)

        next_state = Circle(radius=0.65, color=TEAL, stroke_width=2).move_to([-4.55, -1.8, 0])
        next_math = MathTex("n+1", font_size=32, color=TEAL).move_to(next_state)
        yes = connector([-1.7, -1.8, 0], [-3.85, -1.8, 0], TEAL)
        yes_label = label("yes", 25, TEAL).next_to(yes, UP, buff=0.12)
        next_label = label("Accept next time", 27, TEAL).move_to([-4.55, -2.75, 0])
        self.play(Create(yes), FadeIn(yes_label), Create(next_state),
                  FadeIn(next_math), FadeIn(next_label), run_time=0.8)
        self.wait(1.8)

        reject1 = Line([0, -2.68, 0], [0, -3.15, 0], color=ORANGE, stroke_width=3)
        reject2 = connector([0, -3.15, 0], [2.05, -3.15, 0], ORANGE)
        no_label = label("no", 25, ORANGE).move_to([1.08, -2.87, 0])
        reject_text = label("Stop or reduce Δt\nRestart from tₙ", 26, ORANGE).move_to([4.53, -3.12, 0])
        self.play(Create(reject1), Create(reject2), FadeIn(no_label), FadeIn(reject_text), run_time=0.8)
        self.wait(2.6)

        footer = label("Explicit mechanics requires a stable time step.",
                       21, GREY).move_to([0, -3.77, 0])
        self.play(FadeIn(footer), run_time=0.7)
        self.wait(3.0)
