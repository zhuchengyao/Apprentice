from manim import *
import numpy as np


class VolumeViaBaseTimesHeightExample(ThreeDScene):
    """
    Geometric meaning of (v × w) · u: v × w is perpendicular to base
    parallelogram with magnitude = base area. Dotting with u extracts
    the height-component of u (perpendicular to base) and multiplies
    by base area, giving volume.
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=25 * DEGREES)

        axes = ThreeDAxes(x_range=[-1, 3, 1], y_range=[-1, 3, 1], z_range=[-1, 3, 1],
                          x_length=4.5, y_length=4.5, z_length=4.5)
        self.add(axes)

        v = np.array([2.0, 0.0, 0.0])
        w = np.array([0.5, 2.0, 0.0])
        u = np.array([0.3, 0.3, 2.0])

        # Base parallelogram (v, w)
        base = Polygon(ORIGIN, v, v + w, w,
                        color=BLUE, fill_color=BLUE, fill_opacity=0.4,
                        stroke_width=2)
        self.add(base)

        # Arrows
        self.add(Arrow3D(ORIGIN, v, color=BLUE, thickness=0.04))
        self.add(Arrow3D(ORIGIN, w, color=ORANGE, thickness=0.04))
        self.add(Arrow3D(ORIGIN, u, color=GREEN, thickness=0.04))

        # v × w (perpendicular, length = base area)
        cross_vw = np.cross(v, w)
        self.add(Arrow3D(ORIGIN, cross_vw, color=PURPLE, thickness=0.05))

        # u's height component — projection onto v×w direction
        cross_unit = cross_vw / np.linalg.norm(cross_vw)
        height_val = np.dot(u, cross_unit)
        height_component = height_val * cross_unit

        # Drop from u down to base plane
        u_projection_on_base = u - height_component  # in base plane
        self.add(DashedLine(u, u_projection_on_base,
                             color=RED, stroke_width=3))

        # Height arrow
        self.add(Arrow3D(u_projection_on_base, u,
                          color=RED, thickness=0.04))

        # Fixed labels
        base_area = np.linalg.norm(cross_vw)
        height = height_val
        volume = base_area * height

        title = Tex(r"Volume $=$ (base area) $\times$ height",
                    font_size=24)
        info = VGroup(
            VGroup(Tex(r"base area $|\vec v\times\vec w|=$", font_size=22),
                   DecimalNumber(base_area, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"height (perp comp of $\vec u$) $=$",
                        font_size=22),
                   DecimalNumber(height, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"volume $=$ ", font_size=24),
                   DecimalNumber(volume, num_decimal_places=3,
                                 font_size=24).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"$=(\vec v\times\vec w)\cdot\vec u$",
                color=YELLOW, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(DR, buff=0.3)

        self.begin_ambient_camera_rotation(rate=0.07)
        self.wait(5)
        self.stop_ambient_camera_rotation()
