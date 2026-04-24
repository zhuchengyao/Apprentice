from manim import *
import numpy as np


class LawOfLargeNumbersCoinExample(Scene):
    """
    Law of Large Numbers for coin flips: empirical fraction of heads
    → 0.5 as N → ∞. Adapted from law_of_large_numbers reference.

    TWO_COLUMN:
      LEFT  — axes with running-mean curve for N=1..800 flips;
              always_redraw; dashed line at 0.5.
      RIGHT — histogram of results + current N, p_hat.
    """

    def construct(self):
        title = Tex(r"Law of Large Numbers: $\hat p_N \to 0.5$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N_MAX = 800
        rng = np.random.default_rng(111)
        flips = (rng.random(N_MAX) < 0.5).astype(int)
        cum = np.cumsum(flips)

        ax = Axes(x_range=[0, N_MAX, N_MAX // 4],
                   y_range=[0, 1, 0.25],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.8, -0.3, 0])
        xlbl = MathTex(r"N", font_size=20).next_to(ax, DOWN, buff=0.1)
        ylbl = MathTex(r"\hat p_N", font_size=20).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xlbl), Write(ylbl))

        target_line = DashedLine(ax.c2p(0, 0.5), ax.c2p(N_MAX, 0.5),
                                   color=YELLOW, stroke_width=2)
        target_lbl = MathTex(r"p = 0.5",
                               color=YELLOW, font_size=20
                               ).next_to(ax.c2p(N_MAX, 0.5), UR, buff=0.1)
        self.play(Create(target_line), Write(target_lbl))

        N_tr = ValueTracker(1)

        def running_mean():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, N_MAX))
            pts = [ax.c2p(n + 1, cum[n] / (n + 1)) for n in range(N)]
            m = VMobject(color=BLUE, stroke_width=2.5)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def rider():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, N_MAX))
            return Dot(ax.c2p(N, cum[N - 1] / N),
                        color=RED, radius=0.1)

        self.add(always_redraw(running_mean), always_redraw(rider))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, N_MAX))
            heads = int(cum[N - 1])
            tails = N - heads
            p_hat = heads / N
            # Confidence: ±1.96·√(p(1-p)/N)
            ci = 1.96 * np.sqrt(p_hat * (1 - p_hat) / N)
            return VGroup(
                MathTex(rf"N = {N}", color=WHITE, font_size=24),
                MathTex(rf"\text{{heads}} = {heads}",
                         color=BLUE, font_size=22),
                MathTex(rf"\text{{tails}} = {tails}",
                         color=RED, font_size=22),
                MathTex(rf"\hat p_N = {p_hat:.4f}",
                         color=GREEN, font_size=24),
                MathTex(rf"\pm 1.96\,\sqrt{{\hat p (1-\hat p)/N}} = \pm {ci:.3f}",
                         color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.3, 0.0, 0])

        self.add(always_redraw(info))

        self.play(N_tr.animate.set_value(N_MAX),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
