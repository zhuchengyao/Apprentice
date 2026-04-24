from manim import *
import numpy as np


class TripleProductEqualsDetExample(ThreeDScene):
    """
    Scalar triple product (v × w) · u = det([v | w | u]) = signed
    volume of parallelepiped spanned by v, w, u.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        axes = ThreeDAxes(x_range=[-1, 3, 1], y_range=[-1, 3, 1], z_range=[-1, 3, 1],
                          x_length=4.5, y_length=4.5, z_length=4.5)
        self.add(axes)

        v = np.array([2.0, 0.0, 0.0])
        w = np.array([1.0, 2.0, 0.0])
        u = np.array([0.5, 0.5, 2.0])

        v_arr = Arrow3D(ORIGIN, v, color=BLUE, thickness=0.04)
        w_arr = Arrow3D(ORIGIN, w, color=ORANGE, thickness=0.04)
        u_arr = Arrow3D(ORIGIN, u, color=GREEN, thickness=0.04)
        self.add(v_arr, w_arr, u_arr)

        # Parallelepiped
        verts = [np.zeros(3), v, v + w, w, u, u + v, u + v + w, u + w]
        faces = [
            Polygon(verts[0], verts[1], verts[2], verts[3]),
            Polygon(verts[4], verts[5], verts[6], verts[7]),
            Polygon(verts[0], verts[1], verts[5], verts[4]),
            Polygon(verts[2], verts[3], verts[7], verts[6]),
            Polygon(verts[0], verts[3], verts[7], verts[4]),
            Polygon(verts[1], verts[2], verts[6], verts[5]),
        ]
        pp = VGroup(*faces)
        pp.set_color(YELLOW)
        pp.set_fill(YELLOW, opacity=0.2)
        pp.set_stroke(YELLOW, width=2)
        self.add(pp)

        # v × w arrow
        cross_vw = np.cross(v, w)
        cross_arr = Arrow3D(ORIGIN, cross_vw, color=PURPLE, thickness=0.05)
        self.add(cross_arr)

        # Fixed labels
        title = Tex(r"$(\vec v\times\vec w)\cdot\vec u=\det[\vec v\,|\,\vec w\,|\,\vec u]=$ volume",
                    font_size=22)

        triple = float(np.dot(np.cross(v, w), u))
        det_val = float(np.linalg.det(np.column_stack([v, w, u])))

        info = VGroup(
            Tex(r"BLUE $\vec v$, ORANGE $\vec w$, GREEN $\vec u$",
                font_size=20),
            Tex(r"PURPLE $\vec v\times\vec w$ (perp)",
                color=PURPLE, font_size=20),
            VGroup(Tex(r"$(\vec v\times\vec w)\cdot\vec u=$", font_size=24),
                   DecimalNumber(triple, num_decimal_places=3,
                                 font_size=24).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\det[\vec v\,|\,\vec w\,|\,\vec u]=$", font_size=24),
                   DecimalNumber(det_val, num_decimal_places=3,
                                 font_size=24).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"= volume of parallelepiped",
                color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(DR, buff=0.3)

        self.wait(6)
        self.stop_ambient_camera_rotation()
