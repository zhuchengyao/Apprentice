from manim import *
import numpy as np


class SphericalTriangleAverageExample(Scene):
    """
    Putnam problem: choose 3 points uniformly on a sphere; expected
    probability that all lie in the same open hemisphere is 1/2 for
    n=3? No — the classic result is 1 − n/2^(n-1) for n≥3; for n=3
    the probability that they're on a SINGLE hemisphere is 1 - 3/4
    = 1/4, so P(the triangle contains the center) = 3/4.

    Wait: the classical Putnam problem — 3 random points on a sphere:
    P(the triangle they form contains the center) = 1/4? Actually
    the result is 1/8 for general position? Let me do the simpler
    version: on a circle, 3 random points form a triangle containing
    the center iff no semicircle contains all three; P = 1/4.

    SINGLE_FOCUS:
      2D simplified: 3 points on a unit circle; ValueTracker t_tr
      drives N trials via trial_idx; fraction of trials where the
      triangle contains the center should → 1/4.
    """

    def construct(self):
        title = Tex(r"Random triangle on a circle: $P(\text{contains center}) = 1/4$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 2.0
        center = np.array([-3, -0.3, 0])
        circ = Circle(radius=R, color=WHITE, stroke_width=2
                       ).move_to(center)
        self.play(Create(circ))

        # Precompute 80 random triangles
        rng = np.random.default_rng(9)
        N = 80
        trials = []
        for _ in range(N):
            thetas = rng.uniform(0, 2 * PI, 3)
            pts = [R * np.array([np.cos(t), np.sin(t), 0])
                   for t in thetas]
            # Check if center (relative to circle) is inside the triangle
            def sign(p1, p2, p3):
                return ((p1[0] - p3[0]) * (p2[1] - p3[1])
                        - (p2[0] - p3[0]) * (p1[1] - p3[1]))
            d1 = sign(np.zeros(3), pts[0], pts[1])
            d2 = sign(np.zeros(3), pts[1], pts[2])
            d3 = sign(np.zeros(3), pts[2], pts[0])
            has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            contains = not (has_neg and has_pos)
            trials.append((pts, contains))

        trial_tr = ValueTracker(0)

        def current_triangle():
            idx = int(round(trial_tr.get_value())) % N
            pts, contains = trials[idx]
            color = GREEN if contains else RED
            return VGroup(
                Polygon(*[center + p for p in pts],
                         color=color, fill_opacity=0.3,
                         stroke_width=2),
                *[Dot(center + p, color=color, radius=0.07) for p in pts],
                Dot(center, color=YELLOW, radius=0.1),
            )

        self.add(always_redraw(current_triangle))

        def info():
            idx = int(round(trial_tr.get_value()))
            idx = max(1, min(idx, N))
            contains_count = sum(1 for (_, c) in trials[:idx] if c)
            frac = contains_count / idx
            pts, cur_contains = trials[idx % N]
            return VGroup(
                MathTex(rf"\text{{trial}} = {idx} / {N}",
                         color=WHITE, font_size=22),
                Tex(rf"current: {'contains' if cur_contains else 'no'}",
                     color=GREEN if cur_contains else RED,
                     font_size=22),
                MathTex(rf"\hat p = {frac:.3f}", color=YELLOW, font_size=26),
                MathTex(r"p = 1/4 = 0.25", color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(trial_tr.animate.set_value(N),
                   run_time=9, rate_func=linear)
        self.wait(0.5)
