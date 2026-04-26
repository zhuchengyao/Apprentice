from manim import *
import numpy as np


class DependentVectorsSpanLineExample(Scene):
    """Dependent vectors only generate a line, not a plane."""

    def arrow_from_coords(
        self,
        plane: NumberPlane,
        coords: np.ndarray,
        color: ManimColor,
        *,
        start_coords: np.ndarray | None = None,
        stroke_width: float = 6,
        opacity: float = 1.0,
    ) -> Line:
        start_coords = np.array([0.0, 0.0]) if start_coords is None else start_coords
        start = plane.c2p(float(start_coords[0]), float(start_coords[1]))
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
        dep_factor = -1.5
        w = dep_factor * v

        title = Tex(
            r"Dependent vectors only span a line",
            font_size=30,
        ).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=6.5,
            y_length=5.0,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.3,
                "stroke_width": 1.0,
            },
            faded_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.14,
                "stroke_width": 0.7,
            },
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        )
        plane.move_to(LEFT * 3.35 + DOWN * 0.35)
        origin = plane.c2p(0, 0)
        self.play(Create(plane))

        line_dir = v / np.linalg.norm(v)
        span_line = Line(
            plane.c2p(*(line_dir * -5.0)),
            plane.c2p(*(line_dir * 5.0)),
            color=GREY_B,
            stroke_width=2.2,
        )
        self.play(Create(span_line))

        v_arrow = self.arrow_from_coords(plane, v, RED)
        w_arrow = self.arrow_from_coords(plane, w, GREEN)
        v_label = MathTex(r"\vec{v}", color=RED, font_size=28)
        w_label = MathTex(r"\vec{w}", color=GREEN, font_size=28)
        v_label.set_stroke(BLACK, width=5, background=True)
        w_label.set_stroke(BLACK, width=5, background=True)
        v_label.next_to(v_arrow.get_end(), RIGHT, buff=0.08)
        w_label.next_to(w_arrow.get_end(), LEFT, buff=0.08)
        self.play(Create(v_arrow), Create(w_arrow), FadeIn(v_label), FadeIn(w_label))

        a_tr = ValueTracker(1.0)
        b_tr = ValueTracker(1.0)

        def combo_scalar() -> float:
            return a_tr.get_value() + dep_factor * b_tr.get_value()

        def combo() -> np.ndarray:
            return combo_scalar() * v

        combo_arrow = always_redraw(lambda: self.arrow_from_coords(plane, combo(), YELLOW, stroke_width=7))
        combo_dot = always_redraw(
            lambda: Dot(plane.c2p(float(combo()[0]), float(combo()[1])), radius=0.08, color=YELLOW)
        )
        scaled_v = always_redraw(
            lambda: self.arrow_from_coords(
                plane,
                a_tr.get_value() * v,
                RED_E,
                stroke_width=5,
                opacity=0.55,
            )
        )
        shifted_w = always_redraw(
            lambda: self.arrow_from_coords(
                plane,
                combo(),
                GREEN_E,
                start_coords=a_tr.get_value() * v,
                stroke_width=5,
                opacity=0.55,
            )
        )
        combo_label = MathTex(r"a\vec{v}+b\vec{w}", color=YELLOW, font_size=28)
        combo_label.set_stroke(BLACK, width=5, background=True)
        combo_label.add_updater(
            lambda m: m.move_to((origin + combo_arrow.get_end()) / 2 + UP * 0.32)
        )

        self.add(scaled_v, shifted_w, combo_arrow, combo_dot, combo_label)

        dep_eq = MathTex(
            r"\vec{w}=-1.5\vec{v}",
            font_size=32,
        )
        dep_eq.set_color_by_tex(r"\vec{v}", RED)
        dep_eq.set_color_by_tex(r"\vec{w}", GREEN)

        combo_eq = MathTex(
            r"a\vec{v}+b\vec{w}=(a-1.5b)\vec{v}",
            font_size=28,
        )
        combo_eq.set_color_by_tex(r"\vec{v}", RED)
        combo_eq.set_color_by_tex(r"\vec{w}", GREEN)

        a_num = DecimalNumber(1.0, num_decimal_places=2, font_size=26, color=RED_E)
        b_num = DecimalNumber(1.0, num_decimal_places=2, font_size=26, color=GREEN_E)
        c_num = DecimalNumber(-0.5, num_decimal_places=2, font_size=26, color=YELLOW)
        readouts = VGroup(
            VGroup(MathTex("a=", font_size=26, color=RED_E), a_num).arrange(RIGHT, buff=0.12),
            VGroup(MathTex("b=", font_size=26, color=GREEN_E), b_num).arrange(RIGHT, buff=0.12),
            VGroup(MathTex("c=", font_size=26, color=YELLOW), c_num).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        note = Tex(
            r"Every endpoint stays on one line.",
            font_size=23,
            color=BLUE_B,
        )

        panel = VGroup(dep_eq, combo_eq, readouts, note).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel.move_to(RIGHT * 3.15 + UP * 0.95)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)

        a_num.add_updater(lambda m: m.set_value(a_tr.get_value()))
        b_num.add_updater(lambda m: m.set_value(b_tr.get_value()))
        c_num.add_updater(lambda m: m.set_value(combo_scalar()))

        self.play(FadeIn(panel_box), FadeIn(panel))

        for a_val, b_val in [(2.0, -0.5), (-0.8, 1.0), (0.5, 2.0), (1.7, 0.3)]:
            self.play(
                a_tr.animate.set_value(a_val),
                b_tr.animate.set_value(b_val),
                run_time=1.7,
            )
            self.wait(0.2)

        sample_points = VGroup()
        for c in np.linspace(-3.5, 3.5, 15):
            p = c * v
            sample_points.add(
                Dot(plane.c2p(float(p[0]), float(p[1])), radius=0.03, color=TEAL_A)
            )
        self.play(LaggedStartMap(FadeIn, sample_points, lag_ratio=0.04, run_time=1.4))
        self.wait(0.8)
