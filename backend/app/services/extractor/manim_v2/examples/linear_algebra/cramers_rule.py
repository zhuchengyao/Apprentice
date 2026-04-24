from manim import *
import numpy as np


class CramersRuleExample(Scene):
    """
    Cramer's rule: solve a 2×2 system as a ratio of parallelogram areas.

    System: 2x + y = 3
            x + 2y = 2

    Visual: a parallelogram on a plane spanned by columns of A = [[2,1],[1,2]].
    Replace each column with the right-hand side b = (3, 2) to get parallelogram
    A_x and A_y; then x = area(A_x)/area(A), y = area(A_y)/area(A).

    Animate the parallelograms forming via Transform: start with A's parallelogram
    in the LEFT panel, sweep through column-replacement to build A_x, then A_y.
    Right column has live area readouts and the final solution.
    """

    def construct(self):
        title = Tex(r"Cramer's rule: $x = \tfrac{\det A_x}{\det A},\ y = \tfrac{\det A_y}{\det A}$",
                    font_size=30).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Matrix and right-hand side
        a1 = np.array([2.0, 1.0])  # column 1 of A
        a2 = np.array([1.0, 2.0])  # column 2 of A
        b = np.array([3.0, 2.0])

        # System equation
        sys_eq = MathTex(
            r"\begin{cases} 2x + y = 3 \\ x + 2y = 2 \end{cases}",
            font_size=30,
        ).move_to([+4.4, +2.5, 0])
        self.play(Write(sys_eq))

        # LEFT plane
        plane = NumberPlane(
            x_range=[-1, 5, 1], y_range=[-1, 4, 1],
            x_length=6.0, y_length=5.0,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-2.4, -0.4, 0])
        self.play(Create(plane))

        def parallelogram_pts(c1, c2):
            origin = plane.c2p(0, 0)
            p1 = plane.c2p(*c1)
            p2 = plane.c2p(*c2)
            p_sum = plane.c2p(*(c1 + c2))
            return [origin, p1, p_sum, p2]

        # Phase 1: original A parallelogram
        det_A = a1[0] * a2[1] - a1[1] * a2[0]  # = 3
        det_Ax = b[0] * a2[1] - b[1] * a2[0]   # = 4
        det_Ay = a1[0] * b[1] - a1[1] * b[0]   # = 1

        pgram_A = Polygon(*parallelogram_pts(a1, a2),
                          color=BLUE, fill_opacity=0.45, stroke_width=2)
        a1_arrow = Arrow(plane.c2p(0, 0), plane.c2p(*a1), buff=0,
                         color=GREEN, stroke_width=4,
                         max_tip_length_to_length_ratio=0.15)
        a2_arrow = Arrow(plane.c2p(0, 0), plane.c2p(*a2), buff=0,
                         color=ORANGE, stroke_width=4,
                         max_tip_length_to_length_ratio=0.15)
        a1_lbl = MathTex(r"\vec a_1", color=GREEN, font_size=24).next_to(
            plane.c2p(*a1), DR, buff=0.1)
        a2_lbl = MathTex(r"\vec a_2", color=ORANGE, font_size=24).next_to(
            plane.c2p(*a2), UL, buff=0.1)

        self.play(GrowArrow(a1_arrow), GrowArrow(a2_arrow),
                  Write(a1_lbl), Write(a2_lbl))
        self.play(FadeIn(pgram_A))

        # Live area readout
        area_readout = MathTex(rf"|\det A| = {abs(det_A):.0f}",
                               color=BLUE, font_size=28).move_to([+4.4, +1.0, 0])
        self.play(Write(area_readout))
        self.wait(0.6)

        # Phase 2: replace column 1 with b, forming A_x parallelogram
        b_arrow = Arrow(plane.c2p(0, 0), plane.c2p(*b), buff=0,
                        color=YELLOW, stroke_width=4,
                        max_tip_length_to_length_ratio=0.15)
        b_lbl = MathTex(r"\vec b = (3, 2)", color=YELLOW, font_size=24).next_to(
            plane.c2p(*b), UR, buff=0.1)
        self.play(GrowArrow(b_arrow), Write(b_lbl))

        pgram_Ax = Polygon(*parallelogram_pts(b, a2),
                           color=YELLOW, fill_opacity=0.55, stroke_width=2)
        ax_label = MathTex(r"|\det A_x| = 4", color=YELLOW, font_size=28).move_to([+4.4, +0.0, 0])

        self.play(Transform(pgram_A, pgram_Ax),
                  FadeOut(a1_arrow), FadeOut(a1_lbl),
                  Write(ax_label),
                  run_time=2)

        x_eq = MathTex(rf"x = \tfrac{{|\det A_x|}}{{|\det A|}} = \tfrac{{4}}{{3}}",
                       color=YELLOW, font_size=28).move_to([+4.4, -0.9, 0])
        self.play(Write(x_eq))
        self.wait(0.7)

        # Phase 3: restore A, then replace column 2 with b
        pgram_Ay = Polygon(*parallelogram_pts(a1, b),
                           color=YELLOW, fill_opacity=0.55, stroke_width=2)
        ay_label = MathTex(r"|\det A_y| = 1", color=YELLOW, font_size=28).move_to([+4.4, -1.6, 0])

        self.play(Transform(pgram_A, pgram_Ay),
                  FadeIn(a1_arrow), FadeIn(a1_lbl),
                  FadeOut(a2_arrow), FadeOut(a2_lbl),
                  Write(ay_label),
                  run_time=2)

        y_eq = MathTex(rf"y = \tfrac{{|\det A_y|}}{{|\det A|}} = \tfrac{{1}}{{3}}",
                       color=YELLOW, font_size=28).move_to([+4.4, -2.5, 0])
        self.play(Write(y_eq))
        self.wait(1.0)
