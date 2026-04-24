from manim import *
import numpy as np


class VisualProofFallaciesExample(Scene):
    """
    Visual proof fallacies (from _2022/visual_proofs/lies): the
    infinite staircase limit paradox — a staircase inscribed in
    a right triangle has perimeter 2 no matter how many steps,
    but the limit (hypotenuse) has length √2. Perimeter is not
    a continuous functional of the curve.

    SINGLE_FOCUS:
      Unit right triangle with hypotenuse dashed (length √2 ≈
      1.414). ValueTracker N_tr steps N = 1, 2, 4, 8, 16, 32;
      staircase approximation drawn with always_redraw; perimeter
      stays at 2 regardless of N.
    """

    def construct(self):
        title = Tex(r"Staircase paradox: perimeter $\ne \lim$ perimeter",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        S = 3.5  # scale
        origin = np.array([-S / 2, -S / 2, 0]) + np.array([1, 0, 0])

        # Triangle vertices
        A = origin
        B = origin + np.array([S, 0, 0])
        C = origin + np.array([0, S, 0])

        # Draw true hypotenuse
        hyp = DashedLine(B, C, color=YELLOW, stroke_width=3)
        tri_sides = VGroup(
            Line(A, B, color=WHITE, stroke_width=2),
            Line(A, C, color=WHITE, stroke_width=2),
            hyp,
        )
        self.play(Create(tri_sides))

        hyp_lbl = MathTex(r"\sqrt 2 \approx 1.414",
                           color=YELLOW, font_size=22
                           ).next_to(hyp, direction=UR, buff=0.1)
        self.play(Write(hyp_lbl))

        N_tr = ValueTracker(1)

        def staircase():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 32))
            # Zigzag from B to C in N steps, each step: up then left
            step = S / N
            pts = [B]
            for i in range(N):
                # Up
                pts.append(pts[-1] + np.array([0, step, 0]))
                # Left
                pts.append(pts[-1] + np.array([-step, 0, 0]))
            m = VMobject(color=RED, stroke_width=3)
            m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(staircase))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 32))
            # Perimeter of staircase = N · (2 · 1/N) · S = 2S (constant)
            # For scale S, perimeter = 2S in scene coords → 2 in problem coords
            return VGroup(
                MathTex(rf"N = {N}", color=RED, font_size=24),
                MathTex(r"\text{staircase length} = 2",
                         color=RED, font_size=22),
                MathTex(r"\text{hypotenuse length} = \sqrt 2",
                         color=YELLOW, font_size=22),
                MathTex(r"\lim_{N\to\infty} \ell_{\text{stair}} \ne \ell_{\lim}",
                         color=ORANGE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.2)

        self.add(always_redraw(info))

        for target in [2, 4, 8, 16, 32]:
            self.play(N_tr.animate.set_value(target),
                       run_time=1.2, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
