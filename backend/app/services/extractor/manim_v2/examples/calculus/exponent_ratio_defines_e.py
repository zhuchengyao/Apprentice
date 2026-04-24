from manim import *
import numpy as np


class ExponentRatioDefinesEExample(Scene):
    """
    For a^t, the ratio (a^(t+dt) - a^t)/dt = a^t · (a^dt - 1)/dt.
    The constant (a^dt - 1)/dt depends only on a. Tour through
    a = 2, 3, 7, 8 and find the one where it equals 1 — that's e.
    """

    def construct(self):
        title = Tex(r"Find $a$ where $\frac{a^{dt}-1}{dt}=1$: that's $e$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 3.2, 0.5], y_range=[0, 2.5, 0.5],
                    x_length=8, y_length=4.2,
                    axis_config={"include_numbers": True, "font_size": 16}
                    ).shift(DOWN * 0.2)
        self.play(Create(axes))

        # Horizontal reference line at 1
        ref_line = DashedLine(axes.c2p(0, 1), axes.c2p(3.2, 1),
                               color=GREEN, stroke_width=2, stroke_opacity=0.6)
        self.add(ref_line)
        self.add(Tex(r"$= 1$", color=GREEN, font_size=22).next_to(axes.c2p(3.2, 1), RIGHT, buff=0.1))

        # Plot (a^dt - 1)/dt as a function of a for dt = 0.01
        dt = 0.01
        curve = axes.plot(lambda a: (a ** dt - 1) / dt,
                           x_range=[0.3, 3.2], color=BLUE, stroke_width=3)
        self.add(curve)
        self.add(Tex(r"$\frac{a^{dt}-1}{dt}$ as fn of $a$", color=BLUE, font_size=22).next_to(axes, UP, buff=0.15))

        # Mark e
        e_val = np.e
        e_dot = Dot(axes.c2p(e_val, (e_val ** dt - 1) / dt), color=YELLOW, radius=0.13)
        self.add(e_dot)
        self.add(Tex(rf"$e\approx 2.718$", color=YELLOW, font_size=22).next_to(e_dot, UR, buff=0.1))

        a_tr = ValueTracker(2.0)

        def probe():
            a = a_tr.get_value()
            return Dot(axes.c2p(a, (a ** dt - 1) / dt),
                        color=RED, radius=0.11)

        def probe_drop():
            a = a_tr.get_value()
            return DashedLine(axes.c2p(a, 0),
                               axes.c2p(a, (a ** dt - 1) / dt),
                               color=RED, stroke_width=1.5)

        self.add(always_redraw(probe), always_redraw(probe_drop))

        info = VGroup(
            VGroup(Tex(r"$a=$", font_size=22),
                   DecimalNumber(2.0, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\ln(a)\approx \frac{a^{dt}-1}{dt}=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(r"$a=e$ gives ratio $=1$",
                color=YELLOW, font_size=22),
            Tex(r"$\Rightarrow \frac{d e^t}{dt}=e^t$",
                color=GREEN, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.5)
        info[0][1].add_updater(lambda m: m.set_value(a_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(
            (a_tr.get_value() ** dt - 1) / dt))
        self.add(info)

        for a_val in [3.0, 7.0, 8.0, e_val]:
            self.play(a_tr.animate.set_value(a_val),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
