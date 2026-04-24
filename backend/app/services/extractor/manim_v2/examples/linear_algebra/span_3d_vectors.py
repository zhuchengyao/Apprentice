from manim import *
import numpy as np


class Span3DVectorsExample(ThreeDScene):
    """
    Span of 3 vectors in ℝ³:
      - 3 linearly independent → span = ℝ³ (full volume)
      - 3 in a plane → span = 2D plane
      - 3 collinear → span = 1D line

    3D scene: three arrow vectors, always_redraw parallelepiped
    from their combinations; ValueTracker s_tr morphs through
    3 configurations via Transform.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-35 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 3, 1], y_range=[-2, 3, 1],
                           z_range=[-1, 3, 1],
                           x_length=4, y_length=4, z_length=3)
        self.add(axes)

        M_full = np.array([[1.5, 0.3, 0.2],
                            [0.2, 1.8, 0.3],
                            [0.3, 0.4, 1.2]])  # det != 0
        M_plane = np.array([[1.5, 1.0, 0.5],
                             [0.0, 1.5, 0.75],
                             [0.0, 0.0, 0.0]])  # third row 0, plane in xy
        M_line = np.array([[1.0, 2.0, 0.5],
                            [0.5, 1.0, 0.25],
                            [0.25, 0.5, 0.125]])  # cols all parallel to (1, 0.5, 0.25)

        state = {"M": M_full, "desc": "3D span"}

        def cols():
            M = state["M"]
            return M[:, 0], M[:, 1], M[:, 2]

        def col_line(idx, color):
            def f():
                c1, c2, c3 = cols()
                vec = [c1, c2, c3][idx]
                return Line(ORIGIN, axes.c2p(*vec), color=color,
                              stroke_width=6)
            return f

        def parallelepiped():
            a, b, c = cols()
            corners = [np.zeros(3), a, b, c,
                       a + b, a + c, b + c, a + b + c]
            faces_idx = [(0, 1, 4, 2), (0, 1, 5, 3),
                         (0, 2, 6, 3), (3, 5, 7, 6),
                         (1, 4, 7, 5), (2, 4, 7, 6)]
            grp = VGroup()
            for face in faces_idx:
                pts3d = [axes.c2p(*corners[i]) for i in face]
                grp.add(Polygon(*pts3d, color=YELLOW,
                                 fill_opacity=0.2, stroke_width=2))
            return grp

        self.add(always_redraw(col_line(0, RED)),
                  always_redraw(col_line(1, GREEN)),
                  always_redraw(col_line(2, BLUE)),
                  always_redraw(parallelepiped))

        title = Tex(r"Span of three vectors in $\mathbb R^3$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def make_panel():
            M = state["M"]
            det = np.linalg.det(M)
            rank = np.linalg.matrix_rank(M)
            spans = {3: "all of $\\mathbb R^3$",
                      2: "a plane",
                      1: "a line",
                      0: "a point"}
            return VGroup(
                MathTex(rf"|\det| = {abs(det):.3f}",
                         color=YELLOW, font_size=24),
                MathTex(rf"\text{{rank}} = {rank}",
                         color=GREEN, font_size=24),
                Tex(rf"span = {spans[rank]}",
                     color=BLUE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.4)

        panel = make_panel()
        self.add_fixed_in_frame_mobjects(panel)

        self.begin_ambient_camera_rotation(rate=0.18)
        self.wait(2.5)

        # Morph to plane configuration
        state["M"] = M_plane
        new_panel = make_panel()
        self.add_fixed_in_frame_mobjects(new_panel)
        self.play(Transform(panel, new_panel), run_time=0.2)
        self.wait(2.5)

        # Morph to line configuration
        state["M"] = M_line
        new_panel = make_panel()
        self.add_fixed_in_frame_mobjects(new_panel)
        self.play(Transform(panel, new_panel), run_time=0.2)
        self.wait(2.5)

        self.stop_ambient_camera_rotation()
