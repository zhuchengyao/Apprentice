from manim import *
import numpy as np


def koch_polys(depth, a, b):
    """Build the polyline of the Koch curve from a to b at given depth."""
    if depth == 0:
        return [a, b]
    direction = b - a
    one_third = a + direction / 3
    two_third = a + 2 * direction / 3
    # Bump apex perpendicular outward
    perp = np.array([-direction[1], direction[0], 0])
    perp = perp / np.linalg.norm(perp)
    apex = (one_third + two_third) / 2 + perp * np.linalg.norm(direction) * np.sqrt(3) / 6
    pts1 = koch_polys(depth - 1, a, one_third)
    pts2 = koch_polys(depth - 1, one_third, apex)
    pts3 = koch_polys(depth - 1, apex, two_third)
    pts4 = koch_polys(depth - 1, two_third, b)
    return pts1[:-1] + pts2[:-1] + pts3[:-1] + pts4


class FractalDimensionExample(Scene):
    """
    Box-counting on the Koch curve: log-log plot of #boxes vs box size.

    TWO_COLUMN:
      LEFT  — Koch curve at depth 4 with overlaid grid; ValueTracker
              box_pow controls box size = 1/2^box_pow. Each frame, the
              boxes that intersect the curve are highlighted.
      RIGHT — log-log plot of N(s) vs 1/s as s shrinks; the slope =
              fractal dimension d ≈ log(4)/log(3) ≈ 1.262.
    """

    def construct(self):
        title = Tex(r"Box-counting dimension: $d = \dfrac{\log N(\varepsilon)}{\log(1/\varepsilon)}$",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Build Koch curve at depth 4
        a = np.array([-2.5, 0.0, 0])
        b = np.array([+2.5, 0.0, 0])
        pts = koch_polys(4, a, b)
        # Center vertically
        koch_pts = [p + np.array([-1.5, +0.4, 0]) for p in pts]
        koch = VMobject(color=BLUE, stroke_width=2)
        koch.set_points_as_corners(koch_pts)
        self.play(Create(koch))

        # Box overlays: ValueTracker box_pow ∈ [0, 4] meaning side = 1/3^box_pow
        # We use 1/3^k because Koch is naturally tri-adic
        box_pow = ValueTracker(0)

        x_min, x_max = -4.0, 1.0
        y_min, y_max = -0.5, 1.5

        def boxes_grid():
            k = int(round(box_pow.get_value()))
            side = 1.0 / (3 ** k) * 2  # scale to fit display
            grp = VGroup()
            count = 0
            x = x_min
            while x < x_max:
                y = y_min
                while y < y_max:
                    # Check if any sample of koch_pts falls in this box
                    in_box = False
                    for p in koch_pts:
                        if x <= p[0] < x + side and y <= p[1] < y + side:
                            in_box = True
                            break
                    if in_box:
                        rect = Rectangle(width=side, height=side,
                                         color=YELLOW, fill_opacity=0.15,
                                         stroke_color=YELLOW, stroke_width=1)
                        rect.move_to([x + side / 2, y + side / 2, 0])
                        grp.add(rect)
                        count += 1
                    y += side
                x += side
            return grp

        self.add(always_redraw(boxes_grid))

        # RIGHT COLUMN: log-log plot
        rcol_x = +4.4

        # Precomputed N values for box_pow = 0, 1, 2, 3, 4
        # Theoretical: N grows like 4^k for s = (1/3)^k, so log4 / log3 ≈ 1.26
        N_values = [3, 8, 22, 76, 290]  # approximate counts
        eps_values = [(1 / 3) ** k for k in range(len(N_values))]

        log_axes = Axes(
            x_range=[-3.5, 0.5, 1], y_range=[0, 7, 1],
            x_length=3.0, y_length=2.4,
            axis_config={"include_tip": False, "include_numbers": True, "font_size": 14},
        ).move_to([rcol_x, +0.4, 0])
        x_lbl = Tex(r"$\log(1/\varepsilon)$", color=GREY_B,
                    font_size=18).next_to(log_axes, DOWN, buff=0.05)
        y_lbl = Tex(r"$\log N$", color=GREY_B,
                    font_size=18).next_to(log_axes, LEFT, buff=0.05)
        self.play(Create(log_axes), Write(x_lbl), Write(y_lbl))

        # Plot points and best-fit line
        log_pts = [(np.log(1 / e), np.log(N)) for e, N in zip(eps_values, N_values)]
        scatter = VGroup(*[
            Dot(log_axes.c2p(x, y), color=YELLOW, radius=0.07)
            for x, y in log_pts
        ])
        # Line slope = log(4)/log(3) ≈ 1.262
        slope = np.log(4) / np.log(3)
        intercept = log_pts[0][1] - slope * log_pts[0][0]
        fit_line = log_axes.plot(lambda x: slope * x + intercept,
                                 x_range=[-3.5, 0.5], color=GREEN)
        slope_lbl = MathTex(rf"d \approx \tfrac{{\log 4}}{{\log 3}} \approx 1.262",
                            color=GREEN, font_size=20).next_to(log_axes, UP, buff=0.1)
        self.play(FadeIn(scatter), Create(fit_line), Write(slope_lbl))

        def box_counter():
            k = int(round(box_pow.get_value()))
            return MathTex(rf"\varepsilon = 1/3^{{{k}}},\ N \approx {N_values[min(k, len(N_values)-1)]}",
                           color=YELLOW, font_size=22).move_to([rcol_x, -1.6, 0])

        self.add(always_redraw(box_counter))

        # Step through box_pow
        for k in range(1, 5):
            self.play(box_pow.animate.set_value(k),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.5)

        self.wait(0.6)
