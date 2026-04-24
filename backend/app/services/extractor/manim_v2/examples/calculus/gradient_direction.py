from manim import *
import numpy as np


class GradientDirectionExample(Scene):
    """
    Gradient is perpendicular to level curves and points uphill.

    SINGLE_FOCUS:
      f(x, y) = x² + y² with several concentric level curves drawn.
      ValueTracker θ_tr moves a GREEN probe dot around the level
      curve x²+y²=4; always_redraw a YELLOW gradient arrow ∇f=(2x,2y)
      at the probe, and a RED tangent-to-level-curve arrow
      perpendicular to it. Proves ∇f ⊥ level set.
    """

    def construct(self):
        title = Tex(r"$\nabla f$ is perpendicular to level curves",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=7.2, y_length=5.4,
                             background_line_style={"stroke_opacity": 0.25}
                             ).move_to([-2.5, -0.3, 0])
        self.play(Create(plane))

        # Level curves of f(x, y) = x² + y²
        levels = VGroup()
        for c in [1, 4, 9]:
            r = np.sqrt(c)
            circ = Circle(radius=r, color=BLUE_D, stroke_width=2
                           ).move_to(plane.c2p(0, 0))
            # visual scale correction for plane
            p0 = plane.c2p(0, 0)
            p1 = plane.c2p(r, 0)
            scale = p1[0] - p0[0]
            circ.set_width(2 * scale)
            levels.add(circ)
            lbl = MathTex(rf"f = {c}", font_size=18, color=BLUE_D
                           ).move_to(plane.c2p(r * 0.9, r * 0.7))
            levels.add(lbl)
        self.play(Create(levels))

        theta_tr = ValueTracker(0.4)
        r_level = 2.0  # probe on circle x²+y²=4

        def probe_point():
            t = theta_tr.get_value()
            return plane.c2p(r_level * np.cos(t), r_level * np.sin(t))

        def grad_arrow():
            t = theta_tr.get_value()
            x, y = r_level * np.cos(t), r_level * np.sin(t)
            gx, gy = 2 * x, 2 * y
            # Scale gradient for display
            s = 0.2
            tail = plane.c2p(x, y)
            head = plane.c2p(x + s * gx, y + s * gy)
            return Arrow(tail, head, color=YELLOW, buff=0,
                          stroke_width=5, max_tip_length_to_length_ratio=0.15)

        def tangent_arrow():
            t = theta_tr.get_value()
            x, y = r_level * np.cos(t), r_level * np.sin(t)
            tx, ty = -np.sin(t), np.cos(t)
            s = 1.2
            tail = plane.c2p(x - s * tx, y - s * ty)
            head = plane.c2p(x + s * tx, y + s * ty)
            return Arrow(tail, head, color=RED, buff=0, stroke_width=3,
                          max_tip_length_to_length_ratio=0.1)

        def probe_dot():
            return Dot(probe_point(), color=GREEN, radius=0.1)

        self.add(always_redraw(tangent_arrow),
                  always_redraw(grad_arrow),
                  always_redraw(probe_dot))

        def info():
            t = theta_tr.get_value()
            x, y = r_level * np.cos(t), r_level * np.sin(t)
            return VGroup(
                MathTex(rf"(x, y) = ({x:+.2f}, {y:+.2f})",
                         color=GREEN, font_size=22),
                MathTex(rf"\nabla f = (2x, 2y) = ({2*x:+.2f}, {2*y:+.2f})",
                         color=YELLOW, font_size=22),
                MathTex(r"\nabla f \cdot \vec t = 0",
                         color=WHITE, font_size=22),
                MathTex(r"\vec t = (-\sin\theta, \cos\theta)",
                         color=RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.3, 0.0, 0])

        self.add(always_redraw(info))

        self.play(theta_tr.animate.set_value(0.4 + 2 * TAU),
                   run_time=10, rate_func=linear)
        self.wait(0.4)
