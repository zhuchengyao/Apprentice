from manim import *
import numpy as np


class DominatedConvergenceExample(Scene):
    """
    Dominated convergence theorem (Lebesgue): if f_n → f pointwise
    and |f_n| ≤ g with ∫g < ∞, then ∫f_n → ∫f. Illustrate with
    f_n(x) = e^(-x/n) · sin(x) / n on [0, ∞); |f_n| ≤ e^(-x/n);
    but choose dominating g(x) = e^(-x) · 2.

    TWO_COLUMN:
      LEFT  — axes with GREEN dominating g(x), BLUE f_n(x) as n grows;
              YELLOW limit f = 0.
      RIGHT — live ∫f_n → 0 = ∫f.
    """

    def construct(self):
        title = Tex(r"Dominated convergence: $|f_n| \le g$, $f_n \to f$ $\Rightarrow \int f_n \to \int f$",
                    font_size=20).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ax = Axes(x_range=[0, 10, 2], y_range=[-0.2, 1.0, 0.25],
                   x_length=8, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        self.play(Create(ax))

        # Dominating function g(x) = e^(-x) · 1.0
        g_curve = ax.plot(lambda x: np.exp(-x),
                            x_range=[0, 10, 0.02],
                            color=GREEN, stroke_width=3)
        g_lbl = MathTex(r"g(x) = e^{-x}", color=GREEN, font_size=20
                          ).next_to(ax.c2p(2, np.exp(-2)), UR, buff=0.1)
        self.play(Create(g_curve), Write(g_lbl))

        # Limit f = 0 (just x-axis)
        zero_line = DashedLine(ax.c2p(0, 0), ax.c2p(10, 0),
                                 color=YELLOW, stroke_width=2)
        self.play(Create(zero_line))

        n_tr = ValueTracker(1.0)

        def f_n_curve():
            n = n_tr.get_value()
            return ax.plot(lambda x: np.exp(-x / n) * np.sin(x) / n,
                            x_range=[0, 10, 0.02],
                            color=BLUE, stroke_width=3)

        self.add(always_redraw(f_n_curve))

        def info():
            n = n_tr.get_value()
            # Numerical integral of f_n
            xs = np.linspace(0, 10, 500)
            f_vals = np.exp(-xs / n) * np.sin(xs) / n
            intg = float(np.trapz(f_vals, xs))
            return VGroup(
                MathTex(rf"n = {n:.2f}", color=BLUE, font_size=22),
                MathTex(rf"f_n(x) = \tfrac{{1}}{{n}} e^{{-x/n}} \sin x",
                         color=BLUE, font_size=18),
                MathTex(rf"\int f_n = {intg:.5f}",
                         color=YELLOW, font_size=22),
                MathTex(r"\text{expected } \int f = 0",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for nv in [2, 5, 10, 30, 100]:
            self.play(n_tr.animate.set_value(nv),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
