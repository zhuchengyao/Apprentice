from manim import *
import numpy as np


class HologramDiffractionDoubleSlitExample(Scene):
    """
    Double-slit diffraction (from _2024/holograms/diffraction):
    intensity pattern I(θ) ∝ cos²(π d sin θ / λ) · sinc²(π a sin θ / λ)
    where d = slit spacing, a = slit width. ValueTracker d_over_lambda
    tunes d/λ.

    TWO_COLUMN:
      LEFT  — 2D heat-intensity strip representation of I(θ).
      RIGHT  — I(θ) line plot; always_redraw as d/λ changes.
    """

    def construct(self):
        title = Tex(r"Double-slit: $I \propto \cos^2(\pi d\sin\theta/\lambda)\cdot \mathrm{sinc}^2(\pi a\sin\theta/\lambda)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # a/λ fixed
        a_over_lambda = 0.8
        d_over_lambda_tr = ValueTracker(3.0)

        def I(theta):
            dol = d_over_lambda_tr.get_value()
            aol = a_over_lambda
            cos_term = np.cos(PI * dol * np.sin(theta)) ** 2
            arg = PI * aol * np.sin(theta)
            if abs(arg) < 1e-6:
                sinc = 1.0
            else:
                sinc = (np.sin(arg) / arg) ** 2
            return cos_term * sinc

        # Intensity strip on left
        bar_origin = np.array([-4.5, 0, 0])
        bar_len = 5.0

        def intensity_strip():
            grp = VGroup()
            N = 60
            dx = bar_len / N
            for i in range(N):
                x_frac = (i + 0.5) / N  # 0 to 1
                theta = (x_frac - 0.5) * PI  # -π/2 to π/2
                val = I(theta)
                color = interpolate_color(BLACK, WHITE, min(val, 1.0))
                rect = Rectangle(width=dx, height=2.2, color=color,
                                   fill_opacity=1, stroke_width=0)
                rect.move_to(bar_origin + np.array([-bar_len/2 + x_frac * bar_len,
                                                       0, 0]))
                grp.add(rect)
            return grp

        self.add(always_redraw(intensity_strip))

        strip_label = Tex("screen intensity", color=WHITE, font_size=22
                           ).next_to(bar_origin, UP, buff=1.3)
        self.play(Write(strip_label))

        # Right: intensity curve
        ax = Axes(x_range=[-PI / 2 - 0.1, PI / 2 + 0.1, PI / 4],
                   y_range=[0, 1.1, 0.25],
                   x_length=5, y_length=3, tips=False,
                   axis_config={"font_size": 12}
                   ).move_to([3, -0.7, 0])
        x_lbl = MathTex(r"\theta", font_size=18).next_to(ax, DOWN, buff=0.1)
        y_lbl = MathTex(r"I(\theta)", font_size=18).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(x_lbl), Write(y_lbl))

        def intensity_curve():
            return ax.plot(I, x_range=[-PI / 2, PI / 2, 0.01],
                            color=YELLOW, stroke_width=3)

        self.add(always_redraw(intensity_curve))

        def info():
            dol = d_over_lambda_tr.get_value()
            return VGroup(
                MathTex(rf"d/\lambda = {dol:.2f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"a/\lambda = {a_over_lambda}",
                         color=WHITE, font_size=20),
                MathTex(r"\theta_{\text{max}} = \arcsin(\lambda/d)",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3, 2.0, 0])

        self.add(always_redraw(info))

        for dv in [1.5, 5.0, 8.0, 3.0]:
            self.play(d_over_lambda_tr.animate.set_value(dv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
