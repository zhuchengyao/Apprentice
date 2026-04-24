from manim import *
import numpy as np


class Implicit3DSurfaceExample(ThreeDScene):
    """
    Level sets of f(x, y, z): the surface f = c parametrized by
    varying c. Here f(x, y, z) = x² + y² - z² − 1 gives hyperboloids.
    For c > 0: one-sheet; c < 0: two-sheet.

    3D scene:
      ValueTracker c_tr sweeps c from -1 → +1; always_redraw the
      level-set surface.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=3)
        self.add(axes)

        c_tr = ValueTracker(0.5)

        def surface():
            c = c_tr.get_value()
            # Hyperboloid: x² + y² = z² + c + 1 (shifted for visual)
            # Parametrize with u = z ∈ [-z_max, z_max], v = θ ∈ [0, 2π]
            # radius² = z² + c; valid for z² + c > 0

            def param(u, v):
                z = u * 1.8
                r_sq = z * z + c
                if r_sq < 0.01:
                    r_sq = 0.01
                r = np.sqrt(r_sq)
                x = r * np.cos(v)
                y = r * np.sin(v)
                return axes.c2p(x, y, z)

            return Surface(param, u_range=[-1, 1], v_range=[0, 2 * PI],
                             resolution=(15, 24),
                             fill_opacity=0.6,
                             checkerboard_colors=[BLUE, BLUE_D])

        self.add(always_redraw(surface))

        title = Tex(r"Level sets of $f(x,y,z) = x^2 + y^2 - z^2$",
                    font_size=24).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            c = c_tr.get_value()
            if c > 0.05:
                kind = "one-sheet hyperboloid"
            elif c < -0.05:
                kind = "two-sheet hyperboloid"
            else:
                kind = "cone (degenerate)"
            return VGroup(
                MathTex(rf"c = {c:+.2f}", color=YELLOW, font_size=24),
                Tex(kind, color=GREEN, font_size=20),
                MathTex(r"x^2 + y^2 - z^2 = c",
                         color=WHITE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        pnl = panel()
        pnl.to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.15)
        for cv in [1.0, 0.0, -0.8, 0.4]:
            self.play(c_tr.animate.set_value(cv),
                       run_time=2, rate_func=smooth)
            new_pnl = panel()
            new_pnl.to_corner(DR, buff=0.4)
            self.add_fixed_in_frame_mobjects(new_pnl)
            self.play(Transform(pnl, new_pnl), run_time=0.2)
            self.wait(0.5)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
