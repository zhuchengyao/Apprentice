from manim import *


class TransformMatchingTexExample(Scene):
    def construct(self):
        eq1 = MathTex("a", "^2", "+", "b", "^2", "=", "c", "^2").scale(1.2)
        eq2 = MathTex("c", "^2", "-", "b", "^2", "=", "a", "^2").scale(1.2)
        self.play(Write(eq1))
        self.wait(0.4)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(0.6)
