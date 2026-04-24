from manim import *
import numpy as np


class SymbolicSolveLinearSystemExample(Scene):
    """
    Derive x = A^(-1) v algebraically from Ax = v:
      Ax = v
      A^(-1) A x = A^(-1) v
      Ix = A^(-1) v
      x = A^(-1) v
    The A^(-1) A = I "do nothing" cancels on the left.
    """

    def construct(self):
        title = Tex(r"Symbolic solve: $A\vec x=\vec v \Rightarrow \vec x=A^{-1}\vec v$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Lines
        l1 = MathTex(r"A", r"\vec x", r"=", r"\vec v", font_size=48).shift(UP * 1.5)
        l1[1].set_color(PINK)
        l1[3].set_color(YELLOW)

        l2 = MathTex(r"A^{-1}", r"A", r"\vec x", r"=", r"A^{-1}", r"\vec v",
                      font_size=44).shift(UP * 0.3)
        l2[0].set_color(GREEN); l2[4].set_color(GREEN)
        l2[2].set_color(PINK); l2[5].set_color(YELLOW)

        l3 = MathTex(r"I", r"\vec x", r"=", r"A^{-1}", r"\vec v",
                      font_size=44).shift(DOWN * 0.9)
        l3[0].set_color(BLUE); l3[3].set_color(GREEN)
        l3[1].set_color(PINK); l3[4].set_color(YELLOW)

        l4 = MathTex(r"\vec x", r"=", r"A^{-1}", r"\vec v",
                      font_size=52, color=WHITE).shift(DOWN * 2.2)
        l4[0].set_color(PINK); l4[2].set_color(GREEN); l4[3].set_color(YELLOW)

        self.play(Write(l1))
        self.wait(0.4)

        # Multiply both sides by A^-1
        note1 = Tex(r"apply $A^{-1}$ to both sides",
                     color=GREEN, font_size=22).next_to(l2, RIGHT, buff=0.3)
        self.play(Write(l2), Write(note1))
        self.wait(0.5)

        # A^-1 A = I
        brace = Brace(VGroup(l2[0], l2[1]), DOWN)
        brace_lbl = MathTex(r"I", color=BLUE, font_size=36).next_to(brace, DOWN, buff=0.1)
        self.play(GrowFromCenter(brace), Write(brace_lbl))
        self.wait(0.4)

        self.play(Write(l3), FadeOut(brace), FadeOut(brace_lbl))
        self.wait(0.3)

        # I disappears
        self.play(FadeOut(l3[0]), l3[1:].animate.shift(LEFT * 0.3))
        self.wait(0.3)
        self.play(Write(l4))
        self.wait(0.5)

        # Final box
        final_box = SurroundingRectangle(l4, color=YELLOW, buff=0.15)
        self.play(Create(final_box))
        self.wait(0.8)
