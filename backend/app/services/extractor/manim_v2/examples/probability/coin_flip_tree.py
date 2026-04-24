from manim import *
import numpy as np
from math import comb


class CoinFlipTreeExample(Scene):
    """
    Binary tree of coin-flip outcomes: depth n has 2^n leaves, with
    C(n, k) leaves showing k heads. The brick-row visualization
    from _2018/eop/chapter1.

    SINGLE_FOCUS:
      ValueTracker depth_tr steps n = 1 → 6. Tree grows via
      always_redraw with each level showing 2^n leaves split into
      k-heads buckets; bricks wide-to-narrow as k varies; sum C(n,k)·
      (1/2)^n = 1.
    """

    def construct(self):
        title = Tex(r"Coin flips: $\binom{n}{k} 2^{-n}$ brick row",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        depth_tr = ValueTracker(1)

        bar_y = -2.0
        total_width = 10.0
        bar_height = 0.6

        def bricks():
            n = int(round(depth_tr.get_value()))
            n = max(1, min(n, 6))
            grp = VGroup()
            total = 2 ** n
            # Compute C(n, k) normalized
            counts = [comb(n, k) for k in range(n + 1)]
            x_cursor = -total_width / 2
            for k, c in enumerate(counts):
                w = total_width * c / total
                b = Rectangle(width=w, height=bar_height,
                               color=BLUE, fill_opacity=0.6,
                               stroke_width=1.5)
                b.move_to([x_cursor + w / 2, bar_y, 0])
                grp.add(b)
                # Count label
                lbl = MathTex(rf"\binom{{{n}}}{{{k}}}={c}",
                                font_size=14, color=WHITE)
                lbl.move_to([x_cursor + w / 2, bar_y, 0])
                grp.add(lbl)
                x_cursor += w
            return grp

        self.add(always_redraw(bricks))

        # Dotted tree above: show depth-n binary tree
        def tree():
            n = int(round(depth_tr.get_value()))
            n = max(1, min(n, 6))
            grp = VGroup()
            # Each level
            for lvl in range(n + 1):
                num_nodes = 2 ** lvl
                for i in range(num_nodes):
                    x = total_width * (i + 0.5) / num_nodes - total_width / 2
                    y = 2.2 - lvl * 0.6
                    grp.add(Dot([x, y, 0], color=YELLOW,
                                  radius=0.04 + 0.02 / max(1, lvl)))
                # connect to next level
                if lvl < n:
                    for i in range(num_nodes):
                        x = total_width * (i + 0.5) / num_nodes - total_width / 2
                        y = 2.2 - lvl * 0.6
                        x_l = total_width * (2 * i + 0.5) / (2 * num_nodes) - total_width / 2
                        x_r = total_width * (2 * i + 1.5) / (2 * num_nodes) - total_width / 2
                        y_next = 2.2 - (lvl + 1) * 0.6
                        grp.add(Line([x, y, 0], [x_l, y_next, 0],
                                       color=GREY_B, stroke_width=1))
                        grp.add(Line([x, y, 0], [x_r, y_next, 0],
                                       color=GREY_B, stroke_width=1))
            return grp

        self.add(always_redraw(tree))

        def info():
            n = int(round(depth_tr.get_value()))
            n = max(1, min(n, 6))
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=26),
                MathTex(rf"2^n = {2 ** n}",
                         color=WHITE, font_size=22),
                MathTex(r"\sum_{k=0}^{n}\tbinom{n}{k} 2^{-n} = 1",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        self.add(always_redraw(info))

        for target in [2, 3, 4, 5, 6]:
            self.play(depth_tr.animate.set_value(target),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
