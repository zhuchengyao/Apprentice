from manim import *
import numpy as np


class IndependenceMultiplicationExample(Scene):
    """
    If A and B are independent, P(A ∩ B) = P(A) · P(B). Visualize
    as a rectangle area: the entire sample space is a unit square;
    events A, B are strips; their intersection is a rectangle whose
    area = P(A) · P(B).

    TWO_COLUMN:
      LEFT  — unit square with VERTICAL strip for A (width P(A)) and
              HORIZONTAL strip for B (height P(B)); intersection is
              the overlapping rectangle. ValueTrackers pA_tr, pB_tr
              sweep through 4 configurations.
      RIGHT — live P(A), P(B), P(A∩B) = P(A)·P(B) comparison.
    """

    def construct(self):
        title = Tex(r"Independence: $P(A \cap B) = P(A) \cdot P(B)$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Unit square
        cx, cy = -2.8, -0.3
        W, H = 4.0, 4.0

        outer = Rectangle(width=W, height=H, color=WHITE, stroke_width=2
                           ).move_to([cx, cy, 0])
        self.play(Create(outer))

        pA_tr = ValueTracker(0.4)
        pB_tr = ValueTracker(0.5)

        def strip_A():
            p = pA_tr.get_value()
            return Rectangle(width=W * p, height=H, color=BLUE,
                              fill_opacity=0.35, stroke_width=0
                              ).move_to([cx - W / 2 + W * p / 2, cy, 0])

        def strip_B():
            p = pB_tr.get_value()
            return Rectangle(width=W, height=H * p, color=RED,
                              fill_opacity=0.35, stroke_width=0
                              ).move_to([cx, cy + H / 2 - H * p / 2, 0])

        def inter():
            pa = pA_tr.get_value()
            pb = pB_tr.get_value()
            return Rectangle(width=W * pa, height=H * pb, color=YELLOW,
                              fill_opacity=0.7, stroke_width=2
                              ).move_to([cx - W / 2 + W * pa / 2,
                                          cy + H / 2 - H * pb / 2, 0])

        self.add(always_redraw(strip_A),
                  always_redraw(strip_B),
                  always_redraw(inter))

        # Labels
        A_lbl = Tex(r"$A$", color=BLUE, font_size=24).move_to([cx - W/2 + 0.3, cy + H/2 + 0.3, 0])
        B_lbl = Tex(r"$B$", color=RED, font_size=24).move_to([cx + W/2 + 0.3, cy + H/2 - 0.3, 0])
        self.play(Write(A_lbl), Write(B_lbl))

        def info():
            pa = pA_tr.get_value()
            pb = pB_tr.get_value()
            return VGroup(
                MathTex(rf"P(A) = {pa:.2f}", color=BLUE, font_size=24),
                MathTex(rf"P(B) = {pb:.2f}", color=RED, font_size=24),
                MathTex(rf"P(A) \cdot P(B) = {pa * pb:.3f}",
                         color=YELLOW, font_size=24),
                MathTex(r"= \text{area of yellow}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.5, 0.5, 0])

        self.add(always_redraw(info))

        tour = [(0.6, 0.3), (0.2, 0.7), (0.9, 0.4), (0.5, 0.5)]
        for (a, b) in tour:
            self.play(pA_tr.animate.set_value(a),
                       pB_tr.animate.set_value(b),
                       run_time=1.8, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
