from manim import *
import numpy as np


class BetaBernoulliConjugateExample(Scene):
    """
    Beta is conjugate prior for Bernoulli: prior Beta(α, β) +
    data k successes in n trials → posterior Beta(α + k, β + n - k).

    TWO_COLUMN: LEFT axes show prior (BLUE, fixed Beta(3, 3)), posterior
    (YELLOW) updated as more data arrives via ValueTracker n_tr.
    """

    def construct(self):
        title = Tex(r"Beta-Bernoulli: posterior $=\mathrm{Beta}(\alpha+k, \beta+n-k)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        np.random.seed(7)
        p_true = 0.3
        N_max = 100
        data = np.random.random(N_max) < p_true  # True = success

        alpha_0, beta_0 = 3.0, 3.0

        axes = Axes(x_range=[0, 1, 0.2], y_range=[0, 10, 2],
                    x_length=6.5, y_length=4.2,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.2 + DOWN * 0.2)
        self.play(Create(axes))

        # Beta PDF
        from math import lgamma
        def beta_pdf(x, a, b):
            if x <= 0 or x >= 1: return 0
            log_num = (a - 1) * np.log(x) + (b - 1) * np.log(1 - x)
            log_beta = lgamma(a) + lgamma(b) - lgamma(a + b)
            return float(np.exp(log_num - log_beta))

        # Prior
        prior_curve = axes.plot(lambda x: beta_pdf(x, alpha_0, beta_0),
                                 x_range=[0.01, 0.99], color=BLUE, stroke_width=2,
                                 stroke_opacity=0.7)
        self.add(prior_curve)
        self.add(Tex(rf"$\mathrm{{Beta}}(3,3)$ prior", color=BLUE,
                     font_size=20).next_to(axes, UP, buff=0.1).shift(LEFT * 2))

        # True p line
        self.add(DashedLine(axes.c2p(p_true, 0), axes.c2p(p_true, 10),
                             color=RED, stroke_width=2))
        self.add(Tex(rf"$p^*={p_true}$", color=RED, font_size=20).next_to(
            axes.c2p(p_true, 10), UP, buff=0.1))

        n_tr = ValueTracker(0.0)

        def n_now():
            return max(0, min(N_max, int(round(n_tr.get_value()))))

        def posterior_params():
            n = n_now()
            k = int(np.sum(data[:n]))
            return alpha_0 + k, beta_0 + n - k, k

        def posterior_curve():
            a, b, k = posterior_params()
            return axes.plot(lambda x: beta_pdf(x, a, b),
                             x_range=[0.01, 0.99],
                             color=YELLOW, stroke_width=4)

        self.add(always_redraw(posterior_curve))

        # Data display
        def data_dots():
            n = n_now()
            grp = VGroup()
            for i in range(min(n, 30)):
                x_pos = data[i]
                col = GREEN if x_pos else ORANGE
                grp.add(Dot(axes.c2p(1 if x_pos else 0, 0.3 + (i % 5) * 0.15),
                             color=col, radius=0.04))
            return grp

        self.add(always_redraw(data_dots))

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$k=$", color=GREEN, font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"posterior $=\mathrm{Beta}($", font_size=22),
                   DecimalNumber(3.0, num_decimal_places=1,
                                 font_size=22).set_color(YELLOW),
                   Tex(",", font_size=22),
                   DecimalNumber(3.0, num_decimal_places=1,
                                 font_size=22).set_color(YELLOW),
                   Tex(r"$)$", font_size=22)
                   ).arrange(RIGHT, buff=0.05),
            VGroup(Tex(r"post. mean $=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[1][1].add_updater(lambda m: m.set_value(posterior_params()[2]))
        info[2][1].add_updater(lambda m: m.set_value(posterior_params()[0]))
        info[2][3].add_updater(lambda m: m.set_value(posterior_params()[1]))
        info[3][1].add_updater(lambda m: m.set_value(
            posterior_params()[0] / (posterior_params()[0] + posterior_params()[1])))
        self.add(info)

        self.play(n_tr.animate.set_value(float(N_max)),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
