from manim import *
import numpy as np


class FourierTransformExample(Scene):
    """
    Fourier transform: time-domain signal vs frequency-domain spectrum.

    THREE_ROW layout:
      TOP    — time-domain signal f(t) = cos(2π·1·t) + 0.6·cos(2π·3·t) + 0.3·cos(2π·6·t).
      MID    — windowed integrand f(t)·cos(2π·ξ·t) for the current trial frequency ξ;
               the overlap area determines |f̂(ξ)|. Drives ValueTracker ξ from 0 to 8.
      BOTTOM — spectrum |f̂(ξ)| being progressively traced as ξ sweeps; peaks
               appear exactly at ξ = 1, 3, 6 with relative heights 1, 0.6, 0.3.
    """

    def construct(self):
        title = Tex(r"Fourier transform: each $\xi$ measures correlation with $\cos(2\pi\xi t)$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        T = 4.0  # time window [-T, T]
        freqs = [1.0, 3.0, 6.0]
        amps = [1.0, 0.6, 0.3]

        def f(t):
            return sum(a * np.cos(2 * PI * fr * t) for a, fr in zip(amps, freqs))

        # === TOP panel: time-domain signal ===
        ax_top = Axes(
            x_range=[-T, T, 1], y_range=[-2.2, 2.2, 1],
            x_length=11, y_length=1.6,
            axis_config={"include_tip": False, "include_numbers": False, "font_size": 16},
        ).move_to([0, 2.4, 0])
        sig = ax_top.plot(f, x_range=[-T, T, 0.02], color=BLUE, stroke_width=2)
        top_lbl = MathTex("f(t)", color=BLUE, font_size=22).next_to(ax_top, LEFT, buff=0.2)
        self.play(Create(ax_top), Create(sig), Write(top_lbl))

        # === MID panel: windowed integrand at trial ξ ===
        ax_mid = Axes(
            x_range=[-T, T, 1], y_range=[-2.5, 2.5, 1],
            x_length=11, y_length=1.6,
            axis_config={"include_tip": False, "include_numbers": False, "font_size": 16},
        ).move_to([0, 0.4, 0])
        mid_lbl = MathTex(r"f(t)\,\cos(2\pi\xi t)",
                          color=ORANGE, font_size=22).next_to(ax_mid, LEFT, buff=0.2)

        xi = ValueTracker(0.0)

        def integrand_curve():
            x = xi.get_value()
            return ax_mid.plot(
                lambda t: f(t) * np.cos(2 * PI * x * t),
                x_range=[-T, T, 0.02],
                color=ORANGE, stroke_width=2,
            )

        def integrand_area():
            x = xi.get_value()
            curve = ax_mid.plot(
                lambda t: f(t) * np.cos(2 * PI * x * t),
                x_range=[-T, T, 0.02],
            )
            return ax_mid.get_area(curve, x_range=[-T, T], color=ORANGE, opacity=0.35)

        self.play(Create(ax_mid), Write(mid_lbl))
        self.add(always_redraw(integrand_area), always_redraw(integrand_curve))

        # === BOTTOM panel: spectrum |f̂(ξ)| being traced as ξ sweeps ===
        ax_bot = Axes(
            x_range=[0, 8, 1], y_range=[0, 1.2, 0.3],
            x_length=11, y_length=2.0,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 16},
        ).move_to([0, -2.4, 0])
        bot_lbl = MathTex(r"|\hat f(\xi)|", color=YELLOW, font_size=22).next_to(ax_bot, LEFT, buff=0.2)
        self.play(Create(ax_bot), Write(bot_lbl))

        # We approximate the FT magnitude as Σ amp · sinc((ξ - f) · 2T) · 2T (windowed cos).
        # For visual clarity we use a clean Lorentzian-style peak instead.
        def ft_mag(x: float) -> float:
            total = 0.0
            for a, fr in zip(amps, freqs):
                # narrow peak at ξ = fr with height a (approximating delta·sinc)
                total += a / (1 + ((x - fr) * 4) ** 2)
            return total

        # Live tracer: a moving dot on the spectrum + a partial curve up to ξ
        spectrum_pts = []

        def spectrum_curve():
            xi_val = xi.get_value()
            xs = np.linspace(0, max(0.001, xi_val), max(2, int(xi_val * 30)))
            pts = [ax_bot.c2p(x, ft_mag(x)) for x in xs]
            curve = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                curve.set_points_smoothly(pts)
            else:
                curve.set_points_as_corners([pts[0], pts[0]])
            return curve

        def cursor_dot():
            xi_val = xi.get_value()
            return Dot(ax_bot.c2p(xi_val, ft_mag(xi_val)), color=YELLOW, radius=0.08)

        def cursor_line():
            xi_val = xi.get_value()
            return DashedLine(ax_bot.c2p(xi_val, 0), ax_bot.c2p(xi_val, ft_mag(xi_val) + 0.1),
                              color=YELLOW, stroke_width=2)

        self.add(always_redraw(spectrum_curve),
                 always_redraw(cursor_dot),
                 always_redraw(cursor_line))

        # Live ξ readout in top-right
        def xi_readout():
            return MathTex(rf"\xi = {xi.get_value():.2f}",
                           color=YELLOW, font_size=24).move_to([5.6, 1.4, 0])

        self.add(always_redraw(xi_readout))

        self.play(xi.animate.set_value(8.0), run_time=10, rate_func=linear)
        self.wait(0.8)
