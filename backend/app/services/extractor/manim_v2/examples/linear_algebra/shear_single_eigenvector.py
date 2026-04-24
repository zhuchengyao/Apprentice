from manim import *
import numpy as np


class ShearSingleEigenvectorExample(Scene):
    """
    Shear [[1, 1], [0, 1]]: only one eigenvector direction (x-axis, λ=1).
    Vectors NOT on x-axis rotate and stretch — not eigenvectors.
    """

    def construct(self):
        title = Tex(r"Shear $[[1, 1], [0, 1]]$: one eigenvector direction",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 4, 1], y_range=[-2, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        S = np.array([[1.0, 1.0], [0.0, 1.0]])

        t_tr = ValueTracker(0.0)

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(2) + t * S

        # Eigenvector on x-axis
        v_eig = np.array([2.0, 0.0])
        def eig_arrow():
            M = M_of()
            p = M @ v_eig
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=6)

        # Non-eigenvector
        v_non = np.array([1.0, 1.5])
        def non_arrow():
            M = M_of()
            p = M @ v_non
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=YELLOW, buff=0, stroke_width=5)

        # Span line for x-axis
        x_span = DashedLine(plane.c2p(-3, 0), plane.c2p(4, 0),
                             color=GREEN, stroke_width=2, stroke_opacity=0.6)
        self.add(x_span)

        self.add(always_redraw(eig_arrow), always_redraw(non_arrow))
        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        info = VGroup(
            Tex(r"$\det(S-\lambda I)=(1-\lambda)^2=0$", font_size=22),
            Tex(r"$\Rightarrow\lambda=1$ (repeated)", color=GREEN, font_size=22),
            Tex(r"eigenspace: $x$-axis only",
                color=GREEN, font_size=22),
            Tex(r"'defective' matrix — 1 direction",
                color=ORANGE, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.play(Write(info))
        self.wait(1.0)
