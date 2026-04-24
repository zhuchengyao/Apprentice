from manim import *
import numpy as np


class ContinuityEpsilonDeltaExample(Scene):
    """
    ε-δ definition of continuity for f(x) = x² at x₀ = 2: for every
    ε > 0, there's a δ > 0 so |x - 2| < δ ⇒ |x² - 4| < ε. Find
    δ = ε/(4+ε) suffices.

    TWO_COLUMN:
      LEFT  — graph y = x² with YELLOW horizontal ε-band around y=4
              and GREEN vertical δ-band around x=2, both driven by
              ValueTracker eps_tr.
      RIGHT — live ε, δ = ε/(4+ε), verification.
    """

    def construct(self):
        title = Tex(r"$\varepsilon$-$\delta$ continuity of $x^2$ at $x_0 = 2$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[0, 4, 1], y_range=[0, 10, 2],
                   x_length=6.5, y_length=5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        self.play(Create(ax))

        # y = x²
        curve = ax.plot(lambda x: x * x, x_range=[0, 3.5],
                          color=BLUE, stroke_width=3)
        self.play(Create(curve))

        # Target point
        target_dot = Dot(ax.c2p(2, 4), color=RED, radius=0.12)
        target_lbl = MathTex(r"(2, 4)", color=RED,
                               font_size=20).next_to(target_dot, UR, buff=0.1)
        self.play(FadeIn(target_dot), Write(target_lbl))

        eps_tr = ValueTracker(2.0)

        def delta_for(eps):
            # Solve (2+δ)² - 4 = ε ⇒ δ² + 4δ = ε ⇒ δ = (-4 + √(16+4ε))/2 = -2 + √(4+ε)
            return -2 + np.sqrt(4 + eps)

        def eps_band():
            eps = eps_tr.get_value()
            return Rectangle(
                width=ax.c2p(3.5, 0)[0] - ax.c2p(0, 0)[0],
                height=(ax.c2p(0, 4 + eps)[1] - ax.c2p(0, 4 - eps)[1]),
                color=YELLOW, fill_opacity=0.25, stroke_width=1
            ).move_to([(ax.c2p(0, 0)[0] + ax.c2p(3.5, 0)[0]) / 2,
                        ax.c2p(0, 4)[1], 0])

        def delta_band():
            eps = eps_tr.get_value()
            delta = delta_for(eps)
            return Rectangle(
                width=ax.c2p(2 + delta, 0)[0] - ax.c2p(2 - delta, 0)[0],
                height=ax.c2p(0, 10)[1] - ax.c2p(0, 0)[1],
                color=GREEN, fill_opacity=0.25, stroke_width=1
            ).move_to([ax.c2p(2, 0)[0],
                        (ax.c2p(0, 0)[1] + ax.c2p(0, 10)[1]) / 2, 0])

        self.add(always_redraw(eps_band), always_redraw(delta_band))

        def info():
            eps = eps_tr.get_value()
            delta = delta_for(eps)
            return VGroup(
                MathTex(rf"\varepsilon = {eps:.3f}",
                         color=YELLOW, font_size=24),
                MathTex(rf"\delta = -2 + \sqrt{{4 + \varepsilon}} = {delta:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"(2 + \delta)^2 - 4 = \varepsilon",
                         color=WHITE, font_size=20),
                Tex(r"$|x - 2| < \delta \Rightarrow |x^2 - 4| < \varepsilon$",
                     color=ORANGE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for target in [4.0, 0.5, 0.1, 2.0]:
            self.play(eps_tr.animate.set_value(target),
                       run_time=2, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
