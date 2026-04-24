from manim import *
import numpy as np


class LawOfTotalExpectationExample(Scene):
    """
    E[X] = E[E[X|Y]] visualized with a mixture model:
      Y ∈ {1, 2, 3} with prior p_Y (4/10, 3/10, 3/10),
      X | Y=k  ~ Normal(μ_k, σ²) with (μ_1, μ_2, μ_3) = (-2, 0.5, 2.5).

    TWO_COLUMN: LEFT axes show 3 conditional densities (color-coded)
    + weighted mixture (yellow). RIGHT shows ValueTracker w_tr interp-
    olating between p_Y and a changed prior; live readout of
    Σ p_k · μ_k (conditional expectation average) and the mixture mean
    via numeric integration — they match.
    """

    def construct(self):
        title = Tex(r"Tower rule: $E[X]=E[E[X\mid Y]]$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-4, 5, 1], y_range=[0, 0.6, 0.2],
                    x_length=6.0, y_length=3.8,
                    axis_config={"include_numbers": True,
                                 "font_size": 18}).shift(LEFT * 2.5 + DOWN * 0.3)
        self.play(Create(axes))

        mus = np.array([-2.0, 0.5, 2.5])
        sigma = 0.7
        p_base = np.array([0.4, 0.3, 0.3])
        p_alt = np.array([0.15, 0.35, 0.5])

        w_tr = ValueTracker(0.0)

        def probs():
            w = w_tr.get_value()
            return (1 - w) * p_base + w * p_alt

        colors = [BLUE, GREEN, RED]

        def density(k):
            def f(x):
                return probs()[k] * np.exp(-0.5 * ((x - mus[k]) / sigma) ** 2) \
                    / (sigma * np.sqrt(2 * PI))
            return f

        def density_curves():
            return VGroup(
                axes.plot(density(0), x_range=[-4, 5], color=colors[0], stroke_width=2),
                axes.plot(density(1), x_range=[-4, 5], color=colors[1], stroke_width=2),
                axes.plot(density(2), x_range=[-4, 5], color=colors[2], stroke_width=2),
            )

        def mixture_curve():
            def f(x):
                return sum(density(k)(x) for k in range(3))
            return axes.plot(f, x_range=[-4, 5], color=YELLOW, stroke_width=4)

        self.add(always_redraw(density_curves), always_redraw(mixture_curve))

        # Vertical lines at conditional means with updating labels
        def vlines():
            p = probs()
            grp = VGroup()
            for k in range(3):
                h = p[k] / (sigma * np.sqrt(2 * PI))
                grp.add(DashedLine(axes.c2p(mus[k], 0),
                                   axes.c2p(mus[k], h),
                                   color=colors[k], stroke_width=1.5))
            return grp
        self.add(always_redraw(vlines))

        def mu_mix():
            p = probs()
            return float(np.dot(p, mus))

        info = VGroup(
            Tex(r"$Y\in\{1,2,3\}$, $X|Y=k\sim \mathcal{N}(\mu_k,\sigma^2)$",
                font_size=22),
            Tex(r"$\mu_1=-2,\ \mu_2=0.5,\ \mu_3=2.5$", font_size=22),
            VGroup(Tex(r"$p_1=$", color=BLUE, font_size=22),
                   DecimalNumber(0.4, num_decimal_places=2,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$p_2=$", color=GREEN, font_size=22),
                   DecimalNumber(0.3, num_decimal_places=2,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$p_3=$", color=RED, font_size=22),
                   DecimalNumber(0.3, num_decimal_places=2,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$E[X]=\sum p_k\mu_k=$", color=YELLOW, font_size=22),
                   DecimalNumber(float(np.dot(p_base, mus)), num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)
                   ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)

        info[2][1].add_updater(lambda m: m.set_value(probs()[0]))
        info[3][1].add_updater(lambda m: m.set_value(probs()[1]))
        info[4][1].add_updater(lambda m: m.set_value(probs()[2]))
        info[5][1].add_updater(lambda m: m.set_value(mu_mix()))
        self.add(info)

        self.play(w_tr.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(w_tr.animate.set_value(0.0), run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(w_tr.animate.set_value(0.6), run_time=2, rate_func=smooth)
        self.wait(0.8)
