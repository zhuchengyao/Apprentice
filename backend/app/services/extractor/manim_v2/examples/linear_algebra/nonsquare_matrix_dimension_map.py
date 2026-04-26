from manim import *
import numpy as np


class NonsquareMatrixDimensionMapExample(Scene):
    """A nonsquare matrix can map vectors between different dimensions."""

    def fixed_tip_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 6,
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
        row = np.array([1.0, 0.5])
        t_tr = ValueTracker(-1.2)

        title = Tex(r"Non-square matrices map between dimensions", font_size=29).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4.8,
            y_length=4.4,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.28, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        ).move_to(LEFT * 3.25 + DOWN * 0.3)
        number_line = NumberLine(x_range=[-4, 4, 1], length=4.4, include_numbers=True)
        number_line.move_to(RIGHT * 2.75 + DOWN * 1.45)

        def input_coords() -> np.ndarray:
            t = t_tr.get_value()
            return np.array([1.2 + t, 1.1 - 0.4 * t])

        def output_value() -> float:
            return float(np.dot(row, input_coords()))

        input_arrow = always_redraw(
            lambda: self.fixed_tip_arrow(
                plane.c2p(0, 0),
                plane.c2p(float(input_coords()[0]), float(input_coords()[1])),
                YELLOW,
                stroke_width=7,
            )
        )
        output_dot = always_redraw(lambda: Dot(number_line.n2p(output_value()), color=PINK, radius=0.08))
        output_arrow = always_redraw(
            lambda: self.fixed_tip_arrow(number_line.n2p(0), number_line.n2p(output_value()), PINK, stroke_width=6)
        )

        formula = MathTex(
            r"\begin{bmatrix}1&0.5\end{bmatrix}",
            r"\begin{bmatrix}x\\y\end{bmatrix}",
            r"\in \mathbb{R}",
            font_size=27,
        )
        formula[1].set_color(YELLOW)
        formula[2].set_color(PINK)
        live = VGroup(
            MathTex(r"L(\vec{x})=", font_size=25, color=PINK),
            DecimalNumber(output_value(), num_decimal_places=2, font_size=25, color=PINK),
        ).arrange(RIGHT, buff=0.08)
        live[1].add_updater(lambda m: m.set_value(output_value()))
        note = Tex("A 1x2 matrix turns a 2D input into one number.", font_size=22, color=BLUE_B)
        panel = VGroup(formula, live, note).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel.move_to(RIGHT * 2.75 + UP * 1.2)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)

        self.play(Create(plane), Create(number_line))
        self.play(FadeIn(panel_box), FadeIn(panel))
        self.add(input_arrow, output_arrow, output_dot)
        self.play(t_tr.animate.set_value(1.5), run_time=2.0)
        self.play(t_tr.animate.set_value(-0.6), run_time=1.8)
        self.wait(0.8)
