from manim import *
import numpy as np


class LipschitzContinuityExample(Scene):
    """
    Lipschitz continuity: |f(x) - f(y)| ≤ K|x - y|. Geometrically,
    the graph fits inside a "double cone" of slope K from every
    point.

    SINGLE_FOCUS:
      Axes with f(x) = sin(x) (Lipschitz with K = 1). ValueTracker
      x_tr moves a point; always_redraw double-cone of slope K from
      that point; curve stays inside.
    """

    def construct(self):
        title = Tex(r"Lipschitz: $|f(x) - f(y)| \le K |x - y|$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[-3, 3, 1], y_range=[-2, 2, 0.5],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([0, -0.3, 0])
        self.play(Create(ax))

        # f(x) = sin(x)
        f_curve = ax.plot(np.sin, x_range=[-3, 3, 0.02],
                            color=BLUE, stroke_width=3)
        f_lbl = MathTex(r"f(x) = \sin x,\ K = 1",
                          color=BLUE, font_size=20
                          ).next_to(ax.c2p(2, 1), UR, buff=0.15)
        self.play(Create(f_curve), Write(f_lbl))

        x_tr = ValueTracker(0.0)
        K = 1.0  # Lipschitz constant

        def cone_lines():
            x = x_tr.get_value()
            y = np.sin(x)
            # Upper cone: y + K(x - x_0)
            # Lower cone: y - K(x - x_0)
            upper = ax.plot(lambda t: y + K * (t - x),
                              x_range=[-3, 3],
                              color=YELLOW, stroke_width=2)
            lower = ax.plot(lambda t: y - K * (t - x),
                              x_range=[-3, 3],
                              color=YELLOW, stroke_width=2)
            return VGroup(upper, lower)

        def current_dot():
            x = x_tr.get_value()
            return Dot(ax.c2p(x, np.sin(x)),
                        color=RED, radius=0.12)

        self.add(always_redraw(cone_lines), always_redraw(current_dot))

        def info():
            x = x_tr.get_value()
            return VGroup(
                MathTex(rf"x_0 = {x:+.2f}", color=RED, font_size=22),
                MathTex(rf"f(x_0) = {np.sin(x):+.3f}",
                         color=RED, font_size=20),
                MathTex(rf"K = {K}", color=YELLOW, font_size=20),
                Tex(r"curve stays inside YELLOW double cone",
                     color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for xv in [1.5, -1.5, 2.5, -2.0, 0]:
            self.play(x_tr.animate.set_value(xv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
