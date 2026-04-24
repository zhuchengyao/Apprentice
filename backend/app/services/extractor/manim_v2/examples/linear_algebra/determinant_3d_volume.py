from manim import *
import numpy as np


class Determinant3DVolumeExample(ThreeDScene):
    """
    |det A| = volume of the parallelepiped spanned by the columns
    of a 3×3 matrix A.

    3D scene:
      3 basis vectors â, b̂, ĉ (color-coded), always_redraw
      parallelepiped + a×b+...+c cross-products; ValueTracker s_tr
      interpolates A(s) = (1-s) I + s M between identity (volume 1)
      and a shearing matrix with det = 3, then one with det = 0
      (degenerate).
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-35 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 3, 1], y_range=[-2, 3, 1],
                           z_range=[-1, 3, 1],
                           x_length=4, y_length=4, z_length=3)
        self.add(axes)

        M_good = np.array([[1.5, 0.5, 0.0],
                            [0.0, 2.0, 0.0],
                            [0.5, 0.5, 1.0]])  # det = 1.5 * 2 * 1 = 3
        M_degen = np.array([[1.0, 2.0, 0.0],
                             [0.5, 1.0, 0.0],
                             [0.0, 0.0, 1.0]])  # det = 0

        I3 = np.eye(3)
        s_tr = ValueTracker(0.0)
        state = {"target": M_good}

        def A():
            s = s_tr.get_value()
            return (1 - s) * I3 + s * state["target"]

        def col_vec(i, color):
            def f():
                a = A()[:, i]
                return Line(ORIGIN, axes.c2p(*a), color=color,
                              stroke_width=6)
            return f

        def parallelepiped():
            M = A()
            a, b, c = M[:, 0], M[:, 1], M[:, 2]
            corners = [
                np.zeros(3),
                a, b, c,
                a + b, a + c, b + c, a + b + c,
            ]
            # 6 faces (pairs of triangles each)
            faces_idx = [
                (0, 1, 4, 2),  # bottom
                (0, 1, 5, 3),
                (0, 2, 6, 3),
                (3, 5, 7, 6),
                (1, 4, 7, 5),
                (2, 4, 7, 6),
            ]
            grp = VGroup()
            for face in faces_idx:
                pts3d = [axes.c2p(*corners[i]) for i in face]
                grp.add(Polygon(*pts3d, color=YELLOW,
                                 fill_opacity=0.2, stroke_width=2))
            return grp

        self.add(always_redraw(col_vec(0, RED)),
                  always_redraw(col_vec(1, GREEN)),
                  always_redraw(col_vec(2, BLUE)),
                  always_redraw(parallelepiped))

        # Fixed-frame panel
        title = Tex(r"$|\det A| = $ volume of parallelepiped",
                    font_size=26)
        title.to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def make_panel():
            s = s_tr.get_value()
            M = A()
            d = np.linalg.det(M)
            panel = VGroup(
                MathTex(rf"s = {s:.2f}", color=WHITE, font_size=24),
                MathTex(rf"|\det A| = {abs(d):.3f}",
                         color=YELLOW, font_size=26),
                Tex(r"col 1 = RED, col 2 = GREEN, col 3 = BLUE",
                     font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            panel.to_corner(DR, buff=0.4)
            return panel

        panel = make_panel()
        self.add_fixed_in_frame_mobjects(panel)

        self.begin_ambient_camera_rotation(rate=0.2)

        # Phase 1: identity → good matrix
        self.play(s_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        new_panel = make_panel()
        self.add_fixed_in_frame_mobjects(new_panel)
        self.play(Transform(panel, new_panel), run_time=0.2)
        self.wait(0.6)

        # Phase 2: reset and morph to degenerate
        state["target"] = M_degen
        self.play(s_tr.animate.set_value(0), run_time=1.0)
        self.play(s_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        new_panel = make_panel()
        self.add_fixed_in_frame_mobjects(new_panel)
        self.play(Transform(panel, new_panel), run_time=0.2)
        self.wait(1.0)

        self.stop_ambient_camera_rotation()
