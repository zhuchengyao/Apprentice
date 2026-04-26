from manim import *
import numpy as np


class LinearityAdditivityExample(Scene):
    """A(v + w) = Av + Aw shown as two routes to the same vector."""

    def arrow_from_vector(
        self,
        plane: NumberPlane,
        vector: np.ndarray,
        color: ManimColor,
        *,
        start: np.ndarray | None = None,
        stroke_width: float = 6,
        opacity: float = 1.0,
    ) -> Arrow:
        if start is None:
            start = np.zeros(2)
        arrow = Arrow(
            plane.c2p(float(start[0]), float(start[1])),
            plane.c2p(float(start[0] + vector[0]), float(start[1] + vector[1])),
            buff=0,
            color=color,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.16,
        )
        arrow.set_opacity(opacity)
        return arrow

    def label_at_tip(
        self,
        arrow: Arrow,
        tex: str,
        color: ManimColor,
        direction: np.ndarray = RIGHT,
        *,
        font_size: int = 26,
    ) -> MathTex:
        label = MathTex(tex, color=color, font_size=font_size)
        label.set_stroke(BLACK, width=5, background=True)
        label.next_to(arrow.get_end(), direction, buff=0.08)
        return label

    def construct(self):
        A = np.array([[1.0, 0.5], [-1.0, 1.0]])
        v = np.array([2.0, -1.0])
        w = np.array([1.0, 2.0])
        v_plus_w = v + w
        av = A @ v
        aw = A @ w
        a_sum = A @ v_plus_w

        title = Tex(r"Linear maps preserve vector addition", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2, 5, 1],
            y_range=[-3, 4, 1],
            x_length=5.2,
            y_length=5.2,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.28, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        )
        plane.move_to(LEFT * 3.05 + DOWN * 0.25)
        self.play(Create(plane))

        formula = MathTex(r"A(\vec{v}+\vec{w})=A\vec{v}+A\vec{w}", font_size=30)
        formula.set_color_by_tex(r"\vec{v}", YELLOW)
        formula.set_color_by_tex(r"\vec{w}", MAROON_B)
        route_one = MathTex(
            r"1.\quad \vec{v}+\vec{w}\xrightarrow{A}A(\vec{v}+\vec{w})",
            font_size=25,
            color=PINK,
        )
        route_two = MathTex(
            r"2.\quad \vec{v}\xrightarrow{A}A\vec{v},\quad \vec{w}\xrightarrow{A}A\vec{w}",
            font_size=25,
            color=BLUE_B,
        )
        note = Tex("Both routes land on the same endpoint.", font_size=22, color=GREY_A)
        panel = VGroup(route_one, route_two, formula, note).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel.move_to(RIGHT * 3.08 + UP * 0.78)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)
        self.play(FadeIn(panel_box), FadeIn(route_one))

        v_arrow = self.arrow_from_vector(plane, v, YELLOW, stroke_width=6)
        w_arrow = self.arrow_from_vector(plane, w, MAROON_B, stroke_width=6)
        shifted_w = self.arrow_from_vector(plane, w, MAROON_B, start=v, stroke_width=6, opacity=0.72)
        sum_arrow = self.arrow_from_vector(plane, v_plus_w, PINK, stroke_width=8)
        parallelogram = Polygon(
            plane.c2p(0, 0),
            plane.c2p(float(v[0]), float(v[1])),
            plane.c2p(float(v_plus_w[0]), float(v_plus_w[1])),
            plane.c2p(float(w[0]), float(w[1])),
            color=TEAL,
            fill_color=TEAL,
            fill_opacity=0.12,
            stroke_width=2.0,
        )
        sum_label = self.label_at_tip(sum_arrow, r"\vec{v}+\vec{w}", PINK, UP + RIGHT)

        self.play(FadeIn(parallelogram), GrowArrow(v_arrow), GrowArrow(w_arrow))
        self.play(GrowArrow(shifted_w), GrowArrow(sum_arrow), FadeIn(sum_label))

        route_one_result = self.arrow_from_vector(plane, a_sum, GREY_A, stroke_width=9, opacity=0.58)
        route_one_label = self.label_at_tip(route_one_result, r"A(\vec{v}+\vec{w})", GREY_A, UP + RIGHT, font_size=25)
        self.play(
            Transform(sum_arrow, route_one_result),
            Transform(sum_label, route_one_label),
            FadeOut(parallelogram),
            FadeOut(v_arrow),
            FadeOut(w_arrow),
            FadeOut(shifted_w),
            run_time=1.6,
        )
        self.play(sum_arrow.animate.set_opacity(0.45), FadeOut(sum_label))

        self.play(FadeIn(route_two))
        route_v = self.arrow_from_vector(plane, v, YELLOW, stroke_width=6)
        route_w = self.arrow_from_vector(plane, w, MAROON_B, stroke_width=6)
        v_label = self.label_at_tip(route_v, r"\vec{v}", YELLOW, DOWN + RIGHT)
        w_label = self.label_at_tip(route_w, r"\vec{w}", MAROON_B, UP + LEFT)
        self.play(GrowArrow(route_v), GrowArrow(route_w), FadeIn(v_label), FadeIn(w_label))

        av_arrow = self.arrow_from_vector(plane, av, YELLOW, stroke_width=7)
        aw_arrow = self.arrow_from_vector(plane, aw, MAROON_B, stroke_width=7)
        av_label = self.label_at_tip(av_arrow, r"A\vec{v}", YELLOW, DOWN + LEFT)
        aw_label = self.label_at_tip(aw_arrow, r"A\vec{w}", MAROON_B, UP + RIGHT)
        self.play(
            Transform(route_v, av_arrow),
            Transform(v_label, av_label),
            Transform(route_w, aw_arrow),
            Transform(w_label, aw_label),
            run_time=1.4,
        )

        shifted_aw = self.arrow_from_vector(plane, aw, MAROON_B, start=av, stroke_width=6, opacity=0.72)
        shifted_aw_label = self.label_at_tip(shifted_aw, r"A\vec{w}", MAROON_B, UP + RIGHT, font_size=24)
        final_arrow = self.arrow_from_vector(plane, av + aw, GREEN_B, stroke_width=6)
        final_label = self.label_at_tip(final_arrow, r"A\vec{v}+A\vec{w}", GREEN_B, DOWN + RIGHT, font_size=25)
        self.play(TransformFromCopy(route_w, shifted_aw), FadeIn(shifted_aw_label), run_time=1.1)
        self.play(GrowArrow(final_arrow), FadeIn(final_label), run_time=1.1)

        self.play(Write(formula), Write(note))
        self.play(Circumscribe(VGroup(sum_arrow, final_arrow), color=YELLOW))
        self.wait(0.8)
