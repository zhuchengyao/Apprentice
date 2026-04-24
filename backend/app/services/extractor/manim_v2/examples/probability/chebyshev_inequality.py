from manim import *
import numpy as np


class ChebyshevInequalityExample(Scene):
    """
    Chebyshev's inequality: P(|X − μ| ≥ k σ) ≤ 1/k².

    For X ~ Normal(0, 1) and k = 1, 2, 3, 4, 5:
      actual tail: 0.3173, 0.0455, 0.00270, 6.3e-5, 5.7e-7
      Chebyshev:     1,      0.25,   0.1111,   0.0625,  0.04

    TWO_COLUMN: LEFT axes show normal density + shaded |X|≥kσ tail.
    ValueTracker k_tr sweeps 1→5. always_redraw shaded region. RIGHT
    shows live empirical tail, Chebyshev bound, gap.
    """

    def construct(self):
        title = Tex(r"Chebyshev: $P(|X-\mu|\ge k\sigma)\le 1/k^2$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-5, 5, 1], y_range=[0, 0.5, 0.1],
                    x_length=6.5, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.0 + DOWN * 0.2)
        self.play(Create(axes))

        pdf = axes.plot(lambda x: float(np.exp(-x * x / 2) / np.sqrt(TAU)),
                        x_range=[-5, 5], color=BLUE, stroke_width=3)
        self.play(Create(pdf))

        k_tr = ValueTracker(1.0)

        def tail_region():
            k = k_tr.get_value()
            xs_l = np.linspace(-5, -k, 40)
            xs_r = np.linspace(k, 5, 40)
            grp = VGroup()
            for xs in [xs_l, xs_r]:
                pts_top = [axes.c2p(x, float(np.exp(-x * x / 2) / np.sqrt(TAU))) for x in xs]
                pts_bot = [axes.c2p(x, 0) for x in xs]
                poly = Polygon(*pts_top, *reversed(pts_bot),
                               color=YELLOW, stroke_width=0,
                               fill_color=YELLOW, fill_opacity=0.55)
                grp.add(poly)
            return grp

        self.add(always_redraw(tail_region))

        def k_line():
            k = k_tr.get_value()
            return VGroup(
                DashedLine(axes.c2p(-k, 0), axes.c2p(-k, 0.45),
                           color=ORANGE, stroke_width=2),
                DashedLine(axes.c2p(k, 0), axes.c2p(k, 0.45),
                           color=ORANGE, stroke_width=2),
            )
        self.add(always_redraw(k_line))

        # Normal CDF via scipy
        def tail_prob():
            from scipy.stats import norm as sp_norm
            k = k_tr.get_value()
            return 2 * float(sp_norm.sf(k))

        def cheb_bound():
            k = k_tr.get_value()
            return min(1.0, 1 / (k * k))

        info = VGroup(
            VGroup(Tex(r"$k=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=2,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"actual tail $=$", font_size=22),
                   DecimalNumber(0.317, num_decimal_places=5,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"Chebyshev $1/k^2=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=5,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"gap $=$", font_size=22),
                   DecimalNumber(0.683, num_decimal_places=5,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"actual $\le 1/k^2$ always",
                color=GREEN, font_size=20),
            Tex(r"tight only for specific distributions",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(k_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(tail_prob()))
        info[2][1].add_updater(lambda m: m.set_value(cheb_bound()))
        info[3][1].add_updater(lambda m: m.set_value(cheb_bound() - tail_prob()))
        self.add(info)

        self.play(k_tr.animate.set_value(5.0),
                  run_time=5, rate_func=linear)
        self.wait(0.5)
        self.play(k_tr.animate.set_value(1.5),
                  run_time=2, rate_func=smooth)
        self.wait(0.5)
