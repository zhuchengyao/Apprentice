from manim import *
import numpy as np


class NullSpaceKernelLineExample(Scene):
    """
    For matrix A = [[1, -1], [-1, 1]] (rank 1, det 0), the null space
    (kernel) is the set of all x with Ax = 0. Here that's the line
    x = y (direction (1, 1)).

    Visualize: 18 vectors along that line, all map to 0 after A.
    """

    def construct(self):
        title = Tex(r"Null space = $\{\vec x : A\vec x=\vec 0\}$ (kernel)",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 5, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[1.0, -1.0], [-1.0, 1.0]])  # det = 0

        # Null space direction: (1, 1) — vectors along x=y map to 0.
        vec_dir = np.array([1.0, 1.0]) / np.sqrt(2)
        null_vectors = []
        for a in np.linspace(-4, 4, 18):
            null_vectors.append(a * vec_dir)

        # Phase 1: show null space vectors highlighted
        null_line = Line(plane.c2p(-3, -3), plane.c2p(3, 3),
                          color=YELLOW, stroke_width=4)
        null_lbl = Tex(r"null space", color=YELLOW,
                        font_size=24).move_to(plane.c2p(3.2, 2.6))

        # Show vectors
        vector_arrows = VGroup()
        for v in null_vectors:
            col = interpolate_color(PINK, YELLOW,
                                     0.5 + 0.5 * v[0] / 4)
            vector_arrows.add(Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                                      color=col, buff=0, stroke_width=2,
                                      max_tip_length_to_length_ratio=0.2))

        self.play(Create(vector_arrows))
        self.wait(0.4)
        self.play(Create(null_line), Write(null_lbl))
        self.wait(0.5)

        # Apply A: all should go to 0
        t_tr = ValueTracker(0.0)

        def arrows_transformed():
            t = t_tr.get_value()
            M = (1 - t) * np.eye(2) + t * A
            grp = VGroup()
            for i, v in enumerate(null_vectors):
                v_now = M @ v
                col = interpolate_color(PINK, YELLOW,
                                         0.5 + 0.5 * v[0] / 4)
                if np.linalg.norm(v_now) < 0.1:
                    grp.add(Dot(plane.c2p(v_now[0], v_now[1]),
                                  color=col, radius=0.08))
                else:
                    grp.add(Arrow(plane.c2p(0, 0), plane.c2p(v_now[0], v_now[1]),
                                   color=col, buff=0, stroke_width=2,
                                   max_tip_length_to_length_ratio=0.2))
            return grp

        self.remove(vector_arrows)
        self.add(always_redraw(arrows_transformed))
        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        # All collapse to origin
        stamp = Tex(r"all null-space vectors $\to \vec 0$",
                     color=YELLOW, font_size=24).to_edge(DOWN, buff=0.4)
        self.play(Write(stamp))
        self.wait(1.0)

        info = VGroup(
            Tex(r"$A=\begin{pmatrix}1&-1\\-1&1\end{pmatrix}$", font_size=22),
            Tex(r"null space: span$(1, 1)$",
                color=YELLOW, font_size=22),
            Tex(r"$A\vec x=\vec 0$ iff $\vec x\in$ null space",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        self.play(Write(info))
        self.wait(0.5)
