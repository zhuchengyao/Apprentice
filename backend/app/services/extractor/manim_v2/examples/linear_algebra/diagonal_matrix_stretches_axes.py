from manim import *
import numpy as np


class DiagonalMatrixStretchesAxesExample(Scene):
    """
    A diagonal matrix [[a, 0], [0, d]] stretches the x-axis by a and
    y-axis by d, independently. Decompose into two sequential steps.
    Det = a·d = product of diagonal entries.

    SINGLE_FOCUS: [[3, 0], [0, 2]]. ValueTracker stage_tr: 0=identity,
    1=x-stretched (î→(3, 0), ĵ still (0, 1)), 2=y-stretched (ĵ→(0, 2)).
    """

    def construct(self):
        title = Tex(r"Diagonal matrix: $\det=a\cdot d$ (x-stretch $\times$ y-stretch)",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 5, 1], y_range=[-2, 3, 1],
                            x_length=9, y_length=5.0,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.3)
        self.play(Create(plane))

        a_val, d_val = 3.0, 2.0

        stage_tr = ValueTracker(0.0)

        def M_of():
            s = stage_tr.get_value()
            if s <= 1:
                return np.diag([1 + s * (a_val - 1), 1.0])
            alpha = s - 1
            return np.diag([a_val, 1 + alpha * (d_val - 1)])

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

        def square():
            M = M_of()
            pts = [plane.c2p(*(M @ p)) for p in
                    [np.array([0, 0]), np.array([1, 0]),
                     np.array([1, 1]), np.array([0, 1])]]
            return Polygon(*pts, color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.3)

        self.add(always_redraw(square), always_redraw(i_arrow), always_redraw(j_arrow))

        # Width and height braces (simple, always based on current square)
        def width_height_labels():
            M = M_of()
            w = M[0, 0]
            h = M[1, 1]
            grp = VGroup(
                Tex(rf"width $={w:.1f}$", color=GREEN, font_size=22).move_to(
                    plane.c2p(w / 2, -0.5)),
                Tex(rf"height $={h:.1f}$", color=RED, font_size=22).move_to(
                    plane.c2p(w + 0.6, h / 2)),
            )
            return grp

        self.add(always_redraw(width_height_labels))

        def area_str():
            M = M_of()
            w, h = M[0, 0], M[1, 1]
            return rf"$\text{{area}}={w:.1f}\cdot {h:.1f}={w * h:.1f}$"

        area_tex = Tex(area_str(), color=YELLOW, font_size=26).to_edge(DOWN, buff=0.3)
        self.add(area_tex)
        def update_area(mob, dt):
            new = Tex(area_str(), color=YELLOW, font_size=26).move_to(area_tex)
            area_tex.become(new)
            return area_tex
        area_tex.add_updater(update_area)

        info = VGroup(
            Tex(r"$A=\begin{pmatrix}3&0\\0&2\end{pmatrix}$", font_size=24),
            Tex(r"$\det A=3\cdot 2=6$", color=YELLOW, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.add(info)

        self.play(stage_tr.animate.set_value(1.0), run_time=2.2, rate_func=smooth)
        self.wait(0.5)
        self.play(stage_tr.animate.set_value(2.0), run_time=2.2, rate_func=smooth)
        self.wait(0.8)
