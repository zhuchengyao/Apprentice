from manim import *
import numpy as np


class LaurentSeriesExample(Scene):
    """
    Laurent series of f(z) = 1/(z·(1-z)) around z=0 in the annulus
    0 < |z| < 1:
       1/(z(1-z)) = 1/z + 1 + z + z² + z³ + ...
    Negative-power terms are the "principal part" at the pole.

    TWO_COLUMN:
      LEFT  — ComplexPlane with annulus of convergence shaded.
      RIGHT — axes showing partial-sum magnitude on a ray, with
              ValueTracker N_tr adding more terms; sum approaches
              the true function.
    """

    def construct(self):
        title = Tex(r"Laurent series of $1/(z(1-z))$: $z^{-1} + 1 + z + z^2 + \ldots$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT: complex plane with annulus
        plane = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                               x_length=5, y_length=5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([-3.5, -0.3, 0])
        self.play(Create(plane))

        # Annulus 0 < |z| < 1
        outer = Circle(radius=plane.c2p(1, 0)[0] - plane.c2p(0, 0)[0],
                         color=YELLOW, stroke_width=3
                         ).move_to(plane.c2p(0, 0))
        inner_dot = Dot(plane.c2p(0, 0), color=RED, radius=0.12)
        pole_lbl = Tex(r"pole at 0", color=RED, font_size=18
                        ).next_to(inner_dot, DOWN, buff=0.15)
        singular_1 = Dot(plane.c2p(1, 0), color=RED, radius=0.12)
        sing_lbl = Tex(r"pole at 1", color=RED, font_size=18
                        ).next_to(singular_1, UP, buff=0.15)
        self.play(Create(outer), FadeIn(inner_dot, singular_1),
                   Write(pole_lbl), Write(sing_lbl))

        conv_note = Tex(r"convergent: $0 < |z| < 1$",
                         color=YELLOW, font_size=20
                         ).next_to(plane, DOWN, buff=0.2)
        self.play(Write(conv_note))

        # RIGHT: partial sum on a real ray z = t for t ∈ (0, 1)
        ax = Axes(x_range=[0.05, 0.95, 0.2], y_range=[0, 20, 5],
                   x_length=5.5, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([3, -0.3, 0])
        xl = MathTex(r"|z|", font_size=20).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"|f(z)|", font_size=20).next_to(ax, LEFT, buff=0.1)

        # True f(z)
        true_curve = ax.plot(lambda t: 1 / (t * (1 - t)),
                               x_range=[0.07, 0.93, 0.005],
                               color=GREY_B, stroke_width=2.5)
        self.play(Create(ax), Write(xl), Write(yl), Create(true_curve))

        N_tr = ValueTracker(1)

        def partial_sum(t, N):
            # 1/t + sum_{k=0}^{N} t^k
            return 1 / t + sum(t ** k for k in range(N + 1))

        def partial_curve():
            N = int(round(N_tr.get_value()))
            N = max(0, min(N, 20))
            return ax.plot(lambda t: min(partial_sum(t, N), 20),
                            x_range=[0.07, 0.93, 0.005],
                            color=BLUE, stroke_width=3)

        self.add(always_redraw(partial_curve))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(0, min(N, 20))
            # Test at t=0.5: true = 4; partial sum = 2 + 1 + 0.5 + 0.25 + ...
            t = 0.5
            approx = partial_sum(t, N)
            err = abs(approx - 1 / (t * (1 - t)))
            return VGroup(
                MathTex(rf"N = {N}", color=BLUE, font_size=24),
                MathTex(r"f(z) = \tfrac{1}{z} + \sum_{k=0}^N z^k",
                         color=BLUE, font_size=20),
                MathTex(rf"f(0.5) \approx {approx:.4f}",
                         color=BLUE, font_size=20),
                MathTex(rf"\text{{true}} = 4.0000",
                         color=GREY_B, font_size=20),
                MathTex(rf"|\text{{err}}| = {err:.4f}",
                         color=RED, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for nv in [1, 3, 6, 12, 20]:
            self.play(N_tr.animate.set_value(nv),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
