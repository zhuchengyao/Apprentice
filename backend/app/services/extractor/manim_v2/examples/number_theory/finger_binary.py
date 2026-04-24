from manim import *
import numpy as np


class FingerBinaryExample(Scene):
    """
    Counting in binary on 5 fingers from 0 to 31; ValueTracker n
    sweeps and the boxes flip up/down to show the binary expansion
    of the current number.

    SINGLE_FOCUS:
      5 boxes labeled 1, 2, 4, 8, 16 (right to left, mimicking finger
      values). ValueTracker n_tr steps through 0, 1, 2, ..., 31. Each
      box is YELLOW (raised) if its bit is set, GREY (down) otherwise.
      Live equation shows the sum.
    """

    def construct(self):
        title = Tex(r"Counting on fingers in binary: $0$ to $31$ on $5$ fingers",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        n_tr = ValueTracker(0)
        powers = [16, 8, 4, 2, 1]  # left to right (high to low for visibility)

        anchor = np.array([-3.0, -0.5, 0])
        spacing = 1.4

        # Static boxes
        boxes = []
        for i, p in enumerate(powers):
            box = Square(side_length=1.2, color=GREY_B, stroke_width=2,
                         fill_color=GREY_D, fill_opacity=0.4)
            box.move_to(anchor + np.array([i * spacing, 0, 0]))
            boxes.append(box)
            lbl = MathTex(str(p), font_size=32, color=WHITE).move_to(box.get_center())
            box.add(lbl)
        for b in boxes:
            self.add(b)

        # Always_redraw highlight overlay
        def fingers_up():
            n = max(0, min(31, int(round(n_tr.get_value()))))
            grp = VGroup()
            # Determine bits (high to low)
            bits = [(n >> i) & 1 for i in (4, 3, 2, 1, 0)]
            for i, bit in enumerate(bits):
                if bit:
                    glow = Square(side_length=1.2, color=YELLOW, stroke_width=4,
                                  fill_color=YELLOW, fill_opacity=0.7)
                    glow.move_to(anchor + np.array([i * spacing, 0, 0]))
                    p = powers[i]
                    glow_lbl = MathTex(str(p), font_size=32,
                                       color=BLACK).move_to(glow.get_center())
                    grp.add(glow)
                    grp.add(glow_lbl)
            return grp

        self.add(always_redraw(fingers_up))

        # Live equation showing the sum
        def equation():
            n = max(0, min(31, int(round(n_tr.get_value()))))
            bits = [(n >> i) & 1 for i in (4, 3, 2, 1, 0)]
            terms = [str(p) for p, b in zip(powers, bits) if b]
            if terms:
                eq_str = " + ".join(terms) + f" = {n}"
            else:
                eq_str = f"0 = {n}"
            return MathTex(eq_str, color=YELLOW, font_size=30).move_to([0, -2.4, 0])

        # Live n value at top right
        def n_readout():
            n = max(0, min(31, int(round(n_tr.get_value()))))
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=36),
                MathTex(rf"\text{{binary}} = {n:05b}",
                        color=GREEN, font_size=24),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR).shift(LEFT * 0.4 + DOWN * 0.5)

        self.add(always_redraw(equation), always_redraw(n_readout))

        # Step through 0 to 31 (skip every other for time, then show count)
        for n in range(0, 32):
            self.play(n_tr.animate.set_value(n),
                      run_time=0.25, rate_func=smooth)
        self.wait(0.6)

        principle = Tex(r"$2^5 = 32$ states $\to 0\dots 31$ on $5$ digits",
                        color=YELLOW, font_size=22).to_edge(DOWN, buff=0.3)
        self.play(Write(principle))
        self.wait(0.8)
