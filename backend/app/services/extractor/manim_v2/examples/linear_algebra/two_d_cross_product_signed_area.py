from manim import *
import numpy as np


class TwoDCrossProductSignedAreaExample(Scene):
    """2D cross product as signed area / orientation."""

    def arrow_from_coords(
        self,
        plane: NumberPlane,
        coords: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 6,
        opacity: float = 1.0,
    ) -> Line:
        start = plane.c2p(0, 0)
        end = plane.c2p(float(coords[0]), float(coords[1]))
        arrow = Line(start, end, color=color, stroke_width=stroke_width)
        length = np.linalg.norm(end - start)
        if length > 0.08:
            arrow.add_tip(
                tip_length=min(0.2, 0.45 * length),
                tip_width=min(0.2, 0.45 * length),
            )
        arrow.set_opacity(opacity)
        return arrow

    def construct(self):
        v = np.array([2.0, 1.0])
        v_angle = float(np.arctan2(v[1], v[0]))
        w_len = 2.4

        title = Tex(
            r"2D cross product = signed area",
            font_size=30,
        ).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3, 4, 1],
            y_range=[-3, 3, 1],
            x_length=6.2,
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
        plane.move_to(LEFT * 3.1 + DOWN * 0.25)
        self.play(Create(plane))

        theta_tr = ValueTracker(v_angle + 70 * DEGREES)

        def w_coords() -> np.ndarray:
            t = theta_tr.get_value()
            return w_len * np.array([np.cos(t), np.sin(t)])

        def cross_val() -> float:
            w = w_coords()
            return float(v[0] * w[1] - v[1] * w[0])

        v_arrow = self.arrow_from_coords(plane, v, RED)
        v_label = MathTex(r"\vec{v}", color=RED, font_size=28)
        v_label.set_stroke(BLACK, width=5, background=True)
        v_label.next_to(v_arrow.get_end(), RIGHT, buff=0.08)
        self.play(Create(v_arrow), FadeIn(v_label))

        w_arrow = always_redraw(lambda: self.arrow_from_coords(plane, w_coords(), GREEN, stroke_width=6))
        w_label = MathTex(r"\vec{w}", color=GREEN, font_size=28)
        w_label.set_stroke(BLACK, width=5, background=True)
        w_label.add_updater(lambda m: m.next_to(w_arrow.get_end(), LEFT, buff=0.08))

        para = always_redraw(
            lambda: Polygon(
                plane.c2p(0, 0),
                plane.c2p(float(v[0]), float(v[1])),
                plane.c2p(float((v + w_coords())[0]), float((v + w_coords())[1])),
                plane.c2p(float(w_coords()[0]), float(w_coords()[1])),
                color=TEAL,
                fill_color=TEAL,
                fill_opacity=0.18,
                stroke_width=2.2,
            )
        )

        self.add(para, w_arrow, w_label)

        formula = MathTex(
            r"\vec{v}\times\vec{w}=\det[\vec{v}\ \vec{w}]",
            font_size=27,
        )
        formula.set_color_by_tex(r"\vec{v}", RED)
        formula.set_color_by_tex(r"\vec{w}", GREEN)

        live_val = VGroup(
            MathTex(r"\vec{v}\times\vec{w}=", font_size=25, color=YELLOW),
            DecimalNumber(cross_val(), num_decimal_places=2, font_size=25, color=YELLOW),
        ).arrange(RIGHT, buff=0.08)

        sign_words = Tex(r"CCW $\to$ positive, CW $\to$ negative", font_size=22, color=BLUE_B)
        panel = VGroup(formula, live_val, sign_words).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        panel.move_to(RIGHT * 3.1 + UP * 1.0)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)
        live_val[1].add_updater(lambda m: m.set_value(cross_val()))
        self.play(FadeIn(panel_box), FadeIn(panel))

        self.play(theta_tr.animate.set_value(v_angle + 25 * DEGREES), run_time=2.0)
        self.play(theta_tr.animate.set_value(v_angle - 25 * DEGREES), run_time=2.0)
        self.play(theta_tr.animate.set_value(v_angle - 75 * DEGREES), run_time=2.0)
        self.wait(0.8)
