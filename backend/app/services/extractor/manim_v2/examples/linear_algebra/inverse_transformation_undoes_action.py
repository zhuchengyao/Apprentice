from manim import *
import numpy as np


class InverseTransformationUndoesActionExample(Scene):
    """Applying A^{-1} undoes the action of A."""

    def arrow_from_coords(
        self,
        plane: NumberPlane,
        coords: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 6,
    ) -> Arrow:
        return Arrow(
            plane.c2p(0, 0),
            plane.c2p(float(coords[0]), float(coords[1])),
            buff=0,
            color=color,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.18,
        )

    def construct(self):
        A = np.array([[1.0, 1.0], [0.0, 1.0]])
        A_inv = np.linalg.inv(A)
        x = np.array([1.0, 1.0])

        title = Tex(
            r"The inverse transformation undoes the original one",
            font_size=28,
        ).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2, 4, 1],
            y_range=[-2, 3, 1],
            # Keep x/y coordinate units equal so ApplyMatrix preserves the
            # alignment between the vector and the transformed unit square.
            x_length=6.0,
            y_length=5.0,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.28,
                "stroke_width": 1.0,
            },
            faded_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.12,
                "stroke_width": 0.7,
            },
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        )
        plane.move_to(LEFT * 3.2 + DOWN * 0.35)
        origin = plane.c2p(0, 0)

        square = Polygon(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            plane.c2p(1, 1),
            plane.c2p(0, 1),
            color=TEAL,
            fill_color=TEAL,
            fill_opacity=0.16,
            stroke_width=2.5,
        )
        x_vec = self.arrow_from_coords(plane, x, PINK, stroke_width=7)
        label = MathTex(r"\vec{x}", color=PINK, font_size=28)
        label.set_stroke(BLACK, width=5, background=True)
        label.next_to(x_vec.get_end(), RIGHT, buff=0.08)
        moving_group = VGroup(square, x_vec)

        self.play(Create(plane), FadeIn(square), GrowArrow(x_vec), FadeIn(label))

        A_eq = MathTex(r"A=\begin{bmatrix}1&1\\0&1\end{bmatrix}", font_size=29)
        inv_eq = MathTex(r"A^{-1}=\begin{bmatrix}1&-1\\0&1\end{bmatrix}", font_size=29)
        solve_eq = MathTex(r"A\vec{x}=\vec{v}\qquad\Rightarrow\qquad \vec{x}=A^{-1}\vec{v}", font_size=26)
        solve_eq.set_color_by_tex(r"\vec{x}", PINK)
        solve_eq.set_color_by_tex(r"\vec{v}", YELLOW)
        note = Tex("Solve by undoing the transformation", font_size=23, color=BLUE_B)
        panel = VGroup(A_eq, inv_eq, solve_eq, note).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel.move_to(RIGHT * 3.15 + UP * 0.95)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.24)
        panel_box.set_fill(BLACK, opacity=0.84)
        self.play(FadeIn(panel_box), FadeIn(panel))

        self.play(ApplyMatrix(A, moving_group, about_point=origin), run_time=2.0)
        v_label = MathTex(r"\vec{v}=A\vec{x}", color=YELLOW, font_size=28)
        v_label.set_stroke(BLACK, width=5, background=True)
        v_label.next_to(x_vec.get_end(), RIGHT, buff=0.08)
        self.play(FadeOut(label), FadeIn(v_label))

        self.play(ApplyMatrix(A_inv, moving_group, about_point=origin), run_time=2.0)
        label.next_to(x_vec.get_end(), RIGHT, buff=0.08)
        self.play(FadeOut(v_label), FadeIn(label))
        self.wait(0.8)
