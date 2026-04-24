from manim import *
import numpy as np


class CollatzConjectureExample(Scene):
    """
    Collatz (3n+1) conjecture: for any positive integer n, iterating
    n → n/2 (if even), n → 3n+1 (if odd) reaches 1. Unproven in
    general but verified to very large n.

    SINGLE_FOCUS: 5 starting values {27, 97, 871, 27, 12}. Each path
    plotted in a different color. ValueTracker idx_tr reveals them
    sequentially.
    """

    def construct(self):
        title = Tex(r"Collatz conjecture: $n\to n/2$ or $3n+1$ always reaches 1",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def collatz(n):
            seq = [n]
            while seq[-1] != 1 and len(seq) < 500:
                n = seq[-1]
                if n % 2 == 0:
                    seq.append(n // 2)
                else:
                    seq.append(3 * n + 1)
            return seq

        starts = [27, 97, 871, 41, 12]
        colors = [BLUE, GREEN, ORANGE, PURPLE, RED]
        paths = [collatz(s) for s in starts]

        max_val = max(max(p) for p in paths)
        max_len = max(len(p) for p in paths)

        axes = Axes(x_range=[0, max_len + 10, 30], y_range=[0, max_val * 1.05, max_val // 4],
                    x_length=9, y_length=4.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 14}).shift(DOWN * 0.3)
        self.play(Create(axes))

        idx_tr = ValueTracker(0.0)
        t_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(len(starts) - 1, int(round(idx_tr.get_value()))))

        def path_display():
            k = k_now()
            grp = VGroup()
            for i in range(k + 1):
                col = colors[i]
                p = paths[i]
                # Use t_tr only for current path; past paths fully drawn
                if i < k:
                    end = len(p)
                else:
                    end = max(2, int(t_tr.get_value() * len(p)))
                pts = [axes.c2p(j, p[j]) for j in range(end)]
                if len(pts) >= 2:
                    grp.add(VMobject().set_points_as_corners(pts)
                             .set_color(col).set_stroke(width=3))
            return grp

        self.add(always_redraw(path_display))

        # Info
        info = VGroup(
            VGroup(Tex(r"start $n_0=$", font_size=22),
                   DecimalNumber(27, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"steps to 1 $=$", font_size=22),
                   DecimalNumber(111, num_decimal_places=0,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"max reached $=$", font_size=22),
                   DecimalNumber(9232, num_decimal_places=0,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(starts[k_now()]))
        info[1][1].add_updater(lambda m: m.set_value(len(paths[k_now()]) - 1))
        info[2][1].add_updater(lambda m: m.set_value(max(paths[k_now()])))
        self.add(info)

        for k in range(len(starts)):
            self.play(idx_tr.animate.set_value(float(k)),
                      t_tr.animate.set_value(0.0),
                      run_time=0.3)
            self.play(t_tr.animate.set_value(1.0),
                      run_time=2.0, rate_func=linear)
            self.wait(0.4)
        self.wait(0.5)
