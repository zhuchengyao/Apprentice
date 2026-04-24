from manim import *
import numpy as np


class GraphColoringExample(Scene):
    """
    Graph coloring: assign colors to vertices so no edge connects
    same color. Chromatic number χ(G). Show 4-color on a planar
    graph.

    SINGLE_FOCUS:
      Planar graph with 7 vertices, ~12 edges. ValueTracker
      step_tr assigns colors greedily (one vertex per step) using
      the first available color; always_redraw colored nodes.
    """

    def construct(self):
        title = Tex(r"Graph coloring: $\chi(G)$ = minimum colors",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 7-vertex planar graph with chromatic number 3
        n = 7
        positions = [
            np.array([-3, 1, 0]),
            np.array([-1, 2, 0]),
            np.array([1.5, 2, 0]),
            np.array([3, 0, 0]),
            np.array([1.5, -2, 0]),
            np.array([-1, -2, 0]),
            np.array([0, 0, 0]),  # center
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (4, 5), (5, 0), (6, 0), (6, 1),
            (6, 2), (6, 3), (6, 4), (6, 5),
        ]

        # Edges
        edge_group = VGroup()
        for (i, j) in edges:
            edge_group.add(Line(positions[i], positions[j],
                                  color=WHITE, stroke_width=2))
        self.play(Create(edge_group))

        # Compute greedy coloring (by vertex order)
        adj = [set() for _ in range(n)]
        for (i, j) in edges:
            adj[i].add(j)
            adj[j].add(i)
        colors_assigned = [-1] * n
        palette = [BLUE, YELLOW, GREEN, RED]
        for v in range(n):
            used = set(colors_assigned[u] for u in adj[v] if colors_assigned[u] != -1)
            for c in range(4):
                if c not in used:
                    colors_assigned[v] = c
                    break

        step_tr = ValueTracker(0)

        def node_dots():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, n))
            grp = VGroup()
            for v in range(n):
                if v < s:
                    col = palette[colors_assigned[v]]
                    fill_op = 0.8
                else:
                    col = GREY_B
                    fill_op = 0.25
                d = Circle(radius=0.3, color=col,
                             fill_opacity=fill_op, stroke_width=2
                             ).move_to(positions[v])
                grp.add(d)
                lbl = MathTex(rf"{v}", font_size=16,
                                color=BLACK if v < s else WHITE
                                ).move_to(positions[v])
                grp.add(lbl)
            return grp

        self.add(always_redraw(node_dots))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, n))
            used_colors = set(colors_assigned[v] for v in range(s)
                                if colors_assigned[v] != -1)
            chi = len(used_colors) if s > 0 else 0
            return VGroup(
                MathTex(rf"\text{{step}} = {s}/{n}",
                         color=WHITE, font_size=22),
                MathTex(rf"\text{{colors used}} = {chi}",
                         color=YELLOW, font_size=22),
                MathTex(r"\chi(G) = 3", color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for s in range(1, n + 1):
            self.play(step_tr.animate.set_value(s),
                       run_time=0.8, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
