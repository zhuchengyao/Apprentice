from manim import *
import numpy as np


class FourierInversionExample(Scene):
    """
    Fourier inversion theorem: f(x) = (1/2π) ∫ f̂(ω) e^{iωx} dω
    recovers f from its transform. Illustrate with f(x) = Gaussian.

    TWO_COLUMN:
      LEFT  — f(x) = e^(-x²/2) / √(2π). ValueTracker omega_max_tr
              adds higher frequency components 0..10 to a partial
              reconstruction on ordinary axes.
      RIGHT — spectrum f̂(ω) also Gaussian; mark ω_max cursor.
    """

    def construct(self):
        title = Tex(r"Fourier inversion: $f = \mathcal F^{-1}\{\mathcal F\{f\}\}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_L = Axes(x_range=[-4, 4, 1], y_range=[-0.05, 0.45, 0.1],
                     x_length=6, y_length=3.5, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([-3.3, -0.3, 0])
        L_lbl = MathTex(r"f(x)", color=BLUE, font_size=20
                          ).next_to(ax_L, UP, buff=0.1)
        self.play(Create(ax_L), Write(L_lbl))

        # True Gaussian
        true_curve = ax_L.plot(lambda x: np.exp(-x ** 2 / 2) / np.sqrt(2 * PI),
                                 x_range=[-4, 4, 0.02],
                                 color=GREY_B, stroke_width=2)
        self.play(Create(true_curve))

        omega_max_tr = ValueTracker(0.5)

        def partial_reconstruction(x, W):
            # Partial inverse via numerical ∫_{-W}^{W} f̂(ω) cos(ωx) / 2π dω
            # since imaginary part cancels for real f
            omegas = np.linspace(-W, W, 200)
            f_hat = np.exp(-omegas ** 2 / 2)  # Gaussian self-transform (up to constants)
            integrand = f_hat * np.cos(omegas * x)
            return np.trapz(integrand, omegas) / (2 * PI)

        def partial_curve():
            W = omega_max_tr.get_value()
            return ax_L.plot(lambda x: partial_reconstruction(x, W),
                              x_range=[-4, 4, 0.04],
                              color=YELLOW, stroke_width=3)

        self.add(always_redraw(partial_curve))

        # RIGHT: spectrum f̂(ω) with cursor
        ax_R = Axes(x_range=[-5, 5, 1], y_range=[0, 1.1, 0.25],
                     x_length=6, y_length=3, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([3.3, -0.3, 0])
        R_lbl = MathTex(r"\hat f(\omega)", color=RED, font_size=20
                          ).next_to(ax_R, UP, buff=0.1)
        self.play(Create(ax_R), Write(R_lbl))

        spec_curve = ax_R.plot(lambda w: np.exp(-w ** 2 / 2),
                                 x_range=[-5, 5, 0.02],
                                 color=RED, stroke_width=3)
        self.play(Create(spec_curve))

        def cursor_band():
            W = omega_max_tr.get_value()
            return Rectangle(
                width=ax_R.c2p(W, 0)[0] - ax_R.c2p(-W, 0)[0],
                height=ax_R.c2p(0, 1)[1] - ax_R.c2p(0, 0)[1],
                color=YELLOW, fill_opacity=0.25,
                stroke_width=1.5
            ).move_to([(ax_R.c2p(-W, 0)[0] + ax_R.c2p(W, 0)[0]) / 2,
                         (ax_R.c2p(0, 0)[1] + ax_R.c2p(0, 1)[1]) / 2, 0])

        self.add(always_redraw(cursor_band))

        def info():
            W = omega_max_tr.get_value()
            return VGroup(
                MathTex(rf"\omega_{{\max}} = {W:.2f}",
                         color=YELLOW, font_size=24),
                Tex(r"GREY: true $f$", color=GREY_B, font_size=18),
                Tex(r"YELLOW: partial $\mathcal F^{-1}$", color=YELLOW, font_size=18),
                Tex(r"BAND: frequencies included",
                     color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for wv in [1.0, 2.0, 3.0, 5.0]:
            self.play(omega_max_tr.animate.set_value(wv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
