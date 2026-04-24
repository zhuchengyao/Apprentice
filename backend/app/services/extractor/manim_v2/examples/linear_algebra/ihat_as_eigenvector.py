from manim import *
import numpy as np


class IHatAsEigenvectorExample(Scene):
    """
    For A with first column (a, 0), î maps to a·î. î is an eigenvector
    with eigenvalue a. More generally, all vectors on the x-axis are
    eigenvectors with eigenvalue a.
    """

    def construct(self):
        title = Tex(r"$\hat\imath$ as eigenvector: all of x-axis is eigenspace",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 4, 1], y_range=[-2, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[3.0, 1.0], [0.0, 2.0]])

        # x-axis dots - they're all eigenvectors
        x_axis_dots = VGroup(*[Dot(plane.c2p(x, 0), color=GREEN, radius=0.1)
                                for x in [-2, -1, 0.5, 1, 2, 3]])
        self.add(x_axis_dots)

        t_tr = ValueTracker(0.0)

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        def x_axis_transformed():
            M = M_of()
            grp = VGroup()
            for x in [-2, -1, 0.5, 1, 2, 3]:
                p = M @ np.array([x, 0])
                grp.add(Dot(plane.c2p(p[0], p[1]), color=GREEN, radius=0.1))
            return grp

        def x_line():
            M = M_of()
            p_neg = M @ np.array([-3, 0])
            p_pos = M @ np.array([4, 0])
            return Line(plane.c2p(p_neg[0], p_neg[1]),
                         plane.c2p(p_pos[0], p_pos[1]),
                         color=GREEN, stroke_width=3)

        self.add(always_redraw(x_line), always_redraw(x_axis_transformed))
        self.remove(x_axis_dots)

        self.wait(0.3)
        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        info = VGroup(
            Tex(r"$A=\begin{pmatrix}3&1\\0&2\end{pmatrix}$", font_size=24),
            Tex(r"$A\hat\imath = 3\hat\imath$ ($\lambda=3$)",
                color=GREEN, font_size=22),
            Tex(r"All $x$-axis vectors: $\lambda=3$",
                color=GREEN, font_size=22),
            Tex(r"(eigenspace = x-axis)",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.play(Write(info))
        self.wait(1.0)
