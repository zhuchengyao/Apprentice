from manim import *


class MovingFrameBoxExample(Scene):
    def construct(self):
        text = MathTex(r"\frac{d}{dx} f(x) g(x)",
                       r"=",
                       r"f(x) \frac{d}{dx} g(x)",
                       r"+",
                       r"g(x) \frac{d}{dx} f(x)")
        self.play(Write(text))

        box = SurroundingRectangle(text[0], color=YELLOW, buff=0.1)
        self.play(Create(box))
        self.wait(0.3)
        self.play(ReplacementTransform(box, SurroundingRectangle(text[2], color=YELLOW, buff=0.1)))
        self.wait(0.3)
        self.play(ReplacementTransform(
            box := SurroundingRectangle(text[2], color=YELLOW, buff=0.1),
            SurroundingRectangle(text[4], color=YELLOW, buff=0.1),
        ))
        self.wait(0.6)
