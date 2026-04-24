from manim import *
import numpy as np


class OccupancyProblemExample(Scene):
    """
    Balls into boxes: N balls thrown uniformly into M boxes. Distribution
    of counts; expected number of empty boxes = M · (1 - 1/M)^N; expected
    max occupancy grows like log N / log log N.

    SINGLE_FOCUS:
      M = 12 boxes at bottom; ValueTracker throw_tr sequentially drops
      N balls, each to a uniformly random box; always_redraw stack
      heights.
    """

    def construct(self):
        title = Tex(r"Balls in boxes: $N = 24$ balls $\to M = 12$ boxes",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        M = 12
        N = 24
        rng = np.random.default_rng(37)
        throws = rng.integers(0, M, size=N)

        box_w = 0.8
        box_h = 0.5
        base_y = -2.2
        x_start = -4.5

        # Box outlines (empty)
        boxes = VGroup()
        for i in range(M):
            b = Rectangle(width=box_w * 0.9, height=box_h,
                            color=WHITE, stroke_width=1.5,
                            fill_opacity=0.05)
            b.move_to([x_start + i * box_w, base_y, 0])
            boxes.add(b)
            lbl = MathTex(rf"{i}", font_size=14, color=GREY_B
                            ).next_to(b, DOWN, buff=0.15)
            boxes.add(lbl)
        self.play(FadeIn(boxes))

        throw_tr = ValueTracker(0)

        def ball_stacks():
            t = int(round(throw_tr.get_value()))
            t = max(0, min(t, N))
            counts = np.zeros(M, dtype=int)
            for i in range(t):
                counts[throws[i]] += 1
            grp = VGroup()
            for i, cnt in enumerate(counts):
                for k in range(cnt):
                    y = base_y + box_h * 0.6 + k * 0.35
                    ball = Circle(radius=0.14, color=BLUE,
                                    fill_opacity=0.7, stroke_width=0.5
                                    ).move_to([x_start + i * box_w, y, 0])
                    grp.add(ball)
            return grp

        self.add(always_redraw(ball_stacks))

        def info():
            t = int(round(throw_tr.get_value()))
            t = max(0, min(t, N))
            counts = np.zeros(M, dtype=int)
            for i in range(t):
                counts[throws[i]] += 1
            empty = int(np.sum(counts == 0))
            max_count = int(np.max(counts)) if t > 0 else 0
            expected_empty = M * (1 - 1/M) ** t if t > 0 else M
            return VGroup(
                MathTex(rf"\text{{throws}} = {t}/{N}",
                         color=WHITE, font_size=22),
                MathTex(rf"\text{{empty}} = {empty}",
                         color=GREY_B, font_size=22),
                MathTex(rf"E[\text{{empty}}] = M(1-1/M)^N = {expected_empty:.2f}",
                         color=GREEN, font_size=18),
                MathTex(rf"\max\,\text{{count}} = {max_count}",
                         color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.8)

        self.add(always_redraw(info))

        self.play(throw_tr.animate.set_value(N),
                   run_time=7, rate_func=linear)
        self.wait(0.4)
