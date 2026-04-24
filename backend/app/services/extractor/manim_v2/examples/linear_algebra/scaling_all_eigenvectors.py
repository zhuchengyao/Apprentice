from manim import *
import numpy as np


class ScalingAllEigenvectorsExample(Scene):
    """
    Pure scaling A = k·I scales all vectors by k. Every vector is an
    eigenvector with eigenvalue k.
    """

    def construct(self):
        title = Tex(r"Scaling $A=kI$: every vector is an eigenvector",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                            x_length=8, y_length=5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.2)
        self.play(Create(plane))

        k = 2.0
        A = k * np.eye(2)

        v_dirs = [(1, 0), (0, 1), (1, 1), (-1, 0.5), (0.5, -1), (-0.8, -0.6)]
        colors = [GREEN, RED, BLUE, ORANGE, PURPLE, TEAL]

        t_tr = ValueTracker(0.0)

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        def arrows():
            M = M_of()
            grp = VGroup()
            for v, col in zip(v_dirs, colors):
                v = np.array(v)
                p = M @ v
                grp.add(Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                                color=col, buff=0, stroke_width=4))
            return grp

        self.add(always_redraw(arrows))
        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        info = VGroup(
            Tex(r"$A=2I=\begin{pmatrix}2&0\\0&2\end{pmatrix}$", font_size=24),
            Tex(r"$A\vec v=2\vec v$ for all $\vec v$",
                color=YELLOW, font_size=22),
            Tex(r"$\lambda=2$ with eigenspace $=\mathbb{R}^2$",
                color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.play(Write(info))
        self.wait(1.0)
