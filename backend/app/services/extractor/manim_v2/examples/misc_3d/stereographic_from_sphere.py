from manim import *
import numpy as np


class StereographicFromSphereExample(ThreeDScene):
    """
    Stereographic projection from the north pole of a unit sphere to
    the equatorial plane. Latitudes → concentric circles. Vertices
    near the south pole map to large circles around the origin.

    3D scene:
      Sphere + plane below; ValueTracker phi_tr moves a point along
      a latitude circle; always_redraw the ray from N through the
      point extended to the plane, showing the projection.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                           z_range=[-1.5, 2, 1],
                           x_length=4, y_length=4, z_length=3)
        self.add(axes)

        R = 1.0
        sphere = Sphere(radius=R, resolution=(16, 16),
                          fill_opacity=0.18,
                          color=BLUE_D).move_to(axes.c2p(0, 0, 0))
        self.add(sphere)

        N = axes.c2p(0, 0, R)
        N_dot = Dot3D(N, color=RED, radius=0.08)
        self.add(N_dot)

        # Equatorial plane (z = 0 visualized as square outline)
        plane_sq = Square(side_length=3.2,
                            color=WHITE, stroke_width=2,
                            fill_opacity=0.05
                            ).move_to(axes.c2p(0, 0, 0))
        self.add(plane_sq)

        lat_state = [45 * DEGREES]  # latitude angle from north pole
        phi_tr = ValueTracker(0.0)

        def sphere_point():
            lat = lat_state[0]
            phi = phi_tr.get_value()
            x = R * np.sin(lat) * np.cos(phi)
            y = R * np.sin(lat) * np.sin(phi)
            z = R * np.cos(lat)
            return axes.c2p(x, y, z)

        def projection_pt():
            # N + t(P - N) with z = 0 gives t = N_z / (N_z - P_z)
            P = sphere_point()
            Nz = N[2]
            Pz = P[2]
            if abs(Nz - Pz) < 1e-6:
                return axes.c2p(0, 0, 0)
            t = Nz / (Nz - Pz)
            return N + t * (P - N)

        def ray():
            return Line(N, projection_pt() + 0.2 * (projection_pt() - N) / (np.linalg.norm(projection_pt() - N) + 1e-8),
                          color=YELLOW, stroke_width=2)

        def sphere_pt_dot():
            return Dot3D(sphere_point(), color=GREEN, radius=0.1)

        def proj_dot():
            return Dot3D(projection_pt(), color=ORANGE, radius=0.1)

        def lat_circle():
            # Draw the latitude circle on the sphere
            lat = lat_state[0]
            pts = []
            for p in np.linspace(0, 2 * PI, 60):
                x = R * np.sin(lat) * np.cos(p)
                y = R * np.sin(lat) * np.sin(p)
                z = R * np.cos(lat)
                pts.append(axes.c2p(x, y, z))
            m = VMobject(color=GREEN, stroke_width=2,
                           stroke_opacity=0.6)
            m.set_points_as_corners(pts + [pts[0]])
            return m

        def proj_circle():
            # Projected circle on plane
            lat = lat_state[0]
            pts = []
            for p in np.linspace(0, 2 * PI, 60):
                x = R * np.sin(lat) * np.cos(p)
                y = R * np.sin(lat) * np.sin(p)
                z = R * np.cos(lat)
                P = axes.c2p(x, y, z)
                Nz = N[2]
                Pz = P[2]
                if abs(Nz - Pz) < 1e-6:
                    continue
                t = Nz / (Nz - Pz)
                pts.append(N + t * (P - N))
            if len(pts) < 2:
                return VMobject()
            m = VMobject(color=ORANGE, stroke_width=2.5)
            m.set_points_as_corners(pts + [pts[0]])
            return m

        self.add(always_redraw(lat_circle),
                  always_redraw(proj_circle),
                  always_redraw(ray),
                  always_redraw(sphere_pt_dot),
                  always_redraw(proj_dot))

        title = Tex(r"Stereographic: $S^2 \setminus \{N\} \to \mathbb R^2$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            lat = lat_state[0]
            phi = phi_tr.get_value()
            return VGroup(
                MathTex(rf"\text{{lat}} = {np.degrees(lat):.0f}^\circ",
                         color=GREEN, font_size=22),
                MathTex(rf"\phi = {np.degrees(phi):.0f}^\circ",
                         color=YELLOW, font_size=22),
                Tex(r"GREEN sphere $\to$ ORANGE plane",
                     color=WHITE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        p = panel()
        self.add_fixed_in_frame_mobjects(p)

        self.begin_ambient_camera_rotation(rate=0.12)
        # Sweep φ at fixed lat=45°
        self.play(phi_tr.animate.set_value(2 * PI),
                   run_time=4, rate_func=linear)
        # Change latitude and sweep again
        lat_state[0] = 75 * DEGREES
        self.play(phi_tr.animate.set_value(4 * PI),
                   run_time=4, rate_func=linear)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
