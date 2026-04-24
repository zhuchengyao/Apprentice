from manim import *
import numpy as np


class SierpinskiCarpetExample(Scene):
    """
    Sierpinski carpet: start with unit square, remove middle 1/9,
    recursively apply. Fractal dimension log 8 / log 3 ≈ 1.893.
    After n iterations, 8^n remaining sub-squares of side 1/3^n.

    SINGLE_FOCUS: ValueTracker level_tr steps 0..4. always_redraw
    rebuilds carpet; live count + fractal dim.
    """

    def construct(self):
        title = Tex(r"Sierpinski carpet: $d=\log 8/\log 3\approx 1.8928$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        size = 4.8

        def cells_at_level(L):
            # Return list of (x, y, s) squares remaining at level L
            if L == 0:
                return [(0, 0, 1.0)]
            sub = cells_at_level(L - 1)
            out = []
            for (cx, cy, s) in sub:
                s_new = s / 3
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        out.append((cx + dx * s_new, cy + dy * s_new, s_new))
            return out

        level_tr = ValueTracker(0.0)

        def carpet():
            L = int(round(level_tr.get_value()))
            L = max(0, min(4, L))
            cells = cells_at_level(L)
            grp = VGroup()
            for (cx, cy, s) in cells:
                rect = Rectangle(width=s * size, height=s * size,
                                  color=YELLOW, stroke_width=0.8,
                                  fill_color=YELLOW,
                                  fill_opacity=0.6).move_to(
                    np.array([cx * size, cy * size, 0]))
                grp.add(rect)
            return grp

        self.add(always_redraw(carpet))

        info = VGroup(
            VGroup(Tex(r"level $L=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"sub-squares $=8^L=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"side length $=1/3^L=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=5,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"total area $=(8/9)^L=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$d=\log 8/\log 3\approx 1.8928$",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        def L_now():
            return max(0, min(4, int(round(level_tr.get_value()))))
        info[0][1].add_updater(lambda m: m.set_value(L_now()))
        info[1][1].add_updater(lambda m: m.set_value(8 ** L_now()))
        info[2][1].add_updater(lambda m: m.set_value(3 ** (-L_now())))
        info[3][1].add_updater(lambda m: m.set_value((8 / 9) ** L_now()))
        self.add(info)

        for L in range(1, 5):
            self.play(level_tr.animate.set_value(float(L)),
                      run_time=1.4, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
