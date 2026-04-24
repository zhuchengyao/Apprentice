from manim import *
import numpy as np


class TangentLineHyperbolaExample(Scene):
    """
    Tangent line to a hyperbola x²/a² - y²/b² = 1 at (x_0, y_0) is
    (x_0 x)/a² - (y_0 y)/b² = 1. ValueTracker theta_tr moves the
    tangent point along the right branch.

    SINGLE_FOCUS:
      Hyperbola with both branches; RED tangent line moves smoothly;
      asymptotes y = ±(b/a)x shown; tangent line intersects axes
      at (a²/x_0, 0) and (0, -b²/y_0).
    """

    def construct(self):
        title = Tex(r"Tangent to hyperbola: $\tfrac{x_0 x}{a^2} - \tfrac{y_0 y}{b^2} = 1$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        a, b = 2.0, 1.5

        ax = Axes(x_range=[-5, 5, 1], y_range=[-3.5, 3.5, 1],
                   x_length=9, y_length=5.5, tips=False,
                   axis_config={"font_size": 14}
                   ).move_to([0, -0.3, 0])
        self.play(Create(ax))

        # Hyperbola right branch: x = a cosh t, y = b sinh t
        right_pts = [ax.c2p(a * np.cosh(t), b * np.sinh(t))
                      for t in np.linspace(-1.5, 1.5, 40)]
        left_pts = [ax.c2p(-a * np.cosh(t), b * np.sinh(t))
                     for t in np.linspace(-1.5, 1.5, 40)]
        right_branch = VMobject(color=BLUE, stroke_width=3)
        right_branch.set_points_as_corners(right_pts)
        left_branch = VMobject(color=BLUE, stroke_width=3)
        left_branch.set_points_as_corners(left_pts)
        self.play(Create(right_branch), Create(left_branch))

        # Asymptotes
        asym1 = DashedLine(ax.c2p(-4, -4 * b / a), ax.c2p(4, 4 * b / a),
                             color=GREY_B, stroke_width=1.5)
        asym2 = DashedLine(ax.c2p(-4, 4 * b / a), ax.c2p(4, -4 * b / a),
                             color=GREY_B, stroke_width=1.5)
        self.play(Create(asym1), Create(asym2))

        theta_tr = ValueTracker(0.6)

        def point_and_tangent():
            t = theta_tr.get_value()
            x0 = a * np.cosh(t)
            y0 = b * np.sinh(t)
            # Tangent line: (x0 x)/a² - (y0 y)/b² = 1
            # At x = a²/x0: y = 0; at y = -b²/y0: x = 0 (if y0 ≠ 0)
            # Parametrize as (x0 + s * dx, y0 + s * dy) where (dx, dy) is tangent.
            # Tangent direction from dx/dt = a sinh t, dy/dt = b cosh t
            dx = a * np.sinh(t)
            dy = b * np.cosh(t)
            mag = np.hypot(dx, dy)
            tx = dx / mag * 2.5
            ty = dy / mag * 2.5
            start = ax.c2p(x0 - tx, y0 - ty)
            end = ax.c2p(x0 + tx, y0 + ty)
            grp = VGroup()
            grp.add(Line(start, end, color=RED, stroke_width=3))
            grp.add(Dot(ax.c2p(x0, y0), color=YELLOW, radius=0.11))
            return grp

        self.add(always_redraw(point_and_tangent))

        def info():
            t = theta_tr.get_value()
            x0 = a * np.cosh(t)
            y0 = b * np.sinh(t)
            return VGroup(
                MathTex(rf"(x_0, y_0) = ({x0:.2f}, {y0:+.2f})",
                         color=YELLOW, font_size=22),
                MathTex(rf"x_0^2/a^2 - y_0^2/b^2 = {x0**2/a**2 - y0**2/b**2:.3f}",
                         color=GREEN, font_size=20),
                MathTex(rf"a = {a},\ b = {b}",
                         color=BLUE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        for tv in [1.2, -0.8, 0.3, 1.0]:
            self.play(theta_tr.animate.set_value(tv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
