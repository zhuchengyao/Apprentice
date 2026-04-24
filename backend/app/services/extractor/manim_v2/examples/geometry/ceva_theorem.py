from manim import *
import numpy as np


class CevaTheoremExample(Scene):
    """
    Ceva's theorem: three cevians (from vertices to opposite sides)
    of a triangle are concurrent iff (AF/FB)·(BD/DC)·(CE/EA) = 1.

    SINGLE_FOCUS:
      Triangle with three cevians from A, B, C to points F, D, E on
      opposite sides. ValueTracker u_tr varies one ratio; the cevians
      meet at a point only when the product equals 1.
    """

    def construct(self):
        title = Tex(r"Ceva's theorem: cevians concurrent iff $\prod = 1$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([-3, -1.5, 0])
        B = np.array([3, -1.5, 0])
        C = np.array([0, 2.5, 0])

        tri = Polygon(A, B, C, color=YELLOW, stroke_width=3,
                        fill_opacity=0.1)
        A_dot = Dot(A, color=GREEN, radius=0.09)
        B_dot = Dot(B, color=GREEN, radius=0.09)
        C_dot = Dot(C, color=GREEN, radius=0.09)
        A_lbl = MathTex(r"A", color=GREEN, font_size=22).next_to(A, DL, buff=0.1)
        B_lbl = MathTex(r"B", color=GREEN, font_size=22).next_to(B, DR, buff=0.1)
        C_lbl = MathTex(r"C", color=GREEN, font_size=22).next_to(C, UP, buff=0.1)
        self.play(Create(tri), FadeIn(A_dot, B_dot, C_dot),
                   Write(A_lbl), Write(B_lbl), Write(C_lbl))

        # Parameterize each cevian-foot by ratio from first vertex:
        # F on AB with AF/FB = u,
        # D on BC with BD/DC = v = 1/u (to make product = 1 when we also set E/EA)
        # Simpler: fix BD/DC = 2 and CE/EA = 3/2, let u = AF/FB vary;
        # product = u · 2 · 3/2 = 3u; concurrent when u = 1/3.

        u_tr = ValueTracker(0.2)

        def foot_F():
            u = u_tr.get_value()
            return A + u / (1 + u) * (B - A)

        def foot_D():
            # BD/DC = 2 ⇒ D = B + 2/3 (C - B)
            return B + 2 / 3 * (C - B)

        def foot_E():
            # CE/EA = 3/2 ⇒ E = C + 3/5 (A - C)
            return C + 3 / 5 * (A - C)

        def cevian_CF():
            return Line(C, foot_F(), color=BLUE, stroke_width=2.5)

        def cevian_AD():
            return Line(A, foot_D(), color=RED, stroke_width=2.5)

        def cevian_BE():
            return Line(B, foot_E(), color=PURPLE, stroke_width=2.5)

        def foot_dots():
            return VGroup(
                Dot(foot_F(), color=BLUE, radius=0.08),
                Dot(foot_D(), color=RED, radius=0.08),
                Dot(foot_E(), color=PURPLE, radius=0.08),
            )

        self.add(always_redraw(cevian_CF),
                  always_redraw(cevian_AD),
                  always_redraw(cevian_BE),
                  always_redraw(foot_dots))

        def info():
            u = u_tr.get_value()
            prod = u * 2 * 1.5
            match = abs(prod - 1) < 0.02
            return VGroup(
                MathTex(rf"AF/FB = {u:.3f}", color=BLUE, font_size=22),
                MathTex(r"BD/DC = 2", color=RED, font_size=22),
                MathTex(r"CE/EA = 1.5", color=PURPLE, font_size=22),
                MathTex(rf"\text{{product}} = {prod:.3f}",
                         color=GREEN if match else YELLOW, font_size=22),
                Tex(r"concurrent!" if match else r"not concurrent",
                     color=GREEN if match else YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for uv in [0.5, 1.0, 1/3, 2.0, 1/3]:
            self.play(u_tr.animate.set_value(uv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
