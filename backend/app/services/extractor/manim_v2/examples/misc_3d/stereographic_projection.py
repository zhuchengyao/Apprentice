from manim import *
import numpy as np


class StereographicProjectionExample(ThreeDScene):
    """
    Stereographic projection from north pole: (x, y, z) on S² ↦
    (x', y') on the equatorial plane via line through (0, 0, 1).

    ThreeDScene:
      Sphere + plane below it. ValueTracker θ moves a point P around
      a "tilted circle" on the sphere (parametrized by latitude α and
      longitude θ). For each P, draw the line from north pole through
      P to the plane and mark the projected point Q. As θ sweeps, Q
      traces a curve on the plane (a circle for any latitude — the
      conformal property).
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES)
        title = Tex(r"Stereographic projection: lines from north pole to the plane",
                    font_size=22)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        sphere = Sphere(radius=1.0, resolution=(24, 24)).set_opacity(0.4).set_color(BLUE)
        north = Dot3D([0, 0, 1], color=RED, radius=0.10)
        north_lbl_3d = Tex(r"\textbf{N}", color=RED, font_size=22)
        self.add_fixed_in_frame_mobjects(north_lbl_3d)
        north_lbl_3d.move_to([3.5, 2.5, 0])
        self.play(Create(sphere), FadeIn(north), Write(north_lbl_3d))

        plane = Surface(
            lambda u, v: np.array([u, v, -1]),
            u_range=[-3, 3], v_range=[-3, 3],
            resolution=(6, 6),
            fill_opacity=0.25, checkerboard_colors=[GREY_D, GREY_C],
            stroke_width=0.4,
        )
        self.play(FadeIn(plane))

        theta_tr = ValueTracker(0.0)
        latitude = PI / 3  # 60° from north pole

        def P_pt():
            t = theta_tr.get_value()
            return np.array([np.sin(latitude) * np.cos(t),
                             np.sin(latitude) * np.sin(t),
                             np.cos(latitude)])

        def Q_pt():
            P = P_pt()
            x, y, z = P
            # Line from N=(0,0,1) through P, hits z=-1 plane
            # Parametrize: r(t) = N + t·(P - N); set z = 1 + t·(z - 1) = -1
            # ⇒ t = -2/(z - 1)
            t = -2.0 / (z - 1)
            return np.array([t * x, t * y, -1])

        def projection_line():
            return Line([0, 0, 1], Q_pt(), color=YELLOW_E, stroke_width=2)

        def p_dot_3d():
            return Dot3D(P_pt(), color=YELLOW, radius=0.07)

        def q_dot_3d():
            return Dot3D(Q_pt(), color=GREEN, radius=0.07)

        # Persistent trail of projected points
        trail_pts: list[np.ndarray] = []

        def trail():
            path = VMobject(color=GREEN, stroke_width=3)
            if len(trail_pts) >= 2:
                path.set_points_as_corners(trail_pts.copy())
            else:
                p = Q_pt()
                path.set_points_as_corners([p, p])
            return path

        def record(_, dt):
            trail_pts.append(Q_pt())
            if len(trail_pts) > 4000:
                del trail_pts[: len(trail_pts) - 4000]

        recorder = Mobject()
        recorder.add_updater(record)
        self.add(recorder)

        self.add(always_redraw(projection_line),
                 always_redraw(p_dot_3d),
                 always_redraw(q_dot_3d),
                 always_redraw(trail))

        formula = Tex(r"Latitude $60^\circ$ on $S^2$ $\to$ circle of radius $\sqrt 3$ on the plane",
                      color=YELLOW, font_size=20)
        self.add_fixed_in_frame_mobjects(formula)
        formula.to_edge(DOWN, buff=0.4)
        self.play(Write(formula))

        self.play(theta_tr.animate.set_value(2 * PI),
                  run_time=6, rate_func=linear)
        recorder.clear_updaters()
        self.wait(0.8)
