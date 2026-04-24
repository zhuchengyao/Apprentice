from manim import *
import numpy as np


class MarkovChainMixingExample(Scene):
    """
    Markov chain mixing: start from any initial distribution, iterate
    the transition matrix; converge to stationary distribution.

    TWO_COLUMN:
      LEFT  — 3-state transition graph (nodes A, B, C with weighted
              arrows); ValueTracker step_tr advances time.
      RIGHT — bar chart of current distribution p_n = p_0 P^n.
    """

    def construct(self):
        title = Tex(r"Markov chain mixing: $p_n \to \pi$ stationary",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 3×3 transition matrix (rows sum to 1)
        P = np.array([
            [0.5, 0.3, 0.2],
            [0.2, 0.6, 0.2],
            [0.1, 0.3, 0.6],
        ])

        # Stationary: solve πP = π, sum=1
        eig_vals, eig_vecs = np.linalg.eig(P.T)
        idx = np.argmin(abs(eig_vals - 1))
        stat = np.real(eig_vecs[:, idx])
        stat = stat / stat.sum()

        # LEFT: 3-node graph
        positions = {
            "A": np.array([-4, 1.5, 0]),
            "B": np.array([-2.5, -1.5, 0]),
            "C": np.array([-0.5, 1.5, 0]),
        }
        colors = {"A": BLUE, "B": GREEN, "C": ORANGE}

        node_group = VGroup()
        for name, pos in positions.items():
            c = Circle(radius=0.4, color=colors[name],
                         fill_opacity=0.3, stroke_width=2
                         ).move_to(pos)
            lbl = Tex(name, color=colors[name],
                       font_size=24).move_to(pos)
            node_group.add(c, lbl)
        self.play(FadeIn(node_group))

        # Edge arrows with weights
        state_names = ["A", "B", "C"]
        for i, src in enumerate(state_names):
            for j, dst in enumerate(state_names):
                if i == j:
                    continue
                start = positions[src]
                end = positions[dst]
                # Offset slightly for clarity
                direction = (end - start) / np.linalg.norm(end - start)
                start_adj = start + 0.4 * direction
                end_adj = end - 0.4 * direction
                arrow = Arrow(start_adj, end_adj,
                                color=GREY_B, buff=0, stroke_width=2,
                                max_tip_length_to_length_ratio=0.1)
                self.add(arrow)
                mid = (start_adj + end_adj) / 2
                lbl = MathTex(rf"{P[i, j]:.1f}", font_size=14,
                                color=WHITE).move_to(mid)
                self.add(lbl)

        # Initial distribution: all mass at A
        step_tr = ValueTracker(0)
        p0 = np.array([1.0, 0.0, 0.0])

        def current_dist():
            n = int(round(step_tr.get_value()))
            n = max(0, min(n, 30))
            return p0 @ np.linalg.matrix_power(P, n)

        # RIGHT: bar chart
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 1, 0.25],
                   x_length=4, y_length=3, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([3.5, 0.5, 0])
        self.play(Create(ax))

        # Stationary reference line
        for k, sv in enumerate(stat):
            x = k + 0.5
            ref = DashedLine(ax.c2p(x - 0.25, sv), ax.c2p(x + 0.25, sv),
                               color=YELLOW, stroke_width=2)
            self.add(ref)

        def bars():
            p = current_dist()
            grp = VGroup()
            for k, pk in enumerate(p):
                h_scene = ax.c2p(0, pk)[1] - ax.c2p(0, 0)[1]
                bar = Rectangle(width=0.4, height=max(h_scene, 0.005),
                                 color=colors[state_names[k]],
                                 fill_opacity=0.75,
                                 stroke_width=1)
                bar.move_to([ax.c2p(k + 0.5, 0)[0],
                             ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        self.add(always_redraw(bars))

        def info():
            n = int(round(step_tr.get_value()))
            p = current_dist()
            return VGroup(
                MathTex(rf"n = {n}", color=WHITE, font_size=22),
                MathTex(rf"p_n^{{(A)}} = {p[0]:.4f}",
                         color=BLUE, font_size=18),
                MathTex(rf"p_n^{{(B)}} = {p[1]:.4f}",
                         color=GREEN, font_size=18),
                MathTex(rf"p_n^{{(C)}} = {p[2]:.4f}",
                         color=ORANGE, font_size=18),
                MathTex(r"\pi: " + f"({stat[0]:.3f}, {stat[1]:.3f}, {stat[2]:.3f})",
                         color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.13).move_to([3.5, -2.3, 0])

        self.add(always_redraw(info))

        for n in [1, 2, 3, 5, 10, 20, 30]:
            self.play(step_tr.animate.set_value(n),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
