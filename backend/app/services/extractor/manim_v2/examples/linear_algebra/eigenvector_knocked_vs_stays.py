from manim import *
import numpy as np


class EigenvectorKnockedVsStaysExample(Scene):
    """
    Under a transformation, most vectors get knocked off their span (their
    direction changes). Eigenvectors stay on their original span — only
    scaled. Example: A = [[3, 1], [0, 2]] with eigenvectors (1, 0) and
    (-1, 1).
    """

    def construct(self):
        title = Tex(r"Most vectors: knocked off span; eigenvectors: stay on span",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 4, 1], y_range=[-2, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[3.0, 1.0], [0.0, 2.0]])
        v_eigen = np.array([1.0, 0.0])           # eigenvalue 3
        v_eigen2 = np.array([-1.0, 1.0])         # eigenvalue 2
        v_generic = np.array([1.5, 1.5])

        stage_tr = ValueTracker(0.0)

        def M_of():
            t = stage_tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        # Span lines (dashed) for the two eigenvectors
        eigen_line = DashedLine(plane.c2p(-3, 0), plane.c2p(4, 0),
                                 color=GREEN, stroke_width=2, stroke_opacity=0.55)
        eigen_line2 = DashedLine(plane.c2p(3, -3), plane.c2p(-3, 3),
                                  color=ORANGE, stroke_width=2, stroke_opacity=0.55)
        self.add(eigen_line, eigen_line2)
        self.add(Tex(r"eigenspan 1", color=GREEN, font_size=18).move_to(plane.c2p(3.5, 0.3)))
        self.add(Tex(r"eigenspan 2", color=ORANGE, font_size=18).move_to(plane.c2p(-2.5, 2.3)))

        def e1_arrow():
            M = M_of()
            p = M @ v_eigen
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=GREEN, buff=0, stroke_width=5)

        def e2_arrow():
            M = M_of()
            p = M @ v_eigen2
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=ORANGE, buff=0, stroke_width=5)

        def gen_arrow():
            M = M_of()
            p = M @ v_generic
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=YELLOW, buff=0, stroke_width=5)

        self.add(always_redraw(e1_arrow), always_redraw(e2_arrow), always_redraw(gen_arrow))

        self.wait(0.3)
        self.play(stage_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        info = VGroup(
            Tex(r"GREEN: eigenvector, $\lambda=3$", color=GREEN, font_size=22),
            Tex(r"ORANGE: eigenvector, $\lambda=2$", color=ORANGE, font_size=22),
            Tex(r"YELLOW: generic, knocked off span",
                color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.play(Write(info))
        self.wait(1.0)
