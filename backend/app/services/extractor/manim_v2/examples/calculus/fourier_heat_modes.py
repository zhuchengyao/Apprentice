from manim import *
import numpy as np


class FourierHeatModesExample(Scene):
    """
    Heat equation u_t = α u_xx on [0, L] with IC decomposed into the
    first N Fourier modes. Higher modes decay faster (from _2019/
    diffyq/part3/discrete_case).

    SINGLE_FOCUS:
      5 stacked axes showing a₁ sin(πx/L)·e^(-α(π/L)²t), a₂ sin(2πx/L)·
      e^(-α(2π/L)²t), ..., a₅ sin(5πx/L)·e^(-α(5π/L)²t). Bottom shows
      their sum. ValueTracker t_tr advances.
    """

    def construct(self):
        title = Tex(r"Heat equation: Fourier modes decay independently",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        L = 1.0
        alpha = 0.01

        # IC: f(x) = triangle (or square), pick coefficients a_k
        # a_k = 2/L ∫ f·sin(kπx/L) dx for a triangle peaking at L/2:
        # a_k = 8·sin(kπ/2)/(kπ)²
        def a(k):
            return 8 * np.sin(k * PI / 2) / (k * PI) ** 2

        t_tr = ValueTracker(0.0)

        mode_axes = []
        N_show = 5
        for i in range(N_show):
            ax = Axes(x_range=[0, 1, 0.25], y_range=[-0.5, 0.5, 0.5],
                       x_length=6, y_length=0.65, tips=False,
                       axis_config={"font_size": 10}
                       ).move_to([-2, 2.3 - i * 0.85, 0])
            mode_axes.append(ax)
            lbl = MathTex(rf"\text{{mode }} {i + 1}", font_size=14,
                            color=interpolate_color(BLUE, RED, i / 4)
                            ).next_to(ax, LEFT, buff=0.15)
            self.add(ax, lbl)

        # Sum axes at bottom
        ax_sum = Axes(x_range=[0, 1, 0.25], y_range=[-0.3, 1.1, 0.5],
                       x_length=6, y_length=1.4, tips=False,
                       axis_config={"font_size": 12}
                       ).move_to([-2, -2.4, 0])
        sum_lbl = Tex("sum", color=YELLOW, font_size=18
                        ).next_to(ax_sum, LEFT, buff=0.15)
        self.add(ax_sum, sum_lbl)

        self.play(*[Create(m) for m in mode_axes], Create(ax_sum),
                   Write(sum_lbl))

        def mode_curve(k, ax):
            def f():
                t = t_tr.get_value()
                amp = a(k)
                decay = np.exp(-alpha * (k * PI / L) ** 2 * t)
                return ax.plot(
                    lambda x: amp * np.sin(k * PI * x / L) * decay,
                    x_range=[0, L, 0.005],
                    color=interpolate_color(BLUE, RED, (k - 1) / 4),
                    stroke_width=2.5)
            return f

        for i, ax in enumerate(mode_axes):
            self.add(always_redraw(mode_curve(i + 1, ax)))

        def sum_curve():
            t = t_tr.get_value()

            def u(x):
                total = 0.0
                for k in range(1, 15):
                    total += (a(k) * np.sin(k * PI * x / L)
                              * np.exp(-alpha * (k * PI / L) ** 2 * t))
                return total

            return ax_sum.plot(u, x_range=[0, L, 0.005],
                                color=YELLOW, stroke_width=3)

        self.add(always_redraw(sum_curve))

        def info():
            t = t_tr.get_value()
            return VGroup(
                MathTex(rf"t = {t:.1f}", color=YELLOW, font_size=22),
                MathTex(r"\tau_k = \tfrac{1}{\alpha(k\pi/L)^2}",
                         color=GREEN, font_size=20),
                MathTex(rf"\tau_1 = {1/(alpha*PI**2):.1f}",
                         color=BLUE, font_size=20),
                MathTex(rf"\tau_5 = {1/(alpha*(5*PI)**2):.1f}",
                         color=RED, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(200),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
