from manim import *
import numpy as np


class ErdosSzekeresExample(Scene):
    """
    Erdős–Szekeres: any sequence of (r-1)(s-1)+1 distinct real numbers
    contains either an increasing subsequence of length r or a
    decreasing subsequence of length s.

    For r=s=3: any 5 distinct reals contain an increasing or
    decreasing subsequence of length 3.

    SINGLE_FOCUS: a sequence of 17 dots at heights. ValueTracker k_tr
    walks dots and always_redraw colors them into a GREEN increasing
    subsequence of length 5 or RED decreasing — forced to appear by
    r=s=5 ⇒ (5-1)² + 1 = 17.
    """

    def construct(self):
        title = Tex(r"Erdős–Szekeres: $(r-1)(s-1)+1$ reals $\Rightarrow$ mono subseq",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        np.random.seed(42)
        N = 17  # (5-1)(5-1)+1
        vals = np.random.permutation(N) + 1.0

        axes = Axes(x_range=[0, N + 1, 2], y_range=[0, N + 1, 2],
                    x_length=9.0, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(DOWN * 0.2)
        self.play(Create(axes))

        dots = VGroup()
        for i, v in enumerate(vals):
            d = Dot(axes.c2p(i + 1, v), color=BLUE, radius=0.1)
            dots.add(d)
        self.play(FadeIn(dots))

        # Compute LIS and LDS
        def longest_increasing(seq):
            n = len(seq)
            lengths = [1] * n
            parent = [-1] * n
            for i in range(n):
                for j in range(i):
                    if seq[j] < seq[i] and lengths[j] + 1 > lengths[i]:
                        lengths[i] = lengths[j] + 1
                        parent[i] = j
            idx = int(np.argmax(lengths))
            out = []
            while idx != -1:
                out.append(idx)
                idx = parent[idx]
            return list(reversed(out))

        def longest_decreasing(seq):
            return longest_increasing([-x for x in seq])

        lis = longest_increasing(vals.tolist())
        lds = longest_decreasing(vals.tolist())
        target = lis if len(lis) >= len(lds) else lds
        target_color = GREEN if len(lis) >= len(lds) else RED
        target_name = "increasing" if len(lis) >= len(lds) else "decreasing"

        k_tr = ValueTracker(0.0)

        def highlight_path():
            k = int(round(k_tr.get_value()))
            k = max(0, min(len(target), k))
            grp = VGroup()
            revealed = target[:k]
            for j, idx in enumerate(revealed):
                grp.add(Dot(axes.c2p(idx + 1, vals[idx]),
                             color=target_color, radius=0.13))
                if j > 0:
                    prev = revealed[j - 1]
                    grp.add(Line(axes.c2p(prev + 1, vals[prev]),
                                  axes.c2p(idx + 1, vals[idx]),
                                  color=target_color, stroke_width=3))
            return grp

        self.add(always_redraw(highlight_path))

        # Info
        info = VGroup(
            Tex(rf"sequence of $N={N}$ distinct reals", font_size=22),
            Tex(rf"$(r-1)(s-1)+1=(5-1)^2+1={N}$", font_size=22),
            VGroup(Tex(rf"LIS length $={len(lis)}$", color=GREEN, font_size=22),
                    ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(rf"LDS length $={len(lds)}$", color=RED, font_size=22),
                    ).arrange(RIGHT, buff=0.1),
            Tex(rf"$\ge 5$ forced, found {target_name}",
                color=target_color, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.3)
        self.add(info)

        for k in range(1, len(target) + 1):
            self.play(k_tr.animate.set_value(float(k)),
                      run_time=0.5, rate_func=smooth)
            self.wait(0.15)
        self.wait(0.8)
