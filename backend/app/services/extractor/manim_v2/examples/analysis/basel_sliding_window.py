from manim import *
import numpy as np


class BaselSlidingWindowExample(Scene):
    """
    Basel sliding-window visualization (from _2018/basel/basel2):
    Σ 1/n² = π²/6 via sliding window partial sums building toward
    the limit. Different angle from the main basel_problem scene.

    SINGLE_FOCUS:
      Stacked rectangles for terms 1/n², each shifted left by the
      previous partial sum; always_redraw as ValueTracker N_tr
      grows. Running comparison with target π²/6 ≈ 1.6449.
    """

    def construct(self):
        title = Tex(r"Basel: $\sum_{n=1}^{\infty} \tfrac{1}{n^2} = \tfrac{\pi^2}{6} \approx 1.6449$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        target = (PI ** 2) / 6

        # Number-line representation of partial sum
        nl = NumberLine(x_range=[0, 2, 0.25], length=12,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 2,
                                                 "font_size": 16}
                         ).move_to([0, -1, 0])
        self.play(Create(nl))

        # Target marker
        target_tick = Line(nl.n2p(target) + UP * 0.4,
                             nl.n2p(target) + DOWN * 0.4,
                             color=YELLOW, stroke_width=3)
        target_lbl = MathTex(r"\pi^2/6", color=YELLOW,
                               font_size=22
                               ).next_to(target_tick, UP, buff=0.15)
        self.play(Create(target_tick), Write(target_lbl))

        N_max = 40
        N_tr = ValueTracker(1)

        def term_bars():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, N_max))
            grp = VGroup()
            cum = 0.0
            for k in range(1, N + 1):
                t = 1 / (k * k)
                x_start = nl.n2p(cum)
                x_end = nl.n2p(cum + t)
                w = x_end[0] - x_start[0]
                if w < 0.005:
                    cum += t
                    continue
                col = interpolate_color(BLUE, RED, min(1.0, 1 - 1/k))
                bar = Rectangle(width=w, height=0.55,
                                 color=col, fill_opacity=0.7,
                                 stroke_width=0.5)
                bar.move_to([(x_start[0] + x_end[0]) / 2,
                             nl.n2p(0)[1] + 0.35, 0])
                grp.add(bar)
                cum += t
            return grp

        self.add(always_redraw(term_bars))

        def sum_marker():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, N_max))
            partial = sum(1 / (k * k) for k in range(1, N + 1))
            return VGroup(
                Line(nl.n2p(partial) + UP * 0.4,
                      nl.n2p(partial) + DOWN * 0.4,
                      color=GREEN, stroke_width=4),
                Dot(nl.n2p(partial), color=GREEN, radius=0.1),
            )

        self.add(always_redraw(sum_marker))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, N_max))
            partial = sum(1 / (k * k) for k in range(1, N + 1))
            gap = target - partial
            return VGroup(
                MathTex(rf"N = {N}", color=WHITE, font_size=24),
                MathTex(rf"S_N = {partial:.5f}",
                         color=GREEN, font_size=22),
                MathTex(rf"\pi^2/6 - S_N = {gap:.5f}",
                         color=RED, font_size=22),
                MathTex(r"\text{gap} \sim 1/N",
                         color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(N_tr.animate.set_value(N_max),
                   run_time=10, rate_func=linear)
        self.wait(0.4)
