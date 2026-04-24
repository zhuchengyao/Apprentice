from manim import *
import numpy as np


class DominoTilings2NExample(Scene):
    """
    Domino tilings of a 2×n strip satisfy F(n) = F(n-1) + F(n-2)
    (Fibonacci). A vertical domino covers column n (1 way to tile
    the rest), a pair of horizontal dominos covers columns n-1 and
    n (1 way to tile columns 1..n-2).

    SINGLE_FOCUS:
      2×n strip; ValueTracker n_tr steps n = 1 → 8; always_redraw
      rebuilds both the strip and a Fibonacci-number-labeled tile
      count. Bonus: 2 example tilings for each n shown below.
    """

    def construct(self):
        title = Tex(r"$2 \times n$ domino tilings: $F(n) = F(n-1) + F(n-2)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n_tr = ValueTracker(1)

        dx = 0.7
        origin_main = np.array([-4, 1.2, 0])

        def strip():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 8))
            grp = VGroup()
            # Outline
            outline = Rectangle(width=n * dx, height=2 * dx,
                                  color=WHITE, stroke_width=2.5,
                                  fill_opacity=0)
            outline.move_to(origin_main + np.array([(n - 1) * dx / 2, 0, 0]))
            grp.add(outline)
            # Grid lines
            for i in range(1, n):
                grp.add(Line(origin_main + np.array([i * dx - dx / 2, -dx, 0]),
                               origin_main + np.array([i * dx - dx / 2, dx, 0]),
                               color=GREY_B, stroke_width=1))
            grp.add(Line(origin_main + np.array([-dx / 2, 0, 0]),
                           origin_main + np.array([(n - 1) * dx + dx / 2, 0, 0]),
                           color=GREY_B, stroke_width=1))
            return grp

        self.add(always_redraw(strip))

        def fib(n):
            a, b = 1, 1
            for _ in range(n):
                a, b = b, a + b
            return a

        # Example tiling for this n (one vertical strategy)
        def one_tiling():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 8))
            grp = VGroup()
            # Just all vertical dominos
            for i in range(n):
                x = origin_main[0] + i * dx
                dom = Rectangle(width=dx * 0.85, height=2 * dx * 0.9,
                                  color=BLUE, fill_opacity=0.55,
                                  stroke_width=1)
                dom.move_to([x, origin_main[1], 0])
                grp.add(dom)
            return grp

        self.add(always_redraw(one_tiling))

        # Second example: horizontal pairs from left
        origin_alt = np.array([-4, -1.2, 0])

        def alt_tiling_strip():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 8))
            grp = VGroup()
            outline = Rectangle(width=n * dx, height=2 * dx,
                                  color=WHITE, stroke_width=2.5,
                                  fill_opacity=0)
            outline.move_to(origin_alt + np.array([(n - 1) * dx / 2, 0, 0]))
            grp.add(outline)
            # Pair up from left: horizontal dominos in pairs, last one vertical if odd
            i = 0
            while i < n:
                if i + 1 < n:
                    # 2 horizontal dominos covering cols i, i+1
                    top = Rectangle(width=2 * dx * 0.9, height=dx * 0.85,
                                      color=ORANGE, fill_opacity=0.55,
                                      stroke_width=1)
                    top.move_to([origin_alt[0] + (i + 0.5) * dx,
                                 origin_alt[1] + dx / 2, 0])
                    bot = Rectangle(width=2 * dx * 0.9, height=dx * 0.85,
                                      color=ORANGE, fill_opacity=0.55,
                                      stroke_width=1)
                    bot.move_to([origin_alt[0] + (i + 0.5) * dx,
                                 origin_alt[1] - dx / 2, 0])
                    grp.add(top, bot)
                    i += 2
                else:
                    v = Rectangle(width=dx * 0.85, height=2 * dx * 0.9,
                                    color=BLUE, fill_opacity=0.55,
                                    stroke_width=1)
                    v.move_to([origin_alt[0] + i * dx, origin_alt[1], 0])
                    grp.add(v)
                    i += 1
            return grp

        self.add(always_redraw(alt_tiling_strip))

        def count_label():
            n = int(round(n_tr.get_value()))
            n = max(1, min(n, 8))
            f = fib(n)
            return MathTex(rf"n = {n}, \quad F(n) = {f}",
                             color=YELLOW, font_size=28
                             ).to_edge(RIGHT, buff=0.5).shift(UP * 0.3)

        self.add(always_redraw(count_label))

        # Tour
        for target in [2, 3, 4, 5, 6, 7, 8]:
            self.play(n_tr.animate.set_value(target),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
