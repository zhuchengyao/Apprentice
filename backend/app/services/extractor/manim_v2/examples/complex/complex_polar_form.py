from manim import *
import numpy as np


class ComplexPolarFormExample(Scene):
    """
    Polar form z = r·e^(iθ) with both r and θ controlled by trackers.

    TWO_COLUMN:
      LEFT  — ComplexPlane with origin, an arrow z = r·e^(iθ), a dot at
              its tip, the radius r marked along the arrow, and an arc
              for the angle θ. Two ValueTrackers r_tr and θ_tr drive
              everything via always_redraw.
      RIGHT — live readouts of r, θ (degrees and radians), Re(z), Im(z),
              and the formula z = r·cosθ + i·r·sinθ instantiated with
              the current numbers.

    Tour: first sweep θ at fixed r=2 to show z trace a circle; then
    sweep r at fixed θ=π/3 to show z slide along a ray.
    """

    def construct(self):
        title = Tex(r"Polar form: $z = r\,e^{i\theta} = r\cos\theta + i\,r\sin\theta$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # LEFT plane
        plane = ComplexPlane(
            x_range=[-3.2, 3.2, 1], y_range=[-3.2, 3.2, 1],
            x_length=5.6, y_length=5.6,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-3.0, -0.2, 0])
        self.play(Create(plane))

        r_tr = ValueTracker(2.0)
        theta_tr = ValueTracker(PI / 6)

        def z_value():
            r = r_tr.get_value()
            t = theta_tr.get_value()
            return r * np.array([np.cos(t), np.sin(t), 0])

        def z_arrow():
            return Arrow(plane.c2p(0, 0), plane.c2p(z_value()[0], z_value()[1]),
                         buff=0, color=YELLOW, stroke_width=5,
                         max_tip_length_to_length_ratio=0.10)

        def z_dot():
            return Dot(plane.c2p(z_value()[0], z_value()[1]),
                       color=YELLOW, radius=0.10)

        def angle_arc():
            t = theta_tr.get_value()
            arc_radius = max(0.55, 0.5 + 0.1 * (t / PI))
            return Arc(radius=arc_radius * (plane.n2p(1)[0] - plane.n2p(0)[0]),
                       start_angle=0, angle=t,
                       arc_center=plane.c2p(0, 0),
                       color=GREEN, stroke_width=4)

        def r_label():
            mid = z_value() / 2
            return MathTex(r"r", color=YELLOW, font_size=24).move_to(
                plane.c2p(mid[0], mid[1]) + np.array([-0.2, 0.25, 0]))

        def theta_label():
            t = theta_tr.get_value()
            arc_radius = 0.85
            mid_angle = t / 2
            offset = arc_radius * np.array([np.cos(mid_angle), np.sin(mid_angle), 0])
            return MathTex(r"\theta", color=GREEN, font_size=24).move_to(
                plane.c2p(0, 0) + offset)

        # Persistent trail of visited z values
        trail_pts: list[np.ndarray] = []

        def trail():
            path = VMobject(color=YELLOW, stroke_width=2, stroke_opacity=0.4)
            if len(trail_pts) >= 2:
                path.set_points_as_corners(trail_pts.copy())
            else:
                p = plane.c2p(z_value()[0], z_value()[1])
                path.set_points_as_corners([p, p])
            return path

        def record(_, dt):
            trail_pts.append(plane.c2p(z_value()[0], z_value()[1]))
            if len(trail_pts) > 4000:
                del trail_pts[: len(trail_pts) - 4000]

        recorder = Mobject()
        recorder.add_updater(record)
        self.add(recorder, always_redraw(trail))

        self.add(always_redraw(z_arrow), always_redraw(z_dot),
                 always_redraw(angle_arc), always_redraw(r_label),
                 always_redraw(theta_label))

        # RIGHT COLUMN: live readouts
        rcol_x = +3.6

        def info_panel():
            r = r_tr.get_value()
            t = theta_tr.get_value()
            re_z = r * np.cos(t)
            im_z = r * np.sin(t)
            return VGroup(
                MathTex(rf"r = {r:.2f}", color=YELLOW, font_size=28),
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ = {t:.3f}\,\text{{rad}}",
                        color=GREEN, font_size=24),
                MathTex(rf"\mathrm{{Re}}(z) = r\cos\theta = {re_z:+.3f}",
                        color=BLUE, font_size=22),
                MathTex(rf"\mathrm{{Im}}(z) = r\sin\theta = {im_z:+.3f}",
                        color=BLUE, font_size=22),
                MathTex(rf"z = {re_z:+.2f} {im_z:+.2f}\,i",
                        color=YELLOW, font_size=26),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +0.6, 0])

        self.add(always_redraw(info_panel))

        # Tour 1: sweep θ at fixed r=2 → circle
        self.play(theta_tr.animate.set_value(2 * PI + PI / 6),
                  run_time=5, rate_func=linear)
        self.wait(0.4)

        # Tour 2: sweep r at fixed θ=π/3 → ray
        self.play(theta_tr.animate.set_value(PI / 3),
                  r_tr.animate.set_value(0.4),
                  run_time=1.5, rate_func=smooth)
        self.play(r_tr.animate.set_value(2.8), run_time=2.5, rate_func=smooth)
        self.play(r_tr.animate.set_value(2.0), run_time=1.0, rate_func=smooth)

        recorder.clear_updaters()

        identity = MathTex(r"e^{i\theta} = \cos\theta + i\sin\theta",
                           color=YELLOW, font_size=28).move_to([rcol_x, -2.6, 0])
        self.play(Write(identity))
        self.wait(1.0)
