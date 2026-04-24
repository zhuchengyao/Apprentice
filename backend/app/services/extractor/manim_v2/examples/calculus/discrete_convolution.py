from manim import *
import numpy as np


class DiscreteConvolutionExample(Scene):
    """
    Discrete convolution (from _2022/convolutions/discrete): (x * h)[n] =
    Σ x[k] h[n-k]. Visualize with x = [1, 2, 3, 2, 1] (wave) and
    h = [1, 1, 1] (moving-average kernel). Output is a longer sequence.

    SINGLE_FOCUS:
      Three stem plots stacked: x[n] fixed, flipped-and-shifted
      h[n-k] driven by ValueTracker n_tr, and cumulative output
      y[n] growing as n sweeps.
    """

    def construct(self):
        title = Tex(r"Discrete convolution: $y[n] = \sum_k x[k]\,h[n-k]$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        x_vals = [1, 2, 3, 2, 1]
        h_vals = [1, 1, 1]
        y_vals = list(np.convolve(x_vals, h_vals))  # length 5+3-1=7

        ax_x = Axes(x_range=[-1, 8, 1], y_range=[0, 4, 1],
                     x_length=9, y_length=1.5, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([0, 2.2, 0])
        ax_h = Axes(x_range=[-1, 8, 1], y_range=[0, 2, 1],
                     x_length=9, y_length=1.4, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([0, 0.3, 0])
        ax_y = Axes(x_range=[-1, 8, 1], y_range=[0, 7, 2],
                     x_length=9, y_length=1.8, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([0, -1.9, 0])

        x_lbl = MathTex(r"x[k]", color=BLUE, font_size=20
                          ).next_to(ax_x, LEFT, buff=0.1)
        h_lbl = MathTex(r"h[n-k]", color=ORANGE, font_size=20
                          ).next_to(ax_h, LEFT, buff=0.1)
        y_lbl = MathTex(r"y[n]", color=GREEN, font_size=20
                          ).next_to(ax_y, LEFT, buff=0.1)
        self.play(Create(ax_x), Create(ax_h), Create(ax_y),
                   Write(x_lbl), Write(h_lbl), Write(y_lbl))

        # Fixed x stems
        x_stems = VGroup()
        for k, v in enumerate(x_vals):
            x_stems.add(Line(ax_x.c2p(k, 0), ax_x.c2p(k, v),
                                color=BLUE, stroke_width=3))
            x_stems.add(Dot(ax_x.c2p(k, v), color=BLUE, radius=0.08))
        self.play(FadeIn(x_stems))

        n_tr = ValueTracker(0)

        def h_stems():
            n = n_tr.get_value()
            grp = VGroup()
            # h[n-k] means h reversed and shifted to center at n
            # Indices where h_vals[n-k] is defined: k in [n-len(h)+1, n]
            for k in range(len(h_vals)):
                # At shift n, h[n-k] gets index k in h_vals (reversed)
                idx = len(h_vals) - 1 - k
                hv = h_vals[idx]
                kpos = n - (len(h_vals) - 1) + k  # k position
                grp.add(Line(ax_h.c2p(kpos, 0), ax_h.c2p(kpos, hv),
                               color=ORANGE, stroke_width=3))
                grp.add(Dot(ax_h.c2p(kpos, hv),
                              color=ORANGE, radius=0.08))
            return grp

        def y_stems():
            n_cur = int(round(n_tr.get_value()))
            grp = VGroup()
            for i in range(min(n_cur + 1, len(y_vals))):
                v = y_vals[i]
                grp.add(Line(ax_y.c2p(i, 0), ax_y.c2p(i, v),
                               color=GREEN, stroke_width=3))
                grp.add(Dot(ax_y.c2p(i, v), color=GREEN, radius=0.08))
                grp.add(MathTex(rf"{v}", font_size=16, color=WHITE
                                  ).next_to(ax_y.c2p(i, v), UP, buff=0.05))
            return grp

        self.add(always_redraw(h_stems), always_redraw(y_stems))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(0, min(n, len(y_vals) - 1))
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=24),
                MathTex(rf"y[{n}] = {y_vals[n]}",
                         color=GREEN, font_size=22),
                Tex(r"$x = [1,2,3,2,1]$", color=BLUE, font_size=18),
                Tex(r"$h = [1,1,1]$", color=ORANGE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 2.5)

        self.add(always_redraw(info))

        self.play(n_tr.animate.set_value(len(y_vals) - 1),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
