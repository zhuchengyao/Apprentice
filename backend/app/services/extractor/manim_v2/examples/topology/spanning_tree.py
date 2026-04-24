from manim import *
import numpy as np


class SpanningTreeExample(Scene):
    """
    Spanning tree of a connected graph: a subset of n-1 edges on
    n vertices that keeps it connected without cycles. Kruskal's
    algorithm demonstration.

    SINGLE_FOCUS:
      Connected weighted graph on 7 vertices. ValueTracker step_tr
      reveals Kruskal's algorithm: sort edges by weight, add them
      greedily unless they form a cycle. always_redraw highlights
      tree edges GREEN, rejected edges grey, non-scanned edges BLUE.
    """

    def construct(self):
        title = Tex(r"Spanning tree via Kruskal's algorithm",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 7 vertices around a circle
        n = 7
        R = 2.5
        center = np.array([-1.5, -0.3, 0])
        positions = [center + R * np.array([np.cos(2 * PI * k / n + PI / 2),
                                               np.sin(2 * PI * k / n + PI / 2), 0])
                     for k in range(n)]

        # Edges with weights (weight, i, j)
        edges = [
            (2, 0, 1), (4, 1, 2), (3, 2, 3),
            (5, 3, 4), (6, 4, 5), (2, 5, 6), (3, 6, 0),
            (9, 0, 2), (7, 1, 3), (8, 2, 4), (11, 3, 5),
            (10, 4, 6), (12, 5, 0), (13, 1, 5),
        ]
        edges.sort()  # by weight ascending

        # Union-find for Kruskal
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False
            parent[px] = py
            return True

        # Precompute status at each step
        #   status[i] = 'tree' | 'rejected' | 'unscanned'
        uf_parent_snapshots = []
        statuses = []
        for step in range(len(edges) + 1):
            # reset
            parent = list(range(n))
            status = {i: "unscanned" for i in range(len(edges))}
            for k in range(step):
                w, a, b = edges[k]
                if find(a) != find(b):
                    union(a, b)
                    status[k] = "tree"
                else:
                    status[k] = "rejected"
            statuses.append(status)

        # Vertex dots
        dots = VGroup()
        for i, p in enumerate(positions):
            c = Dot(p, color=YELLOW, radius=0.14)
            lbl = MathTex(str(i), font_size=22,
                           color=BLACK).move_to(p)
            dots.add(c, lbl)
        self.play(FadeIn(dots))

        step_tr = ValueTracker(0)

        def edge_grp():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(edges)))
            status = statuses[s]
            grp = VGroup()
            for k, (w, a, b) in enumerate(edges):
                st = status[k]
                if st == "tree":
                    color = GREEN
                    width = 5
                elif st == "rejected":
                    color = GREY_B
                    width = 1
                else:
                    color = BLUE
                    width = 2
                ln = Line(positions[a], positions[b],
                           color=color, stroke_width=width,
                           stroke_opacity=0.5 if st == "rejected" else 1.0)
                grp.add(ln)
                mid = (positions[a] + positions[b]) / 2
                w_lbl = MathTex(str(w), font_size=18,
                                 color=WHITE).move_to(mid)
                grp.add(w_lbl)
            return grp

        self.add(always_redraw(edge_grp))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(edges)))
            status = statuses[s]
            tree_count = sum(1 for v in status.values() if v == "tree")
            rej = sum(1 for v in status.values() if v == "rejected")
            return VGroup(
                MathTex(rf"\text{{step}} = {s} / {len(edges)}",
                         color=WHITE, font_size=22),
                MathTex(rf"\text{{tree edges}} = {tree_count}",
                         color=GREEN, font_size=22),
                MathTex(rf"\text{{rejected}} = {rej}", color=GREY_B, font_size=22),
                MathTex(rf"\text{{need }} n-1 = {n-1}",
                         color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        for s in range(1, len(edges) + 1):
            self.play(step_tr.animate.set_value(s),
                       run_time=0.55, rate_func=smooth)
        self.wait(0.5)
