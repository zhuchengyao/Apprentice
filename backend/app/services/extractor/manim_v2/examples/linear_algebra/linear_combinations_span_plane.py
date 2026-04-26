from manim import *
import numpy as np


class LinearCombinationsSpanPlaneExample(Scene):
    """Two non-parallel vectors generate the whole plane."""

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
        w = np.array([-1.0, 1.5])

        title = Tex(
            r"Non-parallel vectors span the plane",
            font_size=30,
        ).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=6.3,
            y_length=5.2,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.32,
                "stroke_width": 1.0,
            },
            faded_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.14,
                "stroke_width": 0.7,
            },
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        )
        plane.move_to(LEFT * 3.45 + DOWN * 0.35)
        self.play(Create(plane))

        v_arrow = self.arrow_from_coords(plane, v, RED)
        w_arrow = self.arrow_from_coords(plane, w, GREEN)
        v_label = MathTex(r"\vec{v}", color=RED, font_size=28)
        w_label = MathTex(r"\vec{w}", color=GREEN, font_size=28)
        v_label.set_stroke(BLACK, width=5, background=True)
        w_label.set_stroke(BLACK, width=5, background=True)
        v_label.next_to(v_arrow.get_end(), RIGHT, buff=0.08)
        w_label.next_to(w_arrow.get_end(), UP, buff=0.08)
        self.play(Create(v_arrow), Create(w_arrow), FadeIn(v_label), FadeIn(w_label))

        a_tr = ValueTracker(1.0)
        b_tr = ValueTracker(1.0)

        def combo() -> np.ndarray:
            return a_tr.get_value() * v + b_tr.get_value() * w

        def scaled_v() -> Arrow:
            return self.arrow_from_coords(
                plane,
                a_tr.get_value() * v,
                RED_E,
                stroke_width=5,
                opacity=0.55,
            )

        def shifted_w() -> Arrow:
            start = a_tr.get_value() * v
            end = start + b_tr.get_value() * w
            return self.arrow_from_coords(
                plane,
                end,
                GREEN_E,
                start_coords=start,
                stroke_width=5,
                opacity=0.55,
            )

        def combo_arrow() -> Arrow:
            return self.arrow_from_coords(plane, combo(), YELLOW, stroke_width=7)

        def combo_dot() -> Dot:
            p = combo()
            return Dot(plane.c2p(float(p[0]), float(p[1])), radius=0.08, color=YELLOW)

        def combo_parallelogram() -> Polygon:
            a_v = a_tr.get_value() * v
            b_w = b_tr.get_value() * w
            return Polygon(
                plane.c2p(0, 0),
                plane.c2p(float(a_v[0]), float(a_v[1])),
                plane.c2p(float((a_v + b_w)[0]), float((a_v + b_w)[1])),
                plane.c2p(float(b_w[0]), float(b_w[1])),
                color=TEAL,
                fill_color=TEAL,
                fill_opacity=0.16,
                stroke_width=2,
            )

        combo_label = MathTex(r"a\vec{v}+b\vec{w}", color=YELLOW, font_size=28)
        combo_label.set_stroke(BLACK, width=5, background=True)

        def place_combo_label(m: Mobject) -> None:
            end = plane.c2p(float(combo()[0]), float(combo()[1]))
            direction = RIGHT if end[0] < -5.4 else LEFT
            m.next_to(end, direction, buff=0.12)

        combo_label.add_updater(place_combo_label)

        self.add(
            always_redraw(combo_parallelogram),
            always_redraw(scaled_v),
            always_redraw(shifted_w),
            always_redraw(combo_arrow),
            always_redraw(combo_dot),
            combo_label,
        )

        formula = MathTex(
            r"a\vec{v}+b\vec{w}",
            font_size=34,
        )
        formula.set_color_by_tex(r"\vec{v}", RED)
        formula.set_color_by_tex(r"\vec{w}", GREEN)
        formula.set_color_by_tex("a", RED_E)
        formula.set_color_by_tex("b", GREEN_E)

        readout = VGroup(
            formula,
            VGroup(
                VGroup(
                    MathTex("a=", font_size=26, color=RED_E),
                    DecimalNumber(1.0, num_decimal_places=2, font_size=26, color=RED_E),
                ).arrange(RIGHT, buff=0.12),
                VGroup(
                    MathTex("b=", font_size=26, color=GREEN_E),
                    DecimalNumber(1.0, num_decimal_places=2, font_size=26, color=GREEN_E),
                ).arrange(RIGHT, buff=0.12),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(
                MathTex(r"a\vec{v}+b\vec{w}=", font_size=26, color=YELLOW),
                DecimalMatrix([[1.0], [2.5]], element_to_mobject_config={"font_size": 24}),
            ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        readout.move_to(RIGHT * 3.1 + UP * 1.1)
        readout_box = SurroundingRectangle(readout, color=GREY_B, buff=0.22)
        readout_box.set_fill(BLACK, opacity=0.84)

        a_num = readout[1][0][1]
        b_num = readout[1][1][1]
        combo_matrix = readout[2][1]
        combo_entries = combo_matrix.get_entries()
        a_num.add_updater(lambda m: m.set_value(a_tr.get_value()))
        b_num.add_updater(lambda m: m.set_value(b_tr.get_value()))
        combo_entries[0].add_updater(lambda m: m.set_value(combo()[0]))
        combo_entries[1].add_updater(lambda m: m.set_value(combo()[1]))

        self.play(FadeIn(readout_box), FadeIn(readout))

        for a_val, b_val in [(1.8, -0.8), (-1.4, 1.3), (0.5, 2.0), (1.2, 0.7)]:
            self.play(
                a_tr.animate.set_value(a_val),
                b_tr.animate.set_value(b_val),
                run_time=1.8,
            )
            self.wait(0.2)

        sample_points = VGroup()
        for a in np.linspace(-2.0, 2.0, 7):
            for b in np.linspace(-2.0, 2.0, 7):
                p = a * v + b * w
                if -4.1 <= p[0] <= 4.1 and -3.1 <= p[1] <= 3.1:
                    sample_points.add(
                        Dot(plane.c2p(float(p[0]), float(p[1])), radius=0.035, color=TEAL_A)
                    )

        note = Tex(
            r"As $a$ and $b$ vary, the endpoints spread across the plane.",
            font_size=23,
            color=BLUE_B,
        ).move_to(RIGHT * 3.15 + DOWN * 1.55)
        note_box = SurroundingRectangle(note, color=GREY_B, buff=0.18)
        note_box.set_fill(BLACK, opacity=0.8)

        self.play(FadeIn(note_box), FadeIn(note))
        self.play(LaggedStartMap(FadeIn, sample_points, lag_ratio=0.01, run_time=1.8))
        self.wait(0.8)
