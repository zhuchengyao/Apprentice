from manim import *
import numpy as np


class ZetaEulerProductExample(Scene):
    """
    Euler product ζ(s) = ∏_p (1 - p^-s)^-1 demonstrated by adding primes
    one at a time and watching the partial product approach the partial
    sum.

    TWO_COLUMN:
      LEFT  — Axes with two always_redraw curves over s ∈ (1, 6]:
              BLUE  = sum form Σ_{n=1}^N 1/n^s  (full N=500)
              GREEN = partial product over first k primes
              ValueTracker prime_idx steps through k = 1..10. As k
              grows, the GREEN curve climbs toward and overlaps BLUE.
      RIGHT — list of primes activated and the partial-product formula
              with k factors written out.
    """

    def construct(self):
        title = Tex(r"Euler product: $\zeta(s) = \displaystyle\prod_{p\,\text{prime}} \dfrac{1}{1 - p^{-s}}$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

        def zeta_sum(s, N=500):
            return sum(1.0 / k ** s for k in range(1, N + 1))

        def euler_partial(s, k):
            prod = 1.0
            for p in primes[:k]:
                prod *= 1.0 / (1.0 - p ** (-s))
            return prod

        axes = Axes(
            x_range=[1, 6, 1], y_range=[0, 6, 1],
            x_length=6.4, y_length=4.6,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.6, -0.4, 0])
        x_lbl = MathTex(r"s", font_size=22).next_to(axes, DOWN, buff=0.1)
        y_lbl = MathTex(r"\zeta(s)", font_size=22).next_to(axes, LEFT, buff=0.1)
        self.play(Create(axes), Write(x_lbl), Write(y_lbl))

        # Sum-form curve (static reference)
        sum_curve = axes.plot(zeta_sum, x_range=[1.05, 5.95, 0.05],
                              color=BLUE, stroke_width=3)
        sum_lbl = MathTex(r"\sum 1/n^s", color=BLUE, font_size=22).next_to(
            axes.c2p(2, zeta_sum(2)), UR, buff=0.1)
        self.play(Create(sum_curve), Write(sum_lbl))

        prime_idx = ValueTracker(1)

        def euler_curve():
            k = max(1, int(round(prime_idx.get_value())))
            return axes.plot(lambda s: euler_partial(s, k),
                             x_range=[1.1, 5.95, 0.05],
                             color=GREEN, stroke_width=3)

        self.add(always_redraw(euler_curve))

        # RIGHT COLUMN
        rcol_x = +4.2

        def info_panel():
            k = max(1, int(round(prime_idx.get_value())))
            primes_str = r"\{" + ", ".join(str(p) for p in primes[:k]) + r"\}"
            # Compare values at s = 2
            sum_val = zeta_sum(2)
            prod_val = euler_partial(2, k)
            return VGroup(
                MathTex(rf"k = {k}\ \text{{primes}}",
                        color=GREEN, font_size=24),
                MathTex(rf"\text{{primes}} = {primes_str}",
                        color=WHITE, font_size=20),
                MathTex(rf"\zeta(2) = \tfrac{{\pi^2}}{{6}} \approx {sum_val:.4f}",
                        color=BLUE, font_size=22),
                MathTex(rf"\prod_k \tfrac{{1}}{{1-p^{{-2}}}} \approx {prod_val:.4f}",
                        color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +1.0, 0])

        self.add(always_redraw(info_panel))

        meaning = Tex(r"Each prime contributes a geometric factor",
                      color=YELLOW, font_size=22).move_to([rcol_x, -2.4, 0])
        self.play(Write(meaning))

        # Step through primes
        for k in range(2, len(primes) + 1):
            self.play(prime_idx.animate.set_value(k),
                      run_time=0.7, rate_func=smooth)
            self.wait(0.2)
        self.wait(0.6)
