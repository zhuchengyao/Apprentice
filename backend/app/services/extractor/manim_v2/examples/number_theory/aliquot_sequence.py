from manim import *
import numpy as np


def aliquot(n):
    """Sum of proper divisors of n."""
    return sum(d for d in range(1, n) if n % d == 0)


class AliquotSequenceExample(Scene):
    """
    Aliquot sequences from 4 different starting numbers, animated step-by-step.

    Each row shows one starting number (12, 95, 30, 220 - amicable):
      - Boxes with values appear one at a time
      - Color codes: BLUE (still iterating), GREEN (perfect/amicable cycle),
        RED (terminates at 0 = prime), YELLOW (open trajectory)

    SINGLE_FOCUS:
      ValueTracker step_idx advances; per step, all four chains gain
      one more box if they haven't terminated.
    """

    def construct(self):
        title = Tex(r"Aliquot sequences: $s(n) = \sum_{d \mid n,\, d < n} d$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        starts = [12, 95, 30, 220]
        max_steps = 10

        # Compute each sequence up to max_steps or termination/cycle
        sequences = []
        for n0 in starts:
            seq = [n0]
            for _ in range(max_steps):
                nxt = aliquot(seq[-1])
                seq.append(nxt)
                if nxt == 0 or nxt == seq[-2] or nxt > 10000:
                    break
            sequences.append(seq)

        # Layout: 4 rows of boxes
        row_ys = [+1.8, +0.6, -0.6, -1.8]
        chain_groups = []
        for seq, y in zip(sequences, row_ys):
            row = VGroup()
            for i, val in enumerate(seq):
                # Color logic
                if val == 0:
                    color = RED
                elif i > 0 and i + 1 < len(seq) and seq[i + 1] == val:
                    color = GREEN  # perfect (e.g., 6 → 6)
                elif val == seq[0] and i == len(seq) - 1 and i > 0:
                    color = GREEN  # amicable cycle returning to start
                else:
                    color = BLUE
                box = RoundedRectangle(width=0.85, height=0.65, corner_radius=0.08,
                                       color=color, stroke_width=2,
                                       fill_color=color, fill_opacity=0.25)
                lbl = MathTex(str(val), font_size=18, color=WHITE).move_to(
                    box.get_center())
                row.add(VGroup(box, lbl))
            row.arrange(RIGHT, buff=0.2)
            row.move_to([0, y, 0])
            chain_groups.append(row)

        # Row labels
        row_lbls = []
        for n0, y in zip(starts, row_ys):
            lbl = Tex(rf"start ${n0}$:", color=WHITE, font_size=20).next_to(
                [0, y, 0], LEFT, buff=0.5)
            lbl.move_to([-5.5, y, 0])
            row_lbls.append(lbl)
            self.play(Write(lbl), run_time=0.3)

        step_tr = ValueTracker(0)

        def visible_chain(row, seq_len):
            def fn():
                k = int(round(step_tr.get_value()))
                k = min(k + 1, len(row))
                return VGroup(*row[:k])
            return fn

        for row, seq in zip(chain_groups, sequences):
            self.add(always_redraw(visible_chain(row, len(seq))))

        # Step through
        for step in range(1, max_steps + 1):
            self.play(step_tr.animate.set_value(step),
                      run_time=0.5, rate_func=smooth)

        # Highlight observations
        legend = VGroup(
            Tex(r"$12 \to 16 \to 15 \to 9 \to 4 \to 3 \to 1 \to 0$",
                color=GREY_B, font_size=20),
            Tex(r"$95 \to 25 \to 6$ (perfect) $\to 6 \to \cdots$",
                color=GREEN, font_size=20),
            Tex(r"$220 \leftrightarrow 284$ (amicable pair)",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        self.play(Write(legend))
        self.wait(1.0)
