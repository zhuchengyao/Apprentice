from manim import *
import numpy as np


class CramersRuleAreaRatioExample(Scene):
    """Cramer's rule as an area ratio in 2D."""

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
        v = np.array([2.0, 1.0])
        w = np.array([1.0, 2.0])
        b = np.array([3.0, 0.0])
        det_A = float(v[0] * w[1] - v[1] * w[0])
        det_x = float(b[0] * w[1] - b[1] * w[0])
        x_val = det_x / det_A
        y_val = float(v[0] * b[1] - v[1] * b[0]) / det_A

        title = Tex(
            r"Cramer's rule: solve by area ratios",
            font_size=29,
        ).to_edge(UP, buff=0.2)
        self.play(Write(title))

        left_plane = NumberPlane(
            x_range=[-1, 4, 1],
            y_range=[-2, 3, 1],
            x_length=3.4,
            y_length=3.4,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.22, "stroke_width": 0.9},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.1, "stroke_width": 0.6},
            axis_config={"stroke_width": 1.8, "stroke_opacity": 0.8},
        ).move_to(LEFT * 4.2 + DOWN * 0.35)
        right_plane = left_plane.copy().move_to(LEFT * 1.2 + DOWN * 0.35)

        self.play(Create(left_plane), Create(right_plane))

        left_para = Polygon(
            left_plane.c2p(0, 0),
            left_plane.c2p(float(v[0]), float(v[1])),
            left_plane.c2p(float((v + w)[0]), float((v + w)[1])),
            left_plane.c2p(float(w[0]), float(w[1])),
            color=TEAL,
            fill_color=TEAL,
            fill_opacity=0.18,
            stroke_width=2.2,
        )
        right_para = Polygon(
            right_plane.c2p(0, 0),
            right_plane.c2p(float(b[0]), float(b[1])),
            right_plane.c2p(float((b + w)[0]), float((b + w)[1])),
            right_plane.c2p(float(w[0]), float(w[1])),
            color=YELLOW_E,
            fill_color=YELLOW_E,
            fill_opacity=0.18,
            stroke_width=2.2,
        )

        v_arrow = self.arrow_from_coords(left_plane, v, RED)
        w_arrow = self.arrow_from_coords(left_plane, w, GREEN)
        b_arrow = self.arrow_from_coords(right_plane, b, YELLOW)
        w2_arrow = self.arrow_from_coords(right_plane, w, GREEN)
        labels = [
            MathTex(r"\vec{v}", color=RED, font_size=24).next_to(v_arrow.get_end(), RIGHT, buff=0.06),
            MathTex(r"\vec{w}", color=GREEN, font_size=24).next_to(w_arrow.get_end(), UP, buff=0.06),
            MathTex(r"\vec{b}", color=YELLOW, font_size=24).next_to(b_arrow.get_end(), UP, buff=0.06),
            MathTex(r"\vec{w}", color=GREEN, font_size=24).next_to(w2_arrow.get_end(), UP, buff=0.06),
        ]
        for lab in labels:
            lab.set_stroke(BLACK, width=5, background=True)

        self.play(
            FadeIn(left_para), GrowArrow(v_arrow), GrowArrow(w_arrow), FadeIn(labels[0]), FadeIn(labels[1])
        )
        self.play(
            FadeIn(right_para),
            TransformFromCopy(v_arrow, b_arrow),
            TransformFromCopy(w_arrow, w2_arrow),
            FadeIn(labels[2]), FadeIn(labels[3]),
        )

        left_words = Tex("det(A) = area(v, w) = 3", font_size=22, color=TEAL_A)
        right_words = Tex("det([b, w]) = 6", font_size=22, color=YELLOW_E)
        left_words.move_to(left_plane.get_bottom() + DOWN * 0.45)
        right_words.move_to(right_plane.get_bottom() + DOWN * 0.45)
        self.play(FadeIn(left_words), FadeIn(right_words))

        formula = MathTex(
            r"x=\frac{\det([\vec{b}\ \vec{w}])}{\det([\vec{v}\ \vec{w}])}"
            r"=\frac{6}{3}=2",
            font_size=27,
        )
        formula.set_color_by_tex(r"\vec{v}", RED)
        formula.set_color_by_tex(r"\vec{w}", GREEN)
        formula.set_color_by_tex(r"\vec{b}", YELLOW)
        note = MathTex(r"y=\frac{\det([\vec{v}\ \vec{b}])}{\det(A)}=-1", font_size=25)
        note.set_color_by_tex(r"\vec{v}", RED)
        note.set_color_by_tex(r"\vec{b}", YELLOW)
        panel = VGroup(formula, note).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        panel.move_to(RIGHT * 2.9 + UP * 0.95)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)
        self.play(FadeIn(panel_box), FadeIn(panel))
        self.wait(0.8)
