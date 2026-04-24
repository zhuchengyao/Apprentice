from manim import *
import numpy as np


class InscribedRectangleLoopVariantExample(Scene):
    """
    Inscribed rectangle on a smooth closed curve (from _2024/
    inscribed_rect/loops): for any simple closed curve, there exist
    4 points forming a rectangle. Here we find several rectangles
    by chord-pair sampling.

    SINGLE_FOCUS:
      A kidney-shaped loop; ValueTracker θ_tr sweeps a test
      direction; for each θ find chord of length L and its
      perpendicular pair — when lengths match we have a rectangle,
      visualized in YELLOW; always_redraw.
    """

    def construct(self):
        title = Tex(r"Inscribed rectangle on a smooth loop",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Smooth kidney curve: r(t) = 2 + cos(2t) + 0.3 cos(3t)
        def loop_point(t):
            r = 2.2 + 0.6 * np.cos(2 * t) + 0.2 * np.cos(3 * t)
            return np.array([r * np.cos(t), r * np.sin(t), 0])

        # Draw the loop
        loop_pts = [loop_point(t) for t in np.linspace(0, 2 * PI, 200)]
        loop_mob = VMobject(color=WHITE, stroke_width=3)
        loop_mob.set_points_as_corners(loop_pts + [loop_pts[0]])
        self.play(Create(loop_mob), run_time=2)

        theta_tr = ValueTracker(0.0)

        def find_chord_pair(theta):
            """At direction θ, find a chord passing through origin's
            approximate center, of length L; return endpoints."""
            # Cast ray in direction θ and -θ from origin; find intersections
            # with the loop. Approximate by sampling.
            cen = np.array([0, 0, 0])
            dir1 = np.array([np.cos(theta), np.sin(theta), 0])
            # Find distance from origin to loop along dir1
            best_r1 = None
            for t in np.linspace(0, 2 * PI, 200):
                p = loop_point(t)
                # Project onto dir1
                d = np.dot(p, dir1)
                perp = np.linalg.norm(p - d * dir1)
                if perp < 0.05 and d > 0:
                    if best_r1 is None or d < best_r1:
                        best_r1 = d
            best_r2 = None
            for t in np.linspace(0, 2 * PI, 200):
                p = loop_point(t)
                d = -np.dot(p, dir1)  # opposite side
                perp = np.linalg.norm(p - (-d) * dir1)
                if perp < 0.05 and d > 0:
                    if best_r2 is None or d < best_r2:
                        best_r2 = d
            if best_r1 is None or best_r2 is None:
                return None
            return (best_r1 * dir1, -best_r2 * dir1)

        def chord_pair_viz():
            theta = theta_tr.get_value()
            grp = VGroup()
            # Chord 1 in direction θ
            cp1 = find_chord_pair(theta)
            cp2 = find_chord_pair(theta + PI / 2)
            if cp1 is None or cp2 is None:
                return grp
            p1a, p1b = cp1
            p2a, p2b = cp2
            grp.add(Line(p1a, p1b, color=BLUE, stroke_width=3))
            grp.add(Line(p2a, p2b, color=ORANGE, stroke_width=3))
            # Rectangle from endpoints (may not close perfectly)
            grp.add(Dot(p1a, color=BLUE, radius=0.08))
            grp.add(Dot(p1b, color=BLUE, radius=0.08))
            grp.add(Dot(p2a, color=ORANGE, radius=0.08))
            grp.add(Dot(p2b, color=ORANGE, radius=0.08))
            # If lengths match, flash rectangle
            L1 = np.linalg.norm(p1a - p1b)
            L2 = np.linalg.norm(p2a - p2b)
            if abs(L1 - L2) < 0.3:
                rect = Polygon(p1a, p2a, p1b, p2b,
                                 color=YELLOW, fill_opacity=0.25,
                                 stroke_width=3)
                grp.add(rect)
            return grp

        self.add(always_redraw(chord_pair_viz))

        def info():
            theta = theta_tr.get_value()
            cp1 = find_chord_pair(theta)
            cp2 = find_chord_pair(theta + PI / 2)
            if cp1 is None or cp2 is None:
                L1 = L2 = 0
            else:
                L1 = np.linalg.norm(cp1[0] - cp1[1])
                L2 = np.linalg.norm(cp2[0] - cp2[1])
            return VGroup(
                MathTex(rf"\theta = {np.degrees(theta):.0f}^\circ",
                         color=WHITE, font_size=22),
                MathTex(rf"L_1 = {L1:.3f}", color=BLUE, font_size=20),
                MathTex(rf"L_2 = {L2:.3f}", color=ORANGE, font_size=20),
                MathTex(rf"|L_1 - L_2| = {abs(L1-L2):.3f}",
                         color=YELLOW if abs(L1-L2) < 0.3 else GREEN,
                         font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(theta_tr.animate.set_value(PI),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
