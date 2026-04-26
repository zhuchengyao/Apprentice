from manim import *
import numpy as np


class DotProductDualTransformExample(Scene):
    """A dot product with a fixed vector is a linear map to the number line."""

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
        v = np.array([2.0, 1.0])
        t_tr = ValueTracker(-0.8)

        title = Tex(r"Dot product as a dual linear transformation", font_size=29).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5.2,
            y_length=4.6,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.28, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        ).move_to(LEFT * 3.25 + DOWN * 0.3)
        number_line = NumberLine(x_range=[-5, 5, 1], length=4.5, include_numbers=True)
        number_line.move_to(RIGHT * 2.8 + DOWN * 1.6)

        def x_coords() -> np.ndarray:
            t = t_tr.get_value()
            return np.array([1.2 + t, 1.4 - 0.7 * t])

        def dot_value() -> float:
            return float(np.dot(v, x_coords()))

        v_arrow = self.fixed_tip_arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]), TEAL_A, stroke_width=6)
        x_arrow = always_redraw(
            lambda: self.fixed_tip_arrow(
                plane.c2p(0, 0),
                plane.c2p(float(x_coords()[0]), float(x_coords()[1])),
                YELLOW,
                stroke_width=7,
            )
        )
        output_dot = always_redraw(lambda: Dot(number_line.n2p(dot_value()), radius=0.08, color=PINK))
        output_arrow = always_redraw(
            lambda: self.fixed_tip_arrow(number_line.n2p(0), number_line.n2p(dot_value()), PINK, stroke_width=6)
        )

        formula = MathTex(
            r"\vec{v}\cdot\vec{x}",
            r"=",
            r"\begin{bmatrix}2&1\end{bmatrix}",
            r"\begin{bmatrix}x\\y\end{bmatrix}",
            font_size=27,
        )
        formula.set_color_by_tex(r"\vec{v}", TEAL_A)
        formula.set_color_by_tex(r"\vec{x}", YELLOW)
        value_row = VGroup(
            MathTex(r"\vec{v}\cdot\vec{x}=", font_size=25, color=PINK),
            DecimalNumber(dot_value(), num_decimal_places=2, font_size=25, color=PINK),
        ).arrange(RIGHT, buff=0.08)
        value_row[1].add_updater(lambda m: m.set_value(dot_value()))
        note = Tex("A row matrix sends 2D inputs to 1D outputs.", font_size=22, color=BLUE_B)
        panel = VGroup(formula, value_row, note).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel.move_to(RIGHT * 2.8 + UP * 1.15)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)

        self.play(Create(plane), Create(number_line))
        self.play(Create(v_arrow), FadeIn(panel_box), FadeIn(panel))
        self.add(x_arrow, output_arrow, output_dot)
        self.play(t_tr.animate.set_value(1.0), run_time=2.0)
        self.play(t_tr.animate.set_value(-1.4), run_time=2.2)
        self.wait(0.8)
