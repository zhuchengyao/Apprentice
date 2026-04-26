from manim import *
import numpy as np


class RotationNoRealEigenvectorsExample(Scene):
    """A 90-degree rotation has no nonzero real eigenvectors."""

    def construct(self):
        title = Tex(r"Some real transformations have no real eigenvectors", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5.0,
            y_length=5.0,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.28, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        ).move_to(LEFT * 3.05 + DOWN * 0.2)
        origin = plane.c2p(0, 0)

        vector = Arrow(origin, plane.c2p(1.5, 0.8), buff=0, color=YELLOW, stroke_width=8)
        span = Line(plane.c2p(-2.1, -1.12), plane.c2p(2.1, 1.12), color=YELLOW_E, stroke_width=4)
        rotated_span = span.copy().set_color(ORANGE)
        rotated_vector = vector.copy().set_color(ORANGE)
        moving = VGroup(rotated_span, rotated_vector)

        v_label = MathTex(r"\vec{v}", font_size=28, color=YELLOW).next_to(vector.get_end(), RIGHT, buff=0.08)
        rv_label = MathTex(r"R\vec{v}", font_size=28, color=ORANGE)
        for label in (v_label, rv_label):
            label.set_stroke(BLACK, width=5, background=True)

        matrix = MathTex(r"R=\begin{bmatrix}0&-1\\1&0\end{bmatrix}", font_size=31)
        eigen_equation = MathTex(r"R\vec{v}=\lambda\vec{v}", font_size=31, color=YELLOW)
        contradiction = MathTex(r"90^\circ\text{ turn } \notin \operatorname{span}(\vec{v})", font_size=29, color=ORANGE)
        conclusion = MathTex(r"\text{No real eigenvectors except } \vec{0}", font_size=28, color=RED_B)
        panel = VGroup(matrix, eigen_equation, contradiction, conclusion).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        panel.move_to(RIGHT * 3.05 + UP * 0.55)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.24)
        panel_box.set_fill(BLACK, opacity=0.84)

        self.play(Create(plane), Create(span), GrowArrow(vector), FadeIn(v_label))
        self.play(FadeIn(panel_box), Write(matrix), Write(eigen_equation))
        self.play(FadeIn(moving))
        self.play(Rotate(moving, angle=PI / 2, about_point=origin), run_time=1.5)
        rv_label.next_to(rotated_vector.get_end(), LEFT, buff=0.08)
        self.play(FadeIn(rv_label), Write(contradiction))
        self.play(Circumscribe(eigen_equation, color=RED_B), Write(conclusion))
        self.wait(0.8)
