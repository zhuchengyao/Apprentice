from manim import *
import numpy as np


class PopulationGrowthExample(Scene):
    """
    Logistic population growth: P' = rP(1 - P/K).

    TWO_COLUMN:
      LEFT  — axes with logistic curve P(t) = K / (1 + A e^{-rt})
              for K=100, r=0.4, P(0)=5. ValueTracker t_tr advances
              time; BLUE rider dot + RED dashed tangent line whose
              slope = instantaneous growth rate P'(t).
      RIGHT — live t, P, P/K, dP/dt, r·P(1-P/K) check.
    """

    def construct(self):
        title = Tex(r"Logistic growth: $\dfrac{dP}{dt} = rP\!\left(1 - \tfrac{P}{K}\right)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        K, r, P0 = 100.0, 0.4, 5.0
        A = (K - P0) / P0

        def P(t):
            return K / (1 + A * np.exp(-r * t))

        def dP(t):
            Pt = P(t)
            return r * Pt * (1 - Pt / K)

        ax = Axes(x_range=[0, 30, 5], y_range=[0, 110, 25],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        xlbl = MathTex(r"t", font_size=22).next_to(ax, DOWN, buff=0.1)
        ylbl = MathTex(r"P", font_size=22).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        curve = ax.plot(P, x_range=[0, 30], color=BLUE, stroke_width=3)
        carrying_K = DashedLine(ax.c2p(0, K), ax.c2p(30, K),
                                 color=GREY_B, stroke_width=1.5)
        K_lbl = MathTex(rf"K = {int(K)}", color=GREY_B,
                         font_size=20).move_to(ax.c2p(2, K + 5))
        self.play(Create(curve), Create(carrying_K), Write(K_lbl))

        t_tr = ValueTracker(0.1)

        def rider():
            t = t_tr.get_value()
            return Dot(ax.c2p(t, P(t)), color=BLUE, radius=0.11)

        def tangent():
            t = t_tr.get_value()
            slope = dP(t)
            tl = max(0, t - 2)
            tr_ = min(30, t + 2)
            return ax.plot(lambda x: P(t) + slope * (x - t),
                            x_range=[tl, tr_], color=RED, stroke_width=2)

        self.add(always_redraw(rider), always_redraw(tangent))

        def info():
            t = t_tr.get_value()
            Pt = P(t)
            dPt = dP(t)
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=WHITE, font_size=24),
                MathTex(rf"P = {Pt:.2f}", color=BLUE, font_size=24),
                MathTex(rf"P/K = {Pt/K:.3f}", color=GREY_B, font_size=22),
                MathTex(rf"dP/dt = {dPt:.3f}", color=RED, font_size=22),
                MathTex(rf"rP(1-P/K) = {r*Pt*(1-Pt/K):.3f}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.3, 0.0, 0])

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(30.0),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
