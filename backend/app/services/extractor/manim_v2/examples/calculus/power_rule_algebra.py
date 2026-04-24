from manim import *


class PowerRuleAlgebraExample(Scene):
    """
    General power rule: d(x^n)/dx = n·x^(n-1) via binomial expansion.
    (x+dx)^n = x^n + n·x^(n-1)·dx + C(n, 2)·x^(n-2)·dx² + ...
    Divide by dx and take limit: only the first-order term survives.
    """

    def construct(self):
        title = Tex(r"Power rule: $\frac{d(x^n)}{dx}=n x^{n-1}$ via binomial expansion",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Binomial expansion
        lines = VGroup(
            MathTex(r"(x+dx)^n",
                      r"=",
                      r"x^n + n\,x^{n-1}\,dx + \binom{n}{2}x^{n-2}dx^2+\cdots",
                      font_size=28),
            MathTex(r"\frac{(x+dx)^n - x^n}{dx}",
                      r"=",
                      r"n\,x^{n-1} + \binom{n}{2}x^{n-2}\,dx + \cdots",
                      font_size=28),
            MathTex(r"\lim_{dx\to 0}\frac{(x+dx)^n-x^n}{dx}",
                      r"=",
                      r"n\,x^{n-1}",
                      font_size=30, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN * 0.1)

        for line in lines:
            self.play(Write(line), run_time=1.0)
            self.wait(0.3)

        # Examples
        examples = VGroup(
            Tex(r"examples:", color=GREEN, font_size=22),
            MathTex(r"\frac{d(x^2)}{dx}=2x,\quad \frac{d(x^3)}{dx}=3x^2,\quad \frac{d(x^5)}{dx}=5x^4",
                      font_size=24, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        self.play(Write(examples))
        self.wait(1.0)
