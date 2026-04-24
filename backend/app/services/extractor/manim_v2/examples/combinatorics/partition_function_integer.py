from manim import *
import numpy as np


class PartitionFunctionIntegerExample(Scene):
    """
    Partition function p(n) counts ways to write n as sum of positive
    integers, order irrelevant. p(1) = 1, p(2) = 2, ..., p(10) = 42.

    SINGLE_FOCUS:
      ValueTracker n_tr steps n = 1..10; always_redraw shows all
      partitions as Ferrers diagrams for current n.
    """

    def construct(self):
        title = Tex(r"Integer partitions $p(n)$: $p(10) = 42$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def partitions(n):
            """Return list of partitions as tuples in non-increasing order."""
            results = []

            def helper(remaining, max_part, current):
                if remaining == 0:
                    results.append(tuple(current))
                    return
                for k in range(min(remaining, max_part), 0, -1):
                    helper(remaining - k, k, current + [k])
            helper(n, n, [])
            return results

        n_tr = ValueTracker(1)

        def ferrers_grid():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 7))  # Cap at 7 for display space
            parts = partitions(n)
            grp = VGroup()
            cell = 0.22
            max_cols = 6
            total = len(parts)
            for idx, part in enumerate(parts):
                col = idx % max_cols
                row = idx // max_cols
                # Origin for this partition
                ox = -5 + col * 2.0
                oy = 2.2 - row * 1.4
                # Draw dots for each row of partition (size cell each)
                for r, row_size in enumerate(part):
                    for c in range(row_size):
                        d = Dot([ox + c * cell, oy - r * cell, 0],
                                  color=YELLOW, radius=0.06)
                        grp.add(d)
            return grp

        self.add(always_redraw(ferrers_grid))

        # Precomputed p(n) values
        p_vals = {1: 1, 2: 2, 3: 3, 4: 5, 5: 7, 6: 11, 7: 15,
                  8: 22, 9: 30, 10: 42}

        def info():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 7))
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=26),
                MathTex(rf"p({n}) = {p_vals[n]}", color=GREEN, font_size=26),
                MathTex(r"\prod_{k \ge 1} \tfrac{1}{1 - x^k} = \sum_n p(n) x^n",
                         color=WHITE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for nv in range(2, 8):
            self.play(n_tr.animate.set_value(nv),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
