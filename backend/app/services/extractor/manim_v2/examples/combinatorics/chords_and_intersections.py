from manim import *
import numpy as np
from math import comb


class ChordsAndIntersectionsExample(Scene):
    """
    n points on a circle in general position:
      C(n, 2) chords and C(n, 4) interior intersections.

    SINGLE_FOCUS:
      Circle with n points, all n·(n-1)/2 chords drawn; ValueTracker
      n_tr sweeps n = 3..9; always_redraw rebuilds points, chords,
      and intersection dots. Live count panel.
    """

    def construct(self):
        title = Tex(r"$n$ points on a circle: $\binom{n}{2}$ chords, $\binom{n}{4}$ intersections",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 2.5
        center = np.array([-2.0, -0.3, 0])
        circ = Circle(radius=R, color=BLUE_D, stroke_width=2
                       ).move_to(center)
        self.play(Create(circ))

        n_tr = ValueTracker(3)

        def pts_of(n):
            return [center + R * np.array([np.cos(2 * PI * k / n),
                                              np.sin(2 * PI * k / n), 0])
                    for k in range(n)]

        def chord_intersection(p1, p2, p3, p4):
            # Line (p1, p2) intersect line (p3, p4)
            x1, y1 = p1[0], p1[1]
            x2, y2 = p2[0], p2[1]
            x3, y3 = p3[0], p3[1]
            x4, y4 = p4[0], p4[1]
            denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if abs(denom) < 1e-9:
                return None
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
            if 0 < t < 1 and 0 < u < 1:
                return np.array([x1 + t * (x2 - x1),
                                 y1 + t * (y2 - y1), 0])
            return None

        def points():
            n = int(round(n_tr.get_value()))
            grp = VGroup()
            for p in pts_of(n):
                grp.add(Dot(p, color=YELLOW, radius=0.1))
            return grp

        def chords():
            n = int(round(n_tr.get_value()))
            pts = pts_of(n)
            grp = VGroup()
            for i in range(n):
                for j in range(i + 1, n):
                    grp.add(Line(pts[i], pts[j], color=BLUE,
                                   stroke_width=1.5))
            return grp

        def intersections():
            n = int(round(n_tr.get_value()))
            pts = pts_of(n)
            grp = VGroup()
            from itertools import combinations
            for combo in combinations(range(n), 4):
                a, b, c, d = combo
                # chord (a,c) and (b,d) cross
                cross = chord_intersection(pts[a], pts[c], pts[b], pts[d])
                if cross is not None:
                    grp.add(Dot(cross, color=RED, radius=0.07))
            return grp

        self.add(always_redraw(chords),
                  always_redraw(points),
                  always_redraw(intersections))

        def info():
            n = int(round(n_tr.get_value()))
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=28),
                MathTex(rf"\binom{{n}}{{2}} = {comb(n, 2)}",
                         color=BLUE, font_size=26),
                MathTex(rf"\binom{{n}}{{4}} = {comb(n, 4)}",
                         color=RED, font_size=26),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.5, 0.8, 0])

        self.add(always_redraw(info))

        for target in [4, 5, 6, 7, 8, 9]:
            self.play(n_tr.animate.set_value(target),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
