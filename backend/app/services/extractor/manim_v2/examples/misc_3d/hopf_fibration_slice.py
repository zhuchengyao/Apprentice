from manim import *
import numpy as np


class HopfFibrationSliceExample(ThreeDScene):
    """
    Hopf fibration: S³ → S² where each fiber is a great circle of
    S³. Visualize via stereographic projection to ℝ³: each fiber
    becomes a circle (or line). Several fibers over a single S² point
    form concentric / nested Villarceau-like circles.

    3D scene:
      3-4 fibers over distinct S² points projected to ℝ³ as circles.
      ValueTracker t_tr rotates camera around them.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-35 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                           z_range=[-2, 2, 1],
                           x_length=5, y_length=5, z_length=3)
        self.add(axes)

        # Each fiber over (θ, φ) on S² is a great circle on S³ which
        # stereographically projects to a circle in ℝ³. We compute it
        # via the parametrization:
        #   (x, y, z, w) = (cos((φ+ψ)/2) sin(θ/2),
        #                   sin((φ+ψ)/2) sin(θ/2),
        #                   cos((φ-ψ)/2) cos(θ/2),
        #                   sin((φ-ψ)/2) cos(θ/2))
        # and project (x, y, z, w) → (x, y, z) / (1 - w).

        def fiber_points(theta, phi):
            """Return list of 3D points for fiber over (θ, φ) on S²,
            parametrized by ψ ∈ [0, 2π]."""
            pts = []
            for psi in np.linspace(0, 2 * PI, 60):
                x = np.cos((phi + psi) / 2) * np.sin(theta / 2)
                y = np.sin((phi + psi) / 2) * np.sin(theta / 2)
                z = np.cos((phi - psi) / 2) * np.cos(theta / 2)
                w = np.sin((phi - psi) / 2) * np.cos(theta / 2)
                if abs(1 - w) < 1e-3:
                    continue
                pts.append(np.array([x / (1 - w),
                                       y / (1 - w),
                                       z / (1 - w), 0]))
            return pts

        # A few fibers over distinct base points
        base_points = [
            (PI / 2, 0.0, RED),
            (PI / 3, PI / 2, BLUE),
            (2 * PI / 3, 0.8 * PI, GREEN),
            (PI / 4, 1.5 * PI, YELLOW),
        ]

        fiber_grp = VGroup()
        for (theta, phi, col) in base_points:
            pts = fiber_points(theta, phi)
            if len(pts) < 3:
                continue
            # Map to scene coords via axes.c2p
            scene_pts = [axes.c2p(p[0], p[1], p[2]) for p in pts]
            # Clip points far from origin to keep visible
            scene_pts = [p for p in scene_pts if np.linalg.norm(p) < 5]
            if len(scene_pts) < 3:
                continue
            fiber = VMobject(color=col, stroke_width=3)
            fiber.set_points_as_corners(scene_pts + [scene_pts[0]])
            fiber_grp.add(fiber)

        self.play(Create(fiber_grp), run_time=2)

        title = Tex(r"Hopf fibration: $S^3 \to S^2$, fibers $= S^1$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        info = VGroup(
            Tex(r"each fiber = great circle of $S^3$",
                 color=WHITE, font_size=18),
            Tex(r"stereo-projected: linked circles in $\mathbb R^3$",
                 color=WHITE, font_size=18),
            Tex(r"4 distinct base points $\to$ 4 linked circles",
                 color=YELLOW, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        info.to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(info)

        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(8)
        self.stop_ambient_camera_rotation()
