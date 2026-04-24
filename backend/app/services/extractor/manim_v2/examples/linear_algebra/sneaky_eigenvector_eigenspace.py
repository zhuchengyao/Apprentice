from manim import *
import numpy as np


class SneakyEigenvectorEigenspaceExample(Scene):
    """
    A has another eigenvector along (-1, 1) direction with eigenvalue 2.
    The 'sneaky' eigenspace — not obvious from the matrix.
    """

    def construct(self):
        title = Tex(r"Sneaky eigenvector: $\lambda=2$ along $(-1, 1)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 4, 1], y_range=[-2, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[3.0, 1.0], [0.0, 2.0]])
        v_dir = np.array([-1.0, 1.0])

        # Span line
        line = Line(plane.c2p(3, -3), plane.c2p(-3, 3),
                     color=ORANGE, stroke_width=3)
        self.add(line)
        self.add(Tex(r"span $(-1, 1)$", color=ORANGE, font_size=20).move_to(plane.c2p(-2.5, 2.5)))

        # Several dots on the line
        dot_scales = [-1.5, -0.8, 0.5, 1.2, 1.8]

        t_tr = ValueTracker(0.0)

        def M_of():
            t = t_tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        def dots_on_line():
            M = M_of()
            grp = VGroup()
            for s in dot_scales:
                p = M @ (s * v_dir)
                grp.add(Dot(plane.c2p(p[0], p[1]), color=ORANGE, radius=0.11))
            return grp

        self.add(always_redraw(dots_on_line))

        self.wait(0.3)
        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        # Show 2x scaling
        scale_note = Tex(r"Each dot scales by $\lambda=2$ (stays on line)",
                          color=ORANGE, font_size=22).to_edge(DOWN, buff=0.5)
        self.play(Write(scale_note))

        info = VGroup(
            Tex(r"$A\vec v = 2\vec v$ for $\vec v$ on this line",
                color=ORANGE, font_size=22),
            Tex(r"$\lambda=2$ eigenspace",
                color=ORANGE, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.play(Write(info))
        self.wait(1.0)
