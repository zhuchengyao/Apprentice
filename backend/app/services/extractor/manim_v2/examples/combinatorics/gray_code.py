from manim import *
import numpy as np


class GrayCodeExample(Scene):
    """
    Gray code: successive binary numbers differ by exactly one bit.
    For n=4, the reflected Gray code sequence 0000, 0001, 0011, 0010,
    0110, 0111, 0101, 0100, 1100, 1101, ..., 1000 visits all 16 values
    with single-bit transitions.

    SINGLE_FOCUS: 16 bit-pattern rows in a vertical column, each
    showing 4 blue/orange slots. ValueTracker k_tr walks the
    sequence; always_redraw puts YELLOW highlight box on current
    row, dashed GREEN arrow connecting to next row, and shows
    which bit flipped.
    """

    def construct(self):
        title = Tex(r"Gray code ($n=4$): successive integers differ by 1 bit",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def gray(i):
            return i ^ (i >> 1)

        seq = [gray(i) for i in range(16)]
        binseq = [format(v, "04b") for v in seq]

        # Layout: left side has the 16 rows with 4 slot cells each
        cell_s = 0.35
        origin = np.array([-3.5, 2.3, 0])

        def bit_slot(bit, pos):
            col = ORANGE if bit == "1" else GREY_D
            op = 0.85 if bit == "1" else 0.25
            return Square(side_length=cell_s * 0.92, color=col,
                          stroke_width=0.9, fill_color=col,
                          fill_opacity=op).move_to(pos)

        row_origins = []
        rows = VGroup()
        for i, b in enumerate(binseq):
            y = origin[1] - i * cell_s * 1.05
            row_origin = np.array([origin[0], y, 0])
            row_origins.append(row_origin)
            for j, digit in enumerate(b):
                rows.add(bit_slot(digit, row_origin + RIGHT * j * cell_s))
            rows.add(Tex(str(i), font_size=14,
                         color=GREY_B).move_to(
                row_origin + LEFT * 0.45))
            rows.add(Tex(f"${b}$", font_size=14,
                         color=GREY_B).move_to(
                row_origin + RIGHT * 4 * cell_s + RIGHT * 0.15))
        self.play(FadeIn(rows), run_time=1.5)

        k_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(15, int(round(k_tr.get_value()))))

        def highlight():
            k = k_now()
            return Rectangle(width=cell_s * 4.6, height=cell_s * 0.98,
                             color=YELLOW, stroke_width=3,
                             fill_opacity=0).move_to(
                row_origins[k] + RIGHT * 1.5 * cell_s)

        def flip_arrow():
            k = k_now()
            if k >= 15:
                return VGroup()
            current = binseq[k]
            nxt = binseq[k + 1]
            flipped = next(j for j in range(4) if current[j] != nxt[j])
            p1 = row_origins[k] + RIGHT * flipped * cell_s + RIGHT * 0.05
            p2 = row_origins[k + 1] + RIGHT * flipped * cell_s + RIGHT * 0.05
            return Arrow(p1 + RIGHT * 0.3, p2 + RIGHT * 0.3,
                          color=GREEN, stroke_width=3,
                          buff=0.05, max_tip_length_to_length_ratio=0.15)

        self.add(always_redraw(highlight), always_redraw(flip_arrow))

        info = VGroup(
            VGroup(Tex(r"$k=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"Gray$(k)=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"flipped bit: GREEN arrow",
                color=GREEN, font_size=22),
            Tex(r"applications: rotary encoder, ",
                font_size=20),
            Tex(r"hypercube Hamiltonian cycle",
                font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(k_now()))
        info[1][1].add_updater(lambda m: m.set_value(seq[k_now()]))
        self.add(info)

        self.play(k_tr.animate.set_value(15.0),
                  run_time=7, rate_func=linear)
        self.wait(0.8)
