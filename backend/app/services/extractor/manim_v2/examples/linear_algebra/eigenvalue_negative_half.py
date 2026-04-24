from manim import *
import numpy as np


class EigenvalueNegativeHalfExample(Scene):
    """
    Eigenvalues can be negative — means the eigenvector FLIPS direction
    while staying on span. Example: A with eigenvalue -0.5.
    """

    def construct(self):
        title = Tex(r"Negative eigenvalue: eigenvector flips (stays on span)",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                            x_length=8, y_length=5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.2)
        self.play(Create(plane))

        # A with eigenvector (1, 0), eigenvalue -0.5 along x-axis
        # and eigenvector (0, 1), eigenvalue 2 along y.
        # A = diag(-0.5, 2)
        A = np.array([[-0.5, 0.0], [0.0, 2.0]])

        # Eigenvector on x-axis
        v_eig = np.array([2.0, 0.0])
        span_line = DashedLine(plane.c2p(-3, 0), plane.c2p(3, 0),
                                color=GREEN, stroke_width=2, stroke_opacity=0.6)
        self.add(span_line)

        t_tr = ValueTracker(0.0)

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        def v_arrow():
            M = M_of()
            p = M @ v_eig
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=6)

        self.add(always_redraw(v_arrow))

        self.wait(0.3)
        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        info = VGroup(
            Tex(r"$A=\begin{pmatrix}-0.5&0\\0&2\end{pmatrix}$", font_size=24),
            Tex(r"$\hat\imath$ direction: $\lambda=-0.5$",
                color=GREEN, font_size=22),
            Tex(r"flipped AND scaled by $1/2$",
                color=GREEN, font_size=20),
            Tex(r"still on original span!",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.play(Write(info))
        self.wait(1.0)
