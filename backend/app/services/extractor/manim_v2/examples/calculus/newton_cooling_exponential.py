from manim import *
import numpy as np


class NewtonCoolingExponentialExample(Scene):
    """
    Newton's law of cooling: dT/dt = -k(T - T_ambient).
    Solution: T(t) = T_ambient + (T_0 - T_ambient) · e^(-k t).
    Plot T(t) approaching ambient asymptotically.
    """

    def construct(self):
        title = Tex(r"Newton's cooling: $T(t)=T_\infty+(T_0-T_\infty)e^{-kt}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 8, 1], y_range=[0, 100, 20],
                    x_length=9, y_length=4.5,
                    axis_config={"include_numbers": True, "font_size": 16}
                    ).shift(DOWN * 0.3)
        self.play(Create(axes))
        self.add(Tex(r"time (s)", font_size=18).next_to(axes, DOWN, buff=0.1))
        self.add(Tex(r"temp (°C)", font_size=18).next_to(axes, LEFT, buff=0.15))

        T_inf = 20.0
        T_0 = 90.0
        k = 0.5

        def T(t):
            return T_inf + (T_0 - T_inf) * np.exp(-k * t)

        # Ambient line
        amb = DashedLine(axes.c2p(0, T_inf), axes.c2p(8, T_inf),
                          color=BLUE, stroke_width=2, stroke_opacity=0.6)
        self.add(amb)
        self.add(Tex(r"$T_\infty=20°$", color=BLUE, font_size=20).next_to(
            axes.c2p(8, T_inf), RIGHT, buff=0.1))

        # T curve
        T_curve = axes.plot(T, x_range=[0, 8], color=RED, stroke_width=3)
        self.add(T_curve)

        t_tr = ValueTracker(0.0)

        def probe():
            t = t_tr.get_value()
            return Dot(axes.c2p(t, T(t)), color=YELLOW, radius=0.12)

        def drop():
            t = t_tr.get_value()
            return DashedLine(axes.c2p(t, 0), axes.c2p(t, T(t)),
                               color=GREY_B, stroke_width=1.5)

        self.add(always_redraw(probe), always_redraw(drop))

        info = VGroup(
            Tex(r"$T_0=90°$, $k=0.5$", color=RED, font_size=22),
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW),
                   Tex(r"s", font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$T(t)=$", font_size=22),
                   DecimalNumber(90.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW),
                   Tex(r"°", font_size=22)).arrange(RIGHT, buff=0.1),
            Tex(r"approaches $T_\infty$ as $t\to\infty$",
                color=BLUE, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(T(t_tr.get_value())))
        self.add(info)

        self.play(t_tr.animate.set_value(8), run_time=6, rate_func=linear)
        self.wait(0.5)
