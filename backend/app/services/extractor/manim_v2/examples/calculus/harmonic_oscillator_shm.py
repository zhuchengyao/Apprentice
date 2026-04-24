from manim import *
import numpy as np


class HarmonicOscillatorSHMExample(Scene):
    """
    Simple harmonic oscillator from _2025/laplace/shm:
    x'' + ω²x = 0 with x(0) = A, x'(0) = 0. Solution x(t) = A cos(ωt).

    TWO_COLUMN:
      LEFT  — position vs time plot; ValueTracker t_tr sweeps with
              always_redraw rider dot; separately v(t) = -Aω sin(ωt).
      RIGHT — phase plot (x, v/ω) traces a closed circle of radius A;
              live (x, v, energy) panel.
    """

    def construct(self):
        title = Tex(r"Simple harmonic motion: $x(t) = A\cos(\omega t)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = 1.5
        omega = 1.2

        # LEFT: time-domain
        ax_t = Axes(x_range=[0, 12, 2], y_range=[-2, 2, 1],
                     x_length=6, y_length=3.5, tips=False,
                     axis_config={"font_size": 14, "include_numbers": True}
                     ).move_to([-3.5, -0.3, 0])
        t_lbl = MathTex(r"t", font_size=20).next_to(ax_t, DOWN, buff=0.1)
        self.play(Create(ax_t), Write(t_lbl))

        x_curve = ax_t.plot(lambda t: A * np.cos(omega * t),
                              x_range=[0, 12], color=BLUE, stroke_width=3)
        v_curve = ax_t.plot(lambda t: -A * omega * np.sin(omega * t) / omega,
                              x_range=[0, 12], color=ORANGE, stroke_width=2,
                              stroke_opacity=0.7)
        self.play(Create(x_curve), Create(v_curve))

        lbl_x = MathTex(r"x(t)", color=BLUE, font_size=20).next_to(
            ax_t.c2p(12, A), UP, buff=0.15)
        lbl_v = MathTex(r"v/\omega", color=ORANGE, font_size=18).next_to(
            ax_t.c2p(12, -A), DOWN, buff=0.15)
        self.play(Write(lbl_x), Write(lbl_v))

        # RIGHT: phase plane
        plane = NumberPlane(x_range=[-2.2, 2.2, 1], y_range=[-2.2, 2.2, 1],
                             x_length=3.5, y_length=3.5,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([3.5, -0.3, 0])
        phase_x_lbl = MathTex(r"x", font_size=18).next_to(plane, DOWN, buff=0.1)
        phase_v_lbl = MathTex(r"v/\omega", font_size=18).next_to(plane, LEFT, buff=0.1)
        orbit = Circle(radius=plane.c2p(A, 0)[0] - plane.c2p(0, 0)[0],
                        color=YELLOW, stroke_width=2.5
                        ).move_to(plane.c2p(0, 0))
        self.play(Create(plane), Write(phase_x_lbl), Write(phase_v_lbl),
                   Create(orbit))

        t_tr = ValueTracker(0.0)

        def x_dot():
            t = t_tr.get_value()
            return Dot(ax_t.c2p(t, A * np.cos(omega * t)),
                        color=BLUE, radius=0.09)

        def v_dot():
            t = t_tr.get_value()
            return Dot(ax_t.c2p(t, -A * np.sin(omega * t)),
                        color=ORANGE, radius=0.09)

        def phase_dot():
            t = t_tr.get_value()
            x = A * np.cos(omega * t)
            v_over_w = -A * np.sin(omega * t)
            return Dot(plane.c2p(x, v_over_w), color=RED, radius=0.1)

        self.add(always_redraw(x_dot),
                  always_redraw(v_dot),
                  always_redraw(phase_dot))

        def info():
            t = t_tr.get_value()
            x = A * np.cos(omega * t)
            v = -A * omega * np.sin(omega * t)
            E = 0.5 * v ** 2 + 0.5 * omega ** 2 * x ** 2
            return VGroup(
                MathTex(rf"t = {t:.2f}", color=WHITE, font_size=22),
                MathTex(rf"x = {x:+.3f}", color=BLUE, font_size=22),
                MathTex(rf"v = {v:+.3f}", color=ORANGE, font_size=22),
                MathTex(rf"E = \tfrac{{1}}{{2}}\omega^2 A^2 = {E:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"\omega = {omega}, A = {A}",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.35)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(12),
                   run_time=8, rate_func=linear)
        self.wait(0.4)
