from manim import *
import numpy as np


class StokesTheoremDemoExample(ThreeDScene):
    """
    Stokes' theorem: ∮_{∂S} F · dr = ∫∫_S (∇×F) · dn. Visualize for
    F = (-y, x, 0) (curl = (0, 0, 2)) with S = unit disk at z=0.5
    and ∂S = unit circle.

    3D scene:
      Disk + circle boundary; traveler on boundary computes line
      integral; surface shaded in GREEN to emphasize area = π.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-1, 2, 1],
                           x_length=4, y_length=4, z_length=3)
        self.add(axes)

        # Disk at z=0.5
        disk_z = 0.5

        def disk_param(u, v):
            # u = r ∈ [0, 1], v = θ ∈ [0, 2π]
            return axes.c2p(u * np.cos(v), u * np.sin(v), disk_z)

        disk = Surface(disk_param, u_range=[0.01, 1], v_range=[0, 2 * PI],
                         resolution=(15, 24),
                         fill_opacity=0.5,
                         checkerboard_colors=[GREEN, GREEN_E])
        self.add(disk)

        # Boundary circle
        boundary_pts = [axes.c2p(np.cos(t), np.sin(t), disk_z)
                         for t in np.linspace(0, 2 * PI, 60)]
        boundary = VMobject(color=YELLOW, stroke_width=4)
        boundary.set_points_as_corners(boundary_pts + [boundary_pts[0]])
        self.add(boundary)

        theta_tr = ValueTracker(0.001)

        def rider():
            t = theta_tr.get_value()
            return Dot3D(axes.c2p(np.cos(t), np.sin(t), disk_z),
                          color=RED, radius=0.12)

        def F_arrow():
            t = theta_tr.get_value()
            # F(cos t, sin t, 0.5) = (-sin t, cos t, 0)
            x, y = np.cos(t), np.sin(t)
            Fx, Fy = -y, x
            start = axes.c2p(x, y, disk_z)
            end = axes.c2p(x + 0.5 * Fx, y + 0.5 * Fy, disk_z)
            return Line(start, end, color=BLUE, stroke_width=5)

        self.add(always_redraw(rider), always_redraw(F_arrow))

        title = Tex(r"Stokes: $\oint F\cdot dr = \iint_S (\nabla\times F)\cdot \hat n$",
                    font_size=22).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        info = VGroup(
            Tex(r"$F = (-y, x, 0)$", color=BLUE, font_size=20),
            Tex(r"$\nabla \times F = (0, 0, 2)$", color=GREEN, font_size=20),
            Tex(r"$\iint_S 2\,dA = 2\pi$ ($\pi$ area)",
                 color=GREEN, font_size=20),
            Tex(r"$\oint F\cdot dr = 2\pi$ as $\theta: 0 \to 2\pi$",
                 color=YELLOW, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(info)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=6, rate_func=linear)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
