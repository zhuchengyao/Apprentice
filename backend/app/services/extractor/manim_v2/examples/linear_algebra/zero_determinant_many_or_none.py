from manim import *
import numpy as np


class ZeroDeterminantManyOrNoneExample(Scene):
    """When det(A)=0, some outputs have many inputs and some have none."""

    def construct(self):
        A = np.array([[1.5, -1.0], [0.5, -1.0 / 3.0]])
        null_vec = np.array([2.0, 3.0])
        x0 = np.array([1.0, 1.0])
        family = [x0 + t * null_vec for t in np.linspace(-0.8, 0.8, 5)]

        title = Tex(r"When $\det(A)=0$, solutions are not unique", font_size=29).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3, 4, 1],
            y_range=[-3, 3, 1],
            x_length=5.833333333333333,
            y_length=5.0,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.28, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        )
        plane.move_to(LEFT * 3.45 + DOWN * 0.25)
        origin = plane.c2p(0, 0)

        family_line = Line(
            plane.c2p(float(family[0][0]), float(family[0][1])),
            plane.c2p(float(family[-1][0]), float(family[-1][1])),
            color=YELLOW,
            stroke_width=3,
        )
        family_dots = VGroup(*[
            Dot(plane.c2p(float(p[0]), float(p[1])), radius=0.07, color=color)
            for p, color in zip(family, color_gradient([YELLOW, MAROON_B], len(family)))
        ])

        equation = MathTex(r"A\vec{x}=\vec{v}", font_size=31)
        det_eq = MathTex(r"\det(A)=0", font_size=30, color=YELLOW)
        note_1 = Tex("A whole line of inputs collapses to one output.", font_size=22, color=BLUE_B)
        note_2 = Tex("Targets off that output line have no solution.", font_size=22, color=RED_B)
        panel = VGroup(equation, det_eq, note_1, note_2).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        panel.move_to(RIGHT * 3.1 + UP * 1.15)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)

        moving_group = VGroup(family_line, family_dots)

        self.play(Create(plane))
        self.play(Create(family_line), FadeIn(family_dots))
        self.play(FadeIn(panel_box), FadeIn(panel))
        image_line = Line(
            origin + LEFT * 1.8 + DOWN * 0.6,
            origin + RIGHT * 1.45 + UP * 0.48,
            color=WHITE,
            stroke_width=3,
        )
        self.play(ApplyMatrix(A, moving_group, about_point=origin), Create(image_line), run_time=2.6)

        collapsed_point = Dot(plane.c2p(float((A @ x0)[0]), float((A @ x0)[1])), radius=0.09, color=YELLOW)
        collapsed_ring = Circle(radius=0.18, color=YELLOW, stroke_width=2.2).move_to(collapsed_point)
        many_label = Tex("many inputs land here", font_size=22, color=YELLOW)
        many_label.set_stroke(BLACK, width=5, background=True)
        many_label.next_to(collapsed_ring, DOWN, buff=0.08)

        unreachable_arrow = Arrow(origin, origin + np.array([0.75, 1.65, 0.0]), buff=0, color=RED, stroke_width=6)
        unreachable_label = Tex("no input lands here", font_size=22, color=RED)
        unreachable_label.set_stroke(BLACK, width=5, background=True)
        unreachable_label.next_to(unreachable_arrow.get_end(), UP + RIGHT, buff=0.08)

        self.play(FadeIn(collapsed_point), Create(collapsed_ring), FadeIn(many_label))
        self.play(GrowArrow(unreachable_arrow), FadeIn(unreachable_label))
        self.wait(0.8)
