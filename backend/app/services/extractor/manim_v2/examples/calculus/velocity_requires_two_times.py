from manim import *
import numpy as np


class VelocityRequiresTwoTimesExample(Scene):
    """
    Philosophical paradox: 'velocity at an instant' requires at least
    two times. A single snapshot gives position only — no velocity.
    Show two snapshots dt apart and compute Δs/Δt.
    """

    def construct(self):
        title = Tex(r"Velocity needs two times: $\Delta s/\Delta t$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 4, 1], y_range=[0, 8, 2],
                    x_length=8, y_length=4.2,
                    axis_config={"include_numbers": True, "font_size": 16}
                    ).shift(DOWN * 0.4)
        self.play(Create(axes))
        self.add(Tex(r"$s(t)=t^2$", color=BLUE, font_size=22).next_to(axes, UP, buff=0.15))

        s_curve = axes.plot(lambda t: t * t, x_range=[0, 3], color=BLUE, stroke_width=3)
        self.add(s_curve)

        t_1 = 1.5
        dt_tr = ValueTracker(1.0)

        def t_2():
            return t_1 + dt_tr.get_value()

        def p1_dot():
            return Dot(axes.c2p(t_1, t_1 ** 2), color=GREEN, radius=0.12)

        def p2_dot():
            t2 = t_2()
            return Dot(axes.c2p(t2, t2 ** 2), color=ORANGE, radius=0.12)

        def secant_line():
            t2 = t_2()
            return Line(axes.c2p(t_1, t_1 ** 2),
                         axes.c2p(t2, t2 ** 2),
                         color=YELLOW, stroke_width=3)

        def dt_bracket():
            t2 = t_2()
            y_min = min(t_1 ** 2, t2 ** 2) - 0.3
            return DashedLine(axes.c2p(t_1, y_min), axes.c2p(t2, y_min),
                               color=GREY_B, stroke_width=2)

        self.add(always_redraw(p1_dot), always_redraw(p2_dot),
                 always_redraw(secant_line), always_redraw(dt_bracket))

        # Labels
        p1_lbl = Tex(r"$(t_1, s(t_1))$", color=GREEN, font_size=20).move_to(
            axes.c2p(t_1, t_1 ** 2) + DOWN * 0.4 + LEFT * 0.4)
        self.add(p1_lbl)

        def v_avg():
            t2 = t_2()
            return (t2 ** 2 - t_1 ** 2) / (t2 - t_1)

        info = VGroup(
            Tex(r"$t_1=1.5$ fixed", color=GREEN, font_size=22),
            VGroup(Tex(r"$\Delta t=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\Delta s/\Delta t=$", color=YELLOW, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\to 2 t_1=3$ as $\Delta t\to 0$", color=GREEN, font_size=20),
                    ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(dt_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(v_avg()))
        self.add(info)

        # Sweep dt → 0
        self.play(dt_tr.animate.set_value(0.05), run_time=4, rate_func=smooth)
        self.wait(0.6)
        self.play(dt_tr.animate.set_value(0.5), run_time=2, rate_func=smooth)
        self.wait(0.5)
