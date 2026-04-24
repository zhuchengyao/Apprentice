from manim import *
import numpy as np


class SumTwoDiceExample(Scene):
    """
    Sum of 2d6: the classic triangular PMF peaked at 7. Empirical
    histogram converges to the PMF as trials grow.

    SINGLE_FOCUS:
      YELLOW theoretical triangle PMF overlay + BLUE empirical bars
      for sums 2..12. ValueTracker N_tr grows 0 → 2000 trials.
      Two dice sprites show current roll.
    """

    def construct(self):
        title = Tex(r"Sum of 2d6: triangular PMF $\to$ empirical",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Theoretical PMF
        counts_th = [0, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]  # index = sum, 2..12
        pmf = {s: counts_th[s] / 36 for s in range(2, 13)}

        # Precompute
        rng = np.random.default_rng(99)
        N_MAX = 2000
        d1 = rng.integers(1, 7, size=N_MAX)
        d2 = rng.integers(1, 7, size=N_MAX)
        sums_trial = d1 + d2

        ax = Axes(x_range=[1, 13, 1], y_range=[0, 0.2, 0.05],
                   x_length=9, y_length=4, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.8, 0])
        xlbl = Tex("sum", font_size=18).next_to(ax, DOWN, buff=0.1)
        ylbl = Tex("frequency", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        # Theoretical bars
        theor = VGroup()
        bar_w = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        for s in range(2, 13):
            h_scene = ax.c2p(0, pmf[s])[1] - ax.c2p(0, 0)[1]
            bar = Rectangle(width=bar_w * 0.9, height=h_scene,
                             color=YELLOW, fill_opacity=0.25,
                             stroke_width=1.5, stroke_color=YELLOW)
            bar.move_to([ax.c2p(s, 0)[0],
                         ax.c2p(0, 0)[1] + h_scene / 2, 0])
            theor.add(bar)
        self.play(Create(theor))

        N_tr = ValueTracker(0)

        def empirical_bars():
            n = int(round(N_tr.get_value()))
            n = max(0, min(n, N_MAX))
            counts = {s: 0 for s in range(2, 13)}
            for k in range(n):
                counts[int(sums_trial[k])] += 1
            grp = VGroup()
            for s in range(2, 13):
                if n == 0:
                    continue
                freq = counts[s] / n
                h_scene = ax.c2p(0, freq)[1] - ax.c2p(0, 0)[1]
                if h_scene < 0.003:
                    continue
                bar = Rectangle(width=bar_w * 0.5, height=h_scene,
                                 color=BLUE, fill_opacity=0.75,
                                 stroke_width=0)
                bar.move_to([ax.c2p(s, 0)[0],
                             ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        self.add(always_redraw(empirical_bars))

        # Dice sprites
        def dice_sprites():
            n = int(round(N_tr.get_value()))
            if n == 0:
                return VGroup()
            idx = min(n - 1, N_MAX - 1)
            a, b = int(d1[idx]), int(d2[idx])
            grp = VGroup()
            for i, val in enumerate([a, b]):
                x = -2 + i * 1.5
                sq = Square(side_length=0.8, color=WHITE,
                              fill_opacity=0.2, stroke_width=2
                              ).move_to([x, 2.3, 0])
                lbl = MathTex(str(val), font_size=30,
                                color=RED).move_to(sq.get_center())
                grp.add(sq, lbl)
            return grp

        self.add(always_redraw(dice_sprites))

        def info():
            n = int(round(N_tr.get_value()))
            n = max(1, min(n, N_MAX))
            avg = float(np.mean(sums_trial[:n]))
            return VGroup(
                MathTex(rf"N = {n}", color=WHITE, font_size=22),
                MathTex(rf"\text{{mean}} = {avg:.3f}",
                         color=BLUE, font_size=22),
                MathTex(r"\text{true mean} = 7", color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 1.5)

        self.add(always_redraw(info))

        self.play(N_tr.animate.set_value(N_MAX),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
