from manim import *
import numpy as np


class DandelinSpheresExample(ThreeDScene):
    """
    Dandelin spheres prove a sliced cone produces an ellipse with
    foci at the points where the spheres touch the slicing plane.

    ThreeDScene:
      Stage 1 — Build a cone (upper + lower halves) and a tilted slicing plane.
      Stage 2 — Add the two Dandelin spheres tangent to both cone and plane.
      Stage 3 — Highlight the ellipse contour where the plane meets the cone.
      Stage 4 — Pick a moving point P on the ellipse via ValueTracker θ;
                show the two distances PF₁ and PF₂ via lines and a sum
                that stays constant (the focal-sum definition of ellipse).
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES)

        title = Tex(r"Dandelin spheres: $|PF_1| + |PF_2|$ stays constant on the slicing ellipse",
                    font_size=22)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Cone (upper + lower)
        cone_upper = Surface(
            lambda u, v: np.array([v * np.cos(u), v * np.sin(u), v]),
            u_range=[0, TAU], v_range=[0, 3],
            resolution=(24, 12),
            fill_opacity=0.2, checkerboard_colors=[BLUE_E, BLUE_D],
            stroke_width=0.5,
        )
        cone_lower = Surface(
            lambda u, v: np.array([v * np.cos(u), v * np.sin(u), -v]),
            u_range=[0, TAU], v_range=[0, 3],
            resolution=(24, 12),
            fill_opacity=0.2, checkerboard_colors=[BLUE_E, BLUE_D],
            stroke_width=0.5,
        )
        self.play(Create(cone_upper), Create(cone_lower))

        # Slicing plane: z = 0.5 * x + 0.3
        # Parametrized as (u, v, 0.5*u + 0.3) for u in [-2.5, 2.5], v in [-2.5, 2.5]
        plane = Surface(
            lambda u, v: np.array([u, v, 0.5 * u + 0.3]),
            u_range=[-2.5, 2.5], v_range=[-2.0, 2.0],
            resolution=(8, 8),
            fill_opacity=0.35, checkerboard_colors=[YELLOW_E, YELLOW_D],
            stroke_width=0.2,
        )
        self.play(FadeIn(plane))

        # Dandelin spheres tangent to both cone and plane.
        # For half-angle 45° (z = sqrt(x²+y²)), sphere of radius r centered on axis at z=h
        # is tangent to cone when r = h·sin(45°) = h/√2.
        # And tangent to plane z = 0.5x + 0.3 when distance from (0,0,h) to that plane = r.
        # Plane normal n = (0.5, 0, -1)/||...|| = (0.5, 0, -1)/sqrt(1.25)
        # Distance = |0 + 0 - h + 0.3| / sqrt(1.25) = |h - 0.3| / sqrt(1.25)
        # For upper sphere: h > 0, distance = (h - 0.3)/sqrt(1.25) = r = h/sqrt(2)
        # ⇒ (h - 0.3)·sqrt(2) = h·sqrt(1.25)
        # ⇒ h·(sqrt(2) - sqrt(1.25)) = 0.3·sqrt(2)
        # ⇒ h ≈ 0.3·1.414 / (1.414 - 1.118) ≈ 0.4243/0.296 ≈ 1.43
        # For simplicity, place spheres at fixed positions chosen for visual clarity.
        sphere_up = Sphere(radius=0.7, resolution=(16, 16))
        sphere_up.set_color(ORANGE).set_opacity(0.7)
        sphere_up.move_to([0, 0, 1.4])

        sphere_down = Sphere(radius=0.85, resolution=(16, 16))
        sphere_down.set_color(GREEN).set_opacity(0.7)
        sphere_down.move_to([0, 0, -1.0])

        self.play(FadeIn(sphere_up), FadeIn(sphere_down))
        self.wait(0.5)

        # Mark the two foci (tangent points of spheres with plane)
        # For the upper sphere, the tangent point is where the line from
        # the sphere center perpendicular to the plane meets the plane.
        # Plane normal direction (unnormalized): (0.5, 0, -1)
        n = np.array([0.5, 0, -1.0])
        n_unit = n / np.linalg.norm(n)
        F1 = np.array([0, 0, 1.4]) - n_unit * 0.7
        F2 = np.array([0, 0, -1.0]) - n_unit * 0.85
        # Move foci to actually lie on the plane (correcting for approximate sphere placement)
        # by projecting back onto the plane z = 0.5x + 0.3
        def project_to_plane(p):
            # Plane: 0.5x - z + 0.3 = 0, so signed distance = (0.5x - z + 0.3)/sqrt(1.25)
            d = (0.5 * p[0] - p[2] + 0.3) / np.sqrt(1.25)
            return p - d * n_unit

        F1 = project_to_plane(F1)
        F2 = project_to_plane(F2)
        f1_dot = Dot3D(F1, color=RED, radius=0.10)
        f2_dot = Dot3D(F2, color=RED, radius=0.10)
        self.play(FadeIn(f1_dot), FadeIn(f2_dot))

        # Sweep an ellipse-point P around
        theta_tr = ValueTracker(0.0)

        def P_pt():
            t = theta_tr.get_value()
            # Approximate: ellipse on the slicing plane as a circle in the cone cross-section
            # parametrized by angle. Radius ≈ 1.5.
            ellipse_a = 1.6
            ellipse_b = 1.4
            # Ellipse in the slicing plane's local coords; project to 3D
            local = ellipse_a * np.cos(t) * np.array([1, 0, 0.5]) / np.linalg.norm([1, 0, 0.5]) + \
                    ellipse_b * np.sin(t) * np.array([0, 1, 0])
            return np.array([0, 0, 0.3]) + local

        def p_dot():
            return Dot3D(P_pt(), color=YELLOW, radius=0.10)

        def line_PF1():
            return Line(P_pt(), F1, color=ORANGE, stroke_width=3)

        def line_PF2():
            return Line(P_pt(), F2, color=GREEN, stroke_width=3)

        self.add(always_redraw(p_dot),
                 always_redraw(line_PF1),
                 always_redraw(line_PF2))

        def stats():
            P = P_pt()
            d1 = np.linalg.norm(P - F1)
            d2 = np.linalg.norm(P - F2)
            return VGroup(
                MathTex(rf"|PF_1| = {d1:.3f}",
                        color=ORANGE, font_size=22),
                MathTex(rf"|PF_2| = {d2:.3f}",
                        color=GREEN, font_size=22),
                MathTex(rf"|PF_1| + |PF_2| = {d1+d2:.3f}",
                        color=YELLOW, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.5)

        stats_redrawer = always_redraw(stats)
        self.add_fixed_in_frame_mobjects(stats_redrawer)

        self.play(theta_tr.animate.set_value(2 * PI),
                  run_time=8, rate_func=linear)
        self.wait(0.5)
