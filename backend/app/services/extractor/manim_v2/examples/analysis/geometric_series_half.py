from manim import *
import numpy as np


class GeometricSeriesHalfExample(Scene):
    """
    Σ 1/2^k = 1 visualized on a unit interval via nested halvings.

    SINGLE_FOCUS:
      Unit interval [0, 1] with tick marks at the partial sums
      S_n = 1 - 1/2^n (n = 1, 2, ...). ValueTracker n_tr steps n → ∞;
      always_redraw adds a GREEN segment [0, S_n] filling the unit
      bar and a red cursor at 1. Live partial sum and gap = 1/2^n.
    """

    def construct(self):
        title = Tex(r"Geometric series: $\sum_{k=1}^{\infty} \tfrac{1}{2^k} = 1$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Unit bar
        bar_left = np.array([-5.0, 0.0, 0])
        bar_right = np.array([5.0, 0.0, 0])
        bar_len = bar_right[0] - bar_left[0]

        bar = Line(bar_left, bar_right, color=WHITE, stroke_width=4)
        tick_0 = Tex(r"$0$", font_size=24).next_to(bar_left, DOWN, buff=0.2)
        tick_1 = Tex(r"$1$", font_size=24).next_to(bar_right, DOWN, buff=0.2)
        self.play(Create(bar), Write(tick_0), Write(tick_1))

        n_tr = ValueTracker(1.0)

        def partial_sum():
            n = n_tr.get_value()
            return 1.0 - 2.0 ** (-n)

        def filled_bar():
            s = partial_sum()
            w = bar_len * s
            return Rectangle(width=w, height=0.35, color=GREEN,
                              fill_opacity=0.55, stroke_width=0
                              ).move_to(bar_left + np.array([w / 2, 0, 0]))

        def ticks_grp():
            n = int(np.floor(n_tr.get_value()))
            grp = VGroup()
            s = 0.0
            for k in range(1, n + 1):
                s += 0.5 ** k
                p = bar_left + np.array([bar_len * s, 0, 0])
                grp.add(Line(p + UP * 0.22, p + DOWN * 0.22,
                              color=YELLOW, stroke_width=2))
                lbl = MathTex(rf"S_{{{k}}}", font_size=16, color=YELLOW)
                lbl.next_to(p, UP, buff=0.08)
                grp.add(lbl)
            return grp

        self.add(always_redraw(filled_bar), always_redraw(ticks_grp))

        def info():
            n_val = n_tr.get_value()
            n_int = int(round(n_val))
            S = 1.0 - 2.0 ** (-n_val)
            gap = 1.0 - S
            return VGroup(
                MathTex(rf"n = {n_int}", color=WHITE, font_size=26),
                MathTex(rf"S_n = 1 - \tfrac{{1}}{{2^n}} = {S:.6f}",
                         color=GREEN, font_size=26),
                MathTex(rf"1 - S_n = \tfrac{{1}}{{2^n}} = {gap:.2e}",
                         color=RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -2.4, 0])

        self.add(always_redraw(info))

        self.play(n_tr.animate.set_value(15), run_time=8, rate_func=linear)
        self.wait(0.5)
