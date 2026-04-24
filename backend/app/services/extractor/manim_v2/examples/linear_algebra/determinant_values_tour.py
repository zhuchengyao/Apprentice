from manim import *
import numpy as np


class DeterminantValuesTourExample(Scene):
    """
    Tour a family of 2×2 matrices and watch their determinants:
    det=2 (stretch), det=-1 (flip), det=3, det=0.5, det=0 (degenerate).

    SINGLE_FOCUS: YELLOW unit square deforms; det value shown both
    inside the deformed square and in the side panel.
    """

    def construct(self):
        title = Tex(r"Tour of determinants: area scale + orientation",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=8, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        configs = [
            ("identity", np.eye(2)),
            ("det = 6", np.array([[3.0, 0.0], [2.0, 2.0]])),
            ("det = -2", np.array([[-1.0, -1.0], [1.0, -1.0]])),
            ("det = 3", np.array([[0.0, -1.5], [2.0, 1.0]])),
            ("det = 0.5", np.array([[0.5, -0.5], [0.5, 0.5]])),
            ("det = 0", np.array([[4.0, 2.0], [2.0, 1.0]])),
        ]

        idx_tr = ValueTracker(0.0)

        def M_of():
            s = idx_tr.get_value()
            k = int(s)
            frac = s - k
            k_next = min(len(configs) - 1, k + 1)
            return (1 - frac) * configs[k][1] + frac * configs[k_next][1]

        def det_now():
            return float(np.linalg.det(M_of()))

        def square():
            M = M_of()
            pts = [plane.c2p(*(M @ p)) for p in
                    [np.array([0, 0]), np.array([1, 0]),
                     np.array([1, 1]), np.array([0, 1])]]
            d = det_now()
            col = GREEN if d > 0.05 else (RED if d < -0.05 else GREY_D)
            return Polygon(*pts, color=col, stroke_width=3,
                            fill_color=col, fill_opacity=0.45)

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=5)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=RED, buff=0, stroke_width=5)

        self.add(always_redraw(square), always_redraw(i_arrow), always_redraw(j_arrow))

        # Dynamic det label inside
        def det_lbl():
            M = M_of()
            pts = [M @ p for p in
                    [np.array([0, 0]), np.array([1, 0]),
                     np.array([1, 1]), np.array([0, 1])]]
            center = (pts[0] + pts[2]) / 2
            d = det_now()
            return Tex(rf"$\det={d:+.2f}$", color=YELLOW, font_size=22).move_to(
                plane.c2p(*center))
        self.add(always_redraw(det_lbl))

        info = VGroup(
            VGroup(Tex(r"config $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\det A=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"GREEN: preserve orientation",
                color=GREEN, font_size=18),
            Tex(r"RED: flipped",
                color=RED, font_size=18),
            Tex(r"GREY: collapsed (det=0)",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)

        def idx_now():
            return max(0, min(len(configs) - 1, int(round(idx_tr.get_value()))))
        info[0][1].add_updater(lambda m: m.set_value(idx_now()))
        info[1][1].add_updater(lambda m: m.set_value(det_now()))
        self.add(info)

        for k in range(1, len(configs)):
            self.play(idx_tr.animate.set_value(float(k)),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.5)
