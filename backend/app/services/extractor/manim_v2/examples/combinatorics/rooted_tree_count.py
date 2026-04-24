from manim import *
import numpy as np


class RootedTreeCountExample(Scene):
    """
    Cayley's formula: number of labeled trees on n vertices is n^(n-2).
    For n=4: 16 labeled trees. For unrooted → rooted: multiply by n.

    SINGLE_FOCUS: enumerate all 16 labeled trees on {1, 2, 3, 4}.
    ValueTracker tree_idx_tr cycles through.
    """

    def construct(self):
        title = Tex(r"Cayley's formula: $n^{n-2}=4^2=16$ labeled trees on 4 vertices",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Generate all 16 labeled trees on vertices {0, 1, 2, 3}
        # via Prüfer sequences (length n-2 = 2)
        def prufer_to_tree(seq, n):
            # seq of length n-2 on vertices 0..n-1
            degree = [1] * n
            for s in seq:
                degree[s] += 1
            edges = []
            for v in seq:
                for u in range(n):
                    if degree[u] == 1:
                        edges.append((u, v))
                        degree[u] -= 1
                        degree[v] -= 1
                        break
            u, v = [i for i in range(n) if degree[i] == 1]
            edges.append((u, v))
            return edges

        n = 4
        trees = []
        for a in range(n):
            for b in range(n):
                trees.append(prufer_to_tree([a, b], n))

        # Layout: positions of 4 vertices
        vertex_pos = [
            np.array([-1, 1, 0]),
            np.array([1, 1, 0]),
            np.array([-1, -1, 0]),
            np.array([1, -1, 0]),
        ]
        colors = [BLUE, GREEN, ORANGE, RED]

        idx_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(len(trees) - 1, int(round(idx_tr.get_value()))))

        def tree_display():
            edges = trees[k_now()]
            grp = VGroup()
            for (u, v) in edges:
                grp.add(Line(vertex_pos[u], vertex_pos[v],
                              color=YELLOW, stroke_width=3))
            for i, pos in enumerate(vertex_pos):
                grp.add(Dot(pos, color=colors[i], radius=0.18))
                grp.add(Tex(str(i + 1), font_size=22, color=WHITE).move_to(pos))
            return grp

        self.add(always_redraw(tree_display))

        info = VGroup(
            VGroup(Tex(r"tree $\#$", font_size=24),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=24).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"Cayley: $n^{n-2}$ labeled trees",
                color=YELLOW, font_size=22),
            Tex(r"$4^2=16$",
                color=GREEN, font_size=26),
            Tex(r"(Prüfer encoding bijection)",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(k_now() + 1))
        self.add(info)

        self.play(idx_tr.animate.set_value(float(len(trees) - 1)),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
