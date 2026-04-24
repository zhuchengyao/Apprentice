from manim import *
import numpy as np


class ImplicitDifferentiationExample(Scene):
    """
    Implicit derivative of x² + y² = 1 visualized along the unit circle.

    TWO_COLUMN:
      LEFT  — NumberPlane with the unit circle. ValueTracker θ moves a
              point P(θ) = (cos θ, sin θ) along the circle; an
              always_redraw tangent line of slope dy/dx = -x/y is drawn
              through P. The slope flips sign predictably as P crosses
              the axes.
      RIGHT — algebra steps (the same as the original) plus live
              numeric x, y, and dy/dx values.
    """

    def construct(self):
        title = Tex(r"Implicit differentiation: $x^2 + y^2 = 1 \Rightarrow \tfrac{dy}{dx} = -\tfrac{x}{y}$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=5.0, y_length=5.0,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-3.0, -0.4, 0])
        unit_circle = Circle(
            radius=plane.n2p(complex(1, 0))[0] - plane.n2p(0)[0],
            color=BLUE, stroke_width=3,
        ).move_to(plane.n2p(0))
        self.play(Create(plane), Create(unit_circle))

        theta_tr = ValueTracker(0.7)

        def P_pt():
            t = theta_tr.get_value()
            return np.array([np.cos(t), np.sin(t)])

        def point_dot():
            p = P_pt()
            return Dot(plane.c2p(p[0], p[1]), color=YELLOW, radius=0.10)

        def tangent_line():
            p = P_pt()
            x, y = p[0], p[1]
            # slope = -x/y; build line of length 2.4 in world units centered at P
            if abs(y) < 1e-3:
                # Vertical tangent
                start = plane.c2p(x, -1.4)
                end = plane.c2p(x, +1.4)
            else:
                m = -x / y
                dx = 1.0
                dy = m * dx
                length = np.sqrt(dx ** 2 + dy ** 2)
                ux, uy = dx / length, dy / length
                start = plane.c2p(x - 1.2 * ux, y - 1.2 * uy)
                end = plane.c2p(x + 1.2 * ux, y + 1.2 * uy)
            return Line(start, end, color=ORANGE, stroke_width=4)

        self.add(always_redraw(tangent_line), always_redraw(point_dot))

        # RIGHT COLUMN: algebra steps + live values
        rcol_x = +3.6

        steps = VGroup(
            MathTex(r"x^2 + y^2 = 1", color=WHITE, font_size=24),
            MathTex(r"\tfrac{d}{dx}(x^2 + y^2) = 0", color=WHITE, font_size=22),
            MathTex(r"2x + 2y\,\tfrac{dy}{dx} = 0", color=WHITE, font_size=24),
            MathTex(r"\tfrac{dy}{dx} = -\tfrac{x}{y}", color=YELLOW, font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +1.6, 0])
        for s in steps:
            self.play(Write(s), run_time=0.6)

        def live_panel():
            t = theta_tr.get_value()
            x, y = np.cos(t), np.sin(t)
            if abs(y) < 1e-3:
                slope_str = r"\pm\infty"
            else:
                slope_str = f"{-x/y:+.3f}"
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                        color=WHITE, font_size=22),
                MathTex(rf"x = {x:+.3f},\ y = {y:+.3f}",
                        color=YELLOW, font_size=22),
                MathTex(rf"\tfrac{{dy}}{{dx}} = {slope_str}",
                        color=ORANGE, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, -1.6, 0])

        self.add(always_redraw(live_panel))

        self.play(theta_tr.animate.set_value(2 * PI + 0.7),
                  run_time=8, rate_func=linear)
        self.wait(1.0)
