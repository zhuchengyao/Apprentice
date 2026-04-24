from manim import *
import numpy as np


class NecklaceSplittingTwoThieves(Scene):
    """The k-jewel, 2-thief necklace-splitting theorem: with 2 thieves and k
    types of jewels, k cuts always suffice so that both thieves get equal
    counts of every jewel type.  Demonstrate for k = 2 (RED vs BLUE jewels):
    a specific 10-jewel necklace is split by 2 cuts into 3 pieces assigned
    to thieves so each gets the same count of each color.
    (A topological consequence of Borsuk-Ulam.)"""

    def construct(self):
        title = Tex(
            r"Necklace splitting: 2 thieves, 2 jewel types, 2 cuts",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        colors = [RED, RED, BLUE, RED, BLUE, BLUE, RED, BLUE, RED, BLUE]
        n = len(colors)
        cell = 0.7
        start_x = -n * cell / 2 + cell / 2

        jewels = VGroup()
        for k, color in enumerate(colors):
            j = Circle(radius=0.27, color=color, fill_opacity=0.85,
                      stroke_width=1.5)
            j.move_to([start_x + k * cell, 0.6, 0])
            jewels.add(j)

        chain = Line(
            jewels[0].get_center() + LEFT * 0.4,
            jewels[-1].get_center() + RIGHT * 0.4,
            color=GREY, stroke_width=3,
        ).shift(DOWN * 0.0)
        self.play(Create(chain))
        self.play(LaggedStart(*[FadeIn(j) for j in jewels], lag_ratio=0.08))

        red_count = sum(1 for c in colors if c == RED)
        blue_count = sum(1 for c in colors if c == BLUE)
        counts = VGroup(
            MathTex(rf"\text{{\#red}} = {red_count}",
                    font_size=28, color=RED),
            MathTex(rf"\text{{\#blue}} = {blue_count}",
                    font_size=28, color=BLUE),
        ).arrange(RIGHT, buff=1.0)
        counts.move_to([0, 1.8, 0])
        self.play(FadeIn(counts))

        cut_positions = [3, 7]
        cut_lines = VGroup(*[
            DashedLine(
                [start_x + (k - 0.5) * cell, 1.2, 0],
                [start_x + (k - 0.5) * cell, -0.2, 0],
                color=YELLOW, stroke_width=3,
                dash_length=0.12,
            )
            for k in cut_positions
        ])
        cut_labels = VGroup(*[
            Tex(f"cut {i+1}", font_size=22, color=YELLOW).move_to(
                [start_x + (k - 0.5) * cell, -0.45, 0]
            )
            for i, k in enumerate(cut_positions)
        ])
        self.play(LaggedStart(*[Create(c) for c in cut_lines], lag_ratio=0.3))
        self.play(LaggedStart(*[FadeIn(c) for c in cut_labels],
                              lag_ratio=0.3))

        piece_ranges = [(0, 2), (3, 6), (7, 9)]
        piece_colors = [GREEN_E, PURPLE_E, GREEN_E]
        piece_owners = ["Thief A", "Thief B", "Thief A"]
        underlines = VGroup()
        owner_labs = VGroup()
        for (a, b), pc, owner in zip(piece_ranges, piece_colors, piece_owners):
            xa = jewels[a].get_center()[0] - cell / 2 + 0.1
            xb = jewels[b].get_center()[0] + cell / 2 - 0.1
            y = -1.2
            under = Line([xa, y, 0], [xb, y, 0],
                         color=pc, stroke_width=6)
            underlines.add(under)
            owner_labs.add(Tex(owner, font_size=22,
                               color=pc).next_to(under, DOWN, buff=0.1))
        self.play(LaggedStart(*[Create(u) for u in underlines],
                              lag_ratio=0.2))
        self.play(LaggedStart(*[FadeIn(o) for o in owner_labs],
                              lag_ratio=0.2))

        def counts_for(ranges):
            r, b = 0, 0
            for (a, c) in ranges:
                for k in range(a, c + 1):
                    if colors[k] == RED:
                        r += 1
                    else:
                        b += 1
            return r, b

        a_ranges = [(0, 2), (7, 9)]
        b_ranges = [(3, 6)]
        r_a, b_a = counts_for(a_ranges)
        r_b, b_b = counts_for(b_ranges)
        result = VGroup(
            MathTex(rf"\text{{A}}: {r_a}\ \text{{red}},\ {b_a}\ \text{{blue}}",
                    font_size=26, color=GREEN_E),
            MathTex(rf"\text{{B}}: {r_b}\ \text{{red}},\ {b_b}\ \text{{blue}}",
                    font_size=26, color=PURPLE_E),
            MathTex(r"\text{each gets equal share of both colors!}",
                    font_size=26, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        result.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(result[0]))
        self.play(FadeIn(result[1]))
        self.play(FadeIn(result[2]))
        self.wait(1.5)
