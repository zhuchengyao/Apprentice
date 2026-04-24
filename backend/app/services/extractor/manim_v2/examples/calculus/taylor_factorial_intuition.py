from manim import *


class TaylorFactorialIntuitionExample(Scene):
    """
    Why do factorials appear in Taylor series? Each term c_n·x^n
    must match the n-th derivative of f at 0. The n-th derivative
    of x^n is n!, so the coefficient must be f^(n)(0) / n!.
    """

    def construct(self):
        title = Tex(r"Why $\dfrac{1}{n!}$ in Taylor series?",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        lines = VGroup(
            MathTex(r"P(x) = \sum_n c_n\,x^n", font_size=32),
            MathTex(r"\frac{d^n}{dx^n}(x^n) = n!", font_size=32, color=BLUE),
            MathTex(r"\text{so } P^{(n)}(0) = c_n\cdot n!", font_size=32),
            MathTex(r"\text{match derivatives: } c_n\cdot n! = f^{(n)}(0)",
                      font_size=28),
            MathTex(r"c_n = \frac{f^{(n)}(0)}{n!}", font_size=36, color=YELLOW),
            MathTex(r"f(x) = \sum_{n=0}^\infty \frac{f^{(n)}(0)}{n!}\,x^n",
                      font_size=36, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 0.2)

        for line in lines:
            self.play(Write(line), run_time=0.9)
            self.wait(0.25)

        self.wait(0.5)
        self.play(Write(
            Tex(r"factorials come from repeated differentiation of $x^n$",
                 color=YELLOW, font_size=22).to_edge(DOWN, buff=0.4)
        ))
        self.wait(1.0)
