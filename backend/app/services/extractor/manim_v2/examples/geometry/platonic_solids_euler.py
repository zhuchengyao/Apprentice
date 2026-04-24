from manim import *
import numpy as np


class PlatonicSolidsEulerExample(Scene):
    """
    Platonic solids: 5 regular polyhedra. Each satisfies Euler's
    formula V - E + F = 2.

    SINGLE_FOCUS:
      Table of 5 solids (tetrahedron, cube, octahedron, dodecahedron,
      icosahedron) with V, E, F counts. ValueTracker idx_tr steps
      through each; always_redraw table + Euler verification.
    """

    def construct(self):
        title = Tex(r"Platonic solids: $V - E + F = 2$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        solids = [
            ("tetrahedron", 4, 6, 4),
            ("cube", 8, 12, 6),
            ("octahedron", 6, 12, 8),
            ("dodecahedron", 20, 30, 12),
            ("icosahedron", 12, 30, 20),
        ]

        # Headers
        headers = VGroup(
            Tex(r"solid", color=WHITE, font_size=22),
            MathTex(r"V", color=BLUE, font_size=24),
            MathTex(r"E", color=GREEN, font_size=24),
            MathTex(r"F", color=ORANGE, font_size=24),
            MathTex(r"V - E + F", color=YELLOW, font_size=22),
        )
        cols_x = [-5, -2.5, -0.8, 0.9, 3]
        row_y_start = 2.0
        row_dy = 0.55
        for i, h in enumerate(headers):
            h.move_to([cols_x[i], row_y_start, 0])
        self.play(Write(headers))

        idx_tr = ValueTracker(0)

        def rows():
            s = int(round(idx_tr.get_value()))
            s = max(0, min(s, len(solids)))
            grp = VGroup()
            for i in range(s):
                name, V, E, F = solids[i]
                euler = V - E + F
                y = row_y_start - (i + 1) * row_dy
                col = GREEN if euler == 2 else RED
                grp.add(Tex(name, color=col, font_size=20
                              ).move_to([cols_x[0], y, 0]))
                grp.add(MathTex(rf"{V}", color=BLUE, font_size=22
                                  ).move_to([cols_x[1], y, 0]))
                grp.add(MathTex(rf"{E}", color=GREEN, font_size=22
                                  ).move_to([cols_x[2], y, 0]))
                grp.add(MathTex(rf"{F}", color=ORANGE, font_size=22
                                  ).move_to([cols_x[3], y, 0]))
                grp.add(MathTex(rf"= {euler}",
                                  color=col, font_size=22
                                  ).move_to([cols_x[4], y, 0]))
            return grp

        self.add(always_redraw(rows))

        def info():
            s = int(round(idx_tr.get_value()))
            return VGroup(
                MathTex(rf"\text{{row}} = {s}/5",
                         color=WHITE, font_size=20),
                Tex(r"all 5: $V - E + F = 2$",
                     color=GREEN, font_size=22),
                Tex(r"(consequence of genus-0 sphere topology)",
                     color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for s in range(1, len(solids) + 1):
            self.play(idx_tr.animate.set_value(s),
                       run_time=0.9, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
