from manim import *
import numpy as np


class NonPlanarK5Example(Scene):
    """
    K_5 (complete graph on 5 vertices) is not planar: any embedding
    has at least one edge crossing. Kuratowski's theorem.

    SINGLE_FOCUS:
      5 vertices arranged on a circle. Draw all C(5, 2) = 10 edges;
      RED-highlight the forced crossings (there's exactly 1
      crossing in a circular embedding of K_5, wait no — 5 crossings
      actually). Use ValueTracker s_tr to morph vertex positions
      through 3 different layouts — each has >= 1 crossing shown in RED.
    """

    def construct(self):
        title = Tex(r"$K_5$ is non-planar: at least one crossing in every drawing",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Three candidate layouts
        L1 = [np.array([2.5 * np.cos(k * 2 * PI / 5 + PI / 2),
                         2.5 * np.sin(k * 2 * PI / 5 + PI / 2), 0])
              for k in range(5)]
        L2 = [np.array([k - 2.5, 0, 0]) for k in range(5)]  # all on a line (degenerate)
        L3 = [  # "outer + one inner" layout
            np.array([0, 2.3, 0]),
            np.array([2.3, 0.7, 0]),
            np.array([1.4, -2.0, 0]),
            np.array([-1.4, -2.0, 0]),
            np.array([0, 0, 0]),  # inner vertex
        ]

        layout_tr = ValueTracker(0.0)

        def positions():
            s = layout_tr.get_value()
            if s < 1.0:
                a = s
                return [(1 - a) * L1[i] + a * L3[i] for i in range(5)]
            else:
                return L3

        def chord_intersect(p1, p2, p3, p4):
            x1, y1 = p1[0], p1[1]
            x2, y2 = p2[0], p2[1]
            x3, y3 = p3[0], p3[1]
            x4, y4 = p4[0], p4[1]
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(denom) < 1e-9:
                return None
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
            if 0.01 < t < 0.99 and 0.01 < u < 0.99:
                return np.array([x1 + t * (x2 - x1),
                                 y1 + t * (y2 - y1), 0])
            return None

        def dots():
            P = positions()
            grp = VGroup()
            for i, p in enumerate(P):
                grp.add(Dot(p, color=YELLOW, radius=0.14))
                lbl = MathTex(str(i + 1), font_size=20, color=BLACK)
                lbl.move_to(p)
                grp.add(lbl)
            return grp

        def edges():
            P = positions()
            grp = VGroup()
            for i in range(5):
                for j in range(i + 1, 5):
                    grp.add(Line(P[i], P[j], color=BLUE, stroke_width=2))
            return grp

        def crossings():
            P = positions()
            grp = VGroup()
            from itertools import combinations
            crosses_found = 0
            edges_list = [(i, j) for i in range(5) for j in range(i + 1, 5)]
            for a, b in combinations(edges_list, 2):
                (i, j) = a
                (k, l) = b
                if len({i, j, k, l}) < 4:
                    continue
                pt = chord_intersect(P[i], P[j], P[k], P[l])
                if pt is not None:
                    grp.add(Dot(pt, color=RED, radius=0.1))
                    crosses_found += 1
            return grp

        self.add(always_redraw(edges),
                  always_redraw(dots),
                  always_redraw(crossings))

        def info():
            P = positions()
            from itertools import combinations
            edges_list = [(i, j) for i in range(5) for j in range(i + 1, 5)]
            crossings_count = 0
            for a, b in combinations(edges_list, 2):
                (i, j) = a
                (k, l) = b
                if len({i, j, k, l}) < 4:
                    continue
                pt = chord_intersect(P[i], P[j], P[k], P[l])
                if pt is not None:
                    crossings_count += 1
            return VGroup(
                MathTex(r"V = 5, E = 10", color=YELLOW, font_size=22),
                MathTex(rf"\text{{crossings}} = {crossings_count}",
                         color=RED, font_size=24),
                MathTex(r"K_5: E > 3V - 6 \Rightarrow \text{non-planar}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.5)

        self.add(always_redraw(info))

        # Tour: layout 1 → layout 3
        self.play(layout_tr.animate.set_value(1.0),
                   run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(layout_tr.animate.set_value(0.5),
                   run_time=2, rate_func=smooth)
        self.wait(0.5)
        self.play(layout_tr.animate.set_value(0.0),
                   run_time=2, rate_func=smooth)
        self.wait(0.5)
