from manim import *
import numpy as np


class HomogeneityScalingPropertyExample(Scene):
    """Linear maps respect scalar multiplication: A(cv)=cAv."""

    def arrow_from_coords(
        self,
        plane: NumberPlane,
        coords: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 7,
        opacity: float = 1.0,
    ) -> Arrow:
        arrow = Arrow(
            plane.c2p(0, 0),
            plane.c2p(float(coords[0]), float(coords[1])),
            buff=0,
            color=color,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.16,
        )
        arrow.set_opacity(opacity)
        return arrow

    def construct(self):
        matrix = np.array([[1.2, 0.5], [-0.25, 1.1]])
        scalar = 1.8
        v = np.array([1.1, 0.8])
        cv = scalar * v
        av = matrix @ v
        acv = matrix @ cv

        title = Tex(r"Linearity also means scaling before or after gives the same result", font_size=28)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3, 4, 1],
            y_range=[-3, 3, 1],
            x_length=5.6,
            y_length=4.8,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.27, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        ).move_to(LEFT * 3.0 + DOWN * 0.25)

        formula = MathTex(r"A(c\vec{v})=cA\vec{v}", font_size=34, color=YELLOW)
        route_one = MathTex(
            r"1.\quad \vec{v}\xrightarrow{\times c}c\vec{v}\xrightarrow{A}A(c\vec{v})",
            font_size=25,
            color=ORANGE,
        )
        route_two = MathTex(
            r"2.\quad \vec{v}\xrightarrow{A}A\vec{v}\xrightarrow{\times c}cA\vec{v}",
            font_size=25,
            color=BLUE_B,
        )
        note = Tex("Both routes land on the same final vector.", font_size=22, color=GREY_A)
        panel = VGroup(
            MathTex(r"c=1.8", font_size=30, color=ORANGE),
            MathTex(r"A=\begin{bmatrix}1.2&0.5\\-0.25&1.1\end{bmatrix}", font_size=29),
            route_one,
            route_two,
            formula,
            note,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel.move_to(RIGHT * 3.05 + UP * 0.55)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.24)
        panel_box.set_fill(BLACK, opacity=0.84)

        base_arrow = self.arrow_from_coords(plane, v, YELLOW, stroke_width=7)
        base_label = MathTex(r"\vec{v}", color=YELLOW, font_size=28)
        base_label.set_stroke(BLACK, width=5, background=True)
        base_label.next_to(base_arrow.get_end(), UP + LEFT, buff=0.07)

        route_arrow = self.arrow_from_coords(plane, v, YELLOW, stroke_width=7)
        route_label = base_label.copy()

        self.play(Create(plane), GrowArrow(base_arrow), FadeIn(base_label))
        self.play(FadeIn(panel_box), FadeIn(panel[0]), FadeIn(panel[1]))

        self.play(Write(route_one))
        self.play(FadeOut(base_arrow), FadeOut(base_label), FadeIn(route_arrow), FadeIn(route_label))

        cv_arrow = self.arrow_from_coords(plane, cv, ORANGE, stroke_width=7)
        cv_label = MathTex(r"c\vec{v}", color=ORANGE, font_size=28)
        cv_label.set_stroke(BLACK, width=5, background=True)
        cv_label.next_to(cv_arrow.get_end(), UP + LEFT, buff=0.07)
        self.play(Transform(route_arrow, cv_arrow), Transform(route_label, cv_label), run_time=1.2)

        acv_arrow = self.arrow_from_coords(plane, acv, GREY_A, stroke_width=9, opacity=0.62)
        acv_label = MathTex(r"A(c\vec{v})", color=GREY_A, font_size=27)
        acv_label.set_stroke(BLACK, width=5, background=True)
        acv_label.next_to(acv_arrow.get_end(), UP + LEFT, buff=0.07)
        self.play(Transform(route_arrow, acv_arrow), Transform(route_label, acv_label), run_time=1.5)
        self.play(route_arrow.animate.set_opacity(0.5), route_label.animate.set_opacity(0.72))

        second_arrow = self.arrow_from_coords(plane, v, YELLOW, stroke_width=6)
        second_label = MathTex(r"\vec{v}", color=YELLOW, font_size=27)
        second_label.set_stroke(BLACK, width=5, background=True)
        second_label.next_to(second_arrow.get_end(), DOWN + RIGHT, buff=0.07)
        self.play(Write(route_two), FadeIn(second_arrow), FadeIn(second_label))

        av_arrow = self.arrow_from_coords(plane, av, BLUE_B, stroke_width=7)
        av_label = MathTex(r"A\vec{v}", color=BLUE_B, font_size=27)
        av_label.set_stroke(BLACK, width=5, background=True)
        av_label.next_to(av_arrow.get_end(), DOWN + RIGHT, buff=0.07)
        self.play(Transform(second_arrow, av_arrow), Transform(second_label, av_label), run_time=1.2)

        cav_arrow = self.arrow_from_coords(plane, acv, GREEN_B, stroke_width=6)
        cav_label = MathTex(r"cA\vec{v}", color=GREEN_B, font_size=27)
        cav_label.set_stroke(BLACK, width=5, background=True)
        cav_label.next_to(cav_arrow.get_end(), DOWN + RIGHT, buff=0.08)
        self.play(Transform(second_arrow, cav_arrow), Transform(second_label, cav_label), run_time=1.5)

        self.play(Write(formula), Write(note), Circumscribe(VGroup(route_arrow, second_arrow), color=YELLOW))
        self.wait(0.8)
