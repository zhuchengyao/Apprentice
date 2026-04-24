from manim import *
import numpy as np


class OrderStatisticsExample(Scene):
    """
    Order statistics: X_(1) ≤ ... ≤ X_(n) from n iid uniform(0, 1).
    Density of X_(k) is Beta(k, n-k+1): f = n! / ((k-1)!(n-k)!) ·
    x^(k-1) (1-x)^(n-k).

    TWO_COLUMN: LEFT plots all n=10 order-statistic densities.
    ValueTracker k_tr selects k; always_redraw highlights current
    density with peak at (k-1)/(n-1). RIGHT has formula + mean k/(n+1).
    """

    def construct(self):
        title = Tex(r"Order statistics: $X_{(k)}\sim\mathrm{Beta}(k,n-k+1)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 10
        axes = Axes(x_range=[0, 1, 0.2], y_range=[0, 4.5, 1],
                    x_length=6.5, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(axes))

        from math import factorial
        def density(x, k):
            return (factorial(n) / (factorial(k - 1) * factorial(n - k))
                    * x ** (k - 1) * (1 - x) ** (n - k))

        # Draw all densities
        all_curves = VGroup()
        for k in range(1, n + 1):
            col = interpolate_color(BLUE, RED, (k - 1) / (n - 1))
            all_curves.add(axes.plot(lambda x, kk=k: float(density(x, kk)),
                                      x_range=[0.01, 0.99],
                                      color=col, stroke_width=1.5,
                                      stroke_opacity=0.5))
        self.add(all_curves)

        k_tr = ValueTracker(1.0)

        def k_now():
            return max(1, min(n, int(round(k_tr.get_value()))))

        def hilite_curve():
            k = k_now()
            col = interpolate_color(BLUE, RED, (k - 1) / (n - 1))
            return axes.plot(lambda x: float(density(x, k)),
                             x_range=[0.01, 0.99],
                             color=col, stroke_width=4)

        def peak_dot():
            k = k_now()
            if k == 1 or k == n:
                return VMobject()
            peak = (k - 1) / (n - 1)
            col = interpolate_color(BLUE, RED, (k - 1) / (n - 1))
            return Dot(axes.c2p(peak, density(peak, k)),
                        color=col, radius=0.1)

        self.add(always_redraw(hilite_curve), always_redraw(peak_dot))

        info = VGroup(
            Tex(rf"$n={n}$ iid Uniform(0, 1)", font_size=22),
            VGroup(Tex(r"$k=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"mean $k/(n+1)=$", font_size=22),
                   DecimalNumber(1 / 11, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"mode $(k-1)/(n-1)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"$k=1$: minimum, $k=n$: maximum",
                color=GREY_B, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[1][1].add_updater(lambda m: m.set_value(k_now()))
        info[2][1].add_updater(lambda m: m.set_value(k_now() / (n + 1)))
        info[3][1].add_updater(lambda m: m.set_value((k_now() - 1) / (n - 1)))
        self.add(info)

        for k in range(2, n + 1):
            self.play(k_tr.animate.set_value(float(k)),
                      run_time=0.7, rate_func=smooth)
            self.wait(0.25)
        self.wait(0.8)
