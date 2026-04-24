from manim import *
import numpy as np


class CumulantExpansionClt(Scene):
    """CLT proof via cumulant-generating functions (CGFs).  For i.i.d. X_i
    with mean 0 variance 1, let Y_n = (X_1 + ... + X_n)/sqrt(n).
    K_{Y_n}(t) = n * K_X(t/sqrt(n)) = n * (t^2/(2n) + kappa_3 * t^3/(6 n^{3/2}) + ...)
    The t^2/2 term survives while the higher-order terms fade as n grows.
    Visualize with three axes of K_{Y_n}(t) for n = 1, 10, 1000, converging
    to t^2/2 — the CGF of the standard Gaussian."""

    def construct(self):
        title = Tex(
            r"CLT by cumulants: $K_{Y_n}(t) \to \tfrac{t^2}{2}$ as $n \to \infty$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 4.5, 1],
            x_length=9, y_length=4.5,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).shift(DOWN * 0.4)
        x_lab = MathTex("t", font_size=26).next_to(
            axes.x_axis.get_end(), DOWN, buff=0.1
        )
        y_lab = MathTex(r"K_{Y_n}(t)", font_size=26).next_to(
            axes.y_axis.get_end(), LEFT, buff=0.1
        )
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab))

        gaussian = axes.plot(lambda t: t * t / 2,
                             x_range=[-3, 3, 0.02],
                             color=YELLOW, stroke_width=4)
        gaussian_lab = MathTex(r"\tfrac{t^2}{2}", font_size=26,
                               color=YELLOW).move_to(
            axes.c2p(2.3, 3.5)
        )
        self.play(Create(gaussian), Write(gaussian_lab))

        kappa3 = 1.5

        def K_of_Y(t, n):
            u = t / np.sqrt(n)
            return n * (u * u / 2 + kappa3 * u ** 3 / 6)

        n_series = [1, 10, 1000]
        colors = [RED, ORANGE, GREEN]
        for n, color in zip(n_series, colors):
            curve = axes.plot(
                lambda t, n=n: K_of_Y(t, n),
                x_range=[-3, 3, 0.02],
                color=color, stroke_width=2.5,
            )
            lab = MathTex(f"n={n}", font_size=24,
                          color=color).move_to(
                axes.c2p(-2.5, 3.8 - 0.5 * n_series.index(n))
            )
            self.play(Create(curve), Write(lab), run_time=1.2)

        derivation = VGroup(
            MathTex(r"K_X(t) = \tfrac{t^2}{2} + \kappa_3 \tfrac{t^3}{6}"
                    r" + \kappa_4 \tfrac{t^4}{24} + \cdots",
                    font_size=22),
            MathTex(r"K_{Y_n}(t) = n\,K_X\!\left(\tfrac{t}{\sqrt n}\right)"
                    r" = \tfrac{t^2}{2} + \tfrac{\kappa_3\,t^3}{6\sqrt n}"
                    r" + \tfrac{\kappa_4\,t^4}{24\,n} + \cdots",
                    font_size=22),
            MathTex(
                r"\text{higher-order terms fade as } 1/\sqrt n",
                font_size=22, color=YELLOW,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        derivation.to_edge(DOWN, buff=0.25)
        self.play(FadeIn(derivation[0]))
        self.play(FadeIn(derivation[1]))
        self.play(FadeIn(derivation[2]))
        self.wait(1.5)
