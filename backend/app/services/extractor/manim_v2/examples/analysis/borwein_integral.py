from manim import *
import numpy as np


class BorweinIntegralExample(Scene):
    """
    Borwein integrals: products of sinc functions integrate to π/2 ...
    until N=8 when the pattern breaks.

    TWO_COLUMN:
      LEFT  — Axes with the always_redraw integrand
              ∏_{k=0}^{N} sinc(x/(2k+1)) for the current N.
              ValueTracker N_idx steps through N = 0, 1, 2, 4, 6, 7, 8.
              Yellow shaded area = numerical integral.
      RIGHT — formula list with each line written as N advances; the
              N=8 line appears in RED with the actual value
              π/2 - δ where δ ≈ 2.31×10^(-11).
    """

    def construct(self):
        title = Tex(r"Borwein: $\int_0^\infty \prod_{k=0}^N \mathrm{sinc}(x/(2k+1))\,dx$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        N_values = [0, 1, 2, 4, 6, 7, 8]

        def sinc(x):
            return np.sin(x) / x if abs(x) > 1e-9 else 1.0

        def integrand_factory(N):
            def f(x):
                product = 1.0
                for k in range(N + 1):
                    product *= sinc(x / (2 * k + 1))
                return product
            return f

        axes = Axes(
            x_range=[0, 30, 5], y_range=[-0.4, 1.1, 0.5],
            x_length=7.0, y_length=3.6,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.0, +0.4, 0])
        self.play(Create(axes))

        N_idx = ValueTracker(0)

        def integrand_curve():
            i = int(round(N_idx.get_value()))
            i = max(0, min(i, len(N_values) - 1))
            N = N_values[i]
            return axes.plot(integrand_factory(N),
                             x_range=[0.05, 29.95, 0.1],
                             color=BLUE, stroke_width=2)

        def integrand_area():
            i = int(round(N_idx.get_value()))
            i = max(0, min(i, len(N_values) - 1))
            N = N_values[i]
            f = integrand_factory(N)
            curve = axes.plot(f, x_range=[0.05, 29.95, 0.1])
            return axes.get_area(curve, x_range=[0.05, 29.95],
                                 color=YELLOW, opacity=0.4)

        self.add(always_redraw(integrand_area), always_redraw(integrand_curve))

        # RIGHT COLUMN
        rcol_x = +4.4

        # Approximate integrals (precomputed for display)
        approx_integrals = {
            0: PI / 2,         # exact
            1: PI / 2,         # exact
            2: PI / 2,
            4: PI / 2,
            6: PI / 2,
            7: PI / 2 - 2.31e-11,  # the famous breakdown
            8: PI / 2 - 4.6e-11,
        }

        def info_panel():
            i = int(round(N_idx.get_value()))
            i = max(0, min(i, len(N_values) - 1))
            N = N_values[i]
            val = approx_integrals[N]
            diff = PI / 2 - val
            color_val = GREEN if abs(diff) < 1e-15 else RED
            return VGroup(
                MathTex(rf"N = {N}", color=YELLOW, font_size=32),
                MathTex(rf"\int = {val:.10f}",
                        color=color_val, font_size=22),
                MathTex(rf"\pi/2 = {PI/2:.10f}",
                        color=GREEN, font_size=22),
                MathTex(rf"\pi/2 - \int \approx {diff:.2e}",
                        color=color_val, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(info_panel))

        explanation = Tex(
            r"At $N = 7$, the harmonic sum $1 + 1/3 + \cdots + 1/15$ "
            r"first exceeds $1$ — the integral drops below $\pi/2$",
            color=GREY_B, font_size=18,
        ).move_to([rcol_x, -2.0, 0])
        self.play(Write(explanation))

        # Step through N's
        for i in range(1, len(N_values)):
            self.play(N_idx.animate.set_value(i),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.6)
