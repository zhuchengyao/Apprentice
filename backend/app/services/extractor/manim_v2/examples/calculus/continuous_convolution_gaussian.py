from manim import *
import numpy as np


class ContinuousConvolutionGaussianExample(Scene):
    """
    Convolution of two Gaussians is a Gaussian (from _2022/
    convolutions/continuous): 𝒩(0, σ₁²) * 𝒩(0, σ₂²) = 𝒩(0, σ₁² + σ₂²).

    TWO_COLUMN:
      LEFT  — axes with 3 curves: f (BLUE), g_τ reversed-sliding
              (ORANGE), and f·g_τ overlap (GREEN fill). ValueTracker
              τ_tr slides.
      RIGHT — output axes showing (f*g)(τ) = another Gaussian with
              σ² = σ₁² + σ₂²; always_redraw trail + rider.
    """

    def construct(self):
        title = Tex(r"Gaussian $\ast$ Gaussian $=$ Gaussian: $\sigma^2 = \sigma_1^2 + \sigma_2^2$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        sigma1, sigma2 = 0.7, 1.0
        sigma_out = np.sqrt(sigma1 ** 2 + sigma2 ** 2)

        ax_in = Axes(x_range=[-4, 4, 1], y_range=[0, 0.7, 0.2],
                      x_length=6.5, y_length=2.8, tips=False,
                      axis_config={"font_size": 13, "include_numbers": True}
                      ).move_to([-3.3, 1.3, 0])
        ax_out = Axes(x_range=[-4, 4, 1], y_range=[0, 0.4, 0.1],
                       x_length=6.5, y_length=2.8, tips=False,
                       axis_config={"font_size": 13, "include_numbers": True}
                       ).move_to([-3.3, -1.8, 0])
        self.play(Create(ax_in), Create(ax_out))

        def gauss(x, s):
            return np.exp(-x ** 2 / (2 * s ** 2)) / (s * np.sqrt(2 * PI))

        # f (static, BLUE)
        f_curve = ax_in.plot(lambda x: gauss(x, sigma1),
                               x_range=[-4, 4, 0.02],
                               color=BLUE, stroke_width=3)
        self.play(Create(f_curve))

        tau_tr = ValueTracker(-3.0)

        def g_curve():
            tau = tau_tr.get_value()
            return ax_in.plot(lambda x: gauss(tau - x, sigma2),
                               x_range=[-4, 4, 0.02],
                               color=ORANGE, stroke_width=3)

        def overlap_fill():
            tau = tau_tr.get_value()
            return ax_in.plot(
                lambda x: min(gauss(x, sigma1), gauss(tau - x, sigma2)),
                x_range=[-4, 4, 0.02],
                color=GREEN, stroke_width=2,
                stroke_opacity=0.7)

        self.add(always_redraw(g_curve), always_redraw(overlap_fill))

        # Output curve (static reference) + growing trail
        out_static = ax_out.plot(lambda x: gauss(x, sigma_out),
                                   x_range=[-4, 4, 0.02],
                                   color=GREY_B, stroke_width=1.5,
                                   stroke_opacity=0.5)
        self.play(Create(out_static))

        def out_trail():
            tau_cur = tau_tr.get_value()
            pts = []
            for t in np.linspace(-4.0, tau_cur, 80):
                # true convolution: (f*g)(τ) = gauss(τ, √(σ1² + σ2²))
                pts.append(ax_out.c2p(t, gauss(t, sigma_out)))
            m = VMobject(color=GREEN, stroke_width=4)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def out_dot():
            tau = tau_tr.get_value()
            return Dot(ax_out.c2p(tau, gauss(tau, sigma_out)),
                        color=RED, radius=0.1)

        self.add(always_redraw(out_trail), always_redraw(out_dot))

        def info():
            tau = tau_tr.get_value()
            val = gauss(tau, sigma_out)
            return VGroup(
                MathTex(rf"\sigma_1 = {sigma1}", color=BLUE, font_size=20),
                MathTex(rf"\sigma_2 = {sigma2}", color=ORANGE, font_size=20),
                MathTex(rf"\tau = {tau:+.2f}", color=WHITE, font_size=22),
                MathTex(rf"(f*g)(\tau) = {val:.4f}",
                         color=GREEN, font_size=22),
                MathTex(rf"\sigma = \sqrt{{\sigma_1^2+\sigma_2^2}} = {sigma_out:.3f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(tau_tr.animate.set_value(3.0),
                   run_time=8, rate_func=linear)
        self.wait(0.5)
