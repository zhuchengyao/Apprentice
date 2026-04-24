from manim import *
import numpy as np


class SoapFilmMinimalExample(ThreeDScene):
    """
    Minimal surface: soap-film catenoid connecting two parallel circles.
    ValueTracker h_tr varies separation; as h grows, the catenoid
    neck shrinks; past the critical h/R ≈ 1.325, the film collapses
    into two disks (not shown here; bound to minimum).

    3D scene:
      Two circles in planes z = ±h/2 connected by a catenoid
      x² + y² = (c cosh(z/c))² for fit c.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-2, 2, 1],
                           x_length=3, y_length=3, z_length=3)
        self.add(axes)

        R = 1.0  # ring radius
        h_tr = ValueTracker(0.4)

        def find_c(h, R):
            """Find c such that c cosh(h/(2c)) = R, via bisection."""
            # Valid when h/R < 1.325 (or so)
            # For small h: c ≈ R. For large h: no solution.
            c_lo, c_hi = 0.05, R
            for _ in range(50):
                c_mid = (c_lo + c_hi) / 2
                if c_mid * np.cosh(h / (2 * c_mid)) > R:
                    c_hi = c_mid
                else:
                    c_lo = c_mid
            return c_mid

        def catenoid_surface():
            h = h_tr.get_value()
            c = find_c(h, R)

            def param(u, v):
                # u = z ∈ [-h/2, h/2], v = θ
                z = u * h / 2
                r = c * np.cosh(z / c)
                r = min(r, R)  # clamp
                x = r * np.cos(v)
                y = r * np.sin(v)
                return axes.c2p(x, y, z)

            return Surface(param, u_range=[-1, 1], v_range=[0, 2 * PI],
                             resolution=(15, 28),
                             fill_opacity=0.5,
                             checkerboard_colors=[BLUE, PURPLE])

        # Top/bottom rings
        def top_ring():
            h = h_tr.get_value()
            pts = [axes.c2p(R * np.cos(t), R * np.sin(t), h / 2)
                   for t in np.linspace(0, 2 * PI, 60)]
            m = VMobject(color=WHITE, stroke_width=3)
            m.set_points_as_corners(pts + [pts[0]])
            return m

        def bot_ring():
            h = h_tr.get_value()
            pts = [axes.c2p(R * np.cos(t), R * np.sin(t), -h / 2)
                   for t in np.linspace(0, 2 * PI, 60)]
            m = VMobject(color=WHITE, stroke_width=3)
            m.set_points_as_corners(pts + [pts[0]])
            return m

        self.add(always_redraw(catenoid_surface),
                  always_redraw(top_ring),
                  always_redraw(bot_ring))

        title = Tex(r"Catenoid: minimal surface between two rings",
                    font_size=24).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            h = h_tr.get_value()
            c = find_c(h, R)
            neck_r = c  # neck radius = c
            return VGroup(
                MathTex(rf"h = {h:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"R = {R}", color=WHITE, font_size=20),
                MathTex(rf"\text{{neck radius}} = {neck_r:.3f}",
                         color=BLUE, font_size=20),
                Tex(r"critical $h/R \approx 1.325$",
                     color=RED, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        pnl = panel()
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.15)
        for hv in [0.8, 1.2, 0.4]:
            self.play(h_tr.animate.set_value(hv),
                       run_time=2, rate_func=smooth)
            new_pnl = panel()
            self.add_fixed_in_frame_mobjects(new_pnl)
            self.play(Transform(pnl, new_pnl), run_time=0.2)
            self.wait(0.4)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
