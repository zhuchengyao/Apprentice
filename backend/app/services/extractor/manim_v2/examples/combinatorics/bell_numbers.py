from manim import *
import numpy as np


def bell(n):
    if n == 0:
        return 1
    row = [1]
    for i in range(1, n + 1):
        new_row = [row[-1]]
        for j in range(len(row)):
            new_row.append(new_row[-1] + row[j])
        row = new_row
    return row[0]


def partitions_of(lst):
    if len(lst) <= 1:
        yield [lst]
        return
    first = lst[0]
    rest = lst[1:]
    for smaller in partitions_of(rest):
        for i, subset in enumerate(smaller):
            yield smaller[:i] + [[first] + subset] + smaller[i+1:]
        yield [[first]] + smaller


class BellNumbersExample(Scene):
    """
    B_n = number of set partitions of an n-element set. Grows fast:
    B_1..B_6 = 1, 2, 5, 15, 52, 203.

    SINGLE_FOCUS:
      ValueTracker n_tr steps through n = 1..5. For each n:
      Transform to a grid showing ALL partitions of {1..n}, each as
      a row of colored boxes grouping elements. Live count B_n.
    """

    def construct(self):
        title = Tex(r"Bell numbers $B_n$: partitions of $\{1, \dots, n\}$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        COLORS = [BLUE, ORANGE, GREEN, RED, PURPLE, YELLOW, TEAL]

        def partition_row(part, row_y, x_start=-5.5):
            """Render one partition as a row of colored small boxes."""
            grp = VGroup()
            x = x_start
            for k, block in enumerate(part):
                for elem in block:
                    box = Square(side_length=0.32,
                                  color=COLORS[k % len(COLORS)],
                                  fill_opacity=0.55, stroke_width=1)
                    box.move_to([x, row_y, 0])
                    lbl = MathTex(str(elem), font_size=16, color=BLACK)
                    lbl.move_to(box.get_center())
                    grp.add(box, lbl)
                    x += 0.34
                x += 0.15
            return grp

        def partitions_grid(n):
            parts = list(partitions_of(list(range(1, n + 1))))
            parts.sort(key=lambda p: (len(p), [len(b) for b in p]))
            # Layout on a grid
            max_cols = 3
            grp = VGroup()
            for i, part in enumerate(parts):
                col = i % max_cols
                row = i // max_cols
                y = 1.6 - row * 0.55
                x_start = -5.5 + col * 3.5
                grp.add(partition_row(part, y, x_start))
            return grp, len(parts)

        # Start with n = 1
        current = partitions_grid(1)[0]
        count_lbl = MathTex(rf"n = 1, \quad B_1 = 1",
                             color=YELLOW, font_size=30).to_edge(DOWN, buff=0.6)
        self.play(Create(current), Write(count_lbl))
        self.wait(0.6)

        for n in range(2, 6):
            new_grp, cnt = partitions_grid(n)
            new_count = MathTex(rf"n = {n}, \quad B_{{{n}}} = {cnt}",
                                 color=YELLOW, font_size=30
                                 ).to_edge(DOWN, buff=0.6)
            self.play(Transform(current, new_grp),
                       Transform(count_lbl, new_count),
                       run_time=1.5)
            self.wait(0.6)

        # Recurrence formula
        formula = MathTex(r"B_{n+1} = \sum_{k=0}^{n} \binom{n}{k} B_k",
                           color=GREEN, font_size=26).to_edge(UP, buff=1.0)
        self.play(Write(formula))
        self.wait(0.6)
