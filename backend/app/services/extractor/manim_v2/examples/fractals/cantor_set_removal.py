from manim import *
import numpy as np


class CantorSetRemovalExample(Scene):
    """
    Cantor ternary set: start with [0, 1], remove middle thirds
    recursively. After n steps, 2^n intervals of total length
    (2/3)^n → 0 but uncountably many points remain.

    SINGLE_FOCUS: horizontal stack of levels; ValueTracker level_tr
    reveals levels 0..6; each row shows the surviving intervals as
    thick horizontal lines.
    """

    def construct(self):
        title = Tex(r"Cantor set: remove middle thirds; dim $=\log 2/\log 3$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def intervals_at_level(L):
            # Return list of [a, b] intervals
            if L == 0:
                return [[0.0, 1.0]]
            prev = intervals_at_level(L - 1)
            out = []
            for (a, b) in prev:
                third = (b - a) / 3
                out.append([a, a + third])
                out.append([b - third, b])
            return out

        line_length = 10.0
        level_tr = ValueTracker(0.0)

        def stack():
            L = int(round(level_tr.get_value()))
            L = max(0, min(6, L))
            grp = VGroup()
            for ell in range(L + 1):
                ints = intervals_at_level(ell)
                y = 2.0 - ell * 0.8
                col = interpolate_color(BLUE, RED, ell / 6)
                for (a, b) in ints:
                    start = np.array([a * line_length - line_length / 2, y, 0])
                    end = np.array([b * line_length - line_length / 2, y, 0])
                    grp.add(Line(start, end, color=col, stroke_width=5))
                # Level label
                grp.add(Tex(rf"$C_{{{ell}}}$", font_size=20, color=col).move_to(
                    [-line_length / 2 - 0.6, y, 0]))
            return grp

        self.add(always_redraw(stack))

        # Info
        def L_now():
            return max(0, min(6, int(round(level_tr.get_value()))))

        info = VGroup(
            VGroup(Tex(r"level $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"intervals $=2^L=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"total length $=(2/3)^L=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"limit: uncountable, measure 0",
                color=YELLOW, font_size=20),
            Tex(r"dim $=\log 2/\log 3\approx 0.6309$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(L_now()))
        info[1][1].add_updater(lambda m: m.set_value(2 ** L_now()))
        info[2][1].add_updater(lambda m: m.set_value((2 / 3) ** L_now()))
        self.add(info)

        for L in range(1, 7):
            self.play(level_tr.animate.set_value(float(L)),
                      run_time=0.9, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
