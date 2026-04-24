from manim import *
import numpy as np


class DartsUncertaintyExample(Scene):
    """
    Darts on a target (from _2018/eop/chapter1/show_uncertainty_darts):
    each throw is jittered around the bullseye with Gaussian noise;
    empirical accuracy (fraction inside a radius-r ring) converges
    to the theoretical probability.

    SINGLE_FOCUS:
      Dartboard circles + 150 precomputed dart hits with Gaussian
      noise σ = 0.6. ValueTracker t_tr drops darts one by one;
      always_redraw dots + running empirical P(|hit| < 1.0) vs
      theoretical (1 - exp(-r²/(2σ²))).
    """

    def construct(self):
        title = Tex(r"Darts: empirical accuracy $\to$ theoretical",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        board_center = np.array([-2.5, -0.3, 0])
        # Concentric rings: radii 0.3, 0.6, 1.0, 1.5
        radii = [0.3, 0.6, 1.0, 1.5]
        ring_colors = [RED, ORANGE, YELLOW, GREY_B]
        rings = VGroup()
        for (r, col) in zip(radii, ring_colors):
            rings.add(Circle(radius=r, color=col,
                               fill_opacity=0.2, stroke_width=2
                               ).move_to(board_center))
        self.play(Create(rings))

        # Precompute 150 throws
        rng = np.random.default_rng(42)
        N = 150
        sigma = 0.6
        hits = rng.normal(scale=sigma, size=(N, 2))

        t_tr = ValueTracker(0)

        def dart_dots():
            k = int(round(t_tr.get_value()))
            k = max(0, min(k, N))
            grp = VGroup()
            for i in range(k):
                p = board_center + np.array([hits[i, 0], hits[i, 1], 0])
                # Color by which ring
                r = np.hypot(hits[i, 0], hits[i, 1])
                if r < radii[0]:
                    col = RED
                elif r < radii[1]:
                    col = ORANGE
                elif r < radii[2]:
                    col = YELLOW
                else:
                    col = GREY_B
                grp.add(Dot(p, color=col, radius=0.05))
            return grp

        self.add(always_redraw(dart_dots))

        # Empirical vs theoretical running plot
        ax = Axes(x_range=[0, N, N // 5], y_range=[0, 1, 0.25],
                   x_length=5, y_length=3, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([3.3, 0.5, 0])
        tr_lbl = MathTex(r"\text{throw}", font_size=18
                           ).next_to(ax, DOWN, buff=0.1)
        p_lbl = MathTex(r"P(|hit| < 1)", font_size=18
                           ).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(tr_lbl), Write(p_lbl))

        # Theoretical: P(r < 1.0) = 1 - exp(-1/(2σ²))
        p_theory = 1 - np.exp(-1 / (2 * sigma ** 2))
        theory_line = DashedLine(ax.c2p(0, p_theory),
                                    ax.c2p(N, p_theory),
                                    color=GREEN, stroke_width=2)
        theory_lbl = MathTex(rf"P_{{\text{{th}}}} = {p_theory:.3f}",
                               color=GREEN, font_size=18
                               ).next_to(ax.c2p(N, p_theory), UR, buff=0.1)
        self.play(Create(theory_line), Write(theory_lbl))

        def emp_curve():
            k = int(round(t_tr.get_value()))
            k = max(1, min(k, N))
            counts = np.zeros(k)
            for i in range(k):
                counts[i] = 1 if np.hypot(hits[i, 0], hits[i, 1]) < 1.0 else 0
            running = np.cumsum(counts) / np.arange(1, k + 1)
            pts = [ax.c2p(i + 1, running[i]) for i in range(k)]
            m = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(emp_curve))

        def info():
            k = int(round(t_tr.get_value()))
            k = max(1, min(k, N))
            inside = sum(
                1 for i in range(k)
                if np.hypot(hits[i, 0], hits[i, 1]) < 1.0)
            p_emp = inside / k
            return VGroup(
                MathTex(rf"k = {k} / {N}", color=WHITE, font_size=22),
                MathTex(rf"\text{{inside}} = {inside}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\hat p = {p_emp:.3f}",
                         color=YELLOW, font_size=24),
                MathTex(rf"p_{{th}} = {p_theory:.3f}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.3, -2.4, 0])

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(N),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
