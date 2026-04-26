from manim import *
import numpy as np


class DeterminantOrientationFlipExample(Scene):
    """Negative determinant flips orientation."""

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
        A = np.array([[1.0, 1.0], [2.0, 0.0]])

        title = Tex(r"A negative determinant flips orientation", font_size=29).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2, 4, 1],
            y_range=[-2, 4, 1],
            x_length=5.0,
            y_length=5.0,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.28, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        )
        plane.move_to(LEFT * 3.15 + DOWN * 0.25)
        origin = plane.c2p(0, 0)
        self.play(Create(plane))

        square = Polygon(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            plane.c2p(1, 1),
            plane.c2p(0, 1),
            color=TEAL,
            fill_color=TEAL,
            fill_opacity=0.18,
            stroke_width=2.4,
        )
        e1_arrow = self.arrow_from_coords(plane, np.array([1.0, 0.0]), GREEN_E)
        e2_arrow = self.arrow_from_coords(plane, np.array([0.0, 1.0]), RED_E)
        orientation_arrow = CurvedArrow(origin + 0.85 * RIGHT, origin + 0.85 * UP, angle=PI / 2, color=YELLOW)

        e1_label = MathTex(r"\hat{\imath}", color=GREEN_E, font_size=25)
        e2_label = MathTex(r"\hat{\jmath}", color=RED_E, font_size=25)
        orient_label = Tex("CCW", font_size=22, color=YELLOW)
        for mob in (e1_label, e2_label, orient_label):
            mob.set_stroke(BLACK, width=5, background=True)
        e1_label.next_to(e1_arrow.get_end(), DOWN + RIGHT, buff=0.12)
        e2_label.next_to(e2_arrow.get_end(), UP + LEFT, buff=0.12)
        orient_label.next_to(orientation_arrow, RIGHT, buff=0.08)

        formula = MathTex(r"\det(A)=-2<0", font_size=31, color=YELLOW)
        note = Tex("Area scales by 2, but the basis order flips.", font_size=22, color=BLUE_B)
        panel = VGroup(formula, note).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel.move_to(RIGHT * 3.0 + UP * 0.98)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)

        moving_group = VGroup(plane, square, e1_arrow, e2_arrow, orientation_arrow)

        self.play(FadeIn(square), GrowArrow(e1_arrow), GrowArrow(e2_arrow))
        self.play(FadeIn(e1_label), FadeIn(e2_label), Create(orientation_arrow), FadeIn(orient_label))
        self.play(FadeIn(panel_box), FadeIn(panel))
        self.play(ApplyMatrix(A, moving_group, about_point=origin), run_time=2.4)

        cw_label = Tex("CW", font_size=22, color=YELLOW)
        cw_label.set_stroke(BLACK, width=5, background=True)
        cw_label.next_to(orientation_arrow, RIGHT, buff=0.08)
        self.play(Transform(orient_label, cw_label))
        self.wait(0.8)
