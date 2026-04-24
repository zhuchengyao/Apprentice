from manim import *
import numpy as np


class BorsukUlamAntipodesExample(Scene):
    """
    Borsuk-Ulam (1D): for any continuous f: S¹ → ℝ, there exist
    antipodal points θ, θ + π with f(θ) = f(θ + π). Equivalently,
    g(θ) = f(θ) − f(θ + π) is continuous, g(θ+π) = −g(θ), so g
    must hit zero.

    TWO_COLUMN:
      LEFT  — unit circle with antipodal probe dots at θ and θ+π
              (driven by ValueTracker θ_tr), each colored by
              f(θ) = cos(2θ) + 0.6 sin(3θ).
      RIGHT — axes plotting g(θ) = f(θ) − f(θ + π); always_redraw
              moving point traces along; dashed y=0 line;
              highlight when |g(θ)| < 0.02 (near a zero).
    """

    def construct(self):
        title = Tex(r"Borsuk-Ulam: some antipodes satisfy $f(\theta) = f(\theta + \pi)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 1.6
        circ_center = np.array([-3.8, -0.4, 0])
        circle = Circle(radius=R, color=WHITE, stroke_width=3
                         ).move_to(circ_center)
        self.play(Create(circle))

        def f(theta):
            return np.cos(2 * theta) + 0.6 * np.sin(3 * theta)

        def g(theta):
            return f(theta) - f(theta + PI)

        theta_tr = ValueTracker(0.0)

        def p1():
            t = theta_tr.get_value()
            p = circ_center + R * np.array([np.cos(t), np.sin(t), 0])
            return Dot(p, color=BLUE, radius=0.11)

        def p2():
            t = theta_tr.get_value() + PI
            p = circ_center + R * np.array([np.cos(t), np.sin(t), 0])
            return Dot(p, color=ORANGE, radius=0.11)

        def chord():
            t = theta_tr.get_value()
            p_a = circ_center + R * np.array([np.cos(t), np.sin(t), 0])
            p_b = circ_center + R * np.array([np.cos(t + PI), np.sin(t + PI), 0])
            return DashedLine(p_a, p_b, color=GREY_B, stroke_width=1.8)

        self.add(always_redraw(chord),
                  always_redraw(p1),
                  always_redraw(p2))

        # g(θ) axes on right
        ax = Axes(x_range=[0, 2 * PI + 0.1, PI / 2],
                   y_range=[-3, 3, 1],
                   x_length=6.5, y_length=4.5, tips=False,
                   axis_config={"font_size": 14}
                   ).move_to([3.0, -0.2, 0])
        g_curve = ax.plot(g, x_range=[0, 2 * PI, 0.02],
                           color=GREEN, stroke_width=3)
        zero_line = DashedLine(ax.c2p(0, 0), ax.c2p(2 * PI, 0),
                                color=RED, stroke_width=2)
        x_lbls = VGroup()
        for k, lbl in [(0, r"0"), (1, r"\tfrac{\pi}{2}"), (2, r"\pi"),
                        (3, r"\tfrac{3\pi}{2}"), (4, r"2\pi")]:
            x_lbls.add(MathTex(lbl, font_size=16).next_to(
                ax.c2p(k * PI / 2, 0), DOWN, buff=0.1))
        g_lbl = MathTex(r"g(\theta) = f(\theta) - f(\theta + \pi)",
                         color=GREEN, font_size=22
                         ).next_to(ax, UP, buff=0.15)
        self.play(Create(ax), Create(g_curve), Create(zero_line),
                   Write(g_lbl), FadeIn(x_lbls))

        def rider():
            t = theta_tr.get_value()
            return Dot(ax.c2p(t, g(t)), color=YELLOW, radius=0.1)

        self.add(always_redraw(rider))

        def info():
            t = theta_tr.get_value()
            gv = g(t)
            hit = abs(gv) < 0.05
            return VGroup(
                MathTex(rf"\theta = {t:.3f}", color=WHITE, font_size=22),
                MathTex(rf"f(\theta) = {f(t):+.3f}",
                         color=BLUE, font_size=22),
                MathTex(rf"f(\theta + \pi) = {f(t + PI):+.3f}",
                         color=ORANGE, font_size=22),
                MathTex(rf"g(\theta) = {gv:+.3f}",
                         color=RED if hit else GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(DOWN, buff=0.4)

        self.add(always_redraw(info))

        self.play(theta_tr.animate.set_value(2 * PI),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
