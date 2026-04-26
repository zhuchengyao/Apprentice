from manim import *
import numpy as np


class VectorAdditionHeadToTailExample(Scene):
    """Head-to-tail vector addition in the plane."""

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
            max_tip_length_to_length_ratio=0.18,
        )
        arrow.set_opacity(opacity)
        return arrow

    def construct(self):
        v = np.array([2.0, 1.0])
        w = np.array([1.2, 1.4])
        v_plus_w = v + w

        title = Tex(r"Vector addition = walk head to tail", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 4, 1],
            x_length=6.0,
            y_length=5.0,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.28, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.12, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        )
        plane.move_to(LEFT * 3.15 + DOWN * 0.25)
        self.play(Create(plane))

        v_arrow = self.arrow_from_vector(plane, v, RED)
        w_arrow = self.arrow_from_vector(plane, w, GREEN)
        shifted_w = self.arrow_from_vector(plane, w, GREEN, start=v)
        moving_w = w_arrow.copy()
        sum_arrow = self.arrow_from_vector(plane, v_plus_w, PINK, stroke_width=7)

        v_label = MathTex(r"\vec{v}", color=RED, font_size=28)
        w_label = MathTex(r"\vec{w}", color=GREEN, font_size=28)
        sum_label = MathTex(r"\vec{v}+\vec{w}", color=PINK, font_size=26)
        for mob in (v_label, w_label, sum_label):
            mob.set_stroke(BLACK, width=5, background=True)
        v_label.next_to(v_arrow.get_end(), RIGHT, buff=0.08)
        w_label.next_to(w_arrow.get_end(), UP, buff=0.08)
        sum_label.next_to(sum_arrow.get_end(), RIGHT, buff=0.08)

        formula = MathTex(
            r"\vec{v}+\vec{w}=",
            r"\begin{bmatrix}2\\1\end{bmatrix}",
            r"+",
            r"\begin{bmatrix}1.2\\1.4\end{bmatrix}",
            r"=",
            r"\begin{bmatrix}3.2\\2.4\end{bmatrix}",
            font_size=26,
        )
        formula.set_color_by_tex(r"\vec{v}", RED)
        formula.set_color_by_tex(r"\vec{w}", GREEN)
        note = Tex("Put the second arrow at the first arrow's tip.", font_size=22, color=BLUE_B)
        panel = VGroup(formula, note).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        panel.move_to(RIGHT * 3.05 + UP * 1.05)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)

        self.play(GrowArrow(v_arrow), FadeIn(v_label))
        self.play(GrowArrow(w_arrow), FadeIn(w_label))
        self.play(FadeIn(panel_box), FadeIn(panel))
        self.play(w_arrow.animate.set_opacity(0.3), w_label.animate.set_opacity(0.45))
        self.add(moving_w)
        self.play(Transform(moving_w, shifted_w), run_time=1.8)
        self.play(GrowArrow(sum_arrow), FadeIn(sum_label))
        self.wait(0.8)
