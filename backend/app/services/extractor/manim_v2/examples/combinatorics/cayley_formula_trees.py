from manim import *
import numpy as np


class CayleyFormulaTreesExample(Scene):
    """
    Cayley's formula: the number of labeled trees on n vertices is
    n^(n-2). Show all 3 labeled trees on 3 vertices (n^(n-2) = 3^1 = 3)
    and all 16 labeled trees on 4 vertices (4² = 16) — first 8 drawn.

    SINGLE_FOCUS:
      ValueTracker n_tr toggles between n=3 (all 3 trees) and n=4
      (first 8 of 16 trees). always_redraw tree layout.
    """

    def construct(self):
        title = Tex(r"Cayley: labeled trees on $n$ vertices $= n^{n-2}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def draw_tree(edges, vertices, origin, scale=0.5, n=3):
            grp = VGroup()
            # Vertex positions on a small circle
            pos = {}
            for i in range(n):
                angle = 2 * PI * i / n + PI / 2
                pos[i] = origin + scale * np.array([np.cos(angle),
                                                       np.sin(angle), 0])
            # Edges
            for (u, v) in edges:
                grp.add(Line(pos[u], pos[v],
                               color=BLUE, stroke_width=2))
            # Dots + labels
            for i in range(n):
                grp.add(Dot(pos[i], color=YELLOW, radius=0.08))
                grp.add(MathTex(f"{i + 1}", font_size=14,
                                  color=BLACK).move_to(pos[i]))
            return grp

        # All 3 labeled trees on 3 vertices (star shapes)
        trees_3 = [
            [(0, 1), (0, 2)],   # path 2-1-3 (1 is center)
            [(0, 1), (1, 2)],   # path 1-2-3
            [(0, 2), (2, 1)],   # path 1-3-2
        ]
        # We want 3 labeled trees on 3 vertices total (=3^1)

        # First 8 labeled trees on 4 vertices (stars + paths, etc.)
        trees_4 = [
            [(0, 1), (0, 2), (0, 3)],  # star centered at 0
            [(1, 0), (1, 2), (1, 3)],  # star centered at 1
            [(2, 0), (2, 1), (2, 3)],  # star centered at 2
            [(3, 0), (3, 1), (3, 2)],  # star centered at 3
            [(0, 1), (1, 2), (2, 3)],  # path 1-2-3-4
            [(0, 1), (1, 3), (3, 2)],  # path 1-2-4-3
            [(0, 2), (2, 1), (1, 3)],  # path 1-3-2-4
            [(0, 2), (2, 3), (3, 1)],  # path 1-3-4-2
        ]

        n_tr = ValueTracker(3)

        def all_trees():
            n = int(round(n_tr.get_value()))
            if n == 3:
                trees = trees_3
                cols = 3
            else:
                trees = trees_4
                cols = 4
            grp = VGroup()
            for i, edges in enumerate(trees):
                col = i % cols
                row = i // cols
                ox = -4.5 + col * 2.5
                oy = 2.0 - row * 2.0
                grp.add(draw_tree(edges, n, np.array([ox, oy, 0]),
                                    scale=0.7, n=n))
            return grp

        self.add(always_redraw(all_trees))

        def info():
            n = int(round(n_tr.get_value()))
            count = n ** (n - 2)
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=24),
                MathTex(rf"n^{{n-2}} = {count}",
                         color=GREEN, font_size=24),
                Tex(rf"all {count} labeled trees" if n == 3 else rf"first 8 of {count}",
                     color=BLUE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.wait(1.0)
        self.play(n_tr.animate.set_value(4), run_time=1.5)
        self.wait(1.5)
        self.play(n_tr.animate.set_value(3), run_time=1.2)
        self.wait(0.5)
