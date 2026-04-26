from manim import *
import numpy as np


class DeterminantADMinusBCExample(Scene):
    """The 2D determinant is the signed area ad - bc."""

    def fixed_tip_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 7,
        tip_length: float = 0.2,
        tip_width: float = 0.2,
    ) -> Line:
        arrow = Line(start, end, color=color, stroke_width=stroke_width)
        length = np.linalg.norm(end - start)
        if length > 0.08:
            arrow.add_tip(
                tip_length=min(tip_length, 0.45 * length),
                tip_width=min(tip_width, 0.45 * length),
            )
        return arrow

    def construct(self):
        a = 1.8
        c = 0.7
        d = 1.5
        b = ValueTracker(0.3)

        title = Tex(r"The $2\times2$ determinant is signed area", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2.5, 3, 1],
            y_range=[-2, 2.5, 1],
            x_length=5.3,
            y_length=4.6,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.27, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        ).move_to(LEFT * 3.05 + DOWN * 0.25)
        origin = plane.c2p(0, 0)

        def u() -> np.ndarray:
            return np.array([a, c])

        def v() -> np.ndarray:
            return np.array([b.get_value(), d])

        def det_value() -> float:
            return a * d - b.get_value() * c

        parallelogram = always_redraw(
            lambda: Polygon(
                origin,
                plane.c2p(*u()),
                plane.c2p(*(u() + v())),
                plane.c2p(*v()),
                color=YELLOW,
                fill_color=YELLOW,
                fill_opacity=0.2,
                stroke_width=2.5,
            )
        )
        u_arrow = self.fixed_tip_arrow(origin, plane.c2p(*u()), RED, stroke_width=7)
        v_arrow = always_redraw(
            lambda: self.fixed_tip_arrow(
                origin,
                plane.c2p(*v()),
                GREEN,
                stroke_width=7,
            )
        )
        v_copy = always_redraw(
            lambda: self.fixed_tip_arrow(
                plane.c2p(*u()),
                plane.c2p(*(u() + v())),
                GREEN_E,
                stroke_width=4,
                tip_length=0.16,
                tip_width=0.16,
            )
        )
        u_label = MathTex(r"\begin{bmatrix}a\\c\end{bmatrix}", font_size=24, color=RED).next_to(u_arrow.get_end(), DOWN, buff=0.06)
        v_label = always_redraw(lambda: MathTex(r"\begin{bmatrix}b\\d\end{bmatrix}", font_size=24, color=GREEN).next_to(v_arrow.get_end(), UP, buff=0.06))
        for mob in (u_label,):
            mob.set_stroke(BLACK, width=5, background=True)

        det_number = DecimalNumber(det_value(), num_decimal_places=2, font_size=30, color=YELLOW)
        det_number.add_updater(lambda m: m.set_value(det_value()))
        b_number = DecimalNumber(b.get_value(), num_decimal_places=1, font_size=28, color=GREEN)
        b_number.add_updater(lambda m: m.set_value(b.get_value()))

        matrix = MathTex(r"A=\begin{bmatrix}a&b\\c&d\end{bmatrix}", font_size=31)
        b_readout = VGroup(MathTex(r"b=", font_size=27, color=GREEN), b_number).arrange(RIGHT, buff=0.08)
        formula = VGroup(
            MathTex(r"\det(A)=ad-bc=", font_size=30),
            det_number,
        ).arrange(RIGHT, buff=0.08)
        note = Tex("The sign tracks orientation; the magnitude is parallelogram area.", font_size=22, color=BLUE_B)
        panel = VGroup(matrix, b_readout, formula, note).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        panel.move_to(RIGHT * 3.0 + UP * 0.75)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.24)
        panel_box.set_fill(BLACK, opacity=0.84)

        self.play(Create(plane), FadeIn(parallelogram), Create(u_arrow), Create(v_arrow), Create(v_copy))
        self.play(FadeIn(u_label), FadeIn(v_label), FadeIn(panel_box), FadeIn(panel))
        self.play(b.animate.set_value(1.6), run_time=2.0)
        self.play(b.animate.set_value(-0.7), run_time=2.0)
        self.play(b.animate.set_value(0.8), run_time=1.6)
        self.wait(0.7)
