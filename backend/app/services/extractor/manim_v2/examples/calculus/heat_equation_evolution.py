from manim import *
import numpy as np


class HeatEquationEvolutionExample(Scene):
    """
    Heat equation u_t = α u_xx on [0, L] with Dirichlet BCs:
    initial square-wave profile decomposes into Fourier modes
    sin(n π x / L), each decaying at rate α(nπ/L)². Higher modes
    decay FASTER → temperature smooths.

    From _2019/diffyq/part2/heat_equation.

    SINGLE_FOCUS:
      axes with temperature u(x, t) vs x; ValueTracker t_tr advances
      time; always_redraw u(x, t) = Σ a_n sin(nπx/L)·exp(-α(nπ/L)²t).
      Sharp initial profile smooths to its fundamental mode.
    """

    def construct(self):
        title = Tex(r"Heat equation: $u_t = \alpha u_{xx}$ — higher modes decay faster",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        L = 1.0
        alpha = 0.01

        # Square-wave initial coefficients a_n = (2/L) ∫ f sin(nπx/L) dx
        # For f = 1 on [0.3, 0.7], 0 else: a_n = 2/nπ · (cos(0.3nπ) - cos(0.7nπ))
        def coef(n):
            return 2 / (n * PI) * (np.cos(0.3 * n * PI) - np.cos(0.7 * n * PI))

        N_modes = 30
        a = np.array([coef(n + 1) for n in range(N_modes)])

        ax = Axes(x_range=[0, L, 0.2], y_range=[-0.3, 1.2, 0.25],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        x_lbl = MathTex(r"x", font_size=22).next_to(ax, DOWN, buff=0.1)
        u_lbl = MathTex(r"u(x, t)", font_size=22).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(x_lbl), Write(u_lbl))

        # Ambient temperature dashed at 0
        zero_line = DashedLine(ax.c2p(0, 0), ax.c2p(L, 0),
                                color=GREY_B, stroke_width=1.5)
        self.play(Create(zero_line))

        t_tr = ValueTracker(0.0)

        def u(x, t):
            total = 0.0
            for n in range(1, N_modes + 1):
                total += a[n - 1] * np.sin(n * PI * x / L) * np.exp(-alpha * (n * PI / L) ** 2 * t)
            return total

        def curve():
            t = t_tr.get_value()
            return ax.plot(lambda x: u(x, t),
                            x_range=[0, L, 0.005],
                            color=RED, stroke_width=4)

        self.add(always_redraw(curve))

        # Initial reference (t=0 square)
        init_curve = ax.plot(lambda x: u(x, 0),
                              x_range=[0, L, 0.005],
                              color=GREY_B, stroke_width=2,
                              stroke_opacity=0.5)
        self.play(Create(init_curve))

        def info():
            t = t_tr.get_value()
            # dominant mode amplitude
            a1 = abs(a[0]) * np.exp(-alpha * (PI / L) ** 2 * t)
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=WHITE, font_size=24),
                MathTex(rf"\alpha = {alpha}", color=BLUE, font_size=22),
                MathTex(rf"|a_1(t)| = {a1:.4f}",
                         color=YELLOW, font_size=22),
                MathTex(r"\text{decay}: \exp(-\alpha (n\pi/L)^2 t)",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(300),
                   run_time=10, rate_func=linear)
        self.wait(0.5)
