from manim import *


class BooleanOperationsExample(Scene):
    def construct(self):
        a = Circle(radius=1.1, color=BLUE, fill_opacity=0.4).shift(LEFT * 0.6)
        b = Circle(radius=1.1, color=RED, fill_opacity=0.4).shift(RIGHT * 0.6)
        self.play(Create(a), Create(b))
        self.wait(0.3)

        union = Union(a, b, color=PURPLE, fill_opacity=0.6).to_edge(DOWN)
        inter = Intersection(a, b, color=YELLOW, fill_opacity=0.8).to_edge(DOWN)
        diff = Difference(a, b, color=GREEN, fill_opacity=0.6).to_edge(DOWN)

        label = Text("Union", font_size=28).to_edge(UP)
        self.play(FadeIn(union), Write(label))
        self.wait(0.4)
        self.play(
            ReplacementTransform(union, inter),
            Transform(label, Text("Intersection", font_size=28).to_edge(UP)),
        )
        self.wait(0.4)
        self.play(
            ReplacementTransform(inter, diff),
            Transform(label, Text("Difference", font_size=28).to_edge(UP)),
        )
        self.wait(0.6)
