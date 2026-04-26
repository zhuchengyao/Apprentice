from manim import *
import numpy as np


class DiagonalEigenbasisRepeatedPowersExample(Scene):
    """In an eigenbasis, repeated multiplication is just repeated scaling."""

    def fixed_tip_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 7,
    ) -> Line:
        arrow = Line(start, end, color=color, stroke_width=stroke_width)
        length = np.linalg.norm(end - start)
        if length > 0.08:
            arrow.add_tip(
                tip_length=min(0.2, 0.45 * length),
                tip_width=min(0.2, 0.45 * length),
            )
        return arrow

    def construct(self):
        t = ValueTracker(0.0)

        title = Tex(r"An eigenbasis turns repeated multiplication into independent scaling", font_size=28)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3, 5, 1],
            y_range=[-2, 3, 1],
            x_length=5.6,
            y_length=4.7,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.27, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        ).move_to(LEFT * 3.0 + DOWN * 0.25)
        origin = plane.c2p(0, 0)

        def lam1() -> float:
            return 1.45 ** t.get_value()

        def lam2() -> float:
            return 0.72 ** t.get_value()

        red_axis = Line(plane.c2p(-2.5, 0), plane.c2p(4.5, 0), color=RED_E, stroke_width=3)
        green_axis = Line(plane.c2p(0, -1.7), plane.c2p(0, 2.6), color=GREEN_E, stroke_width=3)
        red_arrow = always_redraw(lambda: self.fixed_tip_arrow(origin, plane.c2p(lam1(), 0), RED, stroke_width=7))
        green_arrow = always_redraw(lambda: self.fixed_tip_arrow(origin, plane.c2p(0, lam2()), GREEN, stroke_width=7))
        mix_arrow = always_redraw(lambda: self.fixed_tip_arrow(origin, plane.c2p(lam1(), lam2()), YELLOW, stroke_width=7))

        n_number = DecimalNumber(t.get_value(), num_decimal_places=1, font_size=29, color=YELLOW)
        n_number.add_updater(lambda m: m.set_value(t.get_value()))
        live_n = VGroup(MathTex(r"n=", font_size=29, color=YELLOW), n_number).arrange(RIGHT, buff=0.08)
        formula = MathTex(
            r"D^n\begin{bmatrix}1\\1\end{bmatrix}=\begin{bmatrix}1.45^n\\0.72^n\end{bmatrix}",
            font_size=31,
        )
        note = Tex("Each eigen-direction evolves without mixing into the other.", font_size=22, color=BLUE_B)
        panel = VGroup(
            MathTex(r"D=\begin{bmatrix}1.45&0\\0&0.72\end{bmatrix}", font_size=30),
            live_n,
            formula,
            note,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel.move_to(RIGHT * 3.05 + UP * 0.55)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.24)
        panel_box.set_fill(BLACK, opacity=0.84)

        self.play(Create(plane), Create(red_axis), Create(green_axis))
        self.add(red_arrow, green_arrow, mix_arrow)
        self.play(FadeIn(panel_box), FadeIn(panel))
        self.play(t.animate.set_value(4.0), run_time=3.0)
        self.play(Circumscribe(mix_arrow, color=YELLOW))
        self.wait(0.8)
