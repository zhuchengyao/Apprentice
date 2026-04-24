from manim import *
import numpy as np


class AreaScaleFactorOnBlobExample(Scene):
    """
    A linear transformation scales ALL areas by the same factor.
    Demonstrate with a blob of area 1 morphing into a blob of area
    |det A| under matrix A = [[2, -1], [1, 1]] (det = 3).

    SINGLE_FOCUS: BLUE blob. ValueTracker t_tr applies A gradually.
    Label changes from "Area" to "3·Area".
    """

    def construct(self):
        title = Tex(r"Linear transform scales all areas by $|\det A|$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 5, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[2.0, -1.0], [1.0, 1.0]])
        det_A = np.linalg.det(A)

        t_tr = ValueTracker(0.0)

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        # Blob: irregular closed curve
        np.random.seed(7)
        base_pts = []
        for theta in np.linspace(0, TAU, 50, endpoint=False):
            r = 1.0 + 0.25 * np.sin(3 * theta + 0.7) + 0.15 * np.cos(5 * theta)
            base_pts.append(np.array([r * np.cos(theta) + 1.5, r * np.sin(theta) + 0.5]))

        def blob():
            M = M_of()
            pts = [plane.c2p(*(M @ p)) for p in base_pts]
            return Polygon(*pts, color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.35)

        self.add(always_redraw(blob))

        # Dynamic area label
        def area_lbl():
            t = t_tr.get_value()
            factor = 1 + t * (abs(det_A) - 1)
            center_orig = np.array([1.5, 0.5])
            M = M_of()
            center_now = M @ center_orig
            txt = r"Area" if t < 0.05 else rf"${factor:.2f}\cdot$Area"
            return Tex(txt, color=YELLOW, font_size=24).move_to(
                plane.c2p(*center_now))

        self.add(always_redraw(area_lbl))

        info = VGroup(
            Tex(r"$A=\begin{pmatrix}2&-1\\1&1\end{pmatrix}$", font_size=24),
            Tex(rf"$\det A={det_A:.1f}$", color=YELLOW, font_size=24),
            VGroup(Tex(r"$t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(r"area scale $=|\det A|$",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[2][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        self.add(info)

        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.8)
