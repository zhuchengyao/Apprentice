from manim import *
import numpy as np


class CatenoidSoapFilmExample(ThreeDScene):
    """
    A soap film between two parallel rings forms a catenoid: the only
    minimal surface of revolution. Parametrize:
      x(u, v) = cosh(v/a) · cos(u) · a
      y(u, v) = cosh(v/a) · sin(u) · a
      z(u, v) = v
    with u ∈ [0, 2π], v ∈ [-h, h]. "Neck radius" = a.

    ValueTracker neck_tr sweeps a, narrowing the neck until the
    critical ratio where the film breaks.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=30 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.05)

        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1], z_range=[-2, 2, 1],
                          x_length=4.0, y_length=4.0, z_length=4.0)
        self.add(axes)

        h = 1.3
        neck_tr = ValueTracker(1.0)

        def cat(u, v):
            a = neck_tr.get_value()
            return np.array([a * np.cosh(v / a) * np.cos(u),
                              a * np.cosh(v / a) * np.sin(u),
                              v])

        def surface():
            return Surface(
                lambda u, v: cat(u, v),
                u_range=[0, TAU],
                v_range=[-h, h],
                resolution=(36, 16),
                fill_opacity=0.55,
            ).set_color_by_gradient(BLUE, TEAL)

        self.add(always_redraw(surface))

        # Boundary rings
        def ring(z0):
            a = neck_tr.get_value()
            R_ring = a * np.cosh(z0 / a)
            pts = []
            for u in np.linspace(0, TAU, 60, endpoint=False):
                pts.append(np.array([R_ring * np.cos(u),
                                      R_ring * np.sin(u),
                                      z0]))
            return VMobject().set_points_as_corners(pts + [pts[0]])\
                .set_color(YELLOW).set_stroke(width=4)

        def top_ring():
            return ring(h)

        def bot_ring():
            return ring(-h)

        self.add(always_redraw(top_ring), always_redraw(bot_ring))

        title = Tex(r"Catenoid: minimal surface of revolution",
                    font_size=24)
        info = VGroup(
            VGroup(Tex(r"neck $a=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"ring radius $R=a\cosh(h/a)=$", font_size=20),
                   DecimalNumber(1.98, num_decimal_places=3,
                                 font_size=20).set_color(BLUE)
                   ).arrange(RIGHT, buff=0.1),
            Tex(r"below critical $a$: film breaks",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.add_fixed_in_frame_mobjects(title, info)
        title.to_edge(UP, buff=0.3)
        info.to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(neck_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(
            neck_tr.get_value() * np.cosh(h / neck_tr.get_value())))

        for a in [0.7, 0.5, 1.2, 0.9]:
            self.play(neck_tr.animate.set_value(a),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.5)
        self.stop_ambient_camera_rotation()
