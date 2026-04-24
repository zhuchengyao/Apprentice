from manim import *
import numpy as np


class DynamicProgrammingPathExample(Scene):
    """
    Shortest path in a grid via dynamic programming
    (adapted from _2020/18S191/dynamic_prog).

    SINGLE_FOCUS:
      8×6 grid with random costs; DP table fills cell by cell as
      ValueTracker step_tr advances; always_redraw displays filled
      cells with minimum-cost-to-start values. Second phase: trace
      optimal path from top-right to bottom-left.
    """

    def construct(self):
        title = Tex(r"Grid DP: $f(i, j) = c_{ij} + \min(f(i-1, j), f(i, j-1))$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rows, cols = 5, 8
        rng = np.random.default_rng(7)
        costs = rng.integers(1, 10, (rows, cols))

        # DP table
        dp = np.zeros((rows, cols), dtype=int)
        dp[0, 0] = int(costs[0, 0])
        for c in range(1, cols):
            dp[0, c] = dp[0, c - 1] + int(costs[0, c])
        for r in range(1, rows):
            dp[r, 0] = dp[r - 1, 0] + int(costs[r, 0])
        for r in range(1, rows):
            for c in range(1, cols):
                dp[r, c] = int(costs[r, c]) + min(dp[r - 1, c], dp[r, c - 1])

        cell_size = 0.85
        origin = np.array([-cell_size * (cols - 1) / 2,
                             cell_size * (rows - 1) / 2 - 0.5, 0])

        def cell_center(r, c):
            return origin + np.array([c * cell_size,
                                         -r * cell_size, 0])

        # Draw grid + cost labels
        grid_group = VGroup()
        for r in range(rows):
            for c in range(cols):
                rect = Square(side_length=cell_size * 0.95,
                                color=WHITE, stroke_width=1.5,
                                fill_opacity=0.1)
                rect.move_to(cell_center(r, c))
                lbl = MathTex(str(int(costs[r, c])), font_size=18,
                                color=GREY_B)
                lbl.move_to(cell_center(r, c) + np.array([0, -0.2, 0]))
                grid_group.add(rect, lbl)
        self.play(FadeIn(grid_group), run_time=1.5)

        # Visiting order (row-major)
        order = [(r, c) for r in range(rows) for c in range(cols)]
        step_tr = ValueTracker(0)

        def filled():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(order)))
            grp = VGroup()
            for (r, c) in order[:s]:
                # Highlight cell yellow and show dp value
                rect = Square(side_length=cell_size * 0.95,
                                color=YELLOW,
                                fill_opacity=0.35, stroke_width=1.5)
                rect.move_to(cell_center(r, c))
                grp.add(rect)
                lbl = MathTex(rf"{dp[r, c]}", color=BLACK,
                                font_size=22)
                lbl.move_to(cell_center(r, c) + np.array([0, 0.15, 0]))
                grp.add(lbl)
            return grp

        self.add(always_redraw(filled))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(order)))
            return VGroup(
                MathTex(rf"\text{{cells filled}}: {s} / {rows * cols}",
                         color=YELLOW, font_size=22),
                MathTex(rf"f({rows - 1}, {cols - 1}) = {dp[rows - 1, cols - 1]}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.5)

        self.add(always_redraw(info))

        self.play(step_tr.animate.set_value(len(order)),
                   run_time=6, rate_func=linear)
        self.wait(0.4)

        # Phase 2: traceback optimal path
        path = []
        r, c = rows - 1, cols - 1
        while (r, c) != (0, 0):
            path.append((r, c))
            if r == 0:
                c -= 1
            elif c == 0:
                r -= 1
            elif dp[r - 1, c] < dp[r, c - 1]:
                r -= 1
            else:
                c -= 1
        path.append((0, 0))
        path.reverse()

        path_tr = ValueTracker(0)

        def path_highlight():
            k = int(round(path_tr.get_value()))
            k = max(0, min(k, len(path)))
            grp = VGroup()
            for i in range(k):
                r, c = path[i]
                d = Dot(cell_center(r, c), color=RED, radius=0.15)
                grp.add(d)
            for i in range(1, k):
                r_a, c_a = path[i - 1]
                r_b, c_b = path[i]
                grp.add(Line(cell_center(r_a, c_a),
                               cell_center(r_b, c_b),
                               color=RED, stroke_width=3))
            return grp

        self.add(always_redraw(path_highlight))

        trace_note = Tex(r"traceback: follow the minimum predecessor",
                          color=RED, font_size=22).next_to(title, DOWN, buff=0.3)
        self.play(Write(trace_note))

        self.play(path_tr.animate.set_value(len(path)),
                   run_time=3, rate_func=linear)
        self.wait(0.4)
