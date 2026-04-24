from manim import *
import numpy as np


class ContactTracingGraphExample(Scene):
    """
    Infection propagates through a proximity graph in BFS waves.

    SINGLE_FOCUS:
      18 random people connected by edges if within distance 2.2.
      ValueTracker hop_n steps through 0..5; an always_redraw set
      colors each node by its discovery round (BFS distance from
      seed):
        round 0 = seed (RED)
        round 1 = neighbors (ORANGE)
        round 2 = next-out (YELLOW)
        round 3 = (PURPLE)
        unreached = BLUE
    """

    def construct(self):
        title = Tex(r"Contact tracing: BFS rounds from a seed",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        np.random.seed(11)
        n_people = 18
        positions = []
        for _ in range(n_people):
            positions.append(np.array([np.random.uniform(-5, 5),
                                       np.random.uniform(-2.5, 1.8)]))

        # Build adjacency
        adj = {i: [] for i in range(n_people)}
        edges_pairs = []
        for i in range(n_people):
            for j in range(i + 1, n_people):
                if np.linalg.norm(positions[i] - positions[j]) < 2.2:
                    adj[i].append(j)
                    adj[j].append(i)
                    edges_pairs.append((i, j))

        # BFS from seed=3 to compute round of each node
        seed = 3
        rounds = [-1] * n_people
        rounds[seed] = 0
        frontier = [seed]
        while frontier:
            nxt = []
            for u in frontier:
                for v in adj[u]:
                    if rounds[v] == -1:
                        rounds[v] = rounds[u] + 1
                        nxt.append(v)
            frontier = nxt
        max_round = max(rounds)

        # Render edges
        edges = VGroup(*[
            Line([positions[i][0], positions[i][1], 0],
                 [positions[j][0], positions[j][1], 0],
                 stroke_opacity=0.4, color=GREY_B, stroke_width=1.5)
            for (i, j) in edges_pairs
        ])
        self.play(Create(edges), run_time=1.5)

        round_colors = {0: RED, 1: ORANGE, 2: YELLOW, 3: PURPLE,
                        4: TEAL, 5: GREEN}

        hop_tr = ValueTracker(0)

        def colored_nodes():
            cur = int(round(hop_tr.get_value()))
            grp = VGroup()
            for i in range(n_people):
                r = rounds[i]
                if 0 <= r <= cur:
                    color = round_colors.get(r, BLUE)
                    radius = 0.16 if r == 0 else 0.14
                else:
                    color = BLUE_E
                    radius = 0.10
                grp.add(Dot([positions[i][0], positions[i][1], 0],
                            color=color, radius=radius))
            return grp

        self.add(always_redraw(colored_nodes))

        def info_panel():
            cur = int(round(hop_tr.get_value()))
            visited = sum(1 for r in rounds if 0 <= r <= cur)
            return VGroup(
                MathTex(rf"\text{{hop}} = {cur}", color=YELLOW, font_size=28),
                MathTex(rf"\text{{infected}} = {visited}/{n_people}",
                        color=ORANGE, font_size=24),
                MathTex(rf"R_0 \cdot S = ?",
                        color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UL).shift(DOWN * 0.6 + RIGHT * 0.2)

        self.add(always_redraw(info_panel))

        # Step through BFS rounds
        for r in range(0, max_round + 1):
            self.play(hop_tr.animate.set_value(r),
                      run_time=1.2, rate_func=smooth)
            self.wait(0.3)

        caption = Tex(r"Each new round reveals one BFS layer of contacts",
                      color=YELLOW, font_size=22).to_edge(DOWN, buff=0.4)
        self.play(Write(caption))
        self.wait(1.0)
