from manim import *


class TextStylingExample(Scene):
    def construct(self):
        title = Text("Styled Text", font_size=44, weight=BOLD).to_edge(UP)
        line1 = Text(
            "color, slant, and weight",
            font_size=32,
            t2c={"color": BLUE, "weight": GREEN},
            t2s={"slant": ITALIC},
            t2w={"weight": BOLD},
        )
        line1.next_to(title, DOWN, buff=0.8)

        formula = MathTex(r"E = m c^{2}", font_size=52, color=YELLOW).next_to(line1, DOWN, buff=0.7)

        self.play(Write(title))
        self.play(FadeIn(line1, shift=UP))
        self.play(Write(formula))
        self.wait(0.6)
