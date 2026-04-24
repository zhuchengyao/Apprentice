from manim import *
import numpy as np


class TaylorSeriesSinExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-PI, PI, PI / 2], y_range=[-1.6, 1.6, 0.5],
            x_length=10, y_length=4, tips=False,
        ).to_edge(DOWN, buff=0.6)
        sine = axes.plot(np.sin, color=BLUE)
        self.play(Create(axes), Create(sine))

        title_box = MathTex(r"\sin x \approx", font_size=36).to_corner(UL).add_background_rectangle()
        self.play(Write(title_box))

        def taylor(n_terms):
            def poly(x):
                return sum(
                    ((-1) ** k) * x ** (2 * k + 1) / np.math.factorial(2 * k + 1)
                    for k in range(n_terms)
                )
            return poly

        colors = [YELLOW, GREEN, RED, ORANGE]
        terms_list = [1, 2, 3, 5]
        approx = axes.plot(taylor(terms_list[0]), color=colors[0])
        lbl = MathTex(r"x", font_size=30, color=colors[0]).next_to(title_box, RIGHT, buff=0.2).add_background_rectangle()
        self.play(Create(approx), Write(lbl))

        labels_tex = [
            r"x - \tfrac{x^3}{3!}",
            r"x - \tfrac{x^3}{3!} + \tfrac{x^5}{5!}",
            r"\dots + \tfrac{x^9}{9!}",
        ]
        for i, n in enumerate(terms_list[1:], start=1):
            new_curve = axes.plot(taylor(n), color=colors[i])
            new_lbl = MathTex(labels_tex[i - 1], font_size=30, color=colors[i])
            new_lbl.next_to(title_box, RIGHT, buff=0.2).add_background_rectangle()
            self.play(Transform(approx, new_curve), Transform(lbl, new_lbl), run_time=1.2)
            self.wait(0.2)
        self.wait(0.6)
