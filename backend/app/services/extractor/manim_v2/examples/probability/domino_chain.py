from manim import *
import numpy as np


class DominoChainExample(Scene):
    def construct(self):
        title = Text("Induction as a falling domino chain", font_size=30).to_edge(UP)
        self.play(Write(title))

        n = 10
        dominoes = VGroup()
        spacing = 0.75
        for k in range(n):
            d = Rectangle(width=0.35, height=1.2, color=BLUE, fill_opacity=0.7)
            d.move_to([-4.2 + k * spacing, -0.3, 0])
            dominoes.add(d)
        self.play(LaggedStart(*[FadeIn(d) for d in dominoes], lag_ratio=0.1))

        # Fall them one by one (rotate around bottom-right corner)
        for k in range(n):
            pivot = dominoes[k].get_corner(DR)
            self.play(Rotate(dominoes[k], angle=-PI / 2.5, about_point=pivot), run_time=0.28)

        caption = VGroup(
            MathTex(r"\text{Base case: } P(1)", font_size=28),
            MathTex(r"\text{Step: } P(k) \Rightarrow P(k+1)", font_size=28),
            MathTex(r"\Rightarrow \forall n \geq 1:\; P(n)", font_size=28, color=YELLOW),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
