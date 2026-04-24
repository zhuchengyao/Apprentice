from manim import *
import numpy as np


class StarsAndBarsExample(Scene):
    """
    Stars and bars: number of ways to distribute n identical objects
    into k bins = C(n + k − 1, k − 1).

    Example: n=5 stars in k=3 bins → C(7, 2) = 21 distributions.

    SINGLE_FOCUS: 21 layouts of 5 stars separated by 2 bars drawn
    sequentially via ValueTracker idx_tr; always_redraw shows current
    arrangement. Running count + formula.
    """

    def construct(self):
        title = Tex(r"Stars and bars: $n=5$ stars in $k=3$ bins $= \binom{7}{2}=21$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Generate all 21 compositions of 5 into 3 parts
        arrangements = []
        for a in range(6):
            for b in range(6 - a):
                c = 5 - a - b
                arrangements.append((a, b, c))
        # Should have 21
        assert len(arrangements) == 21

        idx_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(len(arrangements) - 1, int(round(idx_tr.get_value()))))

        def layout():
            a, b, c = arrangements[k_now()]
            origin = np.array([-3.5, 0.5, 0])
            spacing = 0.55
            grp = VGroup()
            pos = 0
            for count, (n_stars, color) in enumerate([(a, BLUE), (b, GREEN), (c, ORANGE)]):
                for _ in range(n_stars):
                    star = Star(n=5, color=color, fill_color=color,
                                 fill_opacity=0.9).scale(0.18).move_to(
                        origin + RIGHT * pos * spacing)
                    grp.add(star)
                    pos += 1
                if count < 2:
                    bar = Line(origin + RIGHT * pos * spacing + UP * 0.3,
                                origin + RIGHT * pos * spacing + DOWN * 0.3,
                                color=RED, stroke_width=4)
                    grp.add(bar)
                    pos += 1
            return grp

        self.add(always_redraw(layout))

        # Decomposition label
        def arrange_str():
            a, b, c = arrangements[k_now()]
            return rf"$({a}, {b}, {c})$"

        arr_tex = Tex(arrange_str(), font_size=30, color=YELLOW).next_to(
            np.array([-3.5, 0.5, 0]) + DOWN * 1.2, DOWN, buff=0)
        self.add(arr_tex)
        def update_arr(mob, dt):
            new = Tex(arrange_str(), font_size=30, color=YELLOW).move_to(arr_tex)
            arr_tex.become(new)
            return arr_tex
        arr_tex.add_updater(update_arr)

        info = VGroup(
            VGroup(Tex(r"arrangement $\#$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"ways $=\binom{n+k-1}{k-1}$",
                font_size=22),
            Tex(r"$=\binom{7}{2}=21$",
                color=GREEN, font_size=22),
            Tex(r"2 bars separate 3 bins",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(k_now() + 1))
        self.add(info)

        self.play(idx_tr.animate.set_value(float(len(arrangements) - 1)),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
