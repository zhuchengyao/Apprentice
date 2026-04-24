from manim import *
import numpy as np


class ParametricSurfaceAreaExample(ThreeDScene):
    """
    Surface area of parametric surface: A = ∫∫ |r_u × r_v| du dv.
    Example: hemisphere r(u, v) = (sin u cos v, sin u sin v, cos u),
    u ∈ [0, π/2], v ∈ [0, 2π], has area 2π.

    3D scene:
      Hemisphere + Riemann approximation parallelograms; ValueTracker
      N_tr refines N×N grid; approximate area → 2π.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-1.5, 1.5, 0.5], y_range=[-1.5, 1.5, 0.5],
                           z_range=[0, 1.5, 0.5],
                           x_length=4, y_length=4, z_length=2)
        self.add(axes)

        # Hemisphere (unit)
        def param(u, v):
            return axes.c2p(np.sin(u) * np.cos(v),
                             np.sin(u) * np.sin(v),
                             np.cos(u))

        hemi = Surface(param, u_range=[0.01, PI / 2], v_range=[0, 2 * PI],
                         resolution=(15, 25),
                         fill_opacity=0.3,
                         checkerboard_colors=[BLUE_D, BLUE_E])
        self.add(hemi)

        N_tr = ValueTracker(3)

        def rect_patches():
            N = int(round(N_tr.get_value()))
            N = max(2, min(N, 15))
            du = (PI / 2) / N
            dv = (2 * PI) / (2 * N)
            grp = VGroup()
            for i in range(N):
                for j in range(2 * N):
                    u0 = i * du
                    v0 = j * dv
                    # Parallelogram from r(u0, v0), r(u0+du, v0), etc.
                    p00 = np.array([np.sin(u0) * np.cos(v0),
                                     np.sin(u0) * np.sin(v0),
                                     np.cos(u0)])
                    p10 = np.array([np.sin(u0 + du) * np.cos(v0),
                                     np.sin(u0 + du) * np.sin(v0),
                                     np.cos(u0 + du)])
                    p11 = np.array([np.sin(u0 + du) * np.cos(v0 + dv),
                                     np.sin(u0 + du) * np.sin(v0 + dv),
                                     np.cos(u0 + du)])
                    p01 = np.array([np.sin(u0) * np.cos(v0 + dv),
                                     np.sin(u0) * np.sin(v0 + dv),
                                     np.cos(u0)])
                    poly = Polygon(axes.c2p(*p00), axes.c2p(*p10),
                                     axes.c2p(*p11), axes.c2p(*p01),
                                     color=YELLOW, fill_opacity=0.35,
                                     stroke_width=0.3)
                    grp.add(poly)
            return grp

        self.add(always_redraw(rect_patches))

        title = Tex(r"Surface area: $A = \iint |r_u \times r_v|\,du\,dv$",
                    font_size=22).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            N = int(round(N_tr.get_value()))
            N = max(2, min(N, 15))
            # Numerical approximation of area
            du = (PI / 2) / N
            dv = (2 * PI) / (2 * N)
            total = 0.0
            for i in range(N):
                for j in range(2 * N):
                    u = (i + 0.5) * du
                    v = (j + 0.5) * dv
                    # |r_u × r_v| = sin u for unit sphere
                    total += np.sin(u) * du * dv
            return VGroup(
                MathTex(rf"N = {N}", color=YELLOW, font_size=22),
                MathTex(rf"A_N = {total:.4f}",
                         color=YELLOW, font_size=20),
                MathTex(rf"A_{{\text{{true}}}} = 2\pi = {2 * PI:.4f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        pnl = panel()
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.12)
        for nv in [5, 10, 15]:
            self.play(N_tr.animate.set_value(nv),
                       run_time=1.8, rate_func=smooth)
            new_pnl = panel()
            self.add_fixed_in_frame_mobjects(new_pnl)
            self.play(Transform(pnl, new_pnl), run_time=0.2)
            self.wait(0.5)
        self.stop_ambient_camera_rotation()
