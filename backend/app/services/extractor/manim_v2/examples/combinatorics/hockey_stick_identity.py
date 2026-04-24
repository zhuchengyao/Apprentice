from manim import *
import numpy as np
from math import comb


class HockeyStickIdentityExample(Scene):
    """
    Hockey stick identity in Pascal's triangle:
    Σ_{k=r}^{n} C(k, r) = C(n+1, r+1).

    SINGLE_FOCUS:
      Pascal's triangle rows 0..8 drawn; ValueTracker n_tr highlights
      a "hockey stick" (diagonal down, then horizontal) and shows
      the sum equals the C(n+1, r+1) entry.
    """

    def construct(self):
        title = Tex(r"Hockey stick: $\sum_{k=r}^n \binom{k}{r} = \binom{n+1}{r+1}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        MAX_N = 8
        dx = 0.8
        dy = 0.55
        top_y = 2.8

        # Draw full triangle
        triangle = VGroup()
        positions = {}
        for n in range(MAX_N + 1):
            row_w = n * dx
            x_start = -row_w / 2
            for k in range(n + 1):
                x = x_start + k * dx
                y = top_y - n * dy
                val = comb(n, k)
                lbl = MathTex(rf"{val}", font_size=20, color=WHITE)
                lbl.move_to([x, y, 0])
                triangle.add(lbl)
                positions[(n, k)] = np.array([x, y, 0])
        self.play(FadeIn(triangle))

        # Highlight hockey stick: C(r, r), C(r+1, r), ..., C(n, r), then C(n+1, r+1)
        r_val = 2
        n_tr = ValueTracker(r_val)

        def hockey_stick():
            n = int(round(n_tr.get_value()))
            n = max(r_val, min(n, MAX_N - 1))
            grp = VGroup()
            # Sum diagonal: C(k, r) for k=r..n
            for k in range(r_val, n + 1):
                p = positions.get((k, r_val))
                if p is not None:
                    sq = Circle(radius=0.25, color=YELLOW,
                                  stroke_width=3, fill_opacity=0.25
                                  ).move_to(p)
                    grp.add(sq)
            # Result: C(n+1, r+1)
            p_res = positions.get((n + 1, r_val + 1))
            if p_res is not None:
                sq = Circle(radius=0.28, color=GREEN,
                              stroke_width=3, fill_opacity=0.45
                              ).move_to(p_res)
                grp.add(sq)
            return grp

        self.add(always_redraw(hockey_stick))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(r_val, min(n, MAX_N - 1))
            total = sum(comb(k, r_val) for k in range(r_val, n + 1))
            target = comb(n + 1, r_val + 1)
            return VGroup(
                MathTex(rf"r = {r_val},\ n = {n}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\sum_{{k={r_val}}}^{{{n}}} \binom{{k}}{{{r_val}}} = {total}",
                         color=YELLOW, font_size=20),
                MathTex(rf"\binom{{{n + 1}}}{{{r_val + 1}}} = {target}",
                         color=GREEN, font_size=22),
                Tex(rf"match: {total == target}",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for nv in [3, 5, 7]:
            self.play(n_tr.animate.set_value(nv),
                       run_time=1.3, rate_func=smooth)
            self.wait(0.8)
        self.wait(0.5)
