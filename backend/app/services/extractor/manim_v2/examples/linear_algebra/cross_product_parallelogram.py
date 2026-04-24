from manim import *
import numpy as np


class CrossProductParallelogramExample(ThreeDScene):
    """
    |a × b| = |a| |b| sin θ = area of the a-b parallelogram.

    3D scene: a = (2, 0, 0) is fixed. ValueTracker theta_tr rotates
    b around the z-axis through 5 configurations (30°, 60°, 90°,
    120°, 150°). always_redraw keeps b-arrow, the a-b parallelogram,
    and the a×b vector in sync. A fixed-frame panel shows live θ
    and |a × b|; ambient camera rotation makes the 3D structure of
    a × b (perpendicular to the parallelogram) obvious.
    """

    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-2, 4, 1],
            x_length=5, y_length=5, z_length=4,
        )
        self.add(axes)

        a_vec = np.array([2.0, 0.0, 0.0])
        a_arrow = Line(ORIGIN, a_vec, color=GREEN, stroke_width=6)
        a_lbl = MathTex(r"\vec a", color=GREEN, font_size=32)
        a_lbl.next_to(axes.c2p(*a_vec), RIGHT, buff=0.15)
        self.add_fixed_orientation_mobjects(a_lbl)
        self.play(Create(a_arrow), Write(a_lbl))

        theta_tr = ValueTracker(30 * DEGREES)
        b_len = 2.0

        def b_vec():
            t = theta_tr.get_value()
            return b_len * np.array([np.cos(t), np.sin(t), 0])

        def b_arrow():
            return Line(ORIGIN, b_vec(), color=RED, stroke_width=6)

        def para():
            b = b_vec()
            return Polygon(ORIGIN, a_vec, a_vec + b, b,
                           color=YELLOW, fill_opacity=0.35,
                           stroke_width=2)

        def cross_arrow():
            c = np.cross(a_vec, b_vec())
            return Line(ORIGIN, c, color=BLUE, stroke_width=6)

        self.add(always_redraw(b_arrow),
                 always_redraw(para),
                 always_redraw(cross_arrow))

        # Fixed-frame overlays (title + live panel)
        title = Tex(r"$|\vec a \times \vec b| = |\vec a|\,|\vec b|\,\sin\theta$ $=$ area",
                    font_size=28).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def make_panel():
            t = theta_tr.get_value()
            area = 2.0 * b_len * np.sin(t)
            panel = VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                        color=WHITE, font_size=26),
                MathTex(rf"|\vec a \times \vec b| = {area:.3f}",
                        color=YELLOW, font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            panel.to_corner(DR, buff=0.5)
            return panel

        panel = make_panel()
        self.add_fixed_in_frame_mobjects(panel)

        # Ambient camera rotation so the reader sees a×b stick up
        self.begin_ambient_camera_rotation(rate=0.2)

        for target_deg in [60, 90, 120, 150, 45]:
            self.play(theta_tr.animate.set_value(target_deg * DEGREES),
                      run_time=1.6, rate_func=smooth)
            new_panel = make_panel()
            self.add_fixed_in_frame_mobjects(new_panel)
            self.play(Transform(panel, new_panel), run_time=0.25)
            self.wait(0.35)

        self.stop_ambient_camera_rotation()
        self.wait(0.5)
