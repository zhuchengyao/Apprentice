from manim import *
import numpy as np


class StereographicTilingExample(ThreeDScene):
    """
    Stereographic projection of a regular triangular tiling from the
    plane to the sphere: straight lines on the plane become circles
    on the sphere (through the south pole), preserving angles.

    TWO_COLUMN split visually via 3D layout: a triangular grid on
    the z=0 plane gets mapped up to the unit sphere via inverse
    stereographic projection. ValueTracker s_tr morphs the grid
    progressively upward through interp.
    """

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=40 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-1.5, 1.8, 1],
                          x_length=4.5, y_length=4.5, z_length=3.2)
        self.add(axes)

        # Sphere
        sphere = Sphere(radius=1.0, resolution=(18, 36),
                        fill_opacity=0.25).set_color(BLUE)
        self.add(sphere)

        # Generate triangular tiling on z=0 (within square [-2.5, 2.5])
        side = 0.6
        tri_centers = []
        for i in range(-4, 5):
            for j in range(-4, 5):
                cx = i * side + (0.5 * side if j % 2 else 0)
                cy = j * side * (np.sqrt(3) / 2)
                if abs(cx) < 2.4 and abs(cy) < 2.4:
                    tri_centers.append(np.array([cx, cy, 0]))

        # Inverse stereographic from plane z=0 (through south pole -e_z)
        def inv_stereo(x, y):
            d = x * x + y * y
            X = 2 * x / (1 + d)
            Y = 2 * y / (1 + d)
            Z = (d - 1) / (d + 1)
            return np.array([X, Y, Z])

        s_tr = ValueTracker(0.0)

        def interp(P):
            s = s_tr.get_value()
            target = inv_stereo(P[0], P[1])
            return (1 - s) * P + s * target

        def tri_grid():
            grp = VGroup()
            # Generate triangle edges: triangles have vertices on two sub-lattices
            # Simpler: draw segments between nearby centers
            for i in range(len(tri_centers)):
                for j in range(i + 1, len(tri_centers)):
                    d = np.linalg.norm(tri_centers[i] - tri_centers[j])
                    if side * 0.9 < d < side * 1.3:
                        p1 = interp(tri_centers[i])
                        p2 = interp(tri_centers[j])
                        # subdivide along projection path
                        pts = []
                        N = 10
                        for k in range(N + 1):
                            t = k / N
                            pt_plane = (1 - t) * tri_centers[i] + t * tri_centers[j]
                            pts.append(interp(pt_plane))
                        grp.add(VMobject().set_points_as_corners(pts)
                                 .set_color(YELLOW).set_stroke(width=2))
            return grp

        self.add(always_redraw(tri_grid))

        title = Tex(r"Stereographic tiling: plane triangles $\to$ sphere circles",
                    font_size=24)
        info = VGroup(
            VGroup(Tex(r"morph $s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"angles preserved (conformal)",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(DR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(s_tr.get_value()))

        self.play(s_tr.animate.set_value(1.0),
                  run_time=5, rate_func=smooth)
        self.wait(0.8)
        self.play(s_tr.animate.set_value(0.0),
                  run_time=2.5, rate_func=smooth)
        self.play(s_tr.animate.set_value(1.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.8)
        self.stop_ambient_camera_rotation()
