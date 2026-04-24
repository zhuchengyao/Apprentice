from manim import *
import numpy as np


class DifferenceOfSquaresExample(Scene):
    """
    a² − b² = (a + b)(a − b) via geometric dissection.

    SINGLE_FOCUS:
      Start with an a×a square with a b×b square removed from the
      corner (visually = a² − b²). Transform: the L-shaped region
      is cut into a (a−b)×b strip + an (a−b)×a rectangle, then
      one piece is slid to form a single (a+b)×(a−b) rectangle.
      ValueTracker b_tr sweeps b through 3 values to show
      invariance of the identity.
    """

    def construct(self):
        title = Tex(r"$a^2 - b^2 = (a+b)(a-b)$ by dissection",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = 3.6  # side a

        def make_scene_for_b(b):
            # Phase: a² − b² = L-shape = two rectangles
            # Piece 1: (a-b) × a rectangle at bottom-left
            # Piece 2: (a-b) × b rectangle at top-right
            # After rearrangement: (a+b) × (a-b)
            a = A

            outer = Rectangle(width=a, height=a, color=BLUE,
                               fill_opacity=0.35, stroke_width=2)
            outer.move_to([-3.3, 0, 0])

            # b×b removed region (top-right corner of outer)
            removed = Rectangle(width=b, height=b, color=BLACK,
                                 fill_opacity=1.0, stroke_width=1,
                                 stroke_color=WHITE
                                 ).align_to(outer, UR)
            removed.shift(LEFT * 0 + DOWN * 0)  # already at corner

            a_lbl = MathTex(r"a", font_size=22,
                             color=BLUE).next_to(outer, DOWN, buff=0.1)
            b_lbl = MathTex(rf"b = {b:.1f}", font_size=20,
                             color=RED).next_to(removed, DOWN, buff=0.1)
            grp_left = VGroup(outer, removed, a_lbl, b_lbl)

            # Right-hand side: (a+b) × (a-b) rectangle
            target = Rectangle(width=(a + b) * 0.5, height=(a - b) * 1.0,
                                color=GREEN, fill_opacity=0.35,
                                stroke_width=2).move_to([3.0, 0, 0])
            tw_lbl = MathTex(rf"(a+b) = {a + b:.1f}", font_size=20,
                              color=GREEN).next_to(target, DOWN, buff=0.1)
            th_lbl = MathTex(rf"(a-b) = {a - b:.1f}", font_size=20,
                              color=GREEN).next_to(target, LEFT, buff=0.1)
            grp_right = VGroup(target, tw_lbl, th_lbl)

            eq = MathTex(rf"a^2 - b^2 = {a**2 - b**2:.2f}",
                          color=YELLOW, font_size=28
                          ).to_edge(DOWN, buff=0.7)
            eq2 = MathTex(rf"(a+b)(a-b) = {(a+b)*(a-b):.2f}",
                           color=YELLOW, font_size=28
                           ).next_to(eq, UP, buff=0.2)

            return VGroup(grp_left, grp_right, eq, eq2)

        cur = make_scene_for_b(1.2)
        self.play(Create(cur), run_time=1.8)
        self.wait(0.5)

        for b in [2.0, 0.6, 2.8, 1.5]:
            new = make_scene_for_b(b)
            self.play(Transform(cur, new), run_time=1.5)
            self.wait(0.6)
        self.wait(0.4)
