from manim import *
import numpy as np


class SecretaryProblemExample(Scene):
    """
    Secretary problem: interview n candidates in random order; pick
    the first one better than all previously seen after a "reject
    phase" of size ⌊n/e⌋. Success probability → 1/e as n → ∞.

    SINGLE_FOCUS:
      n = 10 candidates with random ranks. ValueTracker t_tr
      reveals one candidate at a time; reject phase fades in GREY,
      accept phase colors GREEN/RED (best vs not-best).
    """

    def construct(self):
        title = Tex(r"Secretary problem: reject $\lfloor n/e \rfloor$, then pick first better",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 10
        reject_phase = int(n / np.e)  # = 3

        rng = np.random.default_rng(7)
        # Random ranks 1 (worst) to n (best)
        ranks = list(range(1, n + 1))
        rng.shuffle(ranks)
        ranks = np.array(ranks)

        # Simulate strategy
        best_in_reject = max(ranks[:reject_phase]) if reject_phase > 0 else 0
        selected = None
        for i in range(reject_phase, n):
            if ranks[i] > best_in_reject:
                selected = i
                break

        cell = 0.7
        y = 0.5
        x_start = -3.5

        boxes = VGroup()
        for i in range(n):
            b = Rectangle(width=cell * 0.9, height=cell * 0.9,
                            color=WHITE, fill_opacity=0.1,
                            stroke_width=1.5)
            b.move_to([x_start + i * cell, y, 0])
            boxes.add(b)
            lbl = MathTex(rf"{i + 1}", font_size=14, color=GREY_B
                            ).next_to(b, DOWN, buff=0.1)
            boxes.add(lbl)
        self.play(FadeIn(boxes))

        t_tr = ValueTracker(0)

        def revealed_cards():
            t = int(round(t_tr.get_value()))
            t = max(0, min(t, n))
            grp = VGroup()
            for i in range(t):
                if i < reject_phase:
                    col = GREY_B
                    op = 0.5
                elif i == selected:
                    col = GREEN
                    op = 0.85
                elif selected is not None and i > selected:
                    col = GREY_B
                    op = 0.4  # skipped (strategy already picked)
                else:
                    col = ORANGE
                    op = 0.5
                sq = Square(side_length=cell * 0.9,
                              color=col, fill_opacity=op,
                              stroke_width=1.5)
                sq.move_to([x_start + i * cell, y, 0])
                grp.add(sq)
                grp.add(MathTex(rf"{ranks[i]}", font_size=22,
                                  color=BLACK).move_to(sq.get_center()))
            return grp

        self.add(always_redraw(revealed_cards))

        # Mark phases
        reject_band = DashedLine(
            [x_start - cell * 0.5, y + cell * 0.6, 0],
            [x_start + reject_phase * cell - cell * 0.5, y + cell * 0.6, 0],
            color=GREY_B, stroke_width=2)
        reject_lbl = Tex(r"reject phase",
                          color=GREY_B, font_size=18
                          ).next_to(reject_band, UP, buff=0.15)
        accept_band = DashedLine(
            [x_start + reject_phase * cell - cell * 0.5, y + cell * 0.6, 0],
            [x_start + n * cell - cell * 0.5, y + cell * 0.6, 0],
            color=GREEN, stroke_width=2)
        accept_lbl = Tex(r"accept if $>$ best-so-far",
                          color=GREEN, font_size=18
                          ).next_to(accept_band, UP, buff=0.15)
        self.play(Create(reject_band), Create(accept_band),
                   Write(reject_lbl), Write(accept_lbl))

        def info():
            t = int(round(t_tr.get_value()))
            t = max(0, min(t, n))
            best_so_far = max(ranks[:t]) if t > 0 else 0
            return VGroup(
                MathTex(rf"n = {n},\ \lfloor n/e \rfloor = {reject_phase}",
                         color=WHITE, font_size=20),
                MathTex(rf"\text{{seen}} = {t}",
                         color=YELLOW, font_size=20),
                MathTex(rf"\text{{best so far}} = {best_so_far}",
                         color=ORANGE, font_size=20),
                MathTex(r"P(\text{select best}) \to 1/e \approx 0.368",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(n),
                   run_time=6, rate_func=linear)
        self.wait(0.5)
