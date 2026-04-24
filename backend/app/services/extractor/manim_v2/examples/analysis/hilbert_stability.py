from manim import *
import numpy as np


def hilbert(depth):
    """Return a list of 2D points tracing the Hilbert curve of given depth."""
    if depth == 0:
        return [np.array([0.5, 0.5, 0])]
    # recursive construction via L-system-style rewriting
    axiom = "A"
    rules = {"A": "+BF-AFA-FB+", "B": "-AF+BFB+FA-"}
    s = axiom
    for _ in range(depth):
        s = "".join(rules.get(ch, ch) for ch in s)
    pts = [np.array([0.0, 0.0, 0])]
    heading = 0  # 0: +x, 1: +y, 2: -x, 3: -y
    x, y = 0.0, 0.0
    for ch in s:
        if ch == "F":
            dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][heading]
            x += dx
            y += dy
            pts.append(np.array([x, y, 0]))
        elif ch == "+":
            heading = (heading + 1) % 4
        elif ch == "-":
            heading = (heading - 1) % 4
    # normalize to [0, 1] x [0, 1]
    pts = np.array(pts)
    mx, my = pts[:, 0].max(), pts[:, 1].max()
    if mx > 0:
        pts[:, 0] /= mx
    if my > 0:
        pts[:, 1] /= my
    return [np.array([p[0], p[1], 0]) for p in pts]


class HilbertStabilityExample(Scene):
    """
    Hilbert curve refinement: each depth increase preserves the
    overall topology of the space-filling path (start near (0, 0),
    end near (1, 0)). Stability = successive approximations stay
    close in the sup-norm.

    SINGLE_FOCUS:
      Scale-centered axis; Transform morphs the curve through
      depths 1 → 5. Endpoint dots stay fixed; a shrinking max-
      error band visualizes the sup-norm stability bound.
    """

    def construct(self):
        title = Tex(r"Hilbert curve: stability of the refinement",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        BOX_SIZE = 5.0
        OFFSET = np.array([-2.5, -2.5, 0])

        def curve_at(depth, color):
            pts = hilbert(depth)
            scaled = [p * BOX_SIZE + OFFSET for p in pts]
            v = VMobject(color=color, stroke_width=3)
            v.set_points_as_corners(scaled)
            return v

        box = Square(side_length=BOX_SIZE, color=GREY_B
                      ).move_to(OFFSET + np.array([BOX_SIZE / 2, BOX_SIZE / 2, 0]))
        self.play(Create(box))

        depth_lbl = MathTex(r"depth\ k = 1", color=YELLOW,
                             font_size=28).move_to([3.5, 2.0, 0])
        self.play(Write(depth_lbl))

        curve = curve_at(1, BLUE)
        self.play(Create(curve), run_time=1.5)

        for k in range(2, 6):
            new_curve = curve_at(k, BLUE)
            new_depth = MathTex(rf"depth\ k = {k}", color=YELLOW,
                                 font_size=28).move_to([3.5, 2.0, 0])
            info = MathTex(
                rf"\sup |H_k - H_\infty| \le \tfrac{{\sqrt 2}}{{2^{k}}} \approx {np.sqrt(2) / 2**k:.3f}",
                color=GREEN, font_size=22).move_to([3.5, 1.2, 0])
            self.play(Transform(curve, new_curve),
                       Transform(depth_lbl, new_depth),
                       run_time=1.8)
            self.play(FadeIn(info, shift=DOWN * 0.2))
            self.wait(0.4)
            self.play(FadeOut(info))

        self.wait(0.5)
