from manim import *
import numpy as np
from math import pi, gamma


class HighDimSphereVolumeExample(Scene):
    """
    Volume of a unit n-ball V_n = π^(n/2) / Γ(n/2 + 1) peaks at n=5
    and → 0 as n → ∞.

    TWO_COLUMN:
      LEFT  — axes plotting V_n for n = 0..20; ValueTracker n_tr
              walks a cursor across integer n via always_redraw;
              rider dot + dashed drop.
      RIGHT — live n, V_n, formula, and a small rect of the
              unit hypercube-volume (always 1) for contrast.
    """

    def construct(self):
        title = Tex(r"Unit $n$-ball volume: $V_n = \dfrac{\pi^{n/2}}{\Gamma(n/2 + 1)}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def V(n):
            return pi ** (n / 2) / gamma(n / 2 + 1)

        ax = Axes(x_range=[0, 20, 2], y_range=[0, 6, 1],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        xlbl = MathTex(r"n", font_size=22).next_to(ax, DOWN, buff=0.1)
        ylbl = MathTex(r"V_n", font_size=22).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        curve = ax.plot(V, x_range=[0.01, 20, 0.1], color=BLUE, stroke_width=3)
        int_dots = VGroup(*[Dot(ax.c2p(k, V(k)), color=BLUE_D, radius=0.06)
                             for k in range(0, 21)])
        self.play(Create(curve), FadeIn(int_dots))

        peak_dot = Dot(ax.c2p(5, V(5)), color=RED, radius=0.1)
        peak_lbl = MathTex(r"\text{peak at } n=5", color=RED,
                             font_size=20).next_to(peak_dot, UP, buff=0.15)
        self.play(FadeIn(peak_dot), Write(peak_lbl))

        n_tr = ValueTracker(0.01)

        def rider():
            n = n_tr.get_value()
            return Dot(ax.c2p(n, V(n)), color=YELLOW, radius=0.11)

        def drop():
            n = n_tr.get_value()
            return DashedLine(ax.c2p(n, 0), ax.c2p(n, V(n)),
                               color=YELLOW_E, stroke_width=1.5)

        self.add(always_redraw(rider), always_redraw(drop))

        def info():
            n = n_tr.get_value()
            return VGroup(
                MathTex(rf"n = {n:.2f}", color=WHITE, font_size=26),
                MathTex(rf"V_n = {V(n):.4f}", color=YELLOW, font_size=26),
                MathTex(r"[\text{cube}]_n = 1", color=GREY_B, font_size=22),
                MathTex(r"V_n \to 0 \text{ as } n \to \infty",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.3, 0.0, 0])

        self.add(always_redraw(info))

        self.play(n_tr.animate.set_value(20),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
