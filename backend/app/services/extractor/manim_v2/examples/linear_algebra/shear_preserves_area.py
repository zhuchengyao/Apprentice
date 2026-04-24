from manim import *
import numpy as np


class ShearPreservesAreaExample(Scene):
    """
    Shear matrix [[1, 0], [k, 1]] preserves area (det = 1) regardless
    of shear strength k. Unit square becomes a parallelogram with
    same base and height → same area 1.

    ValueTracker k_tr sweeps k through 0, 0.5, 1, 2, -1.
    """

    def construct(self):
        title = Tex(r"Shear $[[1, 0], [k, 1]]$: $\det=1$, area preserved",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 4, 1], y_range=[-2, 3, 1],
                            x_length=8.5, y_length=5.0,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.3)
        self.play(Create(plane))

        k_tr = ValueTracker(0.0)

        def M_of():
            k = k_tr.get_value()
            return np.array([[1.0, k], [0.0, 1.0]])

        def square():
            M = M_of()
            pts = [plane.c2p(*(M @ p)) for p in
                    [np.array([0, 0]), np.array([1, 0]),
                     np.array([1, 1]), np.array([0, 1])]]
            return Polygon(*pts, color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.4)

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=4)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=RED, buff=0, stroke_width=4)

        self.add(always_redraw(square), always_redraw(i_arrow), always_redraw(j_arrow))

        # Base and height lines
        def height_line():
            M = M_of()
            return DashedLine(
                plane.c2p((M @ np.array([0, 1]))[0], 0),
                plane.c2p(*(M @ np.array([0, 1]))),
                color=GREY_B, stroke_width=2)

        self.add(always_redraw(height_line))

        info = VGroup(
            VGroup(Tex(r"$k=$", font_size=24),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=24).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"base $= 1$", color=GREEN, font_size=22),
            Tex(r"height $= 1$", color=RED, font_size=22),
            Tex(r"area $=1\cdot 1=1$", color=YELLOW, font_size=24),
            Tex(r"$\det=1\cdot 1-0\cdot k=1$",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(k_tr.get_value()))
        self.add(info)

        for kval in [0.5, 1.0, 2.0, -1.0, 0.5]:
            self.play(k_tr.animate.set_value(kval),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
