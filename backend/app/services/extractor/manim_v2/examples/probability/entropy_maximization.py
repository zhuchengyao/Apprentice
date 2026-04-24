from manim import *
import numpy as np


class EntropyMaximizationExample(Scene):
    """
    Max-entropy distributions:
      - No constraint on [a, b] → uniform
      - Fixed mean on [0, ∞) → exponential
      - Fixed mean + variance on ℝ → Gaussian

    SINGLE_FOCUS axes show a parametric family p_β(x) = e^{-β x²} / Z
    on ℝ; ValueTracker beta_tr drives it. Live H(p_β) = -∫p log p
    evaluated by Riemann sum, compared with analytic
    ½ log(2πe/β) Gaussian entropy. Annotations confirm β=1/2 →
    N(0, 1) → H = ½ log(2πe).
    """

    def construct(self):
        title = Tex(r"Max entropy: fixed mean + variance $\Rightarrow p^*$ is Gaussian",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-5, 5, 1], y_range=[0, 0.9, 0.2],
                    x_length=6.5, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.0 + DOWN * 0.2)
        self.play(Create(axes))

        beta_tr = ValueTracker(0.5)

        def p_of(x, beta):
            Z = np.sqrt(PI / beta)
            return np.exp(-beta * x * x) / Z

        def curve():
            b = beta_tr.get_value()
            return axes.plot(lambda xx: float(p_of(xx, b)),
                             x_range=[-5, 5], color=YELLOW, stroke_width=4)
        self.add(always_redraw(curve))

        # Static Gaussian reference
        ref = axes.plot(lambda xx: float(p_of(xx, 0.5)),
                        x_range=[-5, 5], color=BLUE, stroke_width=2,
                        stroke_opacity=0.35)
        self.play(Create(ref))

        # Numeric entropy
        def H_numeric():
            b = beta_tr.get_value()
            xs = np.linspace(-6, 6, 400)
            p = p_of(xs, b)
            p_clip = np.where(p > 1e-12, p, 1e-12)
            return float(-np.trapezoid(p_clip * np.log(p_clip), xs))

        def H_analytic():
            b = beta_tr.get_value()
            sigma2 = 1 / (2 * b)
            return 0.5 * np.log(2 * PI * np.e * sigma2)

        info = VGroup(
            Tex(r"$p_\beta(x)=e^{-\beta x^2}/Z,\ \sigma^2=\tfrac{1}{2\beta}$",
                font_size=22),
            VGroup(Tex(r"$\beta=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$H$ (numeric) $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\tfrac12\log(2\pi e\sigma^2)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(r"max $H$ at given $\sigma^2$ $\Rightarrow$ Gaussian",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)

        info[1][1].add_updater(lambda m: m.set_value(beta_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(H_numeric()))
        info[3][1].add_updater(lambda m: m.set_value(H_analytic()))
        self.add(info)

        # Tour beta
        for b in [0.15, 2.0, 0.8, 0.5]:
            self.play(beta_tr.animate.set_value(b),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.8)
