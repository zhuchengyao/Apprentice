from manim import *
import numpy as np


class CoordinatesAsScalarsExample(Scene):
    """Coordinates are the scalar weights placed on basis vectors."""

    def fixed_tip_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 7,
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
        x = ValueTracker(1.2)
        y = ValueTracker(0.8)

        title = Tex(r"Coordinates are scalars on basis vectors", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=5.3,
            y_length=4.6,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.28, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        ).move_to(LEFT * 3.05 + DOWN * 0.25)
        origin = plane.c2p(0, 0)

        e1 = Arrow(origin, plane.c2p(1, 0), buff=0, color=RED, stroke_width=5)
        e2 = Arrow(origin, plane.c2p(0, 1), buff=0, color=GREEN, stroke_width=5)
        e1_label = MathTex(r"\vec{e}_1", color=RED, font_size=26).next_to(e1.get_end(), DOWN, buff=0.08)
        e2_label = MathTex(r"\vec{e}_2", color=GREEN, font_size=26).next_to(e2.get_end(), LEFT, buff=0.08)
        for label in (e1_label, e2_label):
            label.set_stroke(BLACK, width=5, background=True)

        def coords() -> tuple[float, float]:
            return x.get_value(), y.get_value()

        x_component = always_redraw(
            lambda: self.fixed_tip_arrow(
                origin,
                plane.c2p(coords()[0], 0),
                RED,
                stroke_width=7,
            )
        )
        y_component = always_redraw(
            lambda: self.fixed_tip_arrow(
                plane.c2p(coords()[0], 0),
                plane.c2p(coords()[0], coords()[1]),
                GREEN,
                stroke_width=7,
            )
        )
        vector = always_redraw(
            lambda: self.fixed_tip_arrow(
                origin,
                plane.c2p(coords()[0], coords()[1]),
                YELLOW,
                stroke_width=8,
                tip_length=0.22,
                tip_width=0.22,
            )
        )
        dot = always_redraw(lambda: Dot(plane.c2p(coords()[0], coords()[1]), color=YELLOW, radius=0.07))
        vertical_guide = always_redraw(
            lambda: DashedLine(
                plane.c2p(coords()[0], 0),
                plane.c2p(coords()[0], coords()[1]),
                dash_length=0.08,
                color=GREEN_E,
                stroke_opacity=0.55,
            )
        )
        horizontal_guide = always_redraw(
            lambda: DashedLine(
                plane.c2p(0, coords()[1]),
                plane.c2p(coords()[0], coords()[1]),
                dash_length=0.08,
                color=RED_E,
                stroke_opacity=0.55,
            )
        )

        x_number = DecimalNumber(x.get_value(), num_decimal_places=1, font_size=30, color=RED)
        y_number = DecimalNumber(y.get_value(), num_decimal_places=1, font_size=30, color=GREEN)
        x_number.add_updater(lambda m: m.set_value(x.get_value()))
        y_number.add_updater(lambda m: m.set_value(y.get_value()))

        equation = VGroup(
            MathTex(r"\vec{v}=x\vec{e}_1+y\vec{e}_2", font_size=30, color=YELLOW),
            VGroup(
                MathTex(r"x=", font_size=27, color=RED),
                x_number,
            ).arrange(RIGHT, buff=0.12),
            VGroup(
                MathTex(r"y=", font_size=27, color=GREEN),
                y_number,
            ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        col_x = DecimalNumber(x.get_value(), num_decimal_places=1, font_size=27, color=YELLOW)
        col_y = DecimalNumber(y.get_value(), num_decimal_places=1, font_size=27, color=YELLOW)
        col_x.add_updater(lambda m: m.set_value(x.get_value()))
        col_y.add_updater(lambda m: m.set_value(y.get_value()))
        coordinate_entries = VGroup(col_x, col_y).arrange(DOWN, buff=0.17)
        left_bracket = VGroup(
            Line(UP * 0.62, DOWN * 0.62),
            Line(UP * 0.62, UP * 0.62 + RIGHT * 0.16),
            Line(DOWN * 0.62, DOWN * 0.62 + RIGHT * 0.16),
        ).set_stroke(YELLOW, width=2)
        right_bracket = VGroup(
            Line(UP * 0.62, DOWN * 0.62),
            Line(UP * 0.62, UP * 0.62 + LEFT * 0.16),
            Line(DOWN * 0.62, DOWN * 0.62 + LEFT * 0.16),
        ).set_stroke(YELLOW, width=2)
        coordinate_column = VGroup(left_bracket, coordinate_entries, right_bracket).arrange(RIGHT, buff=0.08)
        coordinate_vector = VGroup(
            MathTex(r"\vec{v}=", font_size=31, color=YELLOW),
            coordinate_column,
        ).arrange(RIGHT, buff=0.08)

        note = Tex(
            "The pair of numbers tells how far to walk along each basis direction.",
            font_size=22,
            color=BLUE_B,
        )
        panel = VGroup(equation, coordinate_vector, note).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel.move_to(RIGHT * 3.0 + UP * 0.6)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.24)
        panel_box.set_fill(BLACK, opacity=0.84)

        self.play(Create(plane), GrowArrow(e1), GrowArrow(e2), FadeIn(e1_label), FadeIn(e2_label))
        self.play(FadeIn(panel_box), FadeIn(panel))
        self.add(vertical_guide, horizontal_guide, x_component, y_component, vector, dot)
        self.play(x.animate.set_value(2.3), y.animate.set_value(1.5), run_time=2.0)
        self.play(x.animate.set_value(-1.4), y.animate.set_value(1.9), run_time=2.0)
        self.play(x.animate.set_value(1.6), y.animate.set_value(-1.1), run_time=2.0)
        self.wait(0.7)
