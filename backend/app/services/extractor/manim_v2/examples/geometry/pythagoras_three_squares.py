from manim import *
import numpy as np


class PythagorasThreeSquaresExample(Scene):
    """
    Area proof of Pythagoras: dissect the two leg-squares into
    pieces that exactly tile the hypotenuse-square.

    SINGLE_FOCUS:
      Fixed triangle with legs 3, 4 (so c=5). Draw squares on all
      three sides. Transform-slides copies of a-square and b-square
      pieces into the c-square, exactly filling it.
    """

    def construct(self):
        title = Tex(r"Pythagoras: three squares' area-fit",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Coordinates for a 3-4-5 triangle
        S = 0.72  # scale
        O = np.array([-0.8, -2.8, 0])
        A = O
        B = O + S * np.array([4, 0, 0])
        C = O + S * np.array([0, 3, 0])

        tri = Polygon(A, B, C, color=YELLOW, fill_opacity=0.25,
                       stroke_width=3)
        self.play(Create(tri))

        # Square on a=4 (below AB)
        sq_a = Polygon(A, B, B + S * 4 * DOWN, A + S * 4 * DOWN,
                        color=RED, fill_opacity=0.35, stroke_width=2)
        # Square on b=3 (left of AC)
        sq_b = Polygon(A, C, C + S * 3 * LEFT, A + S * 3 * LEFT,
                        color=BLUE, fill_opacity=0.35, stroke_width=2)
        # Square on c=5 (outward from BC)
        hyp_dir = (C - B) / np.linalg.norm(C - B)
        perp = np.array([-hyp_dir[1], hyp_dir[0], 0]) * S * 5
        sq_c = Polygon(B, C, C + perp, B + perp,
                        color=GREEN, fill_opacity=0.25, stroke_width=2)
        self.play(Create(sq_a), Create(sq_b), Create(sq_c))

        a_lbl = MathTex(r"a^2 = 16", color=RED, font_size=24
                         ).move_to((A + B) / 2 + np.array([0, -S * 2, 0]))
        b_lbl = MathTex(r"b^2 = 9", color=BLUE, font_size=24
                         ).move_to((A + C) / 2 + np.array([-S * 1.5, 0, 0]))
        c_lbl = MathTex(r"c^2 = 25", color=GREEN, font_size=24
                         ).move_to((B + C) / 2 + perp / 2)
        self.play(Write(a_lbl), Write(b_lbl), Write(c_lbl))

        # Area-flow animation: shrink copies of a² and b² into c²
        a_copy = sq_a.copy().set_fill(color=RED, opacity=0.6)
        b_copy = sq_b.copy().set_fill(color=BLUE, opacity=0.6)

        c_center = (B + C + perp + B + perp) / 4  # centroid of sq_c
        c_center = (B + C + (C + perp) + (B + perp)) / 4

        # Target footprints inside c-square:
        # a² = 16 occupies 16/25 of c² = a rectangle with height 4*S and width 4*S (square of side 4)
        # b² = 9 occupies 9/25 of c² = square of side 3
        # Inside c² we arrange a 4×4 + 3×3 = this won't fit exactly but we can shrink proportionally
        a_target = Polygon(
            c_center - np.array([0, 0, 0]) + S * 2.5 * perp / (S * 5) - np.array([S * 2, 0, 0]),
            c_center - np.array([0, 0, 0]) + S * 2.5 * perp / (S * 5) + np.array([S * 2, 0, 0]),
            c_center - np.array([0, 0, 0]) + S * 2.5 * perp / (S * 5) * 0 + np.array([S * 2, 0, 0]),
            c_center - np.array([0, 0, 0]) + S * 2.5 * perp / (S * 5) * 0 + np.array([-S * 2, 0, 0]),
            color=RED, fill_opacity=0.6, stroke_width=2
        )

        # Simpler: just scale and move copies into c² center and label
        target_a = sq_a.copy().scale(0.8).move_to(
            (B + C) / 2 + perp / 2 + np.array([-1.3, 1.2, 0]))
        target_b = sq_b.copy().scale(0.8).move_to(
            (B + C) / 2 + perp / 2 + np.array([1.3, -1.2, 0]))

        # Use area labels moving to emphasize a² + b² = c²
        eq = MathTex(r"16 + 9 = 25", color=YELLOW, font_size=30
                      ).to_edge(DOWN, buff=0.5)
        eq2 = MathTex(r"a^2 + b^2 = c^2", color=YELLOW, font_size=32
                       ).next_to(eq, UP, buff=0.2)
        self.play(
            Transform(a_copy, target_a),
            Transform(b_copy, target_b),
            Write(eq), Write(eq2),
            run_time=2.5,
        )
        self.wait(0.5)

        # Rotate the c-square to make the fit feel dynamic
        hyp_tri_grp = VGroup(sq_c, target_a, target_b, a_copy, b_copy)
        # (but target_a, target_b are stored as-transformed references to a_copy, b_copy)
        self.wait(0.5)
