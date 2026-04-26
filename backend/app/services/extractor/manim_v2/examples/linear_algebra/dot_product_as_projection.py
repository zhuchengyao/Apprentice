from manim import *
import numpy as np


class DotProductAsProjectionExample(Scene):
    """Dot product as length times signed projection."""

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
        v = np.array([3.0, 1.0])
        v_norm = float(np.linalg.norm(v))
        v_unit = v / v_norm
        w_len = 2.7

        title = Tex(
            r"Dot product = length times signed projection",
            font_size=29,
        ).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=6.4,
            y_length=5.2,
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
        plane.move_to(LEFT * 3.2 + DOWN * 0.3)
        self.play(Create(plane))

        support_line = Line(
            plane.c2p(*(v_unit * -4.5)),
            plane.c2p(*(v_unit * 4.5)),
            color=GREY_B,
            stroke_width=2.0,
        )
        v_arrow = self.arrow_from_coords(plane, v, RED)
        v_label = MathTex(r"\vec{v}", color=RED, font_size=28)
        v_label.set_stroke(BLACK, width=5, background=True)
        v_label.next_to(v_arrow.get_end(), RIGHT, buff=0.08)

        theta_tr = ValueTracker(35 * DEGREES)

        def w_coords() -> np.ndarray:
            t = theta_tr.get_value()
            return w_len * np.array([np.cos(t), np.sin(t)])

        def proj_scalar() -> float:
            return float(np.dot(w_coords(), v_unit))

        def proj_coords() -> np.ndarray:
            return proj_scalar() * v_unit

        w_arrow = always_redraw(lambda: self.arrow_from_coords(plane, w_coords(), GREEN, stroke_width=6))
        proj_arrow = always_redraw(
            lambda: self.arrow_from_coords(plane, proj_coords(), YELLOW_E, stroke_width=6, opacity=0.85)
        )
        drop_line = always_redraw(
            lambda: DashedLine(
                plane.c2p(float(w_coords()[0]), float(w_coords()[1])),
                plane.c2p(float(proj_coords()[0]), float(proj_coords()[1])),
                color=GREY_B,
                stroke_width=2,
                dash_length=0.12,
            )
        )
        w_label = MathTex(r"\vec{w}", color=GREEN, font_size=28)
        proj_label = MathTex(r"\mathrm{proj}_{\vec{v}}(\vec{w})", color=YELLOW_E, font_size=24)
        for label in (w_label, proj_label):
            label.set_stroke(BLACK, width=5, background=True)
        w_label.add_updater(lambda m: m.next_to(w_arrow.get_end(), RIGHT, buff=0.08))
        proj_label.add_updater(lambda m: m.next_to(proj_arrow.get_end(), DOWN, buff=0.08))

        self.play(Create(support_line), Create(v_arrow), FadeIn(v_label))
        self.add(drop_line, proj_arrow, w_arrow, w_label, proj_label)

        formula = MathTex(
            r"\vec{v}\cdot\vec{w}=|\vec{v}|\cdot\mathrm{signed\ projection}",
            font_size=27,
        )
        formula.set_color_by_tex(r"\vec{v}", RED)
        formula.set_color_by_tex(r"\vec{w}", GREEN)

        readout = VGroup(
            formula,
            VGroup(
                MathTex(r"|\vec{v}|=", font_size=24, color=RED),
                DecimalNumber(v_norm, num_decimal_places=2, font_size=24, color=RED),
            ).arrange(RIGHT, buff=0.08),
            VGroup(
                MathTex(r"\mathrm{proj}_{\vec{v}}(\vec{w})=", font_size=24, color=YELLOW_E),
                DecimalNumber(proj_scalar(), num_decimal_places=2, font_size=24, color=YELLOW_E),
            ).arrange(RIGHT, buff=0.08),
            VGroup(
                MathTex(r"\vec{v}\cdot\vec{w}=", font_size=24, color=GREEN),
                DecimalNumber(np.dot(v, w_coords()), num_decimal_places=2, font_size=24, color=GREEN),
            ).arrange(RIGHT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        readout.move_to(RIGHT * 3.1 + UP * 0.9)
        readout_box = SurroundingRectangle(readout, color=GREY_B, buff=0.22)
        readout_box.set_fill(BLACK, opacity=0.84)

        proj_num = readout[2][1]
        dot_num = readout[3][1]
        proj_num.add_updater(lambda m: m.set_value(proj_scalar()))
        dot_num.add_updater(lambda m: m.set_value(np.dot(v, w_coords())))

        sign_note = Tex(
            r"Past $90^\circ$, the signed projection and the dot product turn negative.",
            font_size=20,
            color=BLUE_B,
        ).move_to(RIGHT * 2.75 + DOWN * 1.85)
        sign_box = SurroundingRectangle(sign_note, color=GREY_B, buff=0.18)
        sign_box.set_fill(BLACK, opacity=0.8)

        self.play(FadeIn(readout_box), FadeIn(readout))
        self.play(theta_tr.animate.set_value(70 * DEGREES), run_time=2.0)
        self.play(theta_tr.animate.set_value(110 * DEGREES), run_time=2.0)
        self.play(theta_tr.animate.set_value(145 * DEGREES), run_time=2.0)
        self.play(FadeIn(sign_box), FadeIn(sign_note))
        self.wait(0.8)
