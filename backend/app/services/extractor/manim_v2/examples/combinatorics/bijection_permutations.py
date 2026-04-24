from manim import *
import numpy as np


class BijectionPermutationsExample(Scene):
    """
    Every permutation of {1, ..., n} is a bijection. Visualize as
    bipartite graph mapping top row → bottom row. Animate composition
    of two permutations σ and τ showing that composition is also a
    permutation.

    SINGLE_FOCUS: n=5. Top row 1..5 (BLUE), bottom 1..5 (BLUE).
    σ = (1 3 4)(2 5) → (3, 5, 4, 1, 2). τ = (1 2)(3 4 5) → (2, 1, 4, 5, 3).
    Show σ, τ separately then composition τ∘σ.
    """

    def construct(self):
        title = Tex(r"Permutation composition: $\tau\circ \sigma$ is also a bijection",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 5
        # σ in 1-indexed
        sigma = [3, 5, 4, 1, 2]  # σ(i) = sigma[i-1]
        tau = [2, 1, 4, 5, 3]
        comp = [tau[sigma[i] - 1] for i in range(n)]  # (τσ)(i) = τ(σ(i))

        # Layout: 3 rows — top, middle (after σ), bottom (after τ)
        top_y = 2.0
        mid_y = 0.0
        bot_y = -2.0

        spacing = 1.4
        def x_pos(i):
            return (i - (n + 1) / 2) * spacing

        # Draw dots
        top_dots = VGroup(*[Dot(np.array([x_pos(i), top_y, 0]), color=BLUE, radius=0.15)
                             for i in range(1, n + 1)])
        mid_dots = VGroup(*[Dot(np.array([x_pos(i), mid_y, 0]), color=GREEN, radius=0.15)
                             for i in range(1, n + 1)])
        bot_dots = VGroup(*[Dot(np.array([x_pos(i), bot_y, 0]), color=ORANGE, radius=0.15)
                             for i in range(1, n + 1)])
        # labels
        for i in range(1, n + 1):
            self.add(Tex(str(i), font_size=22, color=BLUE).move_to(
                np.array([x_pos(i), top_y + 0.4, 0])))
            self.add(Tex(str(i), font_size=22, color=GREEN).move_to(
                np.array([x_pos(i), mid_y + 0.4, 0])))
            self.add(Tex(str(i), font_size=22, color=ORANGE).move_to(
                np.array([x_pos(i), bot_y - 0.4, 0])))
        self.add(top_dots, mid_dots, bot_dots)

        self.add(Tex(r"$\sigma$", color=GREEN, font_size=28).move_to(np.array([-4.5, top_y / 2 + mid_y / 2, 0])))
        self.add(Tex(r"$\tau$", color=ORANGE, font_size=28).move_to(np.array([-4.5, mid_y / 2 + bot_y / 2, 0])))

        t_tr = ValueTracker(0.0)

        # Phase 1 (t∈[0, 1]): draw σ arrows
        # Phase 2 (t∈[1, 2]): draw τ arrows
        # Phase 3 (t∈[2, 3]): draw composition arrows direct top→bottom

        def sigma_arrows():
            t = t_tr.get_value()
            if t < 0.01:
                return VGroup()
            alpha = min(1.0, t)
            grp = VGroup()
            for i in range(1, n + 1):
                start = np.array([x_pos(i), top_y - 0.2, 0])
                end = np.array([x_pos(sigma[i - 1]), mid_y + 0.2, 0])
                partial_end = start + alpha * (end - start)
                grp.add(Arrow(start, partial_end, color=GREEN,
                               buff=0, stroke_width=2,
                               max_tip_length_to_length_ratio=0.15))
            return grp

        def tau_arrows():
            t = t_tr.get_value()
            if t < 1.0:
                return VGroup()
            alpha = min(1.0, t - 1.0)
            grp = VGroup()
            for i in range(1, n + 1):
                start = np.array([x_pos(i), mid_y - 0.2, 0])
                end = np.array([x_pos(tau[i - 1]), bot_y + 0.2, 0])
                partial_end = start + alpha * (end - start)
                grp.add(Arrow(start, partial_end, color=ORANGE,
                               buff=0, stroke_width=2,
                               max_tip_length_to_length_ratio=0.15))
            return grp

        def comp_arrows():
            t = t_tr.get_value()
            if t < 2.0:
                return VGroup()
            alpha = min(1.0, t - 2.0)
            grp = VGroup()
            for i in range(1, n + 1):
                start = np.array([x_pos(i), top_y - 0.25, 0])
                end = np.array([x_pos(comp[i - 1]), bot_y + 0.25, 0])
                partial_end = start + alpha * (end - start)
                grp.add(Arrow(start, partial_end, color=RED,
                               buff=0, stroke_width=2.5,
                               max_tip_length_to_length_ratio=0.1))
            return grp

        self.add(always_redraw(sigma_arrows),
                 always_redraw(tau_arrows),
                 always_redraw(comp_arrows))

        info = VGroup(
            Tex(rf"$\sigma=({sigma[0]},{sigma[1]},{sigma[2]},{sigma[3]},{sigma[4]})$",
                color=GREEN, font_size=22),
            Tex(rf"$\tau=({tau[0]},{tau[1]},{tau[2]},{tau[3]},{tau[4]})$",
                color=ORANGE, font_size=22),
            Tex(rf"$\tau\circ\sigma=({comp[0]},{comp[1]},{comp[2]},{comp[3]},{comp[4]})$",
                color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.3)
        self.add(info)

        for target in [1.0, 2.0, 3.0]:
            self.play(t_tr.animate.set_value(target),
                      run_time=2.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
