from manim import *
import numpy as np


class MobiusStripExample(ThreeDScene):
    """
    Möbius strip: nonorientable surface formed by gluing a strip
    end-to-end with a half-twist.

    3D scene:
      Parametric Möbius strip; ValueTracker t_tr drives a dot that
      walks along the center circle starting at (R, 0, 0); after
      t = 2π it returns to start but flipped (normal reversed).
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                           z_range=[-1.5, 1.5, 1],
                           x_length=4, y_length=4, z_length=2.5)
        self.add(axes)

        R = 1.8
        w = 0.6

        def mobius_param(u, v):
            # u ∈ [0, 2π], v ∈ [-w, w]
            x = (R + v * np.cos(u / 2)) * np.cos(u)
            y = (R + v * np.cos(u / 2)) * np.sin(u)
            z = v * np.sin(u / 2)
            return axes.c2p(x, y, z)

        surface = Surface(mobius_param,
                            u_range=[0, 2 * PI],
                            v_range=[-w, w],
                            resolution=(60, 10),
                            fill_opacity=0.8,
                            checkerboard_colors=[BLUE_D, BLUE_E])
        self.add(surface)

        # Rider dot + its normal vector
        t_tr = ValueTracker(0.0)

        def rider():
            u = t_tr.get_value()
            v = 0.0
            return Dot3D(mobius_param(u, v), color=YELLOW, radius=0.12)

        def normal_arrow():
            u = t_tr.get_value()
            # Compute tangent & normal numerically
            du = 0.01
            dv = 0.01
            p0 = np.array(mobius_param(u, 0))
            p_du = np.array(mobius_param(u + du, 0))
            p_dv = np.array(mobius_param(u, dv))
            t_vec = (p_du - p0) / du
            n_vec = (p_dv - p0) / dv
            # Normalize and scale
            n_norm = n_vec / (np.linalg.norm(n_vec) + 1e-8)
            start = p0
            end = start + 0.6 * n_norm
            return Line(start, end, color=RED, stroke_width=5)

        self.add(always_redraw(rider), always_redraw(normal_arrow))

        title = Tex(r"Möbius strip: normal flips after one loop",
                    font_size=26).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            t = t_tr.get_value()
            return VGroup(
                MathTex(rf"u = {np.degrees(t):.0f}^\circ",
                         color=YELLOW, font_size=22),
                MathTex(r"\text{normal has a}", color=RED, font_size=20),
                MathTex(r"\text{half-twist per loop}", color=RED, font_size=20),
                MathTex(r"\chi = 0, \text{nonorientable}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        p = panel()
        self.add_fixed_in_frame_mobjects(p)

        self.begin_ambient_camera_rotation(rate=0.15)
        # Complete 2 loops to see normal flip twice
        self.play(t_tr.animate.set_value(4 * PI),
                   run_time=10, rate_func=linear)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
