from manim import *
import numpy as np


class DrivenHarmonicOscillatorExample(Scene):
    """
    Driven damped harmonic oscillator (from _2023/optics_puzzles/
    driven_harmonic_oscillator):
    x'' + 2γ x' + ω₀² x = F cos(ω t). Amplitude response peaks at
    the resonance frequency ω ≈ ω₀ (Lorentzian).

    TWO_COLUMN:
      LEFT  — Lorentzian amplitude curve A(ω); ValueTracker ω_tr
              sweeps; rider dot + dashed vertical at ω.
      RIGHT — time-domain steady-state x(t) at current ω; live
              (ω, phase, amplitude) panel.
    """

    def construct(self):
        title = Tex(r"Driven oscillator: $\ddot x + 2\gamma\dot x + \omega_0^2 x = F\cos(\omega t)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        omega_0 = 2.0
        gamma = 0.15
        F = 1.0

        def A(w):
            return F / np.sqrt((omega_0 ** 2 - w ** 2) ** 2
                                + (2 * gamma * w) ** 2)

        def phase(w):
            # φ = arctan(2γω / (ω₀² - ω²))
            return np.arctan2(2 * gamma * w, omega_0 ** 2 - w ** 2)

        ax_A = Axes(x_range=[0, 4.5, 1], y_range=[0, 4, 1],
                     x_length=6, y_length=3.5, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.5, 0.8, 0])
        xl = MathTex(r"\omega", font_size=20).next_to(ax_A, DOWN, buff=0.1)
        yl = MathTex(r"A(\omega)", font_size=20).next_to(ax_A, LEFT, buff=0.1)

        A_curve = ax_A.plot(A, x_range=[0.01, 4.5, 0.02],
                              color=BLUE, stroke_width=3)
        self.play(Create(ax_A), Write(xl), Write(yl), Create(A_curve))

        w_tr = ValueTracker(0.5)

        def rider():
            w = w_tr.get_value()
            return Dot(ax_A.c2p(w, A(w)), color=YELLOW, radius=0.1)

        def drop():
            w = w_tr.get_value()
            return DashedLine(ax_A.c2p(w, 0), ax_A.c2p(w, A(w)),
                               color=YELLOW_E, stroke_width=1.5)

        self.add(always_redraw(rider), always_redraw(drop))

        # RIGHT: steady-state x(t)
        ax_x = Axes(x_range=[0, 15, 3], y_range=[-4, 4, 2],
                     x_length=6, y_length=2.8, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([3.5, -2.2, 0])
        tl = MathTex(r"t", font_size=20).next_to(ax_x, DOWN, buff=0.08)

        def steady_x():
            w = w_tr.get_value()
            amp = A(w)
            phi = phase(w)
            return ax_x.plot(
                lambda t: amp * np.cos(w * t - phi),
                x_range=[0, 15, 0.05],
                color=RED, stroke_width=3)

        self.play(Create(ax_x), Write(tl))
        self.add(always_redraw(steady_x))

        def info():
            w = w_tr.get_value()
            amp = A(w)
            phi = phase(w)
            return VGroup(
                MathTex(rf"\omega = {w:.3f}", color=YELLOW, font_size=22),
                MathTex(rf"\omega_0 = {omega_0}", color=WHITE, font_size=22),
                MathTex(rf"\gamma = {gamma}", color=WHITE, font_size=20),
                MathTex(rf"A(\omega) = {amp:.3f}",
                         color=BLUE, font_size=22),
                MathTex(rf"\phi = {np.degrees(phi):.1f}^\circ",
                         color=RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.5, 1.5, 0])

        self.add(always_redraw(info))

        # Sweep through resonance
        for target in [1.5, 2.0, 2.3, 3.0, 4.0]:
            self.play(w_tr.animate.set_value(target),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
