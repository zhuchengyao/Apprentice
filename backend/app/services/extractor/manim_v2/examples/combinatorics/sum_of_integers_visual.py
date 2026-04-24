from manim import *
import numpy as np


class SumOfIntegersVisualExample(Scene):
    def construct(self):
        title = Text("1 + 2 + … + n via paired triangles", font_size=28).to_edge(UP)
        self.play(Write(title))

        n = 7
        dot_radius = 0.17
        spacing = 0.44

        left_tri = VGroup()
        for row in range(1, n + 1):
            for col in range(row):
                d = Dot([col * spacing, -row * spacing, 0], color=BLUE, radius=dot_radius)
                left_tri.add(d)
        right_tri = VGroup()
        for row in range(1, n + 1):
            for col in range(row):
                d = Dot([col * spacing, -row * spacing, 0], color=RED, radius=dot_radius)
                right_tri.add(d)

        left_tri.move_to(LEFT * 2.5 + 0.2 * DOWN)
        right_tri.move_to(RIGHT * 2.5 + 0.2 * DOWN).rotate(PI)

        self.play(FadeIn(left_tri), FadeIn(right_tri))
        self.wait(0.3)

        merged_tri = VGroup()
        for row in range(1, n + 1):
            for col in range(n):
                color = BLUE if col < row else RED
                d = Dot([col * spacing, -row * spacing, 0], color=color, radius=dot_radius)
                merged_tri.add(d)
        merged_tri.move_to(0.2 * DOWN)

        self.play(Transform(VGroup(left_tri, right_tri), merged_tri), run_time=2)
        self.wait(0.3)

        formula = MathTex(r"1 + 2 + \cdots + n = \tfrac{n(n+1)}{2}", font_size=36, color=YELLOW).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(0.6)
