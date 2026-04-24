from manim import *


class BinaryIncrementRuleExample(Scene):
    def construct(self):
        title = Text(
            "Binary increment: flip rightmost 0, zero the bits to its right",
            font_size=24,
        ).to_edge(UP)
        self.play(Write(title))

        def bits(n, w=5):
            return list(f"{n:0{w}b}")

        n = 11
        bit_mobs = VGroup(*[MathTex(b, font_size=60) for b in bits(n)])
        bit_mobs.arrange(RIGHT, buff=0.4).shift(DOWN * 0.2)
        self.play(Write(bit_mobs))

        circle = Circle(radius=0.45, color=YELLOW).move_to(bit_mobs[2])
        self.play(Create(circle))

        target = bits(n + 1)
        self.play(
            *[Transform(bit_mobs[i], MathTex(target[i], font_size=60).move_to(bit_mobs[i]))
              for i in range(5)],
            run_time=1.5,
        )
        self.play(FadeOut(circle))

        caption = MathTex(f"{n} \\to {n + 1}", font_size=44, color=YELLOW).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
