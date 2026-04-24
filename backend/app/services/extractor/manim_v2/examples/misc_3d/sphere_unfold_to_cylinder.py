from manim import *
import numpy as np


class SphereUnfoldToCylinderExample(ThreeDScene):
    """
    Archimedes: a sphere and its circumscribed cylinder (of the
    same radius and height 2R) have equal surface area = 4πR².

    3D scene: ValueTracker s_tr morphs a sphere of radius R into a
    cylinder of radius R and height 2R (z-axis projection). The
    always_redraw Surface uses cos(φ) + s·sign(cos φ) ramp to
    preserve local area. Side panel shows "both areas = 4πR²".
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-35 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=4)
        self.add(axes)

        R = 1.2

        s_tr = ValueTracker(0.0)

        def surface():
            s = s_tr.get_value()

            def param(u, v):
                # u ∈ [0, 2π] (longitude), v ∈ [0, π] (colatitude)
                # Sphere: (R sin v cos u, R sin v sin u, R cos v)
                # Cylinder: (R cos u, R sin u, z) with z = R cos v
                # Interpolate: radius = (1-s) R sin v + s R
                rho = (1 - s) * R * np.sin(v) + s * R
                z = R * np.cos(v)
                x = rho * np.cos(u)
                y = rho * np.sin(u)
                return axes.c2p(x, y, z)

            return Surface(param, u_range=[0, 2 * PI],
                             v_range=[0.05, PI - 0.05],
                             resolution=(24, 12),
                             fill_opacity=0.75,
                             checkerboard_colors=[BLUE_D, BLUE_E])

        self.add(always_redraw(surface))

        title = Tex(r"Archimedes: sphere $\to$ cylinder, same lateral area $4\pi R^2$",
                    font_size=22).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            s = s_tr.get_value()
            name = "sphere" if s < 0.05 else ("cylinder" if s > 0.95 else "morph")
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=WHITE, font_size=24),
                Tex(name, color=YELLOW, font_size=22),
                MathTex(r"\text{area} = 4\pi R^2",
                         color=GREEN, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        p = panel()
        p.to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(p)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(s_tr.animate.set_value(1.0), run_time=5, rate_func=smooth)
        new_p = panel()
        new_p.to_corner(DR, buff=0.4)
        self.add_fixed_in_frame_mobjects(new_p)
        self.play(Transform(p, new_p), run_time=0.2)
        self.wait(2.0)
        self.play(s_tr.animate.set_value(0.0), run_time=3, rate_func=smooth)
        self.wait(0.6)
        self.stop_ambient_camera_rotation()
