from manim import *
import numpy as np


class KochSnowflakeDimensionExample(Scene):
    """
    Koch snowflake fractal dimension: d = log 4 / log 3 ≈ 1.262.
    At iteration n, the curve has 4^n segments of length (1/3)^n
    per original side. Total length = 3 · 4^n · (1/3)^n → ∞.
    Enclosed area → 2√3/5 (finite).

    SINGLE_FOCUS: ValueTracker level_tr steps 0..5. always_redraw
    builds full snowflake via Koch rules on initial equilateral triangle.
    """

    def construct(self):
        title = Tex(r"Koch snowflake: $d=\log 4/\log 3\approx 1.2619$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def koch_curve(p1, p2, depth):
            """Return list of points for Koch curve between p1, p2 at given depth."""
            if depth == 0:
                return [p1, p2]
            p1 = np.asarray(p1, dtype=float)
            p2 = np.asarray(p2, dtype=float)
            d = p2 - p1
            q1 = p1 + d / 3
            q3 = p1 + 2 * d / 3
            # Bump point: q1 + rotated perpendicular
            perp = np.array([-d[1], d[0], 0]) / 3
            q2 = q1 + 0.5 * (q3 - q1) + perp * np.sqrt(3) / 2
            # recursion
            out = []
            out += koch_curve(p1, q1, depth - 1)[:-1]
            out += koch_curve(q1, q2, depth - 1)[:-1]
            out += koch_curve(q2, q3, depth - 1)[:-1]
            out += koch_curve(q3, p2, depth - 1)
            return out

        s = 3.6  # side length
        h = s * np.sqrt(3) / 2
        A_pt = np.array([-s / 2, -h / 3, 0])
        B_pt = np.array([s / 2, -h / 3, 0])
        C_pt = np.array([0, 2 * h / 3, 0])

        level_tr = ValueTracker(0.0)

        def snowflake():
            level = int(round(level_tr.get_value()))
            level = max(0, min(5, level))
            pts = []
            pts += koch_curve(A_pt, B_pt, level)[:-1]
            pts += koch_curve(B_pt, C_pt, level)[:-1]
            pts += koch_curve(C_pt, A_pt, level)
            return VMobject().set_points_as_corners(pts).set_color(BLUE).set_stroke(width=2.5)

        self.add(always_redraw(snowflake))

        # Info
        def level_now():
            return max(0, min(5, int(round(level_tr.get_value()))))

        def perim():
            lvl = level_now()
            return 3 * s * (4 / 3) ** lvl

        def area():
            lvl = level_now()
            A0 = np.sqrt(3) / 4 * s ** 2
            if lvl == 0:
                return A0
            total = A0 + A0 * (1 / 3) * sum((4 / 9) ** k for k in range(lvl))
            return total

        info = VGroup(
            VGroup(Tex(r"level $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"perimeter $=3s(4/3)^n=$", font_size=22),
                   DecimalNumber(10.8, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"area $\to \frac{2\sqrt 3}{5}s^2$", font_size=22),
                    ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"area $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$d=\log 4/\log 3\approx 1.2619$",
                color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(level_now()))
        info[1][1].add_updater(lambda m: m.set_value(perim()))
        info[3][1].add_updater(lambda m: m.set_value(area()))
        self.add(info)

        for lvl in range(1, 6):
            self.play(level_tr.animate.set_value(float(lvl)),
                      run_time=1.3, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
