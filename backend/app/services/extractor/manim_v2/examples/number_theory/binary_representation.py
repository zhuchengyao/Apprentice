from manim import *
import numpy as np


class BinaryRepresentationExample(Scene):
    """
    Unsigned 8-bit binary representation of n.

    SINGLE_FOCUS:
      8 boxes labeled with powers 128, 64, 32, 16, 8, 4, 2, 1.
      ValueTracker n_tr sweeps 0 → 255; each box fills YELLOW when
      the corresponding bit is 1 and stays grey when 0; inside each
      box the digit 0 or 1 is shown. A live readout shows the
      expansion sum and the bit string (n)_2, plus decimal n.
    """

    def construct(self):
        title = Tex(r"Binary representation: $n = \sum_{i=0}^{7} b_i\,2^i$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        powers = [2 ** k for k in range(7, -1, -1)]  # 128..1

        boxes = VGroup()
        for k in range(8):
            rect = Rectangle(width=0.95, height=1.05,
                             color=GREY_B, stroke_width=2)
            rect.move_to([-3.6 + k * 1.04, 0.6, 0])
            boxes.add(rect)

        power_lbls = VGroup(*[
            MathTex(rf"2^{{{7 - k}}}", font_size=24, color=GREY_B)
                .next_to(boxes[k], UP, buff=0.12)
            for k in range(8)
        ])
        value_lbls = VGroup(*[
            MathTex(rf"{powers[k]}", font_size=20, color=GREY_B)
                .next_to(boxes[k], DOWN, buff=0.1)
            for k in range(8)
        ])

        self.play(FadeIn(boxes), Write(power_lbls), Write(value_lbls))

        n_tr = ValueTracker(0)

        def bits_of():
            n = int(round(n_tr.get_value()))
            return [(n >> (7 - k)) & 1 for k in range(8)]

        def box_fills():
            bs = bits_of()
            grp = VGroup()
            for k, b in enumerate(bs):
                if b:
                    r = Rectangle(width=0.95, height=1.05,
                                  color=YELLOW, fill_opacity=0.55,
                                  stroke_width=2)
                    r.move_to(boxes[k].get_center())
                    grp.add(r)
            return grp

        def bit_digits():
            bs = bits_of()
            grp = VGroup()
            for k, b in enumerate(bs):
                color = BLACK if b else GREY_B
                d = MathTex(str(b), color=color, font_size=42)
                d.move_to(boxes[k].get_center())
                grp.add(d)
            return grp

        self.add(always_redraw(box_fills),
                 always_redraw(bit_digits))

        def expansion():
            n = int(round(n_tr.get_value()))
            bs = bits_of()
            terms = [str(powers[k]) for k, b in enumerate(bs) if b]
            if not terms:
                txt = r"n = 0"
            else:
                txt = " + ".join(terms) + rf" = {n}"
            return MathTex(txt, font_size=30, color=YELLOW).move_to([0, -1.1, 0])

        def dec_panel():
            n = int(round(n_tr.get_value()))
            bs = bits_of()
            bit_str = "".join(str(b) for b in bs)
            return VGroup(
                MathTex(rf"n = {n}", color=WHITE, font_size=32),
                MathTex(rf"({bit_str})_2", color=YELLOW, font_size=30),
            ).arrange(DOWN, buff=0.25).move_to([0, -2.6, 0])

        self.add(always_redraw(expansion),
                 always_redraw(dec_panel))

        # First pass: sweep smoothly 0 → 255
        self.play(n_tr.animate.set_value(255),
                  run_time=10, rate_func=linear)
        self.wait(0.4)

        # Second pass: jump to a few canonical values
        for target in [170, 85, 128, 1, 255, 13]:
            self.play(n_tr.animate.set_value(target),
                      run_time=0.9, rate_func=smooth)
            self.wait(0.25)
        self.wait(0.4)
