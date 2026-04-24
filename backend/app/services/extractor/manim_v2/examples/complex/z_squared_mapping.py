from manim import *
import numpy as np


class ZSquaredMappingExample(Scene):
    """
    The complex map z ↦ z² as a parameter sweep.

    COMPARISON layout (two side-by-side complex planes):
      LEFT  (input z-plane)  — point z on a circle of radius r; θ swept by ValueTracker.
      RIGHT (output z²-plane) — point z² traces the corresponding squared trajectory:
                                 radius r², argument 2θ.

    A persistent yellow trail on the right collects every visited z². Watch
    how a half-revolution on the left becomes a full revolution on the right.
    """

    def construct(self):
        title = Tex(r"$z \mapsto z^2$ doubles the angle and squares the radius",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # LEFT plane (input z)
        plane_L = ComplexPlane(
            x_range=[-2.2, 2.2, 1], y_range=[-2.2, 2.2, 1],
            x_length=5.2, y_length=5.2,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-3.5, -0.2, 0])
        L_title = Tex(r"$z = r\,e^{i\theta}$", font_size=28, color=BLUE).next_to(plane_L, UP, buff=0.1)
        self.play(Create(plane_L), Write(L_title))

        # RIGHT plane (output z²)
        plane_R = ComplexPlane(
            x_range=[-3.5, 3.5, 1], y_range=[-3.5, 3.5, 1],
            x_length=5.2, y_length=5.2,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([+3.5, -0.2, 0])
        R_title = Tex(r"$z^2 = r^2\,e^{2i\theta}$", font_size=28, color=YELLOW).next_to(plane_R, UP, buff=0.1)
        self.play(Create(plane_R), Write(R_title))

        # Static input circle of radius r=1.5 on left, output |z²|=2.25 on right
        r = 1.5
        in_circle = Circle(
            radius=plane_L.n2p(complex(r, 0))[0] - plane_L.n2p(0)[0],
            color=BLUE, stroke_width=2, stroke_opacity=0.6,
        ).move_to(plane_L.n2p(0))
        out_circle = Circle(
            radius=plane_R.n2p(complex(r * r, 0))[0] - plane_R.n2p(0)[0],
            color=YELLOW, stroke_width=2, stroke_opacity=0.4,
        ).move_to(plane_R.n2p(0))
        self.play(Create(in_circle), Create(out_circle))

        theta = ValueTracker(0.001)

        def z_value():
            t = theta.get_value()
            return r * np.exp(1j * t)

        def z_dot():
            return Dot(plane_L.n2p(z_value()), color=BLUE, radius=0.11)

        def z_arrow():
            return Arrow(plane_L.n2p(0), plane_L.n2p(z_value()),
                         buff=0, color=BLUE, stroke_width=4,
                         max_tip_length_to_length_ratio=0.12)

        def z_squared_dot():
            z = z_value()
            return Dot(plane_R.n2p(z * z), color=YELLOW, radius=0.11)

        def z_squared_arrow():
            z = z_value()
            return Arrow(plane_R.n2p(0), plane_R.n2p(z * z),
                         buff=0, color=YELLOW, stroke_width=4,
                         max_tip_length_to_length_ratio=0.12)

        # Trail of z² visited
        trail_pts: list[np.ndarray] = []

        def trail():
            path = VMobject(color=YELLOW, stroke_width=2, stroke_opacity=0.55)
            if len(trail_pts) >= 2:
                path.set_points_as_corners(trail_pts.copy())
            else:
                p = plane_R.n2p(z_value() ** 2)
                path.set_points_as_corners([p, p])
            return path

        def record_trail(_, dt):
            trail_pts.append(plane_R.n2p(z_value() ** 2))
            if len(trail_pts) > 4000:
                del trail_pts[: len(trail_pts) - 4000]

        recorder = Mobject()
        recorder.add_updater(record_trail)
        self.add(recorder)

        self.add(always_redraw(z_arrow), always_redraw(z_dot),
                 always_redraw(z_squared_arrow), always_redraw(z_squared_dot),
                 always_redraw(trail))

        # Bottom-strip live readouts
        def info_panel():
            t = theta.get_value()
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):+.0f}^\circ",
                        color=BLUE, font_size=24),
                MathTex(rf"2\theta = {np.degrees(2 * t):+.0f}^\circ",
                        color=YELLOW, font_size=24),
                MathTex(rf"|z| = {r:.1f},\;|z^2| = {r * r:.2f}",
                        color=WHITE, font_size=22),
            ).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.4)

        self.add(always_redraw(info_panel))

        # Sweep θ from 0 to 2π so z² goes around twice
        self.play(theta.animate.set_value(2 * PI), run_time=8, rate_func=linear)
        recorder.clear_updaters()
        self.wait(0.8)
