from manim import *
import numpy as np


class SierpinskiDimensionFromMassEquation(Scene):
    """Derive the Sierpinski dimension D = log_2(3) ≈ 1.585 algebraically.
    Start from the mass-scaling relation (1/2)^D * M = (1/3) M, simplify to
    2^D = 3, take log base 2, evaluate."""

    def construct(self):
        title = Tex(
            r"Sierpinski dimension from the mass-scaling rule",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def make_sierpinski(order=5, size=2.6):
            A = np.array([-size / 2, -size * np.sqrt(3) / 6, 0])
            B = np.array([size / 2, -size * np.sqrt(3) / 6, 0])
            C = np.array([0, size * np.sqrt(3) / 3, 0])

            def recurse(a, b, c, depth):
                if depth == 0:
                    return [Polygon(a, b, c, color=YELLOW,
                                    fill_opacity=0.8, stroke_width=0)]
                ab = (a + b) / 2
                bc = (b + c) / 2
                ca = (c + a) / 2
                return (
                    recurse(a, ab, ca, depth - 1)
                    + recurse(ab, b, bc, depth - 1)
                    + recurse(ca, bc, c, depth - 1)
                )

            return VGroup(*recurse(A, B, C, order))

        sier = make_sierpinski(order=5, size=2.6)
        sier.to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        self.play(FadeIn(sier, lag_ratio=0.02, run_time=1.5))

        caption = Tex(
            r"Scale by $\tfrac{1}{2}$, and the mass becomes $\tfrac{1}{3}$ of the whole.",
            font_size=26,
        )
        caption.next_to(sier, UP, buff=0.3)
        self.play(FadeIn(caption))

        eq1 = MathTex(
            r"\left(\tfrac{1}{2}\right)^{D}",
            r"\cdot", r"M",
            r"=", r"\tfrac{1}{3}\, M",
            font_size=42,
        )
        eq1[0].set_color(BLUE)
        eq1[4].set_color(GREEN)
        eq1.move_to(RIGHT * 2.5 + UP * 1.3)
        self.play(Write(eq1))
        self.wait(0.6)

        eq2 = MathTex(
            r"\left(\tfrac{1}{2}\right)^{D}", r"=", r"\tfrac{1}{3}",
            font_size=42,
        )
        eq2[0].set_color(BLUE)
        eq2[2].set_color(GREEN)
        eq2.next_to(eq1, DOWN, buff=0.6)
        self.play(TransformFromCopy(eq1, eq2))
        self.wait(0.4)

        eq3 = MathTex(r"2^{D}", r"=", r"3", font_size=46)
        eq3[0].set_color(BLUE)
        eq3[2].set_color(GREEN)
        eq3.next_to(eq2, DOWN, buff=0.6)
        self.play(ReplacementTransform(eq2.copy(), eq3))
        self.wait(0.5)

        eq4 = MathTex(
            r"D", r"=", r"\log_{2}(3)", font_size=50,
        )
        eq4[0].set_color(YELLOW)
        eq4.next_to(eq3, DOWN, buff=0.6)
        self.play(Write(eq4))
        self.wait(0.3)

        eq5 = MathTex(r"\approx", r"1.585", font_size=46)
        eq5[1].set_color(YELLOW)
        eq5.next_to(eq4, RIGHT, buff=0.2)
        self.play(Write(eq5))

        box = SurroundingRectangle(
            VGroup(eq4, eq5), color=YELLOW, buff=0.2, stroke_width=3,
        )
        self.play(Create(box))
        self.wait(1.5)
