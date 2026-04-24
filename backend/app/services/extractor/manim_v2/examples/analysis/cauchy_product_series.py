from manim import *
import numpy as np


class CauchyProductSeriesExample(Scene):
    """
    Cauchy product: if Σa_n and Σb_n converge absolutely to A and B,
    their Cauchy product Σc_n (c_n = Σ_{k=0}^{n} a_k b_{n-k}) converges
    to AB.

    Example: a_n = 1/n!, b_n = 1/n!. Both Σ = e.
    c_n = Σ 1/(k!(n-k)!) = 2^n/n! so Σc_n = e² as expected.

    TWO_COLUMN: LEFT axes of partial sums S_N^A (BLUE), S_N^B (GREEN),
    S_N^C (YELLOW). RIGHT shows live A, B, AB, C comparison.
    """

    def construct(self):
        title = Tex(r"Cauchy product: $(\sum a_n)(\sum b_n)=\sum c_n$, $c_n=\sum a_k b_{n-k}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 15, 3], y_range=[0, 8, 2],
                    x_length=6.0, y_length=4.2,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(axes))

        from math import factorial
        def a_n(n):
            return 1 / factorial(n)

        def b_n(n):
            return 1 / factorial(n)

        def c_n(n):
            return sum(a_n(k) * b_n(n - k) for k in range(n + 1))

        N_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(15, int(round(N_tr.get_value()))))

        def A_curve():
            grp = VGroup()
            partial = 0.0
            pts = []
            for n in range(k_now() + 1):
                partial += a_n(n)
                pts.append(axes.c2p(n, partial))
            if len(pts) >= 2:
                return VMobject().set_points_as_corners(pts).set_color(BLUE).set_stroke(width=3)
            return VMobject()

        def B_curve():
            partial = 0.0
            pts = []
            for n in range(k_now() + 1):
                partial += b_n(n)
                pts.append(axes.c2p(n, partial))
            if len(pts) >= 2:
                return VMobject().set_points_as_corners(pts).set_color(GREEN).set_stroke(width=3)
            return VMobject()

        def C_curve():
            partial = 0.0
            pts = []
            for n in range(k_now() + 1):
                partial += c_n(n)
                pts.append(axes.c2p(n, partial))
            if len(pts) >= 2:
                return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=3)
            return VMobject()

        self.add(always_redraw(A_curve), always_redraw(B_curve), always_redraw(C_curve))

        # Reference lines
        self.add(DashedLine(axes.c2p(0, np.e), axes.c2p(15, np.e),
                             color=GREY_B, stroke_width=1.5, stroke_opacity=0.5))
        self.add(Tex(r"$e$", color=GREY_B, font_size=20).move_to(
            axes.c2p(14, np.e + 0.3)))
        self.add(DashedLine(axes.c2p(0, np.e * np.e), axes.c2p(15, np.e * np.e),
                             color=ORANGE, stroke_width=1.5, stroke_opacity=0.5))
        self.add(Tex(r"$e^2\approx 7.389$", color=ORANGE, font_size=20).move_to(
            axes.c2p(13, np.e * np.e + 0.3)))

        def A_sum():
            return sum(a_n(n) for n in range(k_now() + 1))

        def B_sum():
            return sum(b_n(n) for n in range(k_now() + 1))

        def C_sum():
            return sum(c_n(n) for n in range(k_now() + 1))

        info = VGroup(
            VGroup(Tex(r"$N=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$S_N^A=\sum 1/n!=$", color=BLUE, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=4,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$S_N^B=$", color=GREEN, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$S_N^C=\sum 2^n/n!=$", color=YELLOW, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=4,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$S_N^A\cdot S_N^B=$", color=ORANGE, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=4,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"$S^C\to e^2$, $S^A\cdot S^B\to e^2$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(k_now()))
        info[1][1].add_updater(lambda m: m.set_value(A_sum()))
        info[2][1].add_updater(lambda m: m.set_value(B_sum()))
        info[3][1].add_updater(lambda m: m.set_value(C_sum()))
        info[4][1].add_updater(lambda m: m.set_value(A_sum() * B_sum()))
        self.add(info)

        self.play(N_tr.animate.set_value(15.0),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
