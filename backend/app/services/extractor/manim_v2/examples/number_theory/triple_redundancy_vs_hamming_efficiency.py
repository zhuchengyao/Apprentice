from manim import *
import numpy as np


class TripleRedundancyVsHammingEfficiency(Scene):
    """Triple redundancy vs Hamming(7,4) for single-bit error correction.
    Triple: send each data bit 3 times, receiver votes majority — uses
    3 bits to protect 1 data bit, overhead 2/3.
    Hamming(7,4): send 7 bits to protect 4 data bits, overhead 3/7 ≈ 43%.
    Visualize both encodings and overhead rates in a side-by-side panel."""

    def construct(self):
        title = Tex(
            r"Single-bit error correction: triple redundancy vs Hamming(7,4)",
            font_size=26,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left_cap = Tex("Triple redundancy", font_size=26,
                       color=RED).move_to([-3.5, 2.3, 0])
        right_cap = Tex("Hamming(7,4)", font_size=26,
                        color=GREEN).move_to([3.5, 2.3, 0])
        self.play(Write(left_cap), Write(right_cap))

        def make_bit_row(bits, x0, y, colors=None):
            grp = VGroup()
            for i, b in enumerate(bits):
                sq = Square(side_length=0.5, stroke_width=1.5)
                if colors is not None:
                    sq.set_fill(colors[i], opacity=0.4)
                    sq.set_stroke(colors[i], width=2)
                t = Tex(str(b), font_size=24,
                        color=colors[i] if colors else WHITE)
                t.move_to(sq)
                cell = VGroup(sq, t)
                cell.move_to([x0 + i * 0.55, y, 0])
                grp.add(cell)
            return grp

        data_bits = [1]
        in_left = make_bit_row(
            data_bits, -5.1, 1.4, colors=[BLUE],
        )
        in_left_lab = Tex("data: 1 bit", font_size=18,
                          color=BLUE).next_to(in_left, UP, buff=0.1)
        out_left_bits = data_bits * 3
        out_left = make_bit_row(
            out_left_bits, -4.3, 0.4,
            colors=[RED] * 3,
        )
        out_left_lab = Tex("sent: 3 bits", font_size=18,
                           color=RED).next_to(out_left, UP, buff=0.1)
        self.play(FadeIn(in_left), FadeIn(in_left_lab))
        self.play(TransformFromCopy(in_left, out_left),
                  FadeIn(out_left_lab))

        flip_idx = 1
        flipped = list(out_left_bits)
        flipped[flip_idx] = 1 - flipped[flip_idx]
        received_left = make_bit_row(
            flipped, -4.3, -0.7,
            colors=[RED if i != flip_idx else ORANGE for i in range(3)],
        )
        received_left_lab = Tex("received", font_size=18,
                                color=RED).next_to(received_left, UP,
                                                   buff=0.1)
        self.play(FadeIn(received_left, received_left_lab))
        self.play(Indicate(received_left[flip_idx], color=ORANGE,
                           scale_factor=1.3))

        decoded_left = 1 if sum(flipped) >= 2 else 0
        verdict_left = VGroup(
            Tex(r"majority vote $\to$", font_size=22, color=YELLOW),
            make_bit_row([decoded_left], -2.5, -1.7, colors=[BLUE]),
        )
        verdict_left[0].move_to([-4.3, -1.7, 0])
        verdict_left[1].move_to([-2.5, -1.7, 0])
        self.play(FadeIn(verdict_left))

        rate_left = MathTex(r"\text{rate} = \tfrac{1}{3} \approx 33\%",
                            font_size=24, color=RED)
        rate_left.move_to([-3.5, -2.6, 0])
        self.play(Write(rate_left))

        in_right = make_bit_row(
            [1, 0, 1, 1], 1.5, 1.4, colors=[BLUE] * 4,
        )
        in_right_lab = Tex("data: 4 bits", font_size=18,
                           color=BLUE).next_to(in_right, UP, buff=0.1)
        out_right = make_bit_row(
            [1, 1, 1, 0, 0, 1, 1], 1.0, 0.4,
            colors=[GREEN_A, GREEN_A, GREEN, GREEN_A, GREEN,
                    GREEN, GREEN],
        )
        out_right_lab = Tex("sent: 7 bits", font_size=18,
                            color=GREEN).next_to(out_right, UP, buff=0.1)
        self.play(FadeIn(in_right, in_right_lab))
        self.play(TransformFromCopy(in_right, out_right),
                  FadeIn(out_right_lab))

        parity_note = Tex(
            r"(positions 1, 2, 4 = parities;\\"
            r"positions 3, 5, 6, 7 = data)",
            font_size=18, color=GREEN_A,
        ).next_to(out_right, DOWN, buff=0.2)
        self.play(FadeIn(parity_note))

        rate_right = MathTex(r"\text{rate} = \tfrac{4}{7} \approx 57\%",
                             font_size=24, color=GREEN)
        rate_right.move_to([3.5, -2.6, 0])
        self.play(Write(rate_right))

        winner = SurroundingRectangle(rate_right, color=YELLOW,
                                      buff=0.15, stroke_width=3)
        self.play(Create(winner))
        self.wait(1.5)
