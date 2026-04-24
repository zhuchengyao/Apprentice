from manim import *
import numpy as np


class OpenIntervalExample(Scene):
    """
    Open interval (a, b) on ℝ: every interior point x has a
    δ-neighborhood entirely inside (a, b).

    SINGLE_FOCUS:
      NumberLine with open endpoints a=0, b=1 shown as hollow
      circles. ValueTracker x_tr moves an interior point x through
      (0, 1); always_redraw keeps a BLUE bar of radius δ(x) =
      min(x-a, b-x) around x — the largest δ that stays inside.
      As x approaches an endpoint, δ shrinks to 0 but stays > 0.
    """

    def construct(self):
        title = Tex(r"Open interval $(a, b)$: every $x \in (a, b)$ has a $\delta$-neighborhood $\subset (a, b)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        nl = NumberLine(x_range=[-0.3, 1.3, 0.25], length=11,
                         include_numbers=False).move_to([0, -0.3, 0])
        tick_a = Line(nl.n2p(0) + UP * 0.15, nl.n2p(0) + DOWN * 0.15,
                       color=WHITE)
        tick_b = Line(nl.n2p(1) + UP * 0.15, nl.n2p(1) + DOWN * 0.15,
                       color=WHITE)
        a_lbl = MathTex(r"a = 0", font_size=24).next_to(nl.n2p(0), DOWN, buff=0.35)
        b_lbl = MathTex(r"b = 1", font_size=24).next_to(nl.n2p(1), DOWN, buff=0.35)
        # Open endpoint circles
        open_a = Circle(radius=0.12, color=WHITE, stroke_width=3,
                         fill_opacity=0).move_to(nl.n2p(0))
        open_b = Circle(radius=0.12, color=WHITE, stroke_width=3,
                         fill_opacity=0).move_to(nl.n2p(1))

        self.play(Create(nl), Create(tick_a), Create(tick_b),
                   Write(a_lbl), Write(b_lbl),
                   Create(open_a), Create(open_b))

        # Highlight interior
        interior = Line(nl.n2p(0) + np.array([0.15, 0, 0]),
                         nl.n2p(1) + np.array([-0.15, 0, 0]),
                         color=GREY_B, stroke_width=8, stroke_opacity=0.45)
        self.play(Create(interior))

        x_tr = ValueTracker(0.5)

        def x_dot():
            return Dot(nl.n2p(x_tr.get_value()), color=YELLOW, radius=0.12)

        def delta_bar():
            x = x_tr.get_value()
            delta = min(x, 1 - x)
            if delta < 1e-4:
                delta = 1e-4
            left = nl.n2p(x - delta)
            right = nl.n2p(x + delta)
            return Rectangle(width=right[0] - left[0], height=0.5,
                              color=BLUE, fill_opacity=0.35, stroke_width=2
                              ).move_to(nl.n2p(x))

        def info():
            x = x_tr.get_value()
            delta = min(x, 1 - x)
            return VGroup(
                MathTex(rf"x = {x:.4f}", color=YELLOW, font_size=26),
                MathTex(rf"\delta = \min(x-a,\,b-x) = {delta:.4f}",
                         color=BLUE, font_size=24),
                MathTex(rf"(x - \delta,\, x + \delta) \subset (0, 1)",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -2.3, 0])

        self.add(always_redraw(delta_bar),
                  always_redraw(x_dot),
                  always_redraw(info))

        self.play(x_tr.animate.set_value(0.02),
                   run_time=3, rate_func=smooth)
        self.play(x_tr.animate.set_value(0.98),
                   run_time=3.5, rate_func=smooth)
        self.play(x_tr.animate.set_value(0.5),
                   run_time=2, rate_func=smooth)
        self.wait(0.5)
