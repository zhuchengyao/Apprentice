from manim import *


class BinaryCounting0To15Example(Scene):
    def construct(self):
        decimal = MathTex("0", font_size=72)
        binary = MathTex("0000", font_size=60)
        binary.next_to(decimal, DOWN, buff=0.9)

        cap_top = Text("Decimal", font_size=22, color=GREY_B).next_to(decimal, UP, buff=0.3)
        cap_bot = Text("Binary", font_size=22, color=GREY_B).next_to(binary, DOWN, buff=0.3)

        self.add(decimal, binary, cap_top, cap_bot)

        for n in range(1, 16):
            new_dec = MathTex(str(n), font_size=72).move_to(decimal)
            new_bin = MathTex(f"{n:04b}", font_size=60).move_to(binary)
            self.play(
                Transform(decimal, new_dec),
                Transform(binary, new_bin),
                run_time=0.3,
            )
        self.wait(0.6)
