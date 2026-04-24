from manim import *
import numpy as np


class MobiusSphereRotationExample(ThreeDScene):
    """
    Möbius transformations of ℂ ∪ {∞} correspond to rotations of
    the Riemann sphere S². Example: the rotation by π around the
    x-axis corresponds to the Möbius transform z → 1/z̄, which on
    the sphere swaps north and south poles while preserving the
    equator.

    SINGLE_FOCUS ThreeDScene: sphere with a grid of meridians +
    parallels + 3 colored test loops (equator + two parallels).
    ValueTracker theta_tr rotates the sphere smoothly; the action
    of the corresponding Möbius map on the stereographic image plane
    shows up as conformal motion.
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=40 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.03)

        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-1.5, 1.5, 1],
                          x_length=4.0, y_length=4.0, z_length=3.0)
        self.add(axes)

        sphere = Sphere(radius=1.0, resolution=(18, 36), fill_opacity=0.25).set_color(BLUE)

        # Initial meridians / parallels
        meridians_parallels = VGroup()
        for lon in np.linspace(0, TAU, 8, endpoint=False):
            pts = []
            for lat in np.linspace(-PI / 2 + 0.05, PI / 2 - 0.05, 40):
                pts.append(np.array([np.cos(lat) * np.cos(lon),
                                      np.cos(lat) * np.sin(lon),
                                      np.sin(lat)]))
            meridians_parallels.add(VMobject().set_points_smoothly(pts)
                                     .set_color(GREY_B).set_stroke(width=1.5))

        for lat in [-PI / 3, 0, PI / 3]:
            pts = []
            for lon in np.linspace(0, TAU, 60):
                pts.append(np.array([np.cos(lat) * np.cos(lon),
                                      np.cos(lat) * np.sin(lon),
                                      np.sin(lat)]))
            col = RED if lat < 0 else (YELLOW if lat == 0 else GREEN)
            meridians_parallels.add(VMobject().set_points_smoothly(pts + [pts[0]])
                                     .set_color(col).set_stroke(width=3))

        sphere_group = VGroup(sphere, meridians_parallels)
        self.add(sphere_group)

        theta_tr = ValueTracker(0.0)

        def rotation_group():
            t = theta_tr.get_value()
            base = VGroup(sphere.copy(), meridians_parallels.copy())
            base.rotate(t, axis=RIGHT, about_point=ORIGIN)
            return base

        rot_grp = always_redraw(rotation_group)
        self.remove(sphere_group)
        self.add(rot_grp)

        title = Tex(r"Möbius ↔ $S^2$ rotation: $z\mapsto 1/\bar z$ = flip poles",
                    font_size=22)
        info = VGroup(
            VGroup(Tex(r"angle $\theta=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"equator $=$ unit circle on plane",
                color=YELLOW, font_size=20),
            Tex(r"south pole $= 0 \in \mathbb{C}$",
                color=RED, font_size=20),
            Tex(r"north pole $= \infty$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(theta_tr.get_value()))

        self.play(theta_tr.animate.set_value(PI),
                  run_time=5, rate_func=smooth)
        self.wait(0.5)
        self.play(theta_tr.animate.set_value(2 * PI),
                  run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.stop_ambient_camera_rotation()
