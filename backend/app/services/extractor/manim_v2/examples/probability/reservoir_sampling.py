from manim import *
import numpy as np


class ReservoirSamplingExample(Scene):
    """
    Reservoir sampling: pick a uniform random element from a stream
    without knowing its length. Keep a reservoir of size k; for the
    i-th item (i > k), replace with prob k/i.

    SINGLE_FOCUS:
      Stream of 40 numbered items flowing past; reservoir slot (k=1)
      at top; ValueTracker t_tr advances stream; always_redraw shows
      which item is currently in the reservoir; final: any item was
      picked with equal probability 1/n.
    """

    def construct(self):
        title = Tex(r"Reservoir sampling: uniform pick from stream",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N = 40
        # Precompute a deterministic reservoir trajectory
        rng = np.random.default_rng(101)
        reservoir = [1]
        for i in range(2, N + 1):
            # Accept with prob 1/i (k=1 case)
            if rng.random() < 1 / i:
                reservoir.append(i)
            else:
                reservoir.append(reservoir[-1])
        # reservoir[i-1] = item in reservoir after processing item i

        # Stream row
        stream_y = 0.5
        item_w = 0.3
        x_start = -5.5

        t_tr = ValueTracker(0)

        def stream():
            t = int(round(t_tr.get_value()))
            t = max(0, min(t, N))
            grp = VGroup()
            for i in range(1, N + 1):
                x = x_start + (i - 1) * item_w
                col = GREY_B if i <= t else BLUE_D
                sq = Square(side_length=item_w * 0.85,
                              color=col, fill_opacity=0.5,
                              stroke_width=0.5)
                sq.move_to([x, stream_y, 0])
                grp.add(sq)
                if i % 5 == 0:
                    lbl = MathTex(rf"{i}", font_size=12, color=WHITE
                                    ).next_to(sq, DOWN, buff=0.08)
                    grp.add(lbl)
            return grp

        self.add(always_redraw(stream))

        # Reservoir box
        res_box = Rectangle(width=1.2, height=0.9, color=YELLOW,
                              fill_opacity=0.15, stroke_width=2
                              ).move_to([-3.5, 2.2, 0])
        res_lbl = Tex(r"reservoir ($k=1$)",
                       color=YELLOW, font_size=18
                       ).next_to(res_box, UP, buff=0.2)
        self.play(Create(res_box), Write(res_lbl))

        def res_value():
            t = int(round(t_tr.get_value()))
            t = max(0, min(t, N))
            if t == 0:
                return VGroup()
            item = reservoir[t - 1]
            return MathTex(rf"{item}", color=YELLOW, font_size=30
                             ).move_to(res_box.get_center())

        self.add(always_redraw(res_value))

        # Current stream element highlight
        def current_highlight():
            t = int(round(t_tr.get_value()))
            if t < 1 or t > N:
                return VGroup()
            x = x_start + (t - 1) * item_w
            return Square(side_length=item_w * 0.95,
                            color=GREEN, stroke_width=3,
                            fill_opacity=0).move_to([x, stream_y, 0])

        self.add(always_redraw(current_highlight))

        def info():
            t = int(round(t_tr.get_value()))
            t = max(0, min(t, N))
            if t == 0:
                p_keep = 1.0
            else:
                p_keep = 1 / t  # probability of replacing at this step
            return VGroup(
                MathTex(rf"t = {t}/{N}", color=WHITE, font_size=22),
                MathTex(rf"P(\text{{replace at }} t) = 1/{max(t, 1)} = {p_keep:.3f}",
                         color=GREEN, font_size=20),
                MathTex(rf"\text{{reservoir}} = {reservoir[t - 1] if t > 0 else '-'}",
                         color=YELLOW, font_size=22),
                Tex(r"uniform over $1..N$ at end",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.25)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(N),
                   run_time=9, rate_func=linear)
        self.wait(0.5)
