from manim import *
import numpy as np


class ParametricKnotAnimationExample(ThreeDScene):
    """
    Animate a parametric curve tracing through several standard knots.
    Torus knot T(2, 3) = trefoil, figure-eight knot via
    x = (cos 2t)(2 + cos 3t), y = (sin 2t)(2 + cos 3t), z = sin 3t.

    ValueTracker t_max_tr grows the knot; second phase morphs
    parameters to "open" it back to a circle to show knotted ↔ unknot.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.06)

        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-1.5, 1.5, 1],
                          x_length=4.5, y_length=4.5, z_length=3.0)
        self.add(axes)

        t_max_tr = ValueTracker(0.5)
        knot_type_tr = ValueTracker(0.0)  # 0 = trefoil, 1 = unknot

        def knot(t):
            k = knot_type_tr.get_value()
            # Trefoil: (2 + cos 3t) cos 2t, (2 + cos 3t) sin 2t, sin 3t
            # Unknot:  2 cos t, 2 sin t, 0
            trefoil = np.array([(2 + np.cos(3 * t)) * np.cos(2 * t),
                                 (2 + np.cos(3 * t)) * np.sin(2 * t),
                                 np.sin(3 * t)])
            unknot = np.array([2 * np.cos(t), 2 * np.sin(t), 0])
            return (1 - k) * trefoil + k * unknot

        def curve():
            t_max = t_max_tr.get_value() * TAU
            ts = np.linspace(0, t_max, max(20, int(200 * t_max / TAU)))
            pts = [knot(t) for t in ts]
            col_grad = [interpolate_color(BLUE, RED, i / max(1, len(pts) - 1))
                        for i in range(len(pts))]
            lines = VGroup()
            for i in range(len(pts) - 1):
                lines.add(Line(pts[i], pts[i + 1],
                                color=col_grad[i], stroke_width=4))
            return lines

        self.add(always_redraw(curve))

        title = Tex(r"Trefoil knot $T(2,3)$ morphs to unknot (forbidden!)",
                    font_size=22)
        info = VGroup(
            VGroup(Tex(r"$t_{\max}/2\pi=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"morph $k=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"$k=0$: trefoil (knotted)",
                color=BLUE, font_size=20),
            Tex(r"$k=1$: circle (unknot)",
                color=GREEN, font_size=20),
            Tex(r"note: knots are not homotopic via ambient isotopy",
                color=RED, font_size=16),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(t_max_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(knot_type_tr.get_value()))

        self.play(t_max_tr.animate.set_value(1.0),
                  run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(knot_type_tr.animate.set_value(1.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(knot_type_tr.animate.set_value(0.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.stop_ambient_camera_rotation()
