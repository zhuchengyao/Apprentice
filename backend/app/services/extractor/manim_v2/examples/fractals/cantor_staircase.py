from manim import *
import numpy as np


class CantorStaircaseExample(Scene):
    """
    Cantor's devil's staircase: the cumulative distribution of the
    uniform measure on the Cantor set. Continuous, non-decreasing,
    with derivative 0 a.e., yet rises from 0 to 1.

    Construct via iterative "middle third" refinement. Phase k has
    2^k flat plateaus. ValueTracker level_tr steps 1..6; always_redraw
    builds the staircase at that level via piecewise-linear approx.
    """

    def construct(self):
        title = Tex(r"Cantor staircase: continuous, $f'=0$ a.e., rises 0 to 1",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 1, 0.2], y_range=[0, 1, 0.2],
                    x_length=8, y_length=4.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(DOWN * 0.3)
        self.play(Create(axes))

        level_tr = ValueTracker(1.0)

        def stairs():
            L = int(round(level_tr.get_value()))
            L = max(1, min(6, L))
            # At level L, we have 2^L plateaus at heights k/2^L for k=1..2^L-1.
            # Plateaus correspond to intervals removed; generate plateau positions.
            # Alternative: iterate — Cantor function f_L via recursion on level L.
            def cantor_f(x, L):
                if L == 0:
                    return x
                if x <= 1 / 3:
                    return 0.5 * cantor_f(3 * x, L - 1)
                elif x < 2 / 3:
                    return 0.5
                else:
                    return 0.5 + 0.5 * cantor_f(3 * x - 2, L - 1)

            pts = []
            N = 600
            xs = np.linspace(0, 1, N)
            for x in xs:
                pts.append(axes.c2p(x, cantor_f(x, L)))
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=3)

        self.add(always_redraw(stairs))

        # Reference y=x diagonal
        diag = axes.plot(lambda x: x, x_range=[0, 1], color=GREY_B,
                         stroke_width=1.5, stroke_opacity=0.4)
        self.add(diag)

        # Info
        def n_now():
            return max(1, min(6, int(round(level_tr.get_value()))))

        info = VGroup(
            VGroup(Tex(r"level $L=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"plateaus $=2^L-1=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            Tex(r"$f(0)=0,\ f(1)=1$", color=YELLOW, font_size=22),
            Tex(r"Hausdorff dim of Cantor set $=\log 2/\log 3$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(2 ** n_now() - 1))
        self.add(info)

        for L in range(2, 7):
            self.play(level_tr.animate.set_value(float(L)),
                      run_time=1.2, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.8)
