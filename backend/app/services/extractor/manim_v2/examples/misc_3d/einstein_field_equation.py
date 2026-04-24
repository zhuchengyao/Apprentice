from manim import *
import numpy as np


class EinsteinFieldEquationExample(ThreeDScene):
    """
    Einstein's field equation: G_μν + Λ g_μν = 8π T_μν / c⁴.
    Visualized via a flexible 2D grid whose curvature responds to
    a point-mass stress-energy source; ValueTracker m_tr grows the
    mass, deforming the grid more and more.

    3D scene with flat grid; mass at origin depresses the grid via
    h(r) = -m/(r+0.3). ValueTracker m_tr sweeps 0 → 3.
    """

    def construct(self):
        title = Tex(r"Einstein field equation: $G_{\mu\nu} + \Lambda g_{\mu\nu} = \tfrac{8\pi G}{c^4} T_{\mu\nu}$",
                    font_size=24)
        title.to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        self.set_camera_orientation(phi=60 * DEGREES, theta=-50 * DEGREES)
        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-4, 4, 1],
                           z_range=[-3, 1, 1],
                           x_length=6, y_length=6, z_length=3)
        self.add(axes)

        m_tr = ValueTracker(0.0)

        def warped_grid():
            m = m_tr.get_value()
            grp = VGroup()
            # Horizontal and vertical grid lines
            def h(x, y):
                r = np.hypot(x, y)
                return -m / (r + 0.3)

            for yv in np.arange(-3, 3.1, 0.6):
                pts = []
                for xv in np.arange(-3, 3.01, 0.2):
                    z = h(xv, yv)
                    pts.append(axes.c2p(xv, yv, z))
                ln = VMobject(color=BLUE_D, stroke_width=1.5)
                ln.set_points_as_corners(pts)
                grp.add(ln)

            for xv in np.arange(-3, 3.1, 0.6):
                pts = []
                for yv in np.arange(-3, 3.01, 0.2):
                    z = h(xv, yv)
                    pts.append(axes.c2p(xv, yv, z))
                ln = VMobject(color=BLUE_D, stroke_width=1.5)
                ln.set_points_as_corners(pts)
                grp.add(ln)
            return grp

        def mass_ball():
            m = m_tr.get_value()
            r = 0.15 + 0.15 * m
            return Sphere(radius=r, color=YELLOW,
                            fill_opacity=0.85,
                            resolution=(12, 12)
                            ).move_to(axes.c2p(0, 0, -m / 0.3))

        self.add(always_redraw(warped_grid),
                  always_redraw(mass_ball))

        def panel():
            m = m_tr.get_value()
            return VGroup(
                MathTex(rf"M = {m:.2f}",
                         color=YELLOW, font_size=24),
                Tex(r"space curves toward mass",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        p = panel()
        p.to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(p)

        self.begin_ambient_camera_rotation(rate=0.15)
        for m_val in [0.5, 1.2, 2.0, 3.0]:
            self.play(m_tr.animate.set_value(m_val),
                       run_time=1.8, rate_func=smooth)
            new_p = panel()
            new_p.to_corner(DR, buff=0.4)
            self.add_fixed_in_frame_mobjects(new_p)
            self.play(Transform(p, new_p), run_time=0.2)
            self.wait(0.4)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
