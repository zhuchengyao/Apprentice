from manim import *
import numpy as np


class ColumnsSpanFullRankExample(ThreeDScene):
    """
    3D matrix columns that span all of ℝ³ (full rank = 3). Visualize
    the 3 column vectors as arrows from origin; parallelepiped they
    span has nonzero volume (det ≠ 0).

    Compare with a degenerate case where 3 columns are coplanar
    (rank 2, det = 0).
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.06)

        axes = ThreeDAxes(x_range=[-1, 3, 1], y_range=[-1, 3, 1], z_range=[-1, 3, 1],
                          x_length=5, y_length=5, z_length=5)
        self.add(axes)

        # Full-rank columns
        A_full = np.array([[2, 1, 0],
                            [0, 2, 1],
                            [1, 0, 2]], dtype=float).T  # as columns

        # Rank-2: third column = sum of first two
        A_rank2 = np.array([[2, 1, 3],
                             [0, 2, 2],
                             [1, 0, 1]], dtype=float).T

        s_tr = ValueTracker(0.0)

        def A_of():
            s = s_tr.get_value()
            return (1 - s) * A_full + s * A_rank2

        def col_arrows():
            A = A_of()
            cols = [A[:, i] for i in range(3)]
            colors = [GREEN, ORANGE, BLUE]
            return VGroup(*[
                Arrow3D(start=ORIGIN, end=cols[i], color=colors[i], thickness=0.04)
                for i in range(3)
            ])

        def parallelepiped():
            A = A_of()
            c1, c2, c3 = A[:, 0], A[:, 1], A[:, 2]
            verts = [np.zeros(3), c1, c1 + c2, c2,
                      c3, c1 + c3, c1 + c2 + c3, c2 + c3]
            faces = [
                Polygon(verts[0], verts[1], verts[2], verts[3]),
                Polygon(verts[4], verts[5], verts[6], verts[7]),
                Polygon(verts[0], verts[1], verts[5], verts[4]),
                Polygon(verts[2], verts[3], verts[7], verts[6]),
                Polygon(verts[0], verts[3], verts[7], verts[4]),
                Polygon(verts[1], verts[2], verts[6], verts[5]),
            ]
            d = abs(float(np.linalg.det(A)))
            col = YELLOW if d > 0.05 else RED
            grp = VGroup(*faces)
            grp.set_color(col)
            grp.set_fill(col, opacity=0.25)
            grp.set_stroke(col, width=2)
            return grp

        self.add(always_redraw(col_arrows), always_redraw(parallelepiped))

        # Fixed-in-frame info
        title = Tex(r"3D columns: full rank vs rank 2", font_size=24)
        info = VGroup(
            VGroup(Tex(r"$s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\det A=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$s=0$: rank 3 (volume>0)",
                color=GREEN, font_size=20),
            Tex(r"$s=1$: rank 2 (coplanar, vol=0)",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(s_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(float(np.linalg.det(A_of()))))

        self.play(s_tr.animate.set_value(1.0), run_time=3.5, rate_func=smooth)
        self.wait(0.8)
        self.play(s_tr.animate.set_value(0.0), run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.stop_ambient_camera_rotation()
