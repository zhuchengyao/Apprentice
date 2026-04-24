from manim import *
import numpy as np


class DiceUncertaintyExample(Scene):
    """
    Empirical histogram of dice-roll sums (from _2018/eop/chapter1/
    show_uncertainty_dice): N independent rolls of the sum of 3
    dice; as N grows the histogram sharpens toward the true
    distribution (triangular-ish for 3d6).

    SINGLE_FOCUS:
      Histogram of empirical sums vs theoretical PMF. ValueTracker
      n_tr grows the sample count 10 → 3000; always_redraw BLUE
      empirical bars + YELLOW theoretical overlay.
    """

    def construct(self):
        title = Tex(r"3d6: empirical sum histogram $\to$ theoretical PMF",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Precompute 3000 rolls
        rng = np.random.default_rng(21)
        N_total = 3000
        rolls = rng.integers(1, 7, size=(N_total, 3))
        sums = rolls.sum(axis=1)  # sums in [3, 18]

        # True PMF of 3d6
        from math import comb
        pmf = {}
        for s_val in range(3, 19):
            cnt = 0
            for a in range(1, 7):
                for b in range(1, 7):
                    for c in range(1, 7):
                        if a + b + c == s_val:
                            cnt += 1
            pmf[s_val] = cnt / 216

        ax = Axes(x_range=[2, 19, 2], y_range=[0, 0.18, 0.03],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.3, -0.5, 0])
        xlbl = Tex("sum of 3 dice", font_size=18).next_to(ax, DOWN, buff=0.15)
        ylbl = Tex("frequency", font_size=18).next_to(ax, LEFT, buff=0.15)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        # Theoretical bars (static, YELLOW outlines)
        theor = VGroup()
        bar_w = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        for s_val in range(3, 19):
            h_scene = ax.c2p(0, pmf[s_val])[1] - ax.c2p(0, 0)[1]
            bar = Rectangle(width=bar_w * 0.9, height=max(h_scene, 0.01),
                             color=YELLOW, fill_opacity=0.25,
                             stroke_width=1.5, stroke_color=YELLOW)
            bar.move_to([ax.c2p(s_val, pmf[s_val] / 2)[0],
                         ax.c2p(0, 0)[1] + h_scene / 2, 0])
            theor.add(bar)
        self.play(Create(theor))

        n_tr = ValueTracker(10)

        def empirical_bars():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, N_total))
            counts = {s_val: 0 for s_val in range(3, 19)}
            for k in range(n):
                counts[int(sums[k])] += 1
            grp = VGroup()
            for s_val in range(3, 19):
                freq = counts[s_val] / n
                h_scene = ax.c2p(0, freq)[1] - ax.c2p(0, 0)[1]
                if h_scene < 0.005:
                    continue
                bar = Rectangle(width=bar_w * 0.6, height=h_scene,
                                 color=BLUE, fill_opacity=0.75,
                                 stroke_width=0)
                bar.move_to([ax.c2p(s_val, freq / 2)[0],
                             ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        self.add(always_redraw(empirical_bars))

        def info():
            n = int(round(n_tr.get_value()))
            return VGroup(
                MathTex(rf"N = {n}", color=WHITE, font_size=26),
                MathTex(r"\text{BLUE}: \text{empirical}",
                         color=BLUE, font_size=20),
                MathTex(r"\text{YELLOW}: \text{theory } \tfrac{\#}{216}",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(n_tr.animate.set_value(N_total),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
