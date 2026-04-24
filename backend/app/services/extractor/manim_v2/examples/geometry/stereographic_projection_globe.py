from manim import *
import numpy as np


class StereographicProjectionGlobeExample(ThreeDScene):
    """
    Stereographic projection of Earth-like globe: longitudes become
    rays, latitudes become circles. Conformal (angle-preserving).

    ThreeDScene with sphere + 6 longitude meridians + 5 latitude
    circles; ValueTracker s_tr morphs points from sphere to z=0 plane
    via inverse projection.
    """

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=40 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.04)

        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-1.5, 2.5, 1],
                          x_length=5.0, y_length=5.0, z_length=3.5)
        self.add(axes)

        sphere = Sphere(radius=1.0, resolution=(18, 36),
                        fill_opacity=0.2).set_color(BLUE)
        self.add(sphere)

        # North pole
        N = np.array([0, 0, 1])

        # Stereographic from N to z=0 plane
        def stereo(p):
            if abs(1 - p[2]) < 1e-6:
                return np.array([1e6, 0, 0])
            k = 1 / (1 - p[2])
            return np.array([p[0] * k, p[1] * k, 0])

        s_tr = ValueTracker(0.0)

        def interp(p):
            s = s_tr.get_value()
            return (1 - s) * p + s * stereo(p)

        def meridian_lines():
            grp = VGroup()
            for lon in np.linspace(0, TAU, 12, endpoint=False):
                pts = []
                for lat in np.linspace(-PI / 2 + 0.08, PI / 2 - 0.1, 40):
                    p = np.array([np.cos(lat) * np.cos(lon),
                                   np.cos(lat) * np.sin(lon),
                                   np.sin(lat)])
                    if np.linalg.norm(interp(p)) < 8:
                        pts.append(interp(p))
                if len(pts) > 1:
                    grp.add(VMobject().set_points_smoothly(pts)
                             .set_color(YELLOW).set_stroke(width=2))
            return grp

        def latitude_lines():
            grp = VGroup()
            for lat in [-PI / 3, -PI / 6, 0, PI / 6, PI / 3]:
                pts = []
                for lon in np.linspace(0, TAU, 60):
                    p = np.array([np.cos(lat) * np.cos(lon),
                                   np.cos(lat) * np.sin(lon),
                                   np.sin(lat)])
                    if np.linalg.norm(interp(p)) < 8:
                        pts.append(interp(p))
                if len(pts) > 1:
                    col = GREEN if lat == 0 else interpolate_color(BLUE, ORANGE, (lat / PI) + 0.5)
                    grp.add(VMobject().set_points_smoothly(pts + [pts[0]])
                             .set_color(col).set_stroke(width=2.5))
            return grp

        self.add(always_redraw(meridian_lines), always_redraw(latitude_lines))

        # Mark north pole
        north_dot = Dot3D(point=N, color=RED, radius=0.1)
        self.add(north_dot)

        title = Tex(r"Stereographic projection: sphere $\to$ plane (conformal)",
                    font_size=24)
        info = VGroup(
            VGroup(Tex(r"morph $s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"latitudes $\to$ circles",
                color=GREEN, font_size=20),
            Tex(r"meridians $\to$ radial lines",
                color=YELLOW, font_size=20),
            Tex(r"angles preserved (conformal)",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(s_tr.get_value()))

        self.play(s_tr.animate.set_value(1.0),
                  run_time=5, rate_func=smooth)
        self.wait(0.5)
        self.play(s_tr.animate.set_value(0.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.stop_ambient_camera_rotation()
