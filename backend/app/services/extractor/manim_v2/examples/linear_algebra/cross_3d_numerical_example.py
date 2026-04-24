from manim import *
import numpy as np


class Cross3dNumericalExampleExample(Scene):
    """
    Compute v × w for specific 3D vectors using the component formula:
    v × w = (v₂w₃ - v₃w₂, v₃w₁ - v₁w₃, v₁w₂ - v₂w₁).

    v = (1, 2, 3), w = (4, -1, 2).
    v × w = (2·2 - 3·(-1), 3·4 - 1·2, 1·(-1) - 2·4) = (7, 10, -9).
    """

    def construct(self):
        title = Tex(r"3D cross computation: $\vec v\times\vec w$ from components",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Show formula and example
        v = Matrix([[1], [2], [3]], v_buff=0.5).set_color(BLUE).scale(0.9)
        times = MathTex(r"\times", font_size=48)
        w = Matrix([[4], [-1], [2]], v_buff=0.5).set_color(ORANGE).scale(0.9)
        eq = MathTex(r"=", font_size=48)
        result = Matrix([[r"v_2w_3-v_3w_2"], [r"v_3w_1-v_1w_3"], [r"v_1w_2-v_2w_1"]],
                         v_buff=0.5).set_color(GREEN).scale(0.7)

        row = VGroup(v, times, w, eq, result).arrange(RIGHT, buff=0.3).shift(UP * 0.5)
        self.play(Write(row))
        self.wait(0.5)

        # Show each computation step
        steps = VGroup(
            MathTex(r"2\cdot 2 - 3\cdot (-1) = 7", color=GREEN, font_size=28),
            MathTex(r"3\cdot 4 - 1\cdot 2 = 10", color=GREEN, font_size=28),
            MathTex(r"1\cdot (-1) - 2\cdot 4 = -9", color=GREEN, font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(row, DOWN, buff=0.6)
        for step in steps:
            self.play(Write(step), run_time=0.7)
            self.wait(0.25)

        # Final answer
        final_vec = Matrix([[7], [10], [-9]]).set_color(YELLOW).scale(0.95)
        final_lbl = MathTex(r"\vec v\times\vec w =", font_size=32)
        final = VGroup(final_lbl, final_vec).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.5)
        self.play(Write(final))
        self.wait(1.0)
