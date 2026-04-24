from manim import *
import numpy as np
from itertools import combinations


class ErdosKoRadoExample(Scene):
    """
    Erdős–Ko–Rado: for n ≥ 2k, the largest intersecting family of
    k-subsets of [n] has size C(n−1, k−1); achieved by the star
    family (all k-subsets containing a fixed element).

    Concrete case n=6, k=3 → max |F| = C(5, 2) = 10.
    All C(6, 3) = 20 subsets are laid out as 6-slot bit indicators.
    A ValueTracker idx walks through the 10 star-family members
    containing element 1. always_redraw highlights the "fixed 1" slot
    GREEN, recolors current set GREEN border, and tracks a running
    count. Final "10 = C(5, 2)" stamp.
    """

    def construct(self):
        n, k = 6, 3
        all_sets = list(combinations(range(n), k))
        star = [S for S in all_sets if 0 in S]  # fix element 1 = index 0

        title = Tex(r"Erdős–Ko–Rado ($n=6,\ k=3$): max intersecting $=\binom{5}{2}=10$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Grid: 4 rows × 5 cols of mini subset cells
        rows, cols = 4, 5
        cell_w = 1.9
        cell_h = 0.75
        subset_rows = VGroup()
        slot_rects = {}  # map set_idx → list of 6 rect mobjects for slots

        for i, S in enumerate(all_sets):
            r = i // cols
            c = i % cols
            base = np.array([(c - (cols - 1) / 2) * cell_w,
                              ((rows - 1) / 2 - r) * cell_h,
                              0]) + DOWN * 0.2
            cell = Rectangle(width=cell_w * 0.9, height=cell_h * 0.85,
                             color=GREY_B, stroke_width=1.2,
                             fill_opacity=0.03).move_to(base)
            subset_rows.add(cell)
            slots = VGroup()
            for s in range(n):
                x = (s - (n - 1) / 2) * 0.2
                slot_col = YELLOW if s in S else GREY_D
                fill_op = 0.85 if s in S else 0.15
                slot = Square(side_length=0.17, color=slot_col,
                              stroke_width=0.6,
                              fill_color=slot_col,
                              fill_opacity=fill_op).move_to(base + np.array([x, 0, 0]))
                slots.add(slot)
            slot_rects[i] = slots
            subset_rows.add(slots)

        self.play(FadeIn(subset_rows))

        # Mark fixed element 1 (index 0) in every set with GREEN if present
        fixed_lbl = Tex(r"fix element $1$ (green slot)", color=GREEN, font_size=22).to_edge(DOWN, buff=0.3).shift(LEFT * 3.5)
        self.play(Write(fixed_lbl))

        # Recolor slot 0 GREEN where element 1 is present
        for i, S in enumerate(all_sets):
            if 0 in S:
                self.play(slot_rects[i][0].animate.set_fill(GREEN, opacity=0.95).set_color(GREEN),
                          run_time=0.05)
        self.wait(0.3)

        idx_tr = ValueTracker(0.0)

        def highlight_current():
            k = int(round(idx_tr.get_value()))
            k = max(0, min(len(star) - 1, k))
            target_set = star[k]
            # find idx in all_sets
            for i, S in enumerate(all_sets):
                if S == target_set:
                    r = i // cols
                    c = i % cols
                    base = np.array([(c - (cols - 1) / 2) * cell_w,
                                      ((rows - 1) / 2 - r) * cell_h,
                                      0]) + DOWN * 0.2
                    return Rectangle(width=cell_w * 0.9, height=cell_h * 0.85,
                                     color=GREEN, stroke_width=3.5,
                                     fill_opacity=0).move_to(base)
            return VGroup()

        self.add(always_redraw(highlight_current))

        counter = VGroup(
            VGroup(Tex(r"star index $=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(GREEN)
                   ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"running count $=$", color=GREEN, font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(GREEN)
                   ).arrange(RIGHT, buff=0.1),
            Tex(r"$\binom{5}{2}=10$", color=GREEN, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.3)
        counter[0][1].add_updater(lambda m: m.set_value(int(round(idx_tr.get_value())) + 1))
        counter[1][1].add_updater(lambda m: m.set_value(int(round(idx_tr.get_value())) + 1))
        self.add(counter)

        self.play(idx_tr.animate.set_value(float(len(star) - 1)),
                  run_time=4, rate_func=linear)
        self.wait(0.5)
