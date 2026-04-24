from manim import *
import numpy as np


class PartialSumsApproachOneExample(Scene):
    """
    1/2 + 1/4 + 1/8 + ... + 1/2^n = 1 - 1/2^n  visualized as filling a unit bar.

    SINGLE_FOCUS animation:
      A unit-length horizontal bar from x=0 to x=1.
      ValueTracker n (integer-step) advances from 0 to 8.
      For each n, n colored sub-rectangles are drawn:
        - rect 1: width 1/2 starting at 0
        - rect 2: width 1/4 starting at 1/2
        - rect 3: width 1/8 starting at 3/4
        - ...
      Each rect has a label "1/2^k" inside.
      The right edge of the union (= S_n = 1 - 1/2^n) is marked, and
      the gap to 1 visibly shrinks.
    """

    def construct(self):
        title = Tex(r"$\sum_{k=1}^{\infty} \tfrac{1}{2^k} = 1$",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Position the bar
        bar_left = -5.0
        bar_right = +5.0
        bar_width = bar_right - bar_left
        bar_y = -0.6

        # Outer reference frame
        frame = Rectangle(width=bar_width, height=0.8, color=WHITE,
                          stroke_width=3).move_to([(bar_left + bar_right) / 2, bar_y, 0])
        zero_lbl = Tex(r"$0$", font_size=22).next_to(
            [bar_left, bar_y, 0], DOWN, buff=0.15)
        one_lbl = Tex(r"$1$", font_size=22).next_to(
            [bar_right, bar_y, 0], DOWN, buff=0.15)
        self.play(Create(frame), Write(zero_lbl), Write(one_lbl))

        n_tr = ValueTracker(0.0)

        def filled_rectangles():
            n = max(0, int(n_tr.get_value()))
            grp = VGroup()
            colors = color_gradient([BLUE, GREEN, YELLOW], 12)
            x_cursor = bar_left
            for k in range(1, n + 1):
                w = bar_width * (1 / (2 ** k))
                rect = Rectangle(width=w, height=0.78,
                                 color=colors[k - 1],
                                 fill_color=colors[k - 1],
                                 fill_opacity=0.7,
                                 stroke_width=1)
                rect.move_to([x_cursor + w / 2, bar_y, 0])
                grp.add(rect)
                if k <= 5:
                    # Label inside (for early rectangles only — later are too small)
                    lbl = MathTex(rf"\tfrac{{1}}{{2^{k}}}",
                                  color=WHITE, font_size=18 if k <= 3 else 14)
                    lbl.move_to([x_cursor + w / 2, bar_y, 0])
                    grp.add(lbl)
                x_cursor += w
            return grp

        self.add(always_redraw(filled_rectangles))

        # Cursor at S_n with vertical line + label
        def edge_marker():
            n = max(0, int(n_tr.get_value()))
            S = 1 - 1 / (2 ** n) if n > 0 else 0
            x_pos = bar_left + S * bar_width
            line = Line([x_pos, bar_y - 0.5, 0], [x_pos, bar_y + 0.6, 0],
                        color=ORANGE, stroke_width=3)
            lbl = MathTex(rf"S_{{{n}}} = 1 - \tfrac{{1}}{{2^{{{n}}}}} = {S:.5f}",
                          color=ORANGE, font_size=22).next_to(
                [x_pos, bar_y + 0.6, 0], UP, buff=0.05)
            return VGroup(line, lbl)

        self.add(always_redraw(edge_marker))

        # Step n through 1, 2, 3, ..., 8 with pauses
        for target_n in range(1, 9):
            self.play(n_tr.animate.set_value(target_n),
                      run_time=0.8, rate_func=smooth)
            self.wait(0.4)

        # Final formula
        formula = MathTex(r"\lim_{n \to \infty} S_n = 1",
                          color=YELLOW, font_size=32).move_to([0, -2.4, 0])
        self.play(Write(formula))
        self.wait(1.0)
