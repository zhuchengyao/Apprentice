from manim import *


class MotivatingIntegralProblemsExample(Scene):
    """
    A gallery of integrals that motivate calculus: from simple
    geometric areas to physics/probability/engineering.
    """

    def construct(self):
        title = Tex(r"Why integrals? A gallery of motivating problems",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        problems = [
            (r"area of a circle: $\displaystyle\int_0^R 2\pi r\,dr=\pi R^2$", BLUE),
            (r"distance from velocity: $\displaystyle\int_0^T v(t)\,dt$", GREEN),
            (r"work done: $\displaystyle\int_{x_1}^{x_2} F(x)\,dx$", ORANGE),
            (r"probability total: $\displaystyle\int_{-\infty}^\infty p(x)\,dx=1$", RED),
            (r"Gaussian: $\displaystyle\int_{-\infty}^\infty e^{-x^2}\,dx=\sqrt\pi$", PURPLE),
            (r"arc length: $\displaystyle\int_a^b\sqrt{1+(f'(x))^2}\,dx$", TEAL),
        ]

        grp = VGroup(*[
            Tex(p, color=c, font_size=24)
            for p, c in problems
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 0.2)

        for item in grp:
            self.play(Write(item), run_time=0.7)
            self.wait(0.25)

        self.wait(0.5)
        self.play(Write(
            Tex(r"all share the same 'sum of little pieces' essence",
                 color=YELLOW, font_size=24).to_edge(DOWN, buff=0.5)
        ))
        self.wait(1.0)
