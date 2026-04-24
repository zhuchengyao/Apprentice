from manim import *


class RsaTrapdoorExample(Scene):
    def construct(self):
        title = Text("RSA trapdoor: easy forward, hard backward", font_size=28).to_edge(UP)
        self.play(Write(title))

        forward = VGroup(
            MathTex(r"p = 61,\; q = 53", font_size=30),
            MathTex(r"n = p \cdot q = 3233", font_size=30, color=GREEN),
        ).arrange(DOWN, buff=0.35)
        self.play(Write(forward[0]))
        self.play(Transform(forward[0].copy(), forward[1]))
        forward_arrow = Arrow(LEFT * 3, RIGHT * 3, color=GREEN, buff=0.2).shift(0.4 * DOWN)
        easy = Text("multiplying is easy", font_size=24, color=GREEN).next_to(forward_arrow, UP, buff=0.1)
        self.play(GrowArrow(forward_arrow), Write(easy))
        self.wait(0.2)

        back = VGroup(forward_arrow.copy().set_color(RED), easy.copy()).arrange(DOWN, buff=0)
        reverse_arrow = Arrow(RIGHT * 3, LEFT * 3, color=RED, buff=0.2).shift(1.6 * DOWN)
        hard = Text("factoring is hard", font_size=24, color=RED).next_to(reverse_arrow, DOWN, buff=0.1)
        self.play(GrowArrow(reverse_arrow), Write(hard))

        rsa = MathTex(
            r"\text{Public: } (n, e) \qquad \text{Private: } (p, q, d)",
            font_size=28, color=YELLOW,
        ).to_edge(DOWN)
        self.play(Write(rsa))
        self.wait(0.6)
