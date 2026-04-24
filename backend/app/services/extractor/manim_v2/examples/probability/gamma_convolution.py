from manim import *
import numpy as np
from math import gamma as gamma_fn


def gamma_pdf(x, k, theta):
    if x <= 0:
        return 0.0
    return x ** (k - 1) * np.exp(-x / theta) / (gamma_fn(k) * theta ** k)


class GammaConvolutionExample(Scene):
    """
    Convolution of two Gamma densities = Gamma with summed shape.

    TWO_COLUMN:
      LEFT  — Axes plotting f_X (BLUE), f_Y (GREEN), and their
              convolution f_{X+Y} (YELLOW). Two ValueTrackers k_x,
              k_y drive the shape parameters; all three curves
              redraw via always_redraw. The yellow curve = Gamma(k_x+k_y, θ).
              At a chosen z, the integrand f_X(x)·f_Y(z-x) is shown
              underneath as a colored area whose total = f_{X+Y}(z).
      RIGHT — live k_x, k_y, total k_x+k_y, mean values μ_x, μ_y,
              μ_sum, and the convolution formula.
    """

    def construct(self):
        title = Tex(r"$\Gamma(k_1, \theta) * \Gamma(k_2, \theta) = \Gamma(k_1 + k_2, \theta)$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        theta = 1.0

        axes = Axes(
            x_range=[0, 14, 2], y_range=[0, 0.5, 0.1],
            x_length=7.0, y_length=4.4,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.4, -0.2, 0])
        self.play(Create(axes))

        kx_tr = ValueTracker(2.0)
        ky_tr = ValueTracker(2.0)

        def fx_curve():
            kx = kx_tr.get_value()
            return axes.plot(lambda x: gamma_pdf(x, kx, theta),
                             x_range=[0.01, 13.9, 0.05], color=BLUE)

        def fy_curve():
            ky = ky_tr.get_value()
            return axes.plot(lambda x: gamma_pdf(x, ky, theta),
                             x_range=[0.01, 13.9, 0.05], color=GREEN)

        def sum_curve():
            kx = kx_tr.get_value()
            ky = ky_tr.get_value()
            return axes.plot(lambda x: gamma_pdf(x, kx + ky, theta),
                             x_range=[0.01, 13.9, 0.05], color=YELLOW)

        self.add(always_redraw(fx_curve), always_redraw(fy_curve),
                 always_redraw(sum_curve))

        # RIGHT COLUMN
        rcol_x = +4.4

        def info_panel():
            kx = kx_tr.get_value()
            ky = ky_tr.get_value()
            return VGroup(
                MathTex(rf"X \sim \Gamma({kx:.1f}, {theta:.1f})",
                        color=BLUE, font_size=24),
                MathTex(rf"Y \sim \Gamma({ky:.1f}, {theta:.1f})",
                        color=GREEN, font_size=24),
                MathTex(rf"X + Y \sim \Gamma({kx + ky:.1f}, {theta:.1f})",
                        color=YELLOW, font_size=24),
                MathTex(rf"\mathbb{{E}}[X] = k_1\theta = {kx*theta:.2f}",
                        color=BLUE, font_size=20),
                MathTex(rf"\mathbb{{E}}[Y] = k_2\theta = {ky*theta:.2f}",
                        color=GREEN, font_size=20),
                MathTex(rf"\mathbb{{E}}[X+Y] = {(kx+ky)*theta:.2f}",
                        color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +1.0, 0])

        self.add(always_redraw(info_panel))

        formula = MathTex(
            r"f_{X+Y}(z) = \int_0^z f_X(x)\,f_Y(z-x)\,dx",
            color=YELLOW, font_size=24,
        ).move_to([rcol_x, -2.4, 0])
        self.play(Write(formula))

        # Sweep through 4 (k_x, k_y) pairs
        for kx_v, ky_v in [(3.0, 1.0), (1.0, 4.0), (2.5, 2.5), (4.0, 3.0)]:
            self.play(kx_tr.animate.set_value(kx_v),
                      ky_tr.animate.set_value(ky_v),
                      run_time=2.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
