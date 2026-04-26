from manim import *
import numpy as np


class ScalarMultiplicationDirectionFlipExample(Scene):
    """Scalar multiplication stretches, shrinks, and flips a vector."""

    def fixed_tip_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 7,
        tip_length: float = 0.22,
        tip_width: float = 0.22,
    ) -> Line:
        arrow = Line(start, end, color=color, stroke_width=stroke_width)
        arrow.add_tip(tip_length=tip_length, tip_width=tip_width)
        return arrow

    def construct(self):
        v = np.array([1.6, 0.8])
        scale_tr = ValueTracker(1.0)

        title = Tex(r"Scalar multiplication changes length and direction", font_size=29).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=6.0,
            y_length=4.5,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.28, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        )
        plane.move_to(LEFT * 3.15 + DOWN * 0.25)
        origin = plane.c2p(0, 0)
        self.play(Create(plane))

        span_line = Line(plane.c2p(*(-2.25 * v)), plane.c2p(*(2.25 * v)), color=GREY_B)
        span_line.set_stroke(width=2, opacity=0.7)
        base_arrow = self.fixed_tip_arrow(
            origin,
            plane.c2p(float(v[0]), float(v[1])),
            GREY_B,
            stroke_width=5,
            tip_length=0.18,
            tip_width=0.18,
        )
        live_arrow = always_redraw(
            lambda: self.fixed_tip_arrow(
                origin,
                plane.c2p(float(scale_tr.get_value() * v[0]), float(scale_tr.get_value() * v[1])),
                YELLOW,
                stroke_width=7,
                tip_length=0.22,
                tip_width=0.22,
            )
        )

        formula = MathTex(r"a\vec{v}", font_size=30, color=YELLOW)
        scalar_row = VGroup(
            MathTex(r"a=", font_size=26, color=YELLOW),
            DecimalNumber(1.0, num_decimal_places=2, font_size=26, color=YELLOW),
        ).arrange(RIGHT, buff=0.08)
        scalar_row[1].add_updater(lambda m: m.set_value(scale_tr.get_value()))
        rules = VGroup(
            Tex(r"$a>1$: stretch", font_size=22),
            Tex(r"$0<a<1$: shrink", font_size=22),
            Tex(r"$a<0$: flip direction", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rules.set_color(BLUE_B)
        panel = VGroup(formula, scalar_row, rules).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel.move_to(RIGHT * 3.0 + UP * 0.95)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)

        self.play(Create(span_line), Create(base_arrow))
        self.play(FadeIn(panel_box), FadeIn(panel))
        self.add(live_arrow)
        self.play(scale_tr.animate.set_value(2.0), run_time=1.8)
        self.play(scale_tr.animate.set_value(0.35), run_time=1.8)
        self.play(scale_tr.animate.set_value(-1.2), run_time=2.0)
        self.wait(0.8)
