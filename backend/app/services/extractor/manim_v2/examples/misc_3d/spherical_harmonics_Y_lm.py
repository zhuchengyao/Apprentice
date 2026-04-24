from manim import *
import numpy as np


class SphericalHarmonicsYlmExample(ThreeDScene):
    """
    Spherical harmonics Y_l^m on unit sphere. For each (l, m), the
    real part is a specific angular pattern. We visualize by
    modulating sphere radius proportional to |Y_l^m(θ, φ)|.

    ValueTracker l_idx_tr cycles through (l, m) ∈ {(0, 0), (1, 0),
    (1, 1), (2, 0), (2, 1), (2, 2), (3, 0), (3, 2)}.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.07)

        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1],
                          x_length=4.0, y_length=4.0, z_length=4.0)
        self.add(axes)

        from scipy.special import sph_harm

        configs = [(0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2), (3, 0), (3, 2)]

        idx_tr = ValueTracker(0.0)

        def idx_now():
            return max(0, min(len(configs) - 1, int(round(idx_tr.get_value()))))

        def Y_shape(u, v):
            l, m = configs[idx_now()]
            Y = sph_harm(m, l, v, u).real
            r = 1.0 + 0.6 * Y
            return np.array([r * np.sin(u) * np.cos(v),
                              r * np.sin(u) * np.sin(v),
                              r * np.cos(u)])

        def surf():
            l, m = configs[idx_now()]
            return Surface(
                lambda u, v: Y_shape(u, v),
                u_range=[0.01, PI - 0.01],
                v_range=[0, TAU],
                resolution=(24, 40),
                fill_opacity=0.75,
            ).set_color_by_gradient(BLUE, YELLOW, RED)

        self.add(always_redraw(surf))

        title = Tex(r"Spherical harmonics $Y_l^m$",
                    font_size=26)
        info = VGroup(
            VGroup(Tex(r"$l=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$m=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"$l$ = angular frequency",
                color=GREY_B, font_size=20),
            Tex(r"$m$ = azimuthal mode",
                color=GREY_B, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(configs[idx_now()][0]))
        info[1][1].add_updater(lambda m: m.set_value(configs[idx_now()][1]))

        for k in range(1, len(configs)):
            self.play(idx_tr.animate.set_value(float(k)),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.6)
        self.stop_ambient_camera_rotation()
