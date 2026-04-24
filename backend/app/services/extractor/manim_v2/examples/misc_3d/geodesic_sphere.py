from manim import *
import numpy as np


class GeodesicSphereExample(ThreeDScene):
    """
    Geodesics on a sphere = great circles. Between two non-antipodal
    points, the shortest path is the arc of the unique great circle.

    3D scene:
      Two points P, Q on a unit sphere; great circle through them +
      arc distinguished; ValueTracker t_tr sweeps a traveler along
      the geodesic. Also show a non-geodesic latitude-path for
      comparison.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=4)
        self.add(axes)

        sphere = Sphere(radius=1.0, resolution=(20, 20),
                          fill_opacity=0.15,
                          color=BLUE_D).move_to(axes.c2p(0, 0, 0))
        self.add(sphere)

        # Two points on sphere
        def sph(lat, lon):
            return np.array([np.sin(lat) * np.cos(lon),
                             np.sin(lat) * np.sin(lon),
                             np.cos(lat)])

        P = sph(0.5, 0.3)
        Q = sph(0.9, 2.0)

        P_dot = Dot3D(axes.c2p(*P), color=GREEN, radius=0.09)
        Q_dot = Dot3D(axes.c2p(*Q), color=RED, radius=0.09)
        self.add(P_dot, Q_dot)

        # Great circle arc P → Q
        def geodesic_pts(P, Q, n=60):
            pts = []
            theta = np.arccos(np.clip(np.dot(P, Q), -1, 1))
            for s in np.linspace(0, 1, n):
                # slerp
                a = np.sin((1 - s) * theta) / np.sin(theta + 1e-8)
                b = np.sin(s * theta) / np.sin(theta + 1e-8)
                pts.append(a * P + b * Q)
            return pts

        geo = VMobject(color=YELLOW, stroke_width=4)
        geo.set_points_as_corners([axes.c2p(*p) for p in geodesic_pts(P, Q)])
        self.add(geo)

        # Non-geodesic: longitude arc (constant latitude interpolation) at mid-lat
        def lat_path_pts(P, Q, n=60):
            pts = []
            lat_P = np.arccos(P[2])
            lat_Q = np.arccos(Q[2])
            lon_P = np.arctan2(P[1], P[0])
            lon_Q = np.arctan2(Q[1], Q[0])
            for s in np.linspace(0, 1, n):
                lat = (1 - s) * lat_P + s * lat_Q
                lon = (1 - s) * lon_P + s * lon_Q
                pts.append(sph(lat, lon))
            return pts

        rhumb = VMobject(color=ORANGE, stroke_width=3,
                           stroke_opacity=0.7)
        rhumb.set_points_as_corners([axes.c2p(*p) for p in lat_path_pts(P, Q)])
        self.add(rhumb)

        t_tr = ValueTracker(0.0)

        def geo_traveler():
            t = t_tr.get_value()
            theta = np.arccos(np.clip(np.dot(P, Q), -1, 1))
            a = np.sin((1 - t) * theta) / np.sin(theta + 1e-8)
            b = np.sin(t * theta) / np.sin(theta + 1e-8)
            p = a * P + b * Q
            return Dot3D(axes.c2p(*p), color=YELLOW, radius=0.11)

        self.add(always_redraw(geo_traveler))

        # Lengths
        theta_PQ = np.arccos(np.clip(np.dot(P, Q), -1, 1))
        geo_len = theta_PQ  # on unit sphere
        rhumb_len = sum(np.linalg.norm(np.diff(np.array(lat_path_pts(P, Q)), axis=0), axis=1))

        title = Tex(r"Geodesic on sphere = arc of great circle",
                    font_size=24).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        info = VGroup(
            Tex(r"YELLOW: geodesic (great circle)", color=YELLOW, font_size=18),
            Tex(r"ORANGE: rhumb line (not geodesic)", color=ORANGE, font_size=18),
            MathTex(rf"\text{{geo length}} = {geo_len:.3f}",
                     color=YELLOW, font_size=18),
            MathTex(rf"\text{{rhumb length}} = {rhumb_len:.3f}",
                     color=ORANGE, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(info)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(t_tr.animate.set_value(1.0), run_time=5, rate_func=linear)
        self.stop_ambient_camera_rotation()
        self.wait(0.5)
