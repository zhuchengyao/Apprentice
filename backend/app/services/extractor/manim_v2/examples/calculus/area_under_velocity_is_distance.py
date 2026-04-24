from manim import *
import numpy as np


class AreaUnderVelocityIsDistanceExample(Scene):
    """
    Area under v(t) graph = total distance traveled.
    Example: v(t) = t(8-t)/4 peaking at t=4. Distance = ∫ v dt.
    """

    def construct(self):
        title = Tex(r"Area under $v(t)$ graph $=$ distance traveled",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 8, 1], y_range=[0, 5, 1],
                    x_length=8.5, y_length=4,
                    axis_config={"include_numbers": True, "font_size": 16}
                    ).shift(DOWN * 0.3)
        self.play(Create(axes))
        self.add(Tex(r"time (s)", font_size=18).next_to(axes, DOWN, buff=0.15))
        self.add(Tex(r"velocity (m/s)", font_size=18).next_to(axes, LEFT, buff=0.15))

        def v(t):
            return t * (8 - t) / 4

        v_curve = axes.plot(v, x_range=[0, 8], color=BLUE, stroke_width=3)
        self.add(v_curve)

        t_tr = ValueTracker(0.1)

        def area_fill():
            t_now = t_tr.get_value()
            if t_now < 0.05:
                return VMobject()
            ts = np.linspace(0, t_now, 60)
            top = [axes.c2p(s, v(s)) for s in ts]
            bot = [axes.c2p(s, 0) for s in ts]
            return Polygon(*top, *reversed(bot),
                            color=GREEN, stroke_width=0,
                            fill_color=GREEN, fill_opacity=0.5)

        self.add(always_redraw(area_fill))

        def probe_line():
            t = t_tr.get_value()
            return DashedLine(axes.c2p(t, 0), axes.c2p(t, v(t)),
                               color=ORANGE, stroke_width=2)

        def probe_dot():
            t = t_tr.get_value()
            return Dot(axes.c2p(t, v(t)), color=ORANGE, radius=0.1)

        self.add(always_redraw(probe_line), always_redraw(probe_dot))

        def distance():
            t = t_tr.get_value()
            if t < 0.02:
                return 0.0
            ts = np.linspace(0, t, 100)
            return float(np.trapezoid([v(s) for s in ts], ts))

        info = VGroup(
            Tex(r"$v(t)=t(8-t)/4$", color=BLUE, font_size=22),
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.1, num_decimal_places=2,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"distance $=\int_0^t v\,ds=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(distance()))
        self.add(info)

        self.play(t_tr.animate.set_value(8.0), run_time=7, rate_func=linear)
        self.wait(0.5)
