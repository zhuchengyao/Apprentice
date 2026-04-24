from manim import *
import numpy as np
from math import comb


class MoserFormulaExample(Scene):
    """
    Derivation of Moser's circle-regions formula via Euler:
    V - E + F = 2 on the planar graph of the chord diagram.

    TWO_COLUMN:
      LEFT  — chord diagram for n=6; highlights walk of V, E, F counts.
      RIGHT — step-by-step derivation building R_n = 1 + C(n,2) + C(n,4);
              ValueTracker step_tr sequentially reveals identity lines.
    """

    def construct(self):
        title = Tex(r"Derivation: $R_n = 1 + \binom{n}{2} + \binom{n}{4}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 6
        R = 2.0
        center = np.array([-3.3, -0.5, 0])
        circ = Circle(radius=R, color=BLUE_D, stroke_width=2).move_to(center)
        pts = [center + R * np.array([np.cos(2 * PI * k / n),
                                         np.sin(2 * PI * k / n), 0])
               for k in range(n)]
        dots = VGroup(*[Dot(p, color=YELLOW, radius=0.1) for p in pts])
        chords = VGroup()
        for i in range(n):
            for j in range(i + 1, n):
                chords.add(Line(pts[i], pts[j], color=BLUE, stroke_width=1.5))

        self.play(Create(circ), FadeIn(dots))
        self.play(Create(chords), run_time=2)

        # Interior intersection dots (C(n,4) general position)
        from itertools import combinations
        inter_dots = VGroup()
        for (a, b_, c, d) in combinations(range(n), 4):
            p1, p2, p3, p4 = pts[a], pts[c], pts[b_], pts[d]
            x1, y1 = p1[0], p1[1]
            x2, y2 = p2[0], p2[1]
            x3, y3 = p3[0], p3[1]
            x4, y4 = p4[0], p4[1]
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(denom) < 1e-9:
                continue
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
            if 0 < t < 1 and 0 < u < 1:
                inter_dots.add(Dot(np.array([x1 + t * (x2 - x1),
                                               y1 + t * (y2 - y1), 0]),
                                    color=RED, radius=0.06))
        self.play(FadeIn(inter_dots))

        V = n + comb(n, 4)
        E = comb(n, 2) + 2 * comb(n, 4) + n
        # Actually: each chord is split by intersections; edges along boundary arcs count
        # Number of edges E = n (arcs) + sum over chords of (pieces)
        # Sum over chords of (1 + intersections on it) = C(n,2) + 2·C(n,4)
        # So E = n + C(n,2) + 2·C(n,4)
        F = 2 - V + E  # includes outer face
        R_n = F - 1    # interior regions

        steps = VGroup(
            MathTex(r"V = n + \binom{n}{4}", color=BLUE, font_size=22),
            MathTex(r"E = n + \binom{n}{2} + 2\binom{n}{4}",
                     color=GREEN, font_size=22),
            MathTex(r"V - E + F = 2", color=YELLOW, font_size=22),
            MathTex(r"F = 2 - V + E = 2 + \binom{n}{2} + \binom{n}{4}",
                     color=ORANGE, font_size=22),
            MathTex(r"R_n = F - 1 = 1 + \binom{n}{2} + \binom{n}{4}",
                     color=RED, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.7, 0.0, 0])

        step_tr = ValueTracker(0)

        def revealed():
            k = int(round(step_tr.get_value()))
            g = VGroup()
            for i, s in enumerate(steps):
                if i < k:
                    g.add(s)
            return g

        self.add(always_redraw(revealed))

        for target in range(1, 6):
            self.play(step_tr.animate.set_value(target),
                       run_time=1.0)
            self.wait(0.6)

        numeric = MathTex(rf"n={n}: V={V},\ E={E},\ F={F},\ R_n={R_n}",
                           color=YELLOW, font_size=24
                           ).to_edge(DOWN, buff=0.35)
        self.play(Write(numeric))
        self.wait(0.5)
