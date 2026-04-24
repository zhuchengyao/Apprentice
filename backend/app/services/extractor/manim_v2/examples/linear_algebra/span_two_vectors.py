from manim import *
import numpy as np


class SpanTwoVectorsExample(Scene):
    """
    Span as the set of all linear combinations.

    Two ValueTrackers a and b drive the combination a·v + b·w. Three
    arrows animate in sync: a·v (green), b·w (red), and their tip-to-
    tail sum (yellow) which is the resulting point. A VMobject trace
    collects every visited sum, sweeping out the plane as (a, b) walk
    over a grid of values. Right-column readouts show current (a, b)
    and the sum coordinates.
    """

    def construct(self):
        title = Tex(r"$\mathrm{span}(\vec v, \vec w) = \{a\vec v + b\vec w : a, b \in \mathbb{R}\}$",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # LEFT COLUMN: plane + arrows
        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-3.5, 3.5, 1],
            x_length=8, y_length=6.4,
            background_line_style={"stroke_opacity": 0.3},
        ).shift(LEFT * 1.8 + 0.2 * DOWN)
        self.play(Create(plane))

        v = np.array([2.0, 0.8])
        w = np.array([-0.8, 1.6])

        a_tr = ValueTracker(1.0)
        b_tr = ValueTracker(0.5)

        def av_point():
            a = a_tr.get_value()
            return plane.c2p(a * v[0], a * v[1])

        def bw_point():
            b = b_tr.get_value()
            a = a_tr.get_value()
            return plane.c2p(a * v[0] + b * w[0], a * v[1] + b * w[1])

        origin_pt = plane.c2p(0, 0)

        def av_arrow():
            return Arrow(origin_pt, av_point(), buff=0, color=GREEN,
                         stroke_width=5, max_tip_length_to_length_ratio=0.12)

        def bw_arrow():
            return Arrow(av_point(), bw_point(), buff=0, color=RED,
                         stroke_width=5, max_tip_length_to_length_ratio=0.12)

        def sum_arrow():
            return Arrow(origin_pt, bw_point(), buff=0, color=YELLOW,
                         stroke_width=5, max_tip_length_to_length_ratio=0.12)

        def sum_dot():
            return Dot(bw_point(), color=YELLOW, radius=0.09)

        self.add(always_redraw(av_arrow), always_redraw(bw_arrow),
                 always_redraw(sum_arrow), always_redraw(sum_dot))

        # Trail of visited sums
        trail_points: list[np.ndarray] = []

        def trail():
            path = VMobject(color=YELLOW, stroke_width=2, stroke_opacity=0.5)
            if len(trail_points) >= 2:
                path.set_points_as_corners(trail_points.copy())
            else:
                p = bw_point()
                path.set_points_as_corners([p, p])
            return path

        self.add(always_redraw(trail))

        def record_trail(mobj, dt):
            trail_points.append(bw_point())
            if len(trail_points) > 4000:
                del trail_points[: len(trail_points) - 4000]

        recorder = Mobject()
        recorder.add_updater(record_trail)
        self.add(recorder)

        # RIGHT COLUMN: readouts
        def info_panel():
            a = a_tr.get_value()
            b = b_tr.get_value()
            x = a * v[0] + b * w[0]
            y = a * v[1] + b * w[1]
            return VGroup(
                MathTex(rf"a = {a:+.2f}", color=GREEN, font_size=28),
                MathTex(rf"b = {b:+.2f}", color=RED, font_size=28),
                MathTex(rf"a\vec v + b\vec w", color=YELLOW, font_size=28),
                MathTex(rf"= ({x:+.2f},\; {y:+.2f})",
                        color=YELLOW, font_size=26),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.4, 1.2, 0])

        self.add(always_redraw(info_panel))

        # Scan (a, b) over a lattice to sweep out the plane
        targets = [
            (2.0, 1.0), (2.0, -1.0), (-2.0, -1.0), (-2.0, 1.0),
            (2.0, 1.5), (-1.5, -2.0), (1.5, 2.0), (-2.0, 1.5), (0.0, 0.0),
        ]
        for (av, bv) in targets:
            self.play(a_tr.animate.set_value(av),
                      b_tr.animate.set_value(bv),
                      run_time=1.4, rate_func=smooth)

        recorder.clear_updaters()

        conclusion = MathTex(
            r"\text{span}(\vec v, \vec w) = \mathbb{R}^2",
            font_size=32, color=YELLOW,
        ).move_to([4.4, -2.6, 0])
        self.play(Write(conclusion))
        self.wait(1.0)
