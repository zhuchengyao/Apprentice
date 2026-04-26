from manim import *
import numpy as np


class EigenvectorInvariantLineExample(Scene):
    """An eigenvector stays on its own span under the transformation."""

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
        A = np.array([[3.0, 0.0], [1.0, 2.0]])
        u = np.array([0.7, 0.7])
        x = np.array([0.75, -0.2])

        title = Tex(
            r"An eigenvector stays on the same line",
            font_size=30,
        ).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-4, 3, 1],
            y_range=[-3, 4, 1],
            # ApplyMatrix acts in screen coordinates, so the coordinate units
            # must be square for an eigenvector to visibly remain on its span.
            x_length=5.4,
            y_length=5.4,
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
        plane.move_to(LEFT * 3.55 + DOWN * 0.25)
        origin = plane.c2p(0, 0)

        eig_line = Line(plane.c2p(-0.35, -0.35), plane.c2p(2.35, 2.35), color=MAROON_B, stroke_width=2.2)
        eig_line_label = Tex("span", font_size=20, color=MAROON_B)
        eig_line_label.set_stroke(BLACK, width=5, background=True)
        eig_line_label.next_to(plane.c2p(1.55, 1.55), DOWN + RIGHT, buff=0.05)
        u_vec = self.arrow_from_coords(plane, u, YELLOW, stroke_width=7)
        x_vec = self.arrow_from_coords(plane, x, BLUE_B, stroke_width=6)
        u_label = MathTex(r"\vec{u}", color=YELLOW, font_size=28)
        x_label = MathTex(r"\vec{x}", color=BLUE_B, font_size=28)
        for mob in (u_label, x_label):
            mob.set_stroke(BLACK, width=5, background=True)
        u_label.next_to(u_vec.get_end(), LEFT, buff=0.08)
        x_label.next_to(x_vec.get_end(), RIGHT, buff=0.08)

        moving_group = VGroup(u_vec, x_vec)

        self.play(Create(plane), Create(eig_line), FadeIn(eig_line_label), GrowArrow(u_vec), GrowArrow(x_vec))
        self.play(FadeIn(u_label), FadeIn(x_label))

        matrix_eq = MathTex(r"A=\begin{bmatrix}3&0\\1&2\end{bmatrix}", font_size=29)
        eigen_eq = MathTex(r"A\vec{u}=3\vec{u}", font_size=30)
        eigen_eq.set_color_by_tex(r"\vec{u}", YELLOW)
        note = Tex(
            r"$\vec{u}$ stays on its span, while a generic vector usually changes direction.",
            font_size=22,
            color=BLUE_B,
        )
        panel = VGroup(matrix_eq, eigen_eq, note).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        panel.move_to(RIGHT * 3.35 + UP * 0.95)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)
        self.play(FadeIn(panel_box), FadeIn(panel))

        self.play(ApplyMatrix(A, moving_group, about_point=origin), run_time=2.3)
        au_label = MathTex(r"A\vec{u}=3\vec{u}", color=YELLOW, font_size=26)
        au_label.set_stroke(BLACK, width=5, background=True)
        au_label.next_to(u_vec.get_end(), LEFT, buff=0.08)
        ax_label = MathTex(r"A\vec{x}", color=BLUE_B, font_size=26)
        ax_label.set_stroke(BLACK, width=5, background=True)
        ax_label.next_to(x_vec.get_end(), DOWN + RIGHT, buff=0.12)
        self.play(FadeOut(u_label), FadeOut(x_label), FadeIn(au_label), FadeIn(ax_label))
        self.wait(0.8)
