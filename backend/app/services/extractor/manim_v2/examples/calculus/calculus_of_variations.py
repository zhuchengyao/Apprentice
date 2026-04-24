from manim import *
import numpy as np


class CalculusOfVariationsExample(Scene):
    """
    Calculus of variations: find curve y(x) minimizing functional
    J[y] = ∫ L(x, y, y') dx. Example: shortest path from (0, 0) to
    (2, 2) minimizes ∫ √(1 + y'²) dx → straight line.

    TWO_COLUMN:
      LEFT  — axes with several candidate paths; straight line has
              minimum length. ValueTracker bend_tr morphs a quadratic
              deviation showing length > straight.
      RIGHT — L[y] = ∫ √(1 + y'²) dx vs bend parameter.
    """

    def construct(self):
        title = Tex(r"Calculus of variations: minimize $\int L(x, y, y')\,dx$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[0, 2.5, 0.5], y_range=[-0.5, 3, 0.5],
                   x_length=5.5, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-3.3, -0.3, 0])
        self.play(Create(ax))

        # Straight-line path (reference)
        straight = ax.plot(lambda x: x, x_range=[0, 2],
                             color=GREEN, stroke_width=3)
        straight_lbl = MathTex(r"y = x", color=GREEN, font_size=20
                                 ).next_to(ax.c2p(2, 2), UR, buff=0.1)
        self.play(Create(straight), Write(straight_lbl))

        # Endpoints
        self.play(FadeIn(Dot(ax.c2p(0, 0), color=BLUE, radius=0.1)),
                   FadeIn(Dot(ax.c2p(2, 2), color=BLUE, radius=0.1)))

        bend_tr = ValueTracker(0.0)

        def candidate():
            b = bend_tr.get_value()
            # y(x) = x + b · x(2 - x) (quadratic perturbation)
            return ax.plot(lambda x: x + b * x * (2 - x),
                            x_range=[0, 2], color=YELLOW,
                            stroke_width=3)

        self.add(always_redraw(candidate))

        # RIGHT: arc length vs bend
        ax_R = Axes(x_range=[-1.5, 1.5, 0.5], y_range=[2.5, 4, 0.5],
                     x_length=4.5, y_length=3, tips=False,
                     axis_config={"font_size": 12}
                     ).move_to([3.5, 0.5, 0])
        xl = MathTex(r"b", font_size=18).next_to(ax_R, DOWN, buff=0.1)
        yl = MathTex(r"J[y]", font_size=18).next_to(ax_R, LEFT, buff=0.1)
        self.play(Create(ax_R), Write(xl), Write(yl))

        # Arc length numerically
        def J_of_b(b):
            xs = np.linspace(0, 2, 200)
            dys = 1 + b * (2 - 2 * xs)
            integrand = np.sqrt(1 + dys ** 2)
            return float(np.trapz(integrand, xs))

        J_curve = ax_R.plot(J_of_b, x_range=[-1.5, 1.5, 0.02],
                              color=RED, stroke_width=2.5)
        self.play(Create(J_curve))

        def J_rider():
            b = bend_tr.get_value()
            return Dot(ax_R.c2p(b, J_of_b(b)),
                        color=YELLOW, radius=0.1)

        self.add(always_redraw(J_rider))

        # Minimum marker at b=0
        min_dot = Dot(ax_R.c2p(0, J_of_b(0)), color=GREEN, radius=0.12)
        min_lbl = Tex(r"min at $b=0$", color=GREEN, font_size=18
                       ).next_to(min_dot, UR, buff=0.1)
        self.play(FadeIn(min_dot), Write(min_lbl))

        def info():
            b = bend_tr.get_value()
            L = J_of_b(b)
            return VGroup(
                MathTex(rf"b = {b:+.2f}", color=YELLOW, font_size=22),
                MathTex(rf"J[y] = \int \sqrt{{1+y'^2}}\,dx = {L:.3f}",
                         color=RED, font_size=20),
                MathTex(rf"J[x] = 2\sqrt 2 \approx 2.828",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for bv in [0.5, -0.5, 1.0, -1.0, 0]:
            self.play(bend_tr.animate.set_value(bv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
