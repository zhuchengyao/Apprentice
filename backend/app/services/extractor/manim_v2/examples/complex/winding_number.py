from manim import *
import numpy as np


class WindingNumberExample(Scene):
    """
    Winding number as cumulative angle.

    A ValueTracker t sweeps 0 → 4π. The partial curve z(t) = r·exp(2i·t)
    (radius modulates slightly so the curve is visible, not just a
    repeated circle) is drawn by always_redraw. A radial line from the
    origin to z(t) rotates with the trace, and the cumulative angle
    swept is shown as an arc that keeps winding. A live readout reports
    the running Δθ and the winding number ⌊Δθ / (2π)⌋.
    """

    def construct(self):
        title = Tex(r"Winding number $=$ total angle $/\, 2\pi$",
                    font_size=34).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # LEFT COLUMN: the complex plane with curve and radial pointer
        plane = ComplexPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5.5, y_length=5.5,
            background_line_style={"stroke_opacity": 0.3},
        ).shift(LEFT * 3 + 0.2 * DOWN)
        self.play(Create(plane))

        origin_dot = Dot(plane.n2p(0), color=RED, radius=0.1)
        self.add(origin_dot)

        t_tracker = ValueTracker(0.001)

        def curve_pt(t_val):
            # Ellipse-ish curve so consecutive windings don't coincide
            r = 1.4 + 0.25 * np.sin(3 * t_val)
            return r * np.array([np.cos(2 * t_val), np.sin(2 * t_val), 0])

        def partial_curve():
            t_end = t_tracker.get_value()
            pts = [plane.n2p(complex(*curve_pt(s)[:2])) for s in np.linspace(0, t_end, 120)]
            path = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                path.set_points_smoothly(pts)
            else:
                path.set_points_as_corners([pts[0], pts[0]])
            return path

        def tip_dot():
            p = curve_pt(t_tracker.get_value())
            return Dot(plane.n2p(complex(p[0], p[1])), color=BLUE, radius=0.1)

        def radial_line():
            p = curve_pt(t_tracker.get_value())
            return Line(plane.n2p(0), plane.n2p(complex(p[0], p[1])),
                        color=BLUE, stroke_width=3)

        self.add(always_redraw(partial_curve), always_redraw(radial_line), always_redraw(tip_dot))

        # RIGHT COLUMN: stacked readouts
        def info_panel():
            t = t_tracker.get_value()
            total_angle = 2 * t
            winding = int(np.floor(total_angle / TAU)) if total_angle >= 0 else int(np.ceil(total_angle / TAU))
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=WHITE, font_size=30),
                MathTex(rf"\Delta\theta = {total_angle:.2f}\text{{ rad}}",
                        color=BLUE, font_size=30),
                MathTex(rf"\Delta\theta/(2\pi) = {total_angle / TAU:.2f}",
                        color=YELLOW, font_size=30),
                MathTex(rf"n = {winding}", color=GREEN, font_size=40),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.0, 0.5, 0])

        self.add(always_redraw(info_panel))

        # Sweep all the way around twice
        self.play(t_tracker.animate.set_value(2 * PI), run_time=8, rate_func=linear)
        self.wait(0.8)

        summary = MathTex(
            r"n = \frac{1}{2\pi}\!\oint_\gamma \frac{dz}{z}",
            font_size=32, color=GREEN,
        ).move_to([3.0, -3.0, 0])
        self.play(Write(summary))
        self.wait(0.8)
