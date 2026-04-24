from manim import *
import numpy as np


class PhaseSpaceOscillatorExample(Scene):
    """
    Harmonic oscillator phase space: (x, p) traces an ellipse.
    Damped case spirals inward; phase-trajectory = energy contour.

    TWO_COLUMN:
      LEFT  — (x, p) plane with always_redraw trajectory trace for
              a harmonic oscillator with small damping γ. ValueTracker
              t_tr advances time; point rides an inward spiral.
      RIGHT — live t, x, p, energy E = ½(x² + p²); second phase
              zero damping + larger amplitude.
    """

    def construct(self):
        title = Tex(r"Phase space of damped oscillator: $\ddot x + 2\gamma\dot x + x = 0$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
                             x_length=5.5, y_length=5.5,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-3.3, -0.3, 0])
        x_lbl = MathTex(r"x", font_size=22
                         ).next_to(plane, RIGHT, buff=0.1).shift(UP * 1.3)
        p_lbl = MathTex(r"p", font_size=22
                         ).next_to(plane, UP, buff=0.1).shift(LEFT * 1.2)
        self.play(Create(plane), Write(x_lbl), Write(p_lbl))

        # Damped oscillator trajectory
        def damped_xp(t, gamma):
            # x(t) = e^{-γt} cos(ωt), ω = √(1 - γ²)
            omega = np.sqrt(max(1 - gamma ** 2, 1e-4))
            A = 2.0
            x = A * np.exp(-gamma * t) * np.cos(omega * t)
            p = A * np.exp(-gamma * t) * (-gamma * np.cos(omega * t)
                                           - omega * np.sin(omega * t))
            return x, p

        state = {"gamma": 0.12}
        t_tr = ValueTracker(0.0)

        def trace():
            T = t_tr.get_value()
            pts = []
            for tv in np.linspace(0, T, int(max(10, T * 25))):
                x, p = damped_xp(tv, state["gamma"])
                pts.append(plane.c2p(x, p))
            v = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                v.set_points_as_corners(pts)
            return v

        def rider():
            T = t_tr.get_value()
            x, p = damped_xp(T, state["gamma"])
            return Dot(plane.c2p(x, p), color=RED, radius=0.1)

        self.add(always_redraw(trace), always_redraw(rider))

        def info():
            T = t_tr.get_value()
            x, p = damped_xp(T, state["gamma"])
            E = 0.5 * (x ** 2 + p ** 2)
            return VGroup(
                MathTex(rf"\gamma = {state['gamma']:.3f}",
                         color=YELLOW, font_size=24),
                MathTex(rf"t = {T:.2f}", color=WHITE, font_size=24),
                MathTex(rf"x = {x:+.3f}", color=BLUE, font_size=22),
                MathTex(rf"p = {p:+.3f}", color=ORANGE, font_size=22),
                MathTex(rf"E = \tfrac{{1}}{{2}}(x^2+p^2) = {E:.3f}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.5, 0.0, 0])

        self.add(always_redraw(info))

        # Phase 1: damped
        self.play(t_tr.animate.set_value(25.0),
                   run_time=7, rate_func=linear)
        self.wait(0.3)

        # Phase 2: reset with no damping (steady ellipse)
        state["gamma"] = 0.0
        self.play(t_tr.animate.set_value(0.0), run_time=0.6)
        self.play(t_tr.animate.set_value(4 * PI),
                   run_time=5, rate_func=linear)
        self.wait(0.4)
