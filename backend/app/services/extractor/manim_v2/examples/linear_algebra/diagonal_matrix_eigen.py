from manim import *
import numpy as np


class DiagonalMatrixEigenExample(Scene):
    """
    For diagonal matrix D = diag(λ_1, λ_2), standard basis vectors are
    the eigenvectors: D î = λ_1 î, D ĵ = λ_2 ĵ.
    """

    def construct(self):
        title = Tex(r"Diagonal matrix: standard basis $=$ eigenvectors",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-1, 4, 1], y_range=[-1, 3, 1],
                            x_length=8, y_length=5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 1.5 + DOWN * 0.2)
        self.play(Create(plane))

        D = np.array([[3.0, 0.0], [0.0, 2.0]])

        t_tr = ValueTracker(0.0)

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(2) + t * D

        def i_arrow():
            M = M_of()
            p = M @ np.array([1, 0])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=6)

        def j_arrow():
            M = M_of()
            p = M @ np.array([0, 1])
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=RED, buff=0, stroke_width=6)

        self.add(always_redraw(i_arrow), always_redraw(j_arrow))
        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.4)

        # Right: formulas
        info = VGroup(
            Tex(r"$D=\begin{pmatrix}3&0\\0&2\end{pmatrix}$", font_size=28),
            Tex(r"$D\hat\imath=3\hat\imath$: $\lambda=3$",
                color=GREEN, font_size=22),
            Tex(r"$D\hat\jmath=2\hat\jmath$: $\lambda=2$",
                color=RED, font_size=22),
            Tex(r"Powers are easy: $D^k=\text{diag}(\lambda_1^k, \lambda_2^k)$",
                color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        self.play(Write(info))
        self.wait(1.0)
