from manim import *
import numpy as np
from math import comb


class BrickRowHistogramExample(Scene):
    """
    Morph brick-row to histogram (from _2018/eop/chapter1/
    morph_brick_row_into_histogram): the C(n, k) bricks of width
    proportional to count sort into a vertical histogram showing
    the binomial distribution.

    SINGLE_FOCUS:
      n = 10 bricks for C(10, k). ValueTracker morph_tr interpolates
      from horizontal brick row (all same height, different widths)
      to vertical histogram (all same width, heights proportional to
      C(10, k)).
    """

    def construct(self):
        title = Tex(r"Brick row $\to$ histogram: $\binom{10}{k}$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 10
        counts = [comb(n, k) for k in range(n + 1)]
        total = sum(counts)  # 2^n = 1024

        morph_tr = ValueTracker(0.0)

        total_width = 11.0
        brick_height = 0.6
        hist_width = 0.9
        brick_y = -2.2

        def bricks():
            s = morph_tr.get_value()
            grp = VGroup()
            x_cursor = -total_width / 2
            # For hist target: evenly spaced, centered
            hist_total_width = (n + 1) * (hist_width + 0.05)
            hist_start = -hist_total_width / 2
            for k, c in enumerate(counts):
                # Horizontal (s=0): width ∝ c, centered in row at brick_y
                w_h = total_width * c / total
                y_h = brick_y
                # Vertical (s=1): width = hist_width, height ∝ c
                h_v = brick_height * 5.0 * c / max(counts)
                x_v = hist_start + (k + 0.5) * (hist_width + 0.05)
                y_v = brick_y + h_v / 2

                # Horizontal rect-center (s=0)
                x_h = x_cursor + w_h / 2
                x_cursor += w_h

                # Interpolate width, height, position
                w = (1 - s) * w_h + s * hist_width
                h = (1 - s) * brick_height + s * h_v
                x = (1 - s) * x_h + s * x_v
                y = (1 - s) * y_h + s * y_v

                bar = Rectangle(width=w, height=h,
                                 color=BLUE, fill_opacity=0.6,
                                 stroke_width=1)
                bar.move_to([x, y, 0])
                grp.add(bar)

                # Count label
                if s < 0.3:
                    lbl = MathTex(rf"{c}", font_size=14, color=WHITE)
                    lbl.move_to([x, y, 0])
                    grp.add(lbl)
            return grp

        self.add(always_redraw(bricks))

        def x_axis_labels():
            s = morph_tr.get_value()
            if s < 0.5:
                return VGroup()
            hist_total_width = (n + 1) * (hist_width + 0.05)
            hist_start = -hist_total_width / 2
            grp = VGroup()
            for k in range(n + 1):
                x = hist_start + (k + 0.5) * (hist_width + 0.05)
                lbl = MathTex(rf"{k}", font_size=18,
                                color=WHITE).move_to([x, brick_y - 0.3, 0])
                grp.add(lbl)
            return grp

        self.add(always_redraw(x_axis_labels))

        def info():
            s = morph_tr.get_value()
            return VGroup(
                MathTex(rf"n = {n},\ 2^n = {2 ** n}",
                         color=WHITE, font_size=22),
                MathTex(rf"\text{{morph}}: {s:.2f}",
                         color=YELLOW, font_size=22),
                MathTex(r"\sum_{k} \binom{n}{k} = 2^n",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 1.8)

        self.add(always_redraw(info))

        self.play(morph_tr.animate.set_value(1.0),
                   run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(morph_tr.animate.set_value(0.0),
                   run_time=3, rate_func=smooth)
        self.wait(0.4)
