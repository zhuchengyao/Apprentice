from manim import *
import numpy as np


class JordanCurveTheoremExample(Scene):
    """
    Jordan curve theorem: every simple closed curve divides the plane
    into exactly 2 connected regions (inside and outside). Even for a
    wildly curvy simple closed curve, the inside/outside test can be
    done by ray-casting — count intersections of an outward ray.

    SINGLE_FOCUS: wobbly simple closed curve. 6 test points colored
    by inside/outside via ray-cast. ValueTracker scan_tr moves a
    probe along a horizontal line; current side shown.
    """

    def construct(self):
        title = Tex(r"Jordan curve theorem: simple closed curve $\Rightarrow$ 2 regions",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-2.5, 2.5, 1],
                            x_length=9, y_length=5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(DOWN * 0.1)
        self.play(Create(plane))

        # Define wobbly simple closed curve r(θ) = 2 + 0.5 cos 3θ + 0.3 sin 5θ
        def curve_xy(t):
            r = 2.0 + 0.5 * np.cos(3 * t) + 0.3 * np.sin(5 * t)
            return np.array([r * np.cos(t), r * np.sin(t) * 0.7])

        curve = ParametricFunction(
            lambda t: plane.c2p(*curve_xy(t)),
            t_range=[0, TAU], color=BLUE, stroke_width=3)
        self.play(Create(curve))

        # Is point inside? Use ray cast to +infinity along +x and count
        # intersections of curve r(θ) with horizontal ray y=const, x>p_x.
        def inside(px, py):
            # Sample curve
            ts = np.linspace(0, TAU, 500, endpoint=False)
            count = 0
            prev = curve_xy(ts[0])
            for t in ts[1:]:
                cur = curve_xy(t)
                # edge from prev to cur; does it cross horizontal line y=py
                # in the region x>=px?
                y1, y2 = prev[1], cur[1]
                if (y1 > py) != (y2 > py):
                    # compute x of intersection
                    alpha = (py - y1) / (y2 - y1)
                    x_cross = prev[0] + alpha * (cur[0] - prev[0])
                    if x_cross > px:
                        count += 1
                prev = cur
            return count % 2 == 1

        test_pts = [(0.0, 0.0),
                    (1.5, 0.7),
                    (-2.3, -0.3),
                    (2.8, 1.8),
                    (-3.2, 1.2),
                    (0.6, -1.1)]
        test_dots = VGroup()
        for (x, y) in test_pts:
            col = GREEN if inside(x, y) else RED
            d = Dot(plane.c2p(x, y), color=col, radius=0.1)
            test_dots.add(d)
            lbl = Tex("in" if inside(x, y) else "out", color=col,
                      font_size=16).next_to(d, UP, buff=0.1)
            test_dots.add(lbl)
        self.play(FadeIn(test_dots))

        scan_tr = ValueTracker(-3.5)

        def probe():
            x = scan_tr.get_value()
            y = -1.9
            col = GREEN if inside(x, y) else RED
            return Dot(plane.c2p(x, y), color=col, radius=0.14)

        def ray():
            x = scan_tr.get_value()
            y = -1.9
            return DashedLine(plane.c2p(x, y), plane.c2p(3.9, y),
                              color=YELLOW, stroke_width=2)

        self.add(always_redraw(probe), always_redraw(ray))

        info = VGroup(
            Tex(r"ray-cast test: count crossings",
                color=YELLOW, font_size=22),
            Tex(r"odd $\Rightarrow$ inside (GREEN)",
                color=GREEN, font_size=22),
            Tex(r"even $\Rightarrow$ outside (RED)",
                color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        self.add(info)

        self.play(scan_tr.animate.set_value(3.5),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
