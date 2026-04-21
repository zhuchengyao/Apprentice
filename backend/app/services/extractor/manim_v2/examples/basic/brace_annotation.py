from manim import *


class BraceAnnotationExample(Scene):
    def construct(self):
        line = Line(LEFT * 2, RIGHT * 2, color=BLUE)
        brace = Brace(line, direction=DOWN, buff=0.15)
        label = brace.get_text("length")
        tex = brace.get_tex(r"\ell = 4")

        self.play(Create(line))
        self.play(GrowFromCenter(brace), Write(label))
        self.wait(0.4)
        self.play(ReplacementTransform(label, tex))
        self.wait(0.6)
