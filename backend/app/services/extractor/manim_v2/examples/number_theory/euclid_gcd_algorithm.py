from manim import *
import numpy as np


class EuclidGCDAlgorithmExample(Scene):
    """
    Euclid's algorithm: gcd(a, b) = gcd(b, a mod b) until 0.
    Illustrate with gcd(1071, 462) = 21.

    SINGLE_FOCUS:
      Step-by-step reveal of the algorithm: (1071, 462) → (462, 147)
      → (147, 21) → (21, 0). ValueTracker step_tr reveals rows one
      at a time; final gcd at bottom.
    """

    def construct(self):
        title = Tex(r"Euclid's algorithm: $\gcd(a, b) = \gcd(b, a \bmod b)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Compute steps for gcd(1071, 462)
        a, b = 1071, 462
        steps = []
        while b != 0:
            q, r = divmod(a, b)
            steps.append((a, b, q, r))
            a, b = b, r
        final_gcd = a

        # Display each step as a row
        step_tr = ValueTracker(0)

        def rows():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(steps)))
            grp = VGroup()
            for i in range(s):
                a_i, b_i, q_i, r_i = steps[i]
                row = MathTex(rf"{a_i} = {q_i} \cdot {b_i} + {r_i}",
                                color=BLUE if i < s - 1 else GREEN,
                                font_size=28)
                row.move_to([0, 1.8 - i * 0.7, 0])
                grp.add(row)
            return grp

        self.add(always_redraw(rows))

        def gcd_box():
            s = int(round(step_tr.get_value()))
            if s >= len(steps):
                return VGroup(
                    Rectangle(width=3.5, height=0.8, color=YELLOW,
                                stroke_width=3, fill_opacity=0.15
                                ).move_to([0, -2.5, 0]),
                    MathTex(rf"\gcd(1071, 462) = {final_gcd}",
                              color=YELLOW, font_size=28).move_to([0, -2.5, 0]),
                )
            return VGroup()

        self.add(always_redraw(gcd_box))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(steps)))
            if s == 0:
                return VGroup()
            a_i, b_i, q_i, r_i = steps[s - 1]
            return VGroup(
                MathTex(rf"\text{{step}} = {s} / {len(steps)}",
                         color=WHITE, font_size=20),
                MathTex(rf"a = {a_i},\ b = {b_i}",
                         color=BLUE, font_size=18),
                MathTex(rf"q = {q_i},\ r = {r_i}",
                         color=ORANGE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        for s in range(1, len(steps) + 1):
            self.play(step_tr.animate.set_value(s),
                       run_time=0.9, rate_func=smooth)
            self.wait(0.7)
        self.wait(0.5)
