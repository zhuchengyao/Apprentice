from manim import *
import numpy as np


class MarkovChainStationaryExample(Scene):
    """
    3-state Markov chain converging to stationary distribution π
    regardless of initial π_0. Chain transition matrix:
        P = [[0.7, 0.2, 0.1],
             [0.3, 0.4, 0.3],
             [0.2, 0.3, 0.5]]

    Stationary π solves π P = π.

    THREE_ROW: top 3-state digraph with animated transition arrows;
    middle bar chart of current distribution driven by ValueTracker
    k_tr; bottom text shows iteration k and live distribution +
    TV-distance to π.
    """

    def construct(self):
        title = Tex(r"Markov chain: $\pi_0 P^k \to \pi$ (stationary)",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        P = np.array([[0.7, 0.2, 0.1],
                      [0.3, 0.4, 0.3],
                      [0.2, 0.3, 0.5]])
        # compute stationary via eigendecomposition
        vals, vecs = np.linalg.eig(P.T)
        idx = np.argmin(abs(vals - 1))
        pi = vecs[:, idx].real
        pi = pi / pi.sum()

        # Precompute evolution from two starts
        starts = [np.array([1.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0])]
        trajs = []
        for s in starts:
            t = [s.copy()]
            d = s.copy()
            for _ in range(30):
                d = d @ P
                t.append(d.copy())
            trajs.append(t)

        # 3-state digraph (top row)
        node_pos = [np.array([-3.0, 1.5, 0]),
                    np.array([0.0, 2.2, 0]),
                    np.array([3.0, 1.5, 0])]
        nodes = VGroup(*[Circle(radius=0.32, color=BLUE,
                                fill_color=BLUE, fill_opacity=0.2).move_to(p)
                         for p in node_pos])
        node_lbls = VGroup(*[Tex(f"$s_{i+1}$", font_size=24).move_to(p)
                              for i, p in enumerate(node_pos)])
        arrows = VGroup()
        for i in range(3):
            for j in range(3):
                if i == j:
                    arc = Arc(radius=0.35, angle=TAU * 0.75,
                              start_angle=PI / 2).move_to(node_pos[i] + UP * 0.6)
                    arc.set_color(GREY_B).set_stroke(width=2)
                    arrows.add(arc)
                else:
                    start = node_pos[i] + 0.32 * (node_pos[j] - node_pos[i])\
                        / np.linalg.norm(node_pos[j] - node_pos[i])
                    end = node_pos[j] - 0.32 * (node_pos[j] - node_pos[i])\
                        / np.linalg.norm(node_pos[j] - node_pos[i])
                    # offset for bidirectional
                    perp = np.cross(node_pos[j] - node_pos[i], np.array([0, 0, 1]))[:3]
                    perp = perp / (np.linalg.norm(perp) + 1e-9) * 0.12
                    arr = Arrow(start + perp, end + perp, color=GREY_B,
                                 buff=0, stroke_width=2)
                    arrows.add(arr)
        self.play(FadeIn(nodes), Write(node_lbls), Create(arrows))

        # Bar chart (middle row)
        bar_origin = np.array([-2.5, -1.0, 0])
        bar_w = 1.5
        bar_h_max = 2.5

        k_tr = ValueTracker(0.0)
        which_tr = ValueTracker(0.0)  # 0 or 1 (start 1 or start 2)

        def current_dist():
            k = int(round(k_tr.get_value()))
            k = max(0, min(30, k))
            idx = int(round(which_tr.get_value()))
            return trajs[idx][k]

        def bars():
            d = current_dist()
            grp = VGroup()
            for i in range(3):
                rect = Rectangle(width=bar_w * 0.85,
                                  height=bar_h_max * d[i],
                                  color=[BLUE, GREEN, RED][i],
                                  fill_color=[BLUE, GREEN, RED][i],
                                  fill_opacity=0.6)
                rect.move_to(bar_origin
                              + RIGHT * (i - 1) * bar_w
                              + UP * bar_h_max * d[i] / 2)
                grp.add(rect)
            return grp

        # Stationary reference bars
        pi_bars = VGroup()
        for i in range(3):
            rect = Rectangle(width=bar_w * 0.85,
                              height=bar_h_max * pi[i],
                              color=YELLOW, stroke_width=2,
                              fill_opacity=0)
            rect.move_to(bar_origin
                          + RIGHT * (i - 1) * bar_w
                          + UP * bar_h_max * pi[i] / 2)
            pi_bars.add(rect)
        self.add(pi_bars)
        self.add(always_redraw(bars))

        bar_lbls = VGroup(*[
            Tex(f"$s_{i+1}$", font_size=20).move_to(bar_origin + RIGHT * (i - 1) * bar_w + DOWN * 0.3)
            for i in range(3)
        ])
        self.add(bar_lbls)

        # Bottom info
        info = VGroup(
            VGroup(Tex(r"$k=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"TV$(\pi_k, \pi)=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$\pi^*\approx (0.478, 0.261, 0.261)$",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2).shift(DOWN * 1.0)

        info[0][1].add_updater(lambda m: m.set_value(int(round(k_tr.get_value()))))
        info[1][1].add_updater(lambda m: m.set_value(
            0.5 * float(np.sum(np.abs(current_dist() - pi)))))
        self.add(info)

        # Animate from start 1
        self.play(k_tr.animate.set_value(30.0),
                  run_time=5, rate_func=linear)
        self.wait(0.5)

        # Restart from start 2
        self.play(which_tr.animate.set_value(1.0),
                  k_tr.animate.set_value(0.0), run_time=0.8)
        self.wait(0.3)
        self.play(k_tr.animate.set_value(30.0),
                  run_time=5, rate_func=linear)
        self.wait(0.8)
