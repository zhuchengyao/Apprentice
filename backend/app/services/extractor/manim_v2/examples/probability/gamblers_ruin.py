from manim import *
import numpy as np


class GamblersRuinExample(Scene):
    """
    Gambler's ruin: start with k dollars; at each step gain $1 with
    probability p or lose $1 with probability 1-p, until 0 or N.
    P(hit N before 0) = (1 - (q/p)^k) / (1 - (q/p)^N) for p ≠ q.

    SINGLE_FOCUS:
      Number line 0 to N=10; ValueTracker t_tr walks a precomputed
      random-walk path; end-state shown (0 = ruin, N = win). Multiple
      simulations overlay to show win probability.
    """

    def construct(self):
        title = Tex(r"Gambler's ruin: start at $k$, reach 0 or $N$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N = 10
        k = 4
        p = 0.48
        q = 1 - p

        nl = NumberLine(x_range=[0, N + 1, 1], length=10,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 0,
                                                 "font_size": 16}
                         ).move_to([0, 0, 0])
        self.play(Create(nl))

        # Boundaries
        left_end = Line(nl.n2p(0) + UP * 0.3, nl.n2p(0) + DOWN * 0.3,
                          color=RED, stroke_width=4)
        right_end = Line(nl.n2p(N) + UP * 0.3, nl.n2p(N) + DOWN * 0.3,
                           color=GREEN, stroke_width=4)
        left_lbl = Tex("ruin", color=RED, font_size=20
                        ).next_to(left_end, DOWN, buff=0.3)
        right_lbl = Tex("win", color=GREEN, font_size=20
                         ).next_to(right_end, DOWN, buff=0.3)
        self.play(Create(left_end), Create(right_end),
                   Write(left_lbl), Write(right_lbl))

        # Precompute 5 simulations
        rng = np.random.default_rng(42)
        sims = []
        for _ in range(5):
            x = k
            path = [x]
            while 0 < x < N:
                step = 1 if rng.random() < p else -1
                x += step
                path.append(x)
            sims.append(path)

        colors = [YELLOW, ORANGE, BLUE, PURPLE, PINK]

        # Run one simulation at a time, draw the trail
        t_tr = ValueTracker(0.0)
        sim_idx = 0

        # Track wins
        wins = []

        for sim_idx in range(5):
            path = sims[sim_idx]
            color = colors[sim_idx]
            t_tr.set_value(0.0)

            def trail_maker(sim_i):
                def f():
                    s = t_tr.get_value()
                    path_local = sims[sim_i]
                    idx = int(s * (len(path_local) - 1))
                    idx = max(0, min(idx, len(path_local) - 1))
                    pts = [nl.n2p(path_local[j]) + UP * (0.5 + sim_i * 0.15)
                           for j in range(idx + 1)]
                    m = VMobject(color=colors[sim_i], stroke_width=2.5)
                    if len(pts) >= 2:
                        m.set_points_as_corners(pts)
                    return m
                return f

            def dot_maker(sim_i):
                def f():
                    s = t_tr.get_value()
                    path_local = sims[sim_i]
                    idx = int(s * (len(path_local) - 1))
                    idx = max(0, min(idx, len(path_local) - 1))
                    return Dot(nl.n2p(path_local[idx])
                                 + UP * (0.5 + sim_i * 0.15),
                                 color=colors[sim_i], radius=0.09)
                return f

            self.add(always_redraw(trail_maker(sim_idx)),
                      always_redraw(dot_maker(sim_idx)))
            self.play(t_tr.animate.set_value(1.0),
                       run_time=2, rate_func=linear)
            wins.append(int(path[-1] == N))

        # Summary
        empirical_wins = sum(wins)
        theoretical_p = (1 - (q/p)**k) / (1 - (q/p)**N) if p != 0.5 else k / N

        summary = VGroup(
            MathTex(rf"k = {k},\ N = {N},\ p = {p}",
                     color=WHITE, font_size=22),
            MathTex(rf"\text{{empirical wins}} = {empirical_wins}/5",
                     color=YELLOW, font_size=22),
            MathTex(rf"P(\text{{win}}) = {theoretical_p:.3f}",
                     color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        self.play(Write(summary))
        self.wait(0.5)
