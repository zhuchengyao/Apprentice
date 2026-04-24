from manim import *
import numpy as np


class DeterminantGeometricExample(Scene):
    """
    Determinant of a 2×2 matrix = signed area of parallelogram
    spanned by its columns (or rows). Sign = orientation.

    SINGLE_FOCUS: A = [[a, b], [c, d]] with all 4 entries driven
    by ValueTrackers. always_redraw parallelogram + det value +
    sign (GREEN if positive, RED if negative, with flip animation).
    """

    def construct(self):
        title = Tex(r"$\det A$: signed area of parallelogram",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                            x_length=7, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.2)
        self.play(Create(plane))

        a_tr = ValueTracker(2.0)
        b_tr = ValueTracker(0.5)
        c_tr = ValueTracker(0.5)
        d_tr = ValueTracker(1.5)

        def cols():
            return (np.array([a_tr.get_value(), c_tr.get_value()]),
                    np.array([b_tr.get_value(), d_tr.get_value()]))

        def det():
            return a_tr.get_value() * d_tr.get_value() - b_tr.get_value() * c_tr.get_value()

        def parallelogram():
            v1, v2 = cols()
            det_val = det()
            col = GREEN if det_val > 0 else RED
            return Polygon(plane.c2p(0, 0),
                            plane.c2p(v1[0], v1[1]),
                            plane.c2p(v1[0] + v2[0], v1[1] + v2[1]),
                            plane.c2p(v2[0], v2[1]),
                            color=col, stroke_width=3,
                            fill_color=col, fill_opacity=0.35)

        def col1_arrow():
            v1, _ = cols()
            return Arrow(plane.c2p(0, 0), plane.c2p(v1[0], v1[1]),
                          color=BLUE, buff=0, stroke_width=4)

        def col2_arrow():
            _, v2 = cols()
            return Arrow(plane.c2p(0, 0), plane.c2p(v2[0], v2[1]),
                          color=ORANGE, buff=0, stroke_width=4)

        self.add(always_redraw(parallelogram),
                 always_redraw(col1_arrow),
                 always_redraw(col2_arrow))

        # Matrix + det panel
        def mat_str():
            return rf"$A=\begin{{pmatrix}}{a_tr.get_value():+.2f}&{b_tr.get_value():+.2f}\\{c_tr.get_value():+.2f}&{d_tr.get_value():+.2f}\end{{pmatrix}}$"

        mat_tex = Tex(mat_str(), font_size=28)
        mat_tex.to_corner(UR, buff=0.3).shift(UP * 0.3)
        self.add(mat_tex)
        def update_mat(mob, dt):
            new = Tex(mat_str(), font_size=28).move_to(mat_tex)
            mat_tex.become(new)
            return mat_tex
        mat_tex.add_updater(update_mat)

        info = VGroup(
            VGroup(Tex(r"$\det A=ad-bc=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"area $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"sign $+$: CCW orientation",
                color=GREEN, font_size=20),
            Tex(r"sign $-$: CW orientation (flipped)",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(det()))
        info[1][1].add_updater(lambda m: m.set_value(abs(det())))
        self.add(info)

        # Tour through configurations
        tour = [(2, 0.5, 0.5, 1.5), (1, 1, 0, 1), (2, 1, 1, 2),  # singular-ish
                (1, 0.5, -0.5, 1.5), (-1, 1, 1, 1)]  # negative det
        for (a, b, c, d) in tour:
            self.play(a_tr.animate.set_value(float(a)),
                      b_tr.animate.set_value(float(b)),
                      c_tr.animate.set_value(float(c)),
                      d_tr.animate.set_value(float(d)),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
