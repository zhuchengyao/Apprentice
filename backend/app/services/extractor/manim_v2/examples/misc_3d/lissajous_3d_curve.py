from manim import *
import numpy as np


class Lissajous3DCurveExample(ThreeDScene):
    """
    3D Lissajous curve: x = sin(at + δ_x), y = sin(bt + δ_y),
    z = sin(ct + δ_z). Frequencies (a, b, c) determine shape; closes
    only when ratios are rational.

    3D scene:
      ValueTracker t_tr traces the curve; always_redraw growing
      trail; ambient camera rotation.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-1.5, 1.5, 0.5],
                           y_range=[-1.5, 1.5, 0.5],
                           z_range=[-1.5, 1.5, 0.5],
                           x_length=4, y_length=4, z_length=4)
        self.add(axes)

        a, b, c = 3, 5, 4
        phase_x, phase_y, phase_z = 0, PI / 2, PI / 3

        t_tr = ValueTracker(0.001)

        def curve_point(t):
            x = np.sin(a * t + phase_x)
            y = np.sin(b * t + phase_y)
            z = np.sin(c * t + phase_z)
            return axes.c2p(x, y, z)

        def curve_trail():
            t_cur = t_tr.get_value()
            n = max(10, int(200 * t_cur / (2 * PI)))
            pts = [curve_point(t) for t in np.linspace(0, t_cur, n)]
            m = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def rider():
            t = t_tr.get_value()
            return Dot3D(curve_point(t), color=RED, radius=0.1)

        self.add(always_redraw(curve_trail), always_redraw(rider))

        title = Tex(r"3D Lissajous: frequencies (3, 5, 4)",
                    font_size=26).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def panel():
            t = t_tr.get_value()
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"(a, b, c) = ({a}, {b}, {c})",
                         color=WHITE, font_size=20),
                MathTex(r"\text{period } = 2\pi",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.4)

        pnl = panel()
        self.add_fixed_in_frame_mobjects(pnl)

        self.begin_ambient_camera_rotation(rate=0.15)
        self.play(t_tr.animate.set_value(2 * PI),
                   run_time=8, rate_func=linear)
        self.stop_ambient_camera_rotation()
