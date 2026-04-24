from manim import *
import numpy as np


class BoxCountingDimensionExample(Scene):
    """
    Box-counting dimension: d = lim (log N(ε)) / log(1/ε) where
    N(ε) is min # boxes of side ε needed to cover the set.
    For Koch curve: d = log 4 / log 3 ≈ 1.262.

    TWO_COLUMN: LEFT Koch curve at depth 4 overlaid with box grid;
    ValueTracker eps_tr shrinks box size. RIGHT log-log plot of
    N vs 1/ε approaches slope d = 1.262.
    """

    def construct(self):
        title = Tex(r"Box-counting dim: $d=\lim\frac{\log N(\epsilon)}{\log (1/\epsilon)}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Left: draw Koch curve depth 4
        def koch_points(p1, p2, depth):
            if depth == 0:
                return [p1, p2]
            p1, p2 = np.asarray(p1, dtype=float), np.asarray(p2, dtype=float)
            d = p2 - p1
            q1 = p1 + d / 3
            q3 = p1 + 2 * d / 3
            perp = np.array([-d[1], d[0], 0]) / 3
            q2 = q1 + 0.5 * (q3 - q1) + perp * np.sqrt(3) / 2
            out = []
            out += koch_points(p1, q1, depth - 1)[:-1]
            out += koch_points(q1, q2, depth - 1)[:-1]
            out += koch_points(q2, q3, depth - 1)[:-1]
            out += koch_points(q3, p2, depth - 1)
            return out

        # Scale
        left_center = LEFT * 2.5 + DOWN * 0.3
        P1 = left_center + np.array([-2.2, -1.2, 0])
        P2 = left_center + np.array([2.2, -1.2, 0])
        koch_pts = koch_points(P1, P2, 4)

        koch_curve = VMobject().set_points_as_corners(koch_pts).set_color(BLUE).set_stroke(width=2.5)
        self.add(koch_curve)

        eps_tr = ValueTracker(0.8)

        def eps_val():
            return eps_tr.get_value()

        def box_grid():
            eps = eps_val()
            # Overlay grid and count boxes intersecting Koch curve
            xs = np.arange(-2.5, 2.5, eps)
            ys = np.arange(-1.5, 1.5, eps)
            grp = VGroup()
            koch_arr = np.array([[p[0], p[1]] for p in koch_pts])
            ref_x = left_center[0]
            ref_y = left_center[1]
            for xi in xs:
                for yi in ys:
                    # Check if any point of koch is in this box
                    gx = xi + ref_x
                    gy = yi + ref_y
                    inside = np.any((koch_arr[:, 0] >= gx) & (koch_arr[:, 0] < gx + eps)
                                     & (koch_arr[:, 1] >= gy) & (koch_arr[:, 1] < gy + eps))
                    if inside:
                        rect = Rectangle(width=eps, height=eps,
                                          color=ORANGE, stroke_width=1,
                                          fill_color=ORANGE,
                                          fill_opacity=0.25).move_to(
                            np.array([gx + eps / 2, gy + eps / 2, 0]))
                        grp.add(rect)
            return grp

        self.add(always_redraw(box_grid))

        def count_N():
            eps = eps_val()
            koch_arr = np.array([[p[0], p[1]] for p in koch_pts])
            ref_x = left_center[0]
            ref_y = left_center[1]
            xs = np.arange(-2.5, 2.5, eps)
            ys = np.arange(-1.5, 1.5, eps)
            n = 0
            for xi in xs:
                for yi in ys:
                    gx = xi + ref_x
                    gy = yi + ref_y
                    inside = np.any((koch_arr[:, 0] >= gx) & (koch_arr[:, 0] < gx + eps)
                                     & (koch_arr[:, 1] >= gy) & (koch_arr[:, 1] < gy + eps))
                    if inside:
                        n += 1
            return n

        # RIGHT: log-log plot
        ax_right = Axes(x_range=[0, 4, 1], y_range=[0, 5, 1],
                        x_length=4.2, y_length=4.0,
                        axis_config={"include_numbers": True,
                                     "font_size": 14}
                        ).shift(RIGHT * 3.2 + DOWN * 0.3)
        self.add(ax_right)
        self.add(Tex(r"$\log N$ vs $\log (1/\epsilon)$", font_size=20).next_to(
            ax_right, UP, buff=0.15))
        # Reference slope line with d = log 4/log 3
        d_theory = np.log(4) / np.log(3)
        self.add(ax_right.plot(lambda x: d_theory * x + 0.5,
                                 x_range=[0.5, 4], color=GREEN,
                                 stroke_width=2))
        self.add(Tex(rf"slope $={d_theory:.3f}$",
                     color=GREEN, font_size=20).next_to(ax_right.c2p(4, 4), UR, buff=0.1))

        # Track points across runs in RED
        history_pts = []

        def history_dots():
            grp = VGroup()
            for (le, ln) in history_pts:
                grp.add(Dot(ax_right.c2p(le, ln), color=RED, radius=0.07))
            return grp

        self.add(always_redraw(history_dots))

        info = VGroup(
            VGroup(Tex(r"$\epsilon=$", font_size=22),
                   DecimalNumber(0.8, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$N(\epsilon)=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DL, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(eps_val()))
        info[1][1].add_updater(lambda m: m.set_value(count_N()))
        self.add(info)

        for eps_val_target in [0.5, 0.3, 0.18, 0.1, 0.06]:
            self.play(eps_tr.animate.set_value(eps_val_target),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.3)
            # Log-log point
            history_pts.append((np.log(1 / eps_val_target), np.log(count_N())))
        self.wait(0.8)
