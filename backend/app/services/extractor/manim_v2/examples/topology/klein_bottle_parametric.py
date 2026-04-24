from manim import *
import numpy as np


class KleinBottleParametricExample(ThreeDScene):
    """
    Klein bottle immersed in ℝ³ (non-embedded — self-intersects).
    Standard parametrization:
       x(u, v) = (R + cos(u/2) sin v − sin(u/2) sin 2v) cos u
       y(u, v) = (R + cos(u/2) sin v − sin(u/2) sin 2v) sin u
       z(u, v) = sin(u/2) sin v + cos(u/2) sin 2v
    u, v ∈ [0, 2π]. R controls size.

    ValueTracker u_max_tr grows the surface from 0 to 2π. Camera
    ambient rotation reveals the "handle passing through the wall."
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.07)

        axes = ThreeDAxes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], z_range=[-2.5, 2.5, 1],
                          x_length=4.5, y_length=4.5, z_length=3.0)
        self.add(axes)

        R = 2.5

        def klein(u, v):
            r = R + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)
            x = r * np.cos(u)
            y = r * np.sin(u)
            z = np.sin(u / 2) * np.sin(v) + np.cos(u / 2) * np.sin(2 * v)
            return np.array([x, y, z])

        u_max_tr = ValueTracker(0.4)

        def surf():
            return Surface(
                lambda u, v: klein(u, v),
                u_range=[0, u_max_tr.get_value()],
                v_range=[0, TAU],
                resolution=(36, 24),
                fill_opacity=0.55,
            ).set_color_by_gradient(BLUE, TEAL, ORANGE)

        self.add(always_redraw(surf))

        title = Tex(r"Klein bottle immersion in $\mathbb{R}^3$",
                    font_size=24)
        info = VGroup(
            VGroup(Tex(r"$u_{\max}=$", font_size=22),
                   DecimalNumber(0.4, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"non-orientable, no boundary",
                color=YELLOW, font_size=20),
            Tex(r"self-intersects in $\mathbb{R}^3$",
                color=RED, font_size=20),
            Tex(r"embeds in $\mathbb{R}^4$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(u_max_tr.get_value()))

        self.play(u_max_tr.animate.set_value(TAU),
                  run_time=6, rate_func=smooth)
        self.wait(1.0)
        self.stop_ambient_camera_rotation()
