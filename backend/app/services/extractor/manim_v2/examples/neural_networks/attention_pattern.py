from manim import *
import numpy as np


class AttentionPatternExample(Scene):
    """
    Attention matrix where each query token attends to all keys with
    a softmax weight; one query at a time is highlighted, and arrows
    of weighted strength flow from each key to the active query's
    output.

    SINGLE_FOCUS:
      Tokens listed left (queries top-down) and bottom (keys L→R).
      A grid of squares with opacity proportional to attention weight.
      ValueTracker query_idx steps through queries 0..4. The active
      row is highlighted; flow lines into the output show which keys
      contributed most.
    """

    def construct(self):
        title = Tex(r"Attention: each query token weighs all keys (softmax)",
                    font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        tokens = ["the", "cat", "sat", "on", "mat"]
        n = len(tokens)
        # Hand-tuned weight matrix (rows = queries, cols = keys), each row sums to 1
        weights = np.array([
            [0.42, 0.10, 0.10, 0.18, 0.20],
            [0.10, 0.45, 0.20, 0.10, 0.15],
            [0.05, 0.30, 0.40, 0.15, 0.10],
            [0.12, 0.15, 0.18, 0.40, 0.15],
            [0.08, 0.20, 0.12, 0.25, 0.35],
        ])

        # Heatmap grid centered on (-1.0, -0.4)
        anchor = np.array([-1.0, -0.4, 0])
        cell = 0.85

        def grid_mobject(active_q):
            grp = VGroup()
            for i in range(n):
                for j in range(n):
                    w = weights[i, j]
                    color = ORANGE if i == active_q else BLUE
                    sq = Rectangle(width=cell * 0.95, height=cell * 0.95,
                                   color=WHITE, stroke_width=1,
                                   fill_color=color, fill_opacity=w * 2.0)
                    sq.move_to(anchor + np.array([(j - 2) * cell, (2 - i) * cell, 0]))
                    grp.add(sq)
                    val_lbl = MathTex(rf"{w:.2f}", color=WHITE,
                                      font_size=14).move_to(sq.get_center())
                    grp.add(val_lbl)
            return grp

        # Query labels (left column)
        query_labels = VGroup()
        for i, tok in enumerate(tokens):
            lbl = Tex(rf"{tok}", color=GREY_B, font_size=22).move_to(
                anchor + np.array([-(2 + 0.7) * cell, (2 - i) * cell, 0]))
            query_labels.add(lbl)
        # Key labels (bottom row)
        key_labels = VGroup()
        for j, tok in enumerate(tokens):
            lbl = Tex(rf"{tok}", color=GREY_B, font_size=22).move_to(
                anchor + np.array([(j - 2) * cell, -(2 + 0.7) * cell, 0]))
            key_labels.add(lbl)
        # Axis-name labels
        q_axis = Tex(r"queries $\downarrow$", color=GREY_B, font_size=20).move_to(
            anchor + np.array([-(2 + 0.7) * cell, -(2 + 1.5) * cell, 0]))
        k_axis = Tex(r"keys $\to$", color=GREY_B, font_size=20).move_to(
            anchor + np.array([0, -(2 + 1.5) * cell, 0]))
        self.play(Write(query_labels), Write(key_labels), Write(q_axis), Write(k_axis))

        q_tr = ValueTracker(0)

        def grid():
            return grid_mobject(int(round(q_tr.get_value())))

        self.add(always_redraw(grid))

        # Highlight box for active row
        def row_highlight():
            i = int(round(q_tr.get_value()))
            return Rectangle(
                width=n * cell + 0.1, height=cell + 0.05,
                color=YELLOW, stroke_width=3, fill_opacity=0,
            ).move_to(anchor + np.array([0, (2 - i) * cell, 0]))

        self.add(always_redraw(row_highlight))

        # RIGHT COLUMN: which token is currently being computed
        rcol_x = +4.6

        def query_panel():
            i = int(round(q_tr.get_value()))
            tok = tokens[i]
            top_key_idx = int(np.argmax(weights[i]))
            return VGroup(
                Tex(rf"query: \textbf{{{tok}}}", color=YELLOW, font_size=24),
                Tex(rf"top key: \textbf{{{tokens[top_key_idx]}}} ($w={weights[i, top_key_idx]:.2f}$)",
                    color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(query_panel))

        formula = MathTex(
            r"a_{ij} = \frac{\exp(q_i \cdot k_j / \sqrt{d})}{\sum_k \exp(q_i \cdot k_k / \sqrt{d})}",
            color=YELLOW, font_size=22,
        ).move_to([rcol_x, -2.4, 0])
        self.play(Write(formula))

        # Step through queries
        for q in range(1, n):
            self.play(q_tr.animate.set_value(q),
                      run_time=1.4, rate_func=smooth)
            self.wait(0.5)

        self.wait(0.8)
