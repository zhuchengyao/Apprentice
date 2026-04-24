from manim import *


class ImplicitDiffGivesLnDerivativeExample(Scene):
    """
    Derive d(ln x)/dx = 1/x via implicit differentiation.
    Let y = ln x, so e^y = x. Differentiate both sides w.r.t. x:
    e^y · y' = 1, so y' = 1/e^y = 1/x.
    """

    def construct(self):
        title = Tex(r"$\frac{d\ln x}{dx}=\frac{1}{x}$ by implicit diff",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Step by step
        steps = VGroup(
            MathTex(r"\text{Let } y = \ln x", font_size=32),
            MathTex(r"e^y = x", font_size=32),
            MathTex(r"\frac{d}{dx}(e^y) = \frac{d}{dx}(x)", font_size=30),
            MathTex(r"e^y \cdot y' = 1", font_size=32, color=BLUE),
            MathTex(r"y' = \frac{1}{e^y} = \frac{1}{x}", font_size=34, color=YELLOW),
            MathTex(r"\therefore \frac{d\ln x}{dx}=\frac{1}{x}", font_size=36, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 0.1)

        for s in steps:
            self.play(Write(s), run_time=0.9)
            self.wait(0.3)

        self.wait(0.5)
        self.play(Write(
            Tex(r"trick: turn $\ln$ into $e^?$ then differentiate",
                 color=YELLOW, font_size=22).to_edge(DOWN, buff=0.4)
        ))
        self.wait(1.0)
