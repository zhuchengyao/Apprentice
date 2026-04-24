from manim import *
import numpy as np


class FourierTimeFrequencyTradeoff(Scene):
    """Heisenberg-style uncertainty for Fourier pairs.  A Gaussian pulse
    exp(-t^2 / 2σ^2) modulated by cos(2π·f₀·t) has Fourier transform also
    Gaussian, with width 1/σ in frequency.  Sweep σ via ValueTracker and
    watch time-domain pulse narrow while frequency-domain lobe widens —
    product σ_t * σ_f stays ≥ 1/2 (in appropriate units)."""

    def construct(self):
        title = Tex(
            r"Fourier uncertainty: $\sigma_t \cdot \sigma_f \ge \tfrac{1}{4\pi}$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax_t = Axes(
            x_range=[-4, 4, 1], y_range=[-1.2, 1.2, 0.5],
            x_length=11, y_length=2.2,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).shift(UP * 1.3)
        ax_f = Axes(
            x_range=[0, 10, 2], y_range=[0, 1.2, 0.5],
            x_length=11, y_length=2.2,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).shift(DOWN * 1.5)
        t_lab = MathTex("t", font_size=24).next_to(
            ax_t.x_axis.get_end(), DOWN, buff=0.1
        )
        y_lab_t = Tex("time signal", font_size=22,
                      color=BLUE).next_to(ax_t.y_axis.get_end(),
                                          LEFT, buff=0.1)
        f_lab = MathTex("f", font_size=24).next_to(
            ax_f.x_axis.get_end(), DOWN, buff=0.1
        )
        y_lab_f = Tex("spectrum $|\\hat s|$", font_size=22,
                      color=RED).next_to(ax_f.y_axis.get_end(),
                                         LEFT, buff=0.1)
        self.play(Create(ax_t), Create(ax_f),
                  FadeIn(t_lab), FadeIn(y_lab_t),
                  FadeIn(f_lab), FadeIn(y_lab_f))

        sigma_tr = ValueTracker(1.0)
        f0 = 4.0

        def time_signal():
            s = sigma_tr.get_value()
            return ax_t.plot(
                lambda t: np.exp(-t ** 2 / (2 * s ** 2))
                * np.cos(2 * np.pi * f0 * t),
                x_range=[-4, 4, 0.01],
                color=BLUE, stroke_width=2.5,
            )

        def envelope():
            s = sigma_tr.get_value()
            return ax_t.plot(
                lambda t: np.exp(-t ** 2 / (2 * s ** 2)),
                x_range=[-4, 4, 0.02],
                color=BLUE_E, stroke_width=1.5,
            )

        def spectrum():
            s = sigma_tr.get_value()
            fwid = 1.0 / (2 * np.pi * s)
            return ax_f.plot(
                lambda f: np.exp(-(f - f0) ** 2 / (2 * fwid ** 2)),
                x_range=[0, 10, 0.02],
                color=RED, stroke_width=2.5,
            )

        def panel():
            s = sigma_tr.get_value()
            fwid = 1.0 / (2 * np.pi * s)
            product = s * fwid
            row = VGroup(
                MathTex(r"\sigma_t=", font_size=22, color=BLUE),
                DecimalNumber(s, num_decimal_places=2,
                              font_size=22, color=BLUE),
                MathTex(r"\quad\sigma_f=", font_size=22, color=RED),
                DecimalNumber(fwid, num_decimal_places=3,
                              font_size=22, color=RED),
                MathTex(r"\quad\sigma_t\sigma_f=", font_size=22,
                        color=YELLOW),
                DecimalNumber(product, num_decimal_places=3,
                              font_size=22, color=YELLOW),
            ).arrange(RIGHT, buff=0.1)
            row.to_edge(DOWN, buff=0.1)
            return row

        t_sig = always_redraw(time_signal)
        env = always_redraw(envelope)
        spec = always_redraw(spectrum)
        readout = always_redraw(panel)
        self.add(t_sig, env, spec, readout)

        for s_val in [0.3, 0.6, 1.0, 1.5, 2.0, 0.5]:
            self.play(sigma_tr.animate.set_value(s_val), run_time=2)
            self.wait(0.25)
        self.wait(1.0)
