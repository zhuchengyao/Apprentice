from manim import *
import numpy as np


class MatrixMultiplicationNoncommutativeExample(Scene):
    """The order of two matrix transformations changes the result."""

    def _plane(self, center: np.ndarray) -> NumberPlane:
        return NumberPlane(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=4.2,
            y_length=4.2,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.24, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.1, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.75},
        ).move_to(center)

    def _unit_square(self, plane: NumberPlane) -> Polygon:
        return Polygon(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            plane.c2p(1, 1),
            plane.c2p(0, 1),
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.18,
            stroke_width=2.5,
        )

    def _corner_vector(self, plane: NumberPlane, origin: np.ndarray) -> Line:
        arrow = Line(origin, plane.c2p(1, 1), color=PINK, stroke_width=7)
        arrow.add_tip(tip_length=0.2, tip_width=0.2)
        return arrow

    def construct(self):
        rotation = np.array([[0.0, -1.0], [1.0, 0.0]])
        shear = np.array([[1.0, 1.0], [0.0, 1.0]])

        title = Tex(r"Matrix multiplication is order-sensitive", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        left_plane = self._plane(LEFT * 3.05 + DOWN * 0.15)
        right_plane = self._plane(RIGHT * 3.05 + DOWN * 0.15)
        left_origin = left_plane.c2p(0, 0)
        right_origin = right_plane.c2p(0, 0)

        left_square = self._unit_square(left_plane)
        right_square = self._unit_square(right_plane)
        left_vec = self._corner_vector(left_plane, left_origin)
        right_vec = self._corner_vector(right_plane, right_origin)

        left_group = VGroup(left_plane, left_square, left_vec)
        right_group = VGroup(right_plane, right_square, right_vec)

        left_label = MathTex(r"S(R\vec{x})", font_size=30, color=YELLOW).next_to(left_plane, UP, buff=0.18)
        right_label = MathTex(r"R(S\vec{x})", font_size=30, color=YELLOW).next_to(right_plane, UP, buff=0.18)
        left_steps = Tex("rotate, then shear", font_size=22, color=BLUE_B).next_to(left_label, DOWN, buff=0.08)
        right_steps = Tex("shear, then rotate", font_size=22, color=BLUE_B).next_to(right_label, DOWN, buff=0.08)

        formula = MathTex(
            r"SR=\begin{bmatrix}1&-1\\1&0\end{bmatrix}",
            r"\neq",
            r"RS=\begin{bmatrix}0&-1\\1&1\end{bmatrix}",
            font_size=28,
        ).to_edge(DOWN, buff=0.35)
        formula[0].set_color(TEAL_A)
        formula[2].set_color(ORANGE)

        self.play(
            Create(left_plane),
            Create(right_plane),
            FadeIn(left_square),
            FadeIn(right_square),
            Create(left_vec),
            Create(right_vec),
        )
        self.play(FadeIn(left_label), FadeIn(right_label), FadeIn(left_steps), FadeIn(right_steps))
        self.play(
            ApplyMatrix(rotation, left_group, about_point=left_origin),
            ApplyMatrix(shear, right_group, about_point=right_origin),
            run_time=1.5,
        )
        self.play(
            ApplyMatrix(shear, left_group, about_point=left_origin),
            ApplyMatrix(rotation, right_group, about_point=right_origin),
            run_time=1.5,
        )
        self.play(Write(formula), Circumscribe(left_vec, color=TEAL_A), Circumscribe(right_vec, color=ORANGE))
        self.wait(0.8)
