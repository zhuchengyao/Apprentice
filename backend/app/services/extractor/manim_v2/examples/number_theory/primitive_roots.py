from manim import *
import numpy as np


class PrimitiveRootsExample(Scene):
    """
    Primitive root mod p: an element g with ord(g) = p-1. For p = 7,
    g = 3 works: 3^1..3^6 = 3, 2, 6, 4, 5, 1 (all nonzero residues).

    SINGLE_FOCUS:
      Table of 3^k mod 7 for k = 1..6. ValueTracker k_tr steps; each
      step shows the power and circles the residue among {1..6};
      all visited → primitive root.
    """

    def construct(self):
        title = Tex(r"Primitive root: $g^k \bmod p$ hits every nonzero residue",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        p = 7
        g = 3
        powers = [pow(g, k, p) for k in range(1, p)]

        # Two rows: top = k values 1..6, bottom = g^k mod p
        cell = 0.8
        y_top = 1.5
        y_bot = 0.5
        x_start = -2.7

        # k labels
        k_group = VGroup()
        for i, k in enumerate(range(1, p)):
            sq = Square(side_length=cell * 0.95,
                          color=WHITE, stroke_width=1,
                          fill_opacity=0.1)
            sq.move_to([x_start + i * cell, y_top, 0])
            k_group.add(sq)
            k_group.add(MathTex(rf"k={k}", font_size=20, color=WHITE
                                  ).move_to(sq.get_center()))
        self.play(FadeIn(k_group))

        # Results row
        res_group = VGroup()
        for i, v in enumerate(powers):
            sq = Square(side_length=cell * 0.95,
                          color=BLUE, stroke_width=1,
                          fill_opacity=0.3)
            sq.move_to([x_start + i * cell, y_bot, 0])
            res_group.add(sq)
            res_group.add(MathTex(rf"{v}", font_size=24,
                                     color=WHITE
                                     ).move_to(sq.get_center()))
        self.play(FadeIn(res_group))

        # Residue tracker at bottom: cells for 1, 2, 3, 4, 5, 6
        residue_box_y = -1.5
        residue_x_start = -2.7
        residue_base_boxes = VGroup()
        for j in range(1, p):
            sq = Square(side_length=cell * 0.85, color=GREY_B,
                          stroke_width=1, fill_opacity=0.2)
            sq.move_to([residue_x_start + (j - 1) * cell, residue_box_y, 0])
            residue_base_boxes.add(sq)
            residue_base_boxes.add(MathTex(rf"{j}", font_size=22, color=WHITE
                                              ).move_to(sq.get_center()))
        self.play(FadeIn(residue_base_boxes))

        k_tr = ValueTracker(0)

        def highlight_power():
            k = int(round(k_tr.get_value()))
            k = max(0, min(k, p - 1))
            grp = VGroup()
            # Highlight k-th column
            if k > 0:
                sq1 = Square(side_length=cell * 0.95, color=YELLOW,
                                stroke_width=3, fill_opacity=0.4)
                sq1.move_to([x_start + (k - 1) * cell, y_top, 0])
                grp.add(sq1)
                sq2 = Square(side_length=cell * 0.95, color=YELLOW,
                                stroke_width=3, fill_opacity=0.4)
                sq2.move_to([x_start + (k - 1) * cell, y_bot, 0])
                grp.add(sq2)
            return grp

        def visited_residues():
            k = int(round(k_tr.get_value()))
            k = max(0, min(k, p - 1))
            visited = set(powers[:k])
            grp = VGroup()
            for j in range(1, p):
                if j in visited:
                    sq = Square(side_length=cell * 0.85,
                                  color=GREEN, fill_opacity=0.7,
                                  stroke_width=1.5)
                    sq.move_to([residue_x_start + (j - 1) * cell,
                                 residue_box_y, 0])
                    grp.add(sq)
                    grp.add(MathTex(rf"{j}", font_size=22,
                                      color=BLACK).move_to(sq.get_center()))
            return grp

        self.add(always_redraw(highlight_power),
                  always_redraw(visited_residues))

        def info():
            k = int(round(k_tr.get_value()))
            k = max(0, min(k, p - 1))
            visited = set(powers[:k])
            return VGroup(
                MathTex(rf"p = 7,\ g = 3", color=WHITE, font_size=22),
                MathTex(rf"k = {k}/6", color=YELLOW, font_size=22),
                MathTex(rf"\text{{visited}} = {sorted(visited)}",
                         color=GREEN, font_size=18),
                Tex(r"all 6 nonzero residues $\Rightarrow$ primitive root",
                     color=GREEN if len(visited) == 6 else WHITE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        for kv in range(1, p):
            self.play(k_tr.animate.set_value(kv),
                       run_time=0.9, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
