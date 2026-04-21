from manim import *


class NewtonSecondLawExample(Scene):
    def construct(self):
        title = Text("Newton's Second Law", font_size=34).to_edge(UP)
        self.play(Write(title))

        box = Square(side_length=1.2, color=BLUE, fill_opacity=0.6).shift(LEFT * 2)
        mass = MathTex(r"m", font_size=32).next_to(box, DOWN, buff=0.2)
        self.play(FadeIn(box), Write(mass))

        force = Arrow(box.get_right(), box.get_right() + RIGHT * 2.5,
                      buff=0.05, color=YELLOW)
        f_label = MathTex(r"\vec{F}", font_size=32).next_to(force, UP, buff=0.1)
        self.play(GrowArrow(force), Write(f_label))

        group = VGroup(box, mass)
        self.play(group.animate.shift(RIGHT * 1.8), run_time=1.5)

        eq = MathTex(r"\vec{F} = m\,\vec{a}", font_size=54).to_edge(DOWN, buff=0.6)
        self.play(Write(eq))
        self.wait(0.8)
