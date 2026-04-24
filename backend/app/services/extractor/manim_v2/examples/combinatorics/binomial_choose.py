from manim import *
import numpy as np
from math import comb


class BinomialChooseExample(Scene):
    """
    C(n, k) = n! / (k!(n-k)!) via the "choose k from n" subset picture.

    TWO_COLUMN:
      LEFT  — row of n = 8 circles; ValueTracker k_tr selects which
              k to highlight YELLOW; a systematic sweep picks each
              k-subset in lex order. Progress bar marks the total
              count.
      RIGHT — live n, k, C(n, k), and partial-count out of the
              total (matching Pascal's identity).
    """

    def construct(self):
        title = Tex(r"Binomial $\binom{n}{k}$: count of $k$-subsets of an $n$-set",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 8
        elem_positions = [np.array([-4.5 + i * 1.0, 1.2, 0]) for i in range(n)]
        elements = VGroup()
        for i, p in enumerate(elem_positions):
            c = Circle(radius=0.28, color=WHITE, fill_opacity=0.15,
                        stroke_width=2).move_to(p)
            lbl = MathTex(str(i + 1), font_size=22).move_to(p)
            elements.add(VGroup(c, lbl))
        self.play(FadeIn(elements))

        # subset progress bar
        bar_bg = Rectangle(width=9.0, height=0.3, color=WHITE, stroke_width=2
                            ).move_to([-0.8, -1.5, 0])
        bar_fill = Rectangle(width=0.01, height=0.3, color=GREEN,
                              fill_opacity=0.7, stroke_width=0
                              ).move_to([-0.8 - 4.5, -1.5, 0])

        self.play(Create(bar_bg), FadeIn(bar_fill))

        k = 3
        from itertools import combinations
        subsets = list(combinations(range(n), k))
        total = len(subsets)
        assert total == comb(n, k)

        def highlight_subset(indices):
            grp = VGroup()
            for i in range(n):
                c = Circle(radius=0.28,
                            color=YELLOW if i in indices else WHITE,
                            fill_opacity=0.7 if i in indices else 0.1,
                            stroke_width=2).move_to(elem_positions[i])
                lbl = MathTex(str(i + 1),
                               color=BLACK if i in indices else WHITE,
                               font_size=22).move_to(elem_positions[i])
                grp.add(VGroup(c, lbl))
            return grp

        current = highlight_subset(subsets[0])
        self.play(Transform(elements, current))

        def info_panel(idx, k_val):
            return VGroup(
                MathTex(rf"n = {n}", color=WHITE, font_size=24),
                MathTex(rf"k = {k_val}", color=YELLOW, font_size=24),
                MathTex(rf"\binom{{{n}}}{{{k_val}}} = {comb(n, k_val)}",
                         color=GREEN, font_size=28),
                MathTex(rf"\text{{shown}}: {idx + 1} / {total}",
                         color=BLUE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        info = info_panel(0, k)
        self.play(Write(info))

        for idx, sub in enumerate(subsets):
            new_grp = highlight_subset(sub)
            new_info = info_panel(idx, k)
            # grow fill bar
            frac = (idx + 1) / total
            new_bar = Rectangle(width=9.0 * frac, height=0.3,
                                 color=GREEN, fill_opacity=0.7,
                                 stroke_width=0
                                 ).move_to([-0.8 - 4.5 + 9.0 * frac / 2, -1.5, 0])
            self.play(Transform(elements, new_grp),
                       Transform(info, new_info),
                       Transform(bar_fill, new_bar),
                       run_time=0.2)
        self.wait(0.6)
