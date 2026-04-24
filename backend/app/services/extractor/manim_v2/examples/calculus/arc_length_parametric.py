from manim import *
import numpy as np


class ArcLengthParametricExample(Scene):
    """
    Arc length for parametric curve (x(t), y(t)):
       L = ∫_a^b √(x'(t)² + y'(t)²) dt.

    Example: logarithmic spiral x = e^(0.2 t) cos t, y = e^(0.2 t) sin t
    on [0, 4π]. Analytic L = √(1 + 0.04)/0.2 · (e^(0.8π) − 1).

    SINGLE_FOCUS: ValueTracker t_tr sweeps endpoint; always_redraw
    YELLOW partial trace + live numerical integral via np.trapezoid.
    """

    def construct(self):
        title = Tex(r"Arc length: $L=\int\sqrt{x'(t)^2+y'(t)^2}\,dt$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-8, 8, 2], y_range=[-6, 6, 2],
                            x_length=8, y_length=5.8,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(DOWN * 0.2)
        self.play(Create(plane))

        a = 0.2

        def xy(t):
            return np.exp(a * t) * np.cos(t), np.exp(a * t) * np.sin(t)

        full = ParametricFunction(
            lambda t: plane.c2p(*xy(t)), t_range=[0, 4 * PI],
            color=GREY_B, stroke_width=1.5, stroke_opacity=0.5,
        )
        self.add(full)

        t_tr = ValueTracker(0.2)

        def partial_trace():
            t = t_tr.get_value()
            return ParametricFunction(
                lambda s: plane.c2p(*xy(s)), t_range=[0, t],
                color=YELLOW, stroke_width=4,
            )

        def head_dot():
            t = t_tr.get_value()
            x, y = xy(t)
            return Dot(plane.c2p(x, y), color=ORANGE, radius=0.11)

        self.add(always_redraw(partial_trace), always_redraw(head_dot))

        def L_numeric():
            t = t_tr.get_value()
            if t < 0.01:
                return 0.0
            ts = np.linspace(0, t, 400)
            dx = np.exp(a * ts) * (a * np.cos(ts) - np.sin(ts))
            dy = np.exp(a * ts) * (a * np.sin(ts) + np.cos(ts))
            return float(np.trapezoid(np.sqrt(dx ** 2 + dy ** 2), ts))

        def L_analytic():
            t = t_tr.get_value()
            return float(np.sqrt(1 + a * a) / a * (np.exp(a * t) - 1))

        info = VGroup(
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.2, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$L$ (numeric) $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$L$ (analytic) $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$=\sqrt{1+a^2}/a\cdot(e^{at}-1)$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(L_numeric()))
        info[2][1].add_updater(lambda m: m.set_value(L_analytic()))
        self.add(info)

        self.play(t_tr.animate.set_value(4 * PI),
                  run_time=7, rate_func=linear)
        self.wait(0.8)
