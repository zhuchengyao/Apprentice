from manim import *
import numpy as np


class ChineseRemainderExample(Scene):
    """
    Chinese Remainder Theorem: solve x ≡ a₁ (mod m₁), x ≡ a₂ (mod m₂)
    with gcd(m₁, m₂) = 1. A 2D grid over (x mod m₁, x mod m₂) is
    bijective to x mod m₁m₂.

    SINGLE_FOCUS:
      Grid of m₁×m₂ = 3×5 = 15 cells. ValueTracker x_tr increments
      0 → 14; always_redraw highlights the cell (x mod 3, x mod 5)
      and current x. Demonstrates bijectivity (no cell hit twice).
    """

    def construct(self):
        title = Tex(r"CRT: $x \leftrightarrow (x \bmod m_1,\ x \bmod m_2)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        m1, m2 = 3, 5
        cell = 0.7
        origin = np.array([-cell * m2 / 2, cell * m1 / 2 - 0.3, 0])

        # Base grid
        grid = VGroup()
        for i in range(m1):
            for j in range(m2):
                sq = Square(side_length=cell * 0.95,
                              color=WHITE, stroke_width=1.5,
                              fill_opacity=0.1)
                sq.move_to(origin + np.array([j * cell, -i * cell, 0]))
                grid.add(sq)
        # Axis labels
        m2_lbls = VGroup(*[MathTex(str(j), font_size=18, color=WHITE
                                      ).move_to(origin + np.array([j * cell, 0.55, 0]))
                            for j in range(m2)])
        m1_lbls = VGroup(*[MathTex(str(i), font_size=18, color=WHITE
                                      ).move_to(origin + np.array([-0.55, -i * cell, 0]))
                            for i in range(m1)])
        m2_axis_lbl = MathTex(r"x \bmod 5", font_size=22).move_to(origin + np.array([m2 / 2 * cell, 1.1, 0]))
        m1_axis_lbl = MathTex(r"x \bmod 3", font_size=22).rotate(PI/2).move_to(origin + np.array([-1.3, -(m1 - 1) / 2 * cell, 0]))
        self.play(FadeIn(grid), Write(m2_lbls), Write(m1_lbls),
                   Write(m2_axis_lbl), Write(m1_axis_lbl))

        x_tr = ValueTracker(0)

        # Show all visited cells as YELLOW, current cell BRIGHT YELLOW
        def visited_cells():
            x_cur = int(round(x_tr.get_value()))
            x_cur = max(0, min(x_cur, m1 * m2 - 1))
            grp = VGroup()
            for x in range(x_cur + 1):
                i = x % m1
                j = x % m2
                is_current = (x == x_cur)
                col = ORANGE if is_current else YELLOW
                op = 0.85 if is_current else 0.4
                sq = Square(side_length=cell * 0.95,
                              color=col, fill_opacity=op,
                              stroke_width=2 if is_current else 0.5)
                sq.move_to(origin + np.array([j * cell, -i * cell, 0]))
                grp.add(sq)
                lbl = MathTex(rf"{x}", font_size=20,
                                color=BLACK if is_current else YELLOW
                                ).move_to(origin + np.array([j * cell, -i * cell, 0]))
                grp.add(lbl)
            return grp

        self.add(always_redraw(visited_cells))

        def info():
            x = int(round(x_tr.get_value()))
            x = max(0, min(x, m1 * m2 - 1))
            return VGroup(
                MathTex(rf"x = {x}", color=YELLOW, font_size=26),
                MathTex(rf"x \bmod 3 = {x % m1}",
                         color=BLUE, font_size=22),
                MathTex(rf"x \bmod 5 = {x % m2}",
                         color=GREEN, font_size=22),
                MathTex(r"\gcd(3, 5) = 1 \Rightarrow \text{bijection}",
                         color=ORANGE, font_size=20),
                MathTex(rf"\text{{visited}}: {x + 1}/{m1 * m2}",
                         color=WHITE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(x_tr.animate.set_value(m1 * m2 - 1),
                   run_time=7, rate_func=linear)
        self.wait(0.5)
