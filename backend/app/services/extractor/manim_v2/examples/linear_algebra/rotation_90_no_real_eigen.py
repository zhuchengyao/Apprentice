from manim import *
import numpy as np


class Rotation90NoRealEigenExample(Scene):
    """
    90° rotation has no real eigenvectors (every vector changes direction).
    Char poly: det(R-λI) = λ² + 1 = 0 → λ = ±i (complex).
    """

    def construct(self):
        title = Tex(r"$90°$ rotation: no real eigenvectors (complex $\lambda=\pm i$)",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                            x_length=5, y_length=5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.0 + DOWN * 0.2)
        self.play(Create(plane))

        R = np.array([[0.0, -1.0], [1.0, 0.0]])

        # Try several vectors; all rotate — none stay on span
        v_dirs = [(1, 0), (1, 1), (-1, 2), (3, -1)]
        colors = [BLUE, GREEN, ORANGE, RED]

        t_tr = ValueTracker(0.0)

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(2) + t * R

        def arrows():
            M = M_of()
            grp = VGroup()
            for v, col in zip(v_dirs, colors):
                v = np.array(v) / max(np.linalg.norm(v), 0.5) * 1.2
                p = M @ v
                grp.add(Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                                color=col, buff=0, stroke_width=4))
            return grp

        self.add(always_redraw(arrows))

        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.4)

        # Right: characteristic polynomial computation
        char_poly = VGroup(
            Tex(r"$R=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$", font_size=24),
            Tex(r"$R-\lambda I=\begin{pmatrix}-\lambda&-1\\1&-\lambda\end{pmatrix}$",
                font_size=22),
            Tex(r"$\det = \lambda^2+1$", font_size=24),
            Tex(r"$\lambda^2+1=0\Rightarrow \lambda=\pm i$",
                color=RED, font_size=26),
            Tex(r"no real eigenvectors!",
                color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        self.play(Write(char_poly))
        self.wait(1.0)
