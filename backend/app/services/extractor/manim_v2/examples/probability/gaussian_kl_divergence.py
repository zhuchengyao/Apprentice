from manim import *
import numpy as np


class GaussianKLDivergenceExample(Scene):
    """
    KL divergence between two 1D Gaussians:
        KL(p || q) = log(σ_q/σ_p) + (σ_p² + (μ_p - μ_q)²)/(2σ_q²) - 1/2.

    TWO_COLUMN: LEFT axes with p (BLUE, fixed N(0, 1)) and q (ORANGE,
    varying); ValueTracker mu_tr, sigma_tr tour q's parameters.
    RIGHT live KL value; minimum KL=0 when p=q.
    """

    def construct(self):
        title = Tex(r"$D_{\mathrm{KL}}(p\|q)=\log\tfrac{\sigma_q}{\sigma_p}+\tfrac{\sigma_p^2+(\mu_p-\mu_q)^2}{2\sigma_q^2}-\tfrac12$",
                    font_size=20).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-4, 4, 1], y_range=[0, 0.8, 0.2],
                    x_length=6.0, y_length=3.8,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.3 + DOWN * 0.4)
        self.play(Create(axes))

        # Fixed p
        p_curve = axes.plot(lambda x: np.exp(-x * x / 2) / np.sqrt(TAU),
                             x_range=[-4, 4], color=BLUE, stroke_width=3)
        p_lbl = Tex(r"$p=\mathcal{N}(0,1)$", color=BLUE, font_size=22).next_to(
            axes, UP, buff=0.1).shift(LEFT * 2)
        self.play(Create(p_curve), Write(p_lbl))

        mu_tr = ValueTracker(0.0)
        sigma_tr = ValueTracker(1.0)

        def q_curve():
            mu = mu_tr.get_value()
            sigma = sigma_tr.get_value()
            return axes.plot(
                lambda x: float(np.exp(-(x - mu) ** 2 / (2 * sigma * sigma)) / (sigma * np.sqrt(TAU))),
                x_range=[-4, 4], color=ORANGE, stroke_width=3)

        self.add(always_redraw(q_curve))

        def KL():
            mu_q = mu_tr.get_value()
            sigma_q = sigma_tr.get_value()
            return float(np.log(sigma_q) + (1 + mu_q * mu_q) / (2 * sigma_q * sigma_q) - 0.5)

        info = VGroup(
            VGroup(Tex(r"$\mu_q=$", color=ORANGE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\sigma_q=$", color=ORANGE, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=2,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$D_{\mathrm{KL}}=$", font_size=24),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=24).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$D_{\mathrm{KL}}\ge 0$ (Gibbs)",
                color=GREEN, font_size=22),
            Tex(r"$=0$ iff $p=q$",
                color=GREEN, font_size=20),
            Tex(r"asymmetric: $D(p\|q)\neq D(q\|p)$",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(mu_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(sigma_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(KL()))
        self.add(info)

        tour = [(1.5, 1.0), (0.0, 2.0), (1.0, 0.6), (-1.0, 1.5), (0.0, 1.0)]
        for (mu, sig) in tour:
            self.play(mu_tr.animate.set_value(mu),
                      sigma_tr.animate.set_value(sig),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
