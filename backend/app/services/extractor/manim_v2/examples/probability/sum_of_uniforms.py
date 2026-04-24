from manim import *
import numpy as np


def irwin_hall_pdf(x, n):
    """Density of sum of n iid Uniform(0,1)."""
    if x <= 0 or x >= n:
        return 0.0
    from math import comb
    s = 0.0
    for k in range(int(np.floor(x)) + 1):
        sign = 1 if k % 2 == 0 else -1
        s += sign * comb(n, k) * (x - k) ** (n - 1)
    from math import factorial
    return s / factorial(n - 1)


class SumOfUniformsExample(Scene):
    """
    Density of S_n = U_1 + U_2 + ... + U_n where U_i ~ Uniform(0, 1).

    SINGLE_FOCUS: ValueTracker n_idx steps through n = 1, 2, 3, 4, 5, 7, 10.
    For each n, the density curve (Irwin-Hall) is computed and morphed
    via Transform from the previous one. The x-axis range adjusts because
    S_n lives on [0, n].
    """

    def construct(self):
        title = Tex(r"Density of $S_n = U_1 + \cdots + U_n$, $U_i \sim \text{Uniform}(0,1)$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Use a fixed wide axis that fits all n up to 10
        axes = Axes(
            x_range=[0, 10, 1], y_range=[0, 1.1, 0.25],
            x_length=10, y_length=4.6,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).shift(0.2 * DOWN)
        self.play(Create(axes))

        ns = [1, 2, 3, 4, 5, 7, 10]

        # Precompute density curves
        def make_curve(n: int):
            return axes.plot(
                lambda x, n=n: irwin_hall_pdf(x, n),
                x_range=[0.001, n - 0.001, 0.02],
                color=YELLOW,
            )

        current = make_curve(1)
        self.add(current)

        n_idx = ValueTracker(0)

        def info_panel():
            i = int(round(n_idx.get_value()))
            i = max(0, min(i, len(ns) - 1))
            n = ns[i]
            mu = n / 2.0
            var = n / 12.0
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=42),
                MathTex(rf"\mu = n/2 = {mu:.2f}", color=GREEN, font_size=22),
                MathTex(rf"\sigma^2 = n/12 \approx {var:.3f}",
                        color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.5)

        self.add(always_redraw(info_panel))

        # Step through n's and Transform the curve
        for i in range(1, len(ns)):
            new_curve = make_curve(ns[i])
            self.play(Transform(current, new_curve),
                      n_idx.animate.set_value(i),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.5)

        clt_lbl = Tex(r"Approaches $\mathcal{N}(n/2, n/12)$ — Central Limit Theorem",
                      color=YELLOW, font_size=24).to_edge(DOWN, buff=0.4)
        self.play(Write(clt_lbl))
        self.wait(1.0)
