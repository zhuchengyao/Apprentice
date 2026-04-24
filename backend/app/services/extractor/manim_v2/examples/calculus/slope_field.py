from manim import *
import numpy as np


class SlopeFieldExample(Scene):
    """
    Slope field for dy/dx = y - x with a growing integral curve.

    TWO_COLUMN:
      LEFT  — axes with a lattice of slope ticks; ValueTracker x_tr
              sweeps from x0=-2.2 to 1.6; an always_redraw integral
              curve through (x0, y0) = (-2.2, -0.7) extends as x_tr
              grows, and a BLUE dot rides the curve.
      RIGHT — live (x, y), dy/dx = y - x, and the closed-form
              solution y = x + 1 - 1/2 e^(x - x_0).
    """

    def construct(self):
        title = Tex(r"Slope field: $\dfrac{dy}{dx} = y - x$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(
            x_range=[-3, 2.2, 1], y_range=[-3, 3, 1],
            x_length=7, y_length=5.5, tips=False,
            axis_config={"include_numbers": True,
                         "font_size": 16},
        ).move_to([-2.8, -0.3, 0])
        self.play(Create(axes))

        # Slope ticks
        ticks = VGroup()
        for xv in np.arange(-2.6, 2.1, 0.4):
            for yv in np.arange(-2.8, 2.9, 0.4):
                slope = yv - xv
                angle = np.arctan(slope)
                p = axes.c2p(xv, yv)
                v = 0.13 * np.array([np.cos(angle), np.sin(angle), 0])
                ticks.add(Line(p - v, p + v,
                               color=BLUE_D, stroke_width=1.5))
        self.play(FadeIn(ticks), run_time=1.5)

        # Closed-form: y = x + 1 + (y0 - x0 - 1)*exp(x - x0)
        x0, y0 = -2.2, -0.7
        C = y0 - x0 - 1  # = -0.5

        def sol(x):
            return x + 1 + C * np.exp(x - x0)

        x_tr = ValueTracker(x0 + 0.001)

        def sol_curve():
            x_end = max(x_tr.get_value(), x0 + 0.01)
            return axes.plot(sol, x_range=[x0, x_end, 0.02],
                             color=YELLOW, stroke_width=4)

        def rider_dot():
            x = x_tr.get_value()
            return Dot(axes.c2p(x, sol(x)),
                       color=BLUE, radius=0.1)

        self.add(always_redraw(sol_curve),
                 always_redraw(rider_dot))

        start_dot = Dot(axes.c2p(x0, y0), color=GREEN, radius=0.1)
        start_lbl = Tex(r"$(x_0, y_0)$", color=GREEN,
                        font_size=18).next_to(start_dot, DL, buff=0.05)
        self.play(FadeIn(start_dot), Write(start_lbl))

        # RIGHT COLUMN
        def info_panel():
            x = x_tr.get_value()
            y = sol(x)
            return VGroup(
                MathTex(rf"x = {x:.2f}", color=WHITE, font_size=26),
                MathTex(rf"y = {y:.2f}", color=YELLOW, font_size=26),
                MathTex(rf"\dfrac{{dy}}{{dx}} = y - x = {(y - x):.2f}",
                        color=BLUE, font_size=24),
                MathTex(r"y = x + 1 - \tfrac{1}{2}e^{x - x_0}",
                        color=GREEN, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, 0.0, 0])

        self.add(always_redraw(info_panel))

        self.play(x_tr.animate.set_value(1.8),
                  run_time=8, rate_func=linear)
        self.wait(0.6)
