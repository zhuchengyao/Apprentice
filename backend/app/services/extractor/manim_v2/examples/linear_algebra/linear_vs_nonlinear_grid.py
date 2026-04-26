from manim import *
import numpy as np


class LinearVsNonlinearGridExample(Scene):
    """Linear transformations keep grid lines straight; nonlinear ones need not."""

    def make_plane(self, center: np.ndarray) -> NumberPlane:
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=4.2,
            y_length=4.2,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.28, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.75},
        )
        plane.move_to(center)
        return plane

    def construct(self):
        title = Tex(r"Linear vs. nonlinear transformations", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        left_plane = self.make_plane(LEFT * 3.05 + DOWN * 0.35)
        right_plane = self.make_plane(RIGHT * 2.55 + DOWN * 0.35)
        left_diag = Line(left_plane.c2p(-2.5, -2.0), left_plane.c2p(2.5, 2.0), color=YELLOW, stroke_width=4)
        right_diag = Line(right_plane.c2p(-2.5, -2.0), right_plane.c2p(2.5, 2.0), color=YELLOW, stroke_width=4)

        left_label = Tex("linear", font_size=25, color=TEAL_A).next_to(left_plane, UP, buff=0.16)
        right_label = Tex("nonlinear", font_size=25, color=RED_B).next_to(right_plane, UP, buff=0.16)
        left_note = Tex("lines remain lines", font_size=21, color=GREY_B).next_to(left_label, DOWN, buff=0.08)
        right_note = Tex("lines can bend", font_size=21, color=GREY_B).next_to(right_label, DOWN, buff=0.08)

        self.play(Create(left_plane), Create(right_plane))
        self.play(Create(left_diag), Create(right_diag), FadeIn(left_label), FadeIn(right_label), FadeIn(left_note), FadeIn(right_note))

        left_group = VGroup(left_plane, left_diag)
        right_group = VGroup(right_plane, right_diag)
        left_origin = left_plane.c2p(0, 0)

        def wiggle(point: np.ndarray) -> np.ndarray:
            local = point - right_plane.c2p(0, 0)
            x = local[0] + 0.35 * np.sin(2.0 * local[1])
            y = local[1] + 0.25 * np.sin(2.2 * local[0])
            return right_plane.c2p(0, 0) + np.array([x, y, 0.0])

        self.play(
            ApplyMatrix(np.array([[1.0, 0.45], [0.0, 1.0]]), left_group, about_point=left_origin),
            ApplyFunction(lambda mob: mob.apply_function(wiggle), right_group),
            run_time=2.5,
        )

        law = MathTex(r"T(a\vec{v}+b\vec{w})=aT(\vec{v})+bT(\vec{w})", font_size=25)
        law_box = SurroundingRectangle(law, color=GREY_B, buff=0.2)
        law_box.set_fill(BLACK, opacity=0.84)
        law_group = VGroup(law_box, law).move_to(DOWN * 3.0)
        self.play(FadeIn(law_group))
        self.wait(0.8)
