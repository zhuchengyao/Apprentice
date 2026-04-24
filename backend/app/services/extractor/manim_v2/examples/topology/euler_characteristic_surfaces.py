from manim import *
import numpy as np


class EulerCharacteristicSurfacesExample(ThreeDScene):
    """
    Euler characteristic χ of closed surfaces: χ(sphere) = 2,
    χ(torus) = 0, χ(double torus) = -2, χ(genus g) = 2 − 2g.

    ValueTracker g_tr morphs between sphere, torus, and "double torus"
    (genus 2) via a simple surface interpolation. Live χ formula
    readout.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-2, 2, 1],
                          x_length=4.0, y_length=4.0, z_length=3.0)
        self.add(axes)

        g_tr = ValueTracker(0.0)

        def sphere_pts(u, v):
            return np.array([1.5 * np.sin(u) * np.cos(v),
                              1.5 * np.sin(u) * np.sin(v),
                              1.5 * np.cos(u)])

        def torus_pts(u, v):
            R = 1.5
            r = 0.5
            return np.array([(R + r * np.cos(v)) * np.cos(u),
                              (R + r * np.cos(v)) * np.sin(u),
                              r * np.sin(v)])

        def double_torus_approx(u, v):
            # approximation: two tori side by side; use (u ∈ [0, π] ↦ torus1,
            # u ∈ [π, 2π] ↦ torus2) with re-scaling
            if u < PI:
                P = torus_pts(u * 2, v)
                P[0] -= 1.2
                return P
            else:
                P = torus_pts((u - PI) * 2, v)
                P[0] += 1.2
                return P

        def surf_pts(u, v):
            g = g_tr.get_value()
            if g < 0.5:
                alpha = g * 2
                return (1 - alpha) * sphere_pts(u, v) + alpha * torus_pts(u, v)
            else:
                alpha = (g - 0.5) * 2
                return (1 - alpha) * torus_pts(u, v) + alpha * double_torus_approx(u, v)

        def surface():
            return Surface(
                lambda u, v: surf_pts(u, v),
                u_range=[0.02, TAU - 0.02] if g_tr.get_value() > 0.5
                         else [0.02, PI - 0.02],
                v_range=[0, TAU],
                resolution=(28, 24),
                fill_opacity=0.55,
            ).set_color_by_gradient(BLUE, GREEN, ORANGE)

        self.add(always_redraw(surface))

        title = Tex(r"Euler characteristic: $\chi = 2-2g$",
                    font_size=26)
        info = VGroup(
            VGroup(Tex(r"stage $g=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"$g=0$: sphere, $\chi=2$",
                color=BLUE, font_size=20),
            Tex(r"$g=1$: torus, $\chi=0$",
                color=GREEN, font_size=20),
            Tex(r"$g=2$: double torus, $\chi=-2$",
                color=ORANGE, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(g_tr.get_value() * 2))

        self.play(g_tr.animate.set_value(0.5),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(g_tr.animate.set_value(1.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(g_tr.animate.set_value(0.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.stop_ambient_camera_rotation()
