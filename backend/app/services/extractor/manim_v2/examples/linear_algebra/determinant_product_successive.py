from manim import *
import numpy as np


class DeterminantProductSuccessiveExample(Scene):
    """Successive transformations multiply area scale factors."""

    def construct(self):
        M2 = np.array([[1.5, -0.5], [0.0, 1.0]])
        M1 = np.array([[1.0, 0.5], [-0.5, 1.5]])
        det2 = np.linalg.det(M2)
        det1 = np.linalg.det(M1)

        title = Tex(r"Determinants multiply under composition", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2, 4, 1],
            y_range=[-3, 3, 1],
            x_length=5.0,
            y_length=5.0,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.28, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        ).move_to(LEFT * 3.15 + DOWN * 0.25)
        origin = plane.c2p(0, 0)

        side = 1.35
        square = Polygon(
            plane.c2p(0, 0),
            plane.c2p(side, 0),
            plane.c2p(side, side),
            plane.c2p(0, side),
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.22,
            stroke_width=2.5,
        )
        square_shadow = square.copy().set_fill(GREY_B, opacity=0.08).set_stroke(GREY_B, width=1.4, opacity=0.55)
        area_label = MathTex(r"A", font_size=28, color=YELLOW).move_to(square)
        area_label.set_stroke(BLACK, width=5, background=True)
        moving_group = VGroup(square, area_label)

        formula = MathTex(
            r"\det(M_1M_2)=\det(M_1)\det(M_2)",
            font_size=28,
        )
        numbers = MathTex(
            rf"{det1 * det2:.2f}",
            r"=",
            rf"{det1:.2f}",
            r"\cdot",
            rf"{det2:.2f}",
            font_size=27,
            color=YELLOW,
        )
        note = Tex("Each transformation rescales the area already produced.", font_size=22, color=BLUE_B)
        panel = VGroup(formula, numbers, note).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel.move_to(RIGHT * 3.05 + UP * 0.95)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)

        self.play(Create(plane), FadeIn(square_shadow), FadeIn(square), FadeIn(area_label))
        self.play(FadeIn(panel_box), FadeIn(panel))
        self.play(ApplyMatrix(M2, moving_group, about_point=origin), run_time=1.8)
        mid_label = MathTex(r"\det(M_2)A", font_size=24, color=YELLOW)
        mid_label.set_stroke(BLACK, width=5, background=True)
        mid_label.move_to(square.get_center())
        self.play(Transform(area_label, mid_label))
        self.play(ApplyMatrix(M1, moving_group, about_point=origin), run_time=1.8)
        final_label = MathTex(rf"{det1 * det2:.2f}A", font_size=27, color=YELLOW)
        final_label.set_stroke(BLACK, width=5, background=True)
        final_label.move_to(square.get_center())
        self.play(Transform(area_label, final_label), Circumscribe(formula, color=TEAL_A))
        self.wait(0.8)
