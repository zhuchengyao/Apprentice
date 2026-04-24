from manim import *
import numpy as np


class WeierstrassFunctionExample(Scene):
    """
    Weierstrass function W(x) = Σ a^k cos(b^k π x), with 0 < a < 1
    and ab > 1 + 3π/2: continuous everywhere but differentiable
    nowhere. Visualize partial sums as they develop fractal
    roughness.

    SINGLE_FOCUS:
      Axes plotting W_N(x) for N = 1..20; ValueTracker N_tr grows
      the number of terms; always_redraw. Roughness keeps increasing.
    """

    def construct(self):
        title = Tex(r"Weierstrass function: continuous, nowhere differentiable",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        a_coef = 0.5
        b_coef = 5

        def W(x, N):
            return sum(a_coef ** k * np.cos(b_coef ** k * PI * x)
                        for k in range(N + 1))

        ax = Axes(x_range=[-1, 1, 0.25], y_range=[-2, 2, 0.5],
                   x_length=9, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        self.play(Create(ax))

        N_tr = ValueTracker(0)

        def weier_curve():
            N = int(round(N_tr.get_value()))
            N = max(0, min(N, 20))
            # Use fine resolution to capture high-frequency terms
            resolution = max(0.0005, 0.01 / (N + 1))
            return ax.plot(lambda x: min(max(W(x, N), -2), 2),
                            x_range=[-1, 1, resolution],
                            color=BLUE, stroke_width=1.5)

        self.add(always_redraw(weier_curve))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(0, min(N, 20))
            return VGroup(
                MathTex(rf"N = {N}", color=BLUE, font_size=26),
                MathTex(rf"a = {a_coef},\ b = {b_coef}",
                         color=WHITE, font_size=20),
                MathTex(rf"ab = {a_coef * b_coef}",
                         color=WHITE, font_size=20),
                MathTex(r"ab > 1 + 3\pi/2 \approx 5.71",
                         color=YELLOW, font_size=20),
                Tex(r"continuous, but $W_N'$ diverges",
                     color=ORANGE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for nv in [2, 4, 8, 14, 20]:
            self.play(N_tr.animate.set_value(nv),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
