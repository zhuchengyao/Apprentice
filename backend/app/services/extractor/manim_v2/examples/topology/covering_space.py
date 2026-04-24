from manim import *
import numpy as np


class CoveringSpaceExample(Scene):
    """
    Covering map p: ℝ → S¹, p(t) = (cos t, sin t). Every loop in
    S¹ lifts uniquely to a path in ℝ once the basepoint is chosen.
    The winding number equals the displacement in the lift.

    TWO_COLUMN: LEFT has the unit circle S¹ with a point moving
    via ValueTracker t_tr. RIGHT has the real line with the lifted
    point. Persistent trail on the line reveals displacement =
    2π × (winding); live readouts.
    """

    def construct(self):
        title = Tex(r"Covering map $p:\mathbb{R}\to S^1$, $p(t)=(\cos t,\sin t)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Left: S^1
        left = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           x_length=4.5, y_length=4.5,
                           background_line_style={"stroke_opacity": 0.3}
                           ).shift(LEFT * 3.3)
        circ = Circle(radius=1.5, color=BLUE, stroke_width=3).move_to(left.c2p(0, 0))
        self.play(Create(left), Create(circ))

        # Right: R (horizontal line)
        right_line = NumberLine(x_range=[-2, 14, 2], length=7,
                                include_numbers=True,
                                font_size=18).shift(RIGHT * 2.5)
        self.play(Create(right_line))

        # Annotate 2π ticks
        tau_lbls = VGroup()
        for k in range(3):
            x = 2 * PI * k
            tau_lbls.add(DashedLine(right_line.n2p(x) + UP * 0.6,
                                     right_line.n2p(x) + DOWN * 0.4,
                                     color=GREY_B, stroke_width=1.5))
            tau_lbls.add(Tex(rf"${k}\!\cdot\!2\pi$", font_size=18, color=GREY_B).next_to(
                right_line.n2p(x), UP, buff=0.5))
        self.add(tau_lbls)

        t_tr = ValueTracker(0.0)

        def circle_dot():
            t = t_tr.get_value() % TAU
            return Dot(left.c2p(1.5 * np.cos(t), 1.5 * np.sin(t)),
                        color=YELLOW, radius=0.1)

        def circle_trail():
            t = t_tr.get_value()
            if t < 0.02:
                return VMobject()
            # keep last 2π of trail
            start = max(0.0, t - TAU)
            ts = np.linspace(start, t, 80)
            pts = [left.c2p(1.5 * np.cos(s), 1.5 * np.sin(s)) for s in ts]
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=3)

        def line_dot():
            t = t_tr.get_value()
            return Dot(right_line.n2p(t), color=GREEN, radius=0.1)

        def line_trail():
            t = t_tr.get_value()
            if t < 0.02:
                return VMobject()
            ts = np.linspace(0, t, 100)
            pts = [right_line.n2p(s) for s in ts]
            return VMobject().set_points_as_corners(pts).set_color(GREEN).set_stroke(width=3)

        def projection_arrow():
            t = t_tr.get_value()
            return DashedLine(right_line.n2p(t) + DOWN * 0.5,
                              left.c2p(1.5 * np.cos(t % TAU),
                                        1.5 * np.sin(t % TAU)),
                              color=GREY_B, stroke_width=1.5, stroke_opacity=0.5)

        self.add(always_redraw(circle_dot), always_redraw(circle_trail),
                 always_redraw(line_dot), always_redraw(line_trail),
                 always_redraw(projection_arrow))

        info = VGroup(
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$t\bmod 2\pi=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"winding $\lfloor t/2\pi\rfloor=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3).shift(RIGHT * 2.5)
        info[0][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(t_tr.get_value() % TAU))
        info[2][1].add_updater(lambda m: m.set_value(int(t_tr.get_value() // TAU)))
        self.add(info)

        self.play(t_tr.animate.set_value(4 * PI),
                  run_time=7, rate_func=linear)
        self.wait(0.8)
