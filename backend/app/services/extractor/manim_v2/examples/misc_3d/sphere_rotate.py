from manim import *
import numpy as np


class SphereRotateExample(ThreeDScene):
    """
    Unit sphere rotating about different axes; points on the
    sphere trace small circles (latitudes).

    3D scene:
      Sphere with a few marked tracer dots at different latitudes;
      ValueTracker phi_tr drives rotation about z-axis; trace dots
      leave trails at their latitude circles. Axis switches via
      Transform after one full rotation.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-30 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=4)
        self.add(axes)

        sphere = Sphere(radius=1.3, color=BLUE_D,
                          resolution=(20, 20), fill_opacity=0.3
                          ).move_to(axes.c2p(0, 0, 0))
        self.add(sphere)

        # Rotation axis marker (start along z)
        axis_state = {"axis": np.array([0, 0, 1.0])}

        def axis_line():
            a = axis_state["axis"]
            return Line(axes.c2p(*(-2 * a)), axes.c2p(*(2 * a)),
                          color=RED, stroke_width=4)

        self.add(always_redraw(axis_line))

        # Four tracer points at different (lat, lon0) on the sphere
        R = 1.3
        tracer_specs = [
            (0.3 * PI, 0, YELLOW),
            (0.5 * PI, 0.3, GREEN),
            (0.7 * PI, 0.5, ORANGE),
            (0.9 * PI, 0.7, PINK),
        ]

        def rodrigues(v, k, theta):
            return (v * np.cos(theta)
                    + np.cross(k, v) * np.sin(theta)
                    + k * np.dot(k, v) * (1 - np.cos(theta)))

        phi_tr = ValueTracker(0.0)

        def tracers():
            grp = VGroup()
            a = axis_state["axis"]
            for (lat, lon, col) in tracer_specs:
                # initial point on sphere
                v0 = R * np.array([np.sin(lat) * np.cos(lon),
                                     np.sin(lat) * np.sin(lon),
                                     np.cos(lat)])
                v = rodrigues(v0, a, phi_tr.get_value())
                grp.add(Dot3D(axes.c2p(*v), color=col, radius=0.08))
            return grp

        def trails():
            grp = VGroup()
            a = axis_state["axis"]
            for (lat, lon, col) in tracer_specs:
                v0 = R * np.array([np.sin(lat) * np.cos(lon),
                                     np.sin(lat) * np.sin(lon),
                                     np.cos(lat)])
                pts = []
                for theta in np.linspace(0, phi_tr.get_value(), 60):
                    v = rodrigues(v0, a, theta)
                    pts.append(axes.c2p(*v))
                mob = VMobject(color=col, stroke_width=2,
                                 stroke_opacity=0.55)
                if len(pts) >= 2:
                    mob.set_points_as_corners(pts)
                grp.add(mob)
            return grp

        self.add(always_redraw(trails), always_redraw(tracers))

        title = Tex(r"Sphere rotation: points trace latitude circles",
                    font_size=26).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        # Phase 1: rotate about z-axis
        self.play(phi_tr.animate.set_value(2 * PI),
                   run_time=5, rate_func=linear)
        self.wait(0.3)

        # Phase 2: switch axis to tilted one and rotate again
        axis_state["axis"] = np.array([0.7, 0.0, 0.7])
        self.play(phi_tr.animate.set_value(0.0), run_time=0.2)
        self.play(phi_tr.animate.set_value(2 * PI),
                   run_time=5, rate_func=linear)
        self.wait(0.5)
