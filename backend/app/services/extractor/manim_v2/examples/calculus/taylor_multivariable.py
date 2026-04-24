from manim import *
import numpy as np


class TaylorMultivariableExample(Scene):
    """
    2D Taylor expansion of f(x, y) = sin(x) cos(y) around (0, 0):
       f ≈ x − x³/6 − x y²/2 + O(4) = x − x·y²/2 − x³/6 + ...

    TWO_COLUMN: LEFT 2D heatmap of true f vs k-th order Taylor
    expansion via ValueTracker order_tr (k ∈ {1, 3, 5}). RIGHT shows
    sup-norm error.
    """

    def construct(self):
        title = Tex(r"Taylor 2D: $f(x,y)=\sin x\cos y$ around $(0,0)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                    x_length=5.0, y_length=4.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(axes))

        def f_true(x, y):
            return np.sin(x) * np.cos(y)

        def taylor(x, y, order):
            # sin x = x - x³/6 + x⁵/120 - ...
            # cos y = 1 - y²/2 + y⁴/24 - ...
            if order == 1:
                return x * 1
            if order == 3:
                sx = x - x ** 3 / 6
                cy = 1 - y ** 2 / 2
                # keep terms up to order 3
                # sx * cy = x + (terms order >=4 from cross products with y)
                # Taylor of sin(x) cos(y) up to degree 3: x - x³/6 - x y²/2
                return x - x ** 3 / 6 - x * y ** 2 / 2
            if order == 5:
                # add x⁵/120, x³ y²/12, x y⁴/24
                return (x - x ** 3 / 6 - x * y ** 2 / 2
                        + x ** 5 / 120 + x ** 3 * y ** 2 / 12 + x * y ** 4 / 24)
            return 0

        order_tr = ValueTracker(1.0)

        def order_now():
            return max(1, min(5, int(round(order_tr.get_value()))))

        # Heatmap
        nx, ny = 20, 20
        xs = np.linspace(-1.9, 1.9, nx)
        ys = np.linspace(-1.9, 1.9, ny)
        cell_w = axes.x_length / nx
        cell_h = axes.y_length / ny

        def heatmap():
            order = order_now()
            grp = VGroup()
            for j, y in enumerate(ys):
                for i, x in enumerate(xs):
                    # Show error
                    err = taylor(x, y, order) - f_true(x, y)
                    if err >= 0:
                        col = interpolate_color(BLACK, GREEN, min(1, abs(err) * 3))
                    else:
                        col = interpolate_color(BLACK, RED, min(1, abs(err) * 3))
                    rect = Rectangle(width=cell_w * 1.05,
                                      height=cell_h * 1.05,
                                      color=col, stroke_width=0,
                                      fill_color=col, fill_opacity=0.85)
                    rect.move_to(axes.c2p(x, y))
                    grp.add(rect)
            return grp

        self.add(always_redraw(heatmap))

        def sup_err():
            order = order_now()
            xs_fine = np.linspace(-1.5, 1.5, 20)
            ys_fine = np.linspace(-1.5, 1.5, 20)
            errs = [abs(taylor(x, y, order) - f_true(x, y))
                    for x in xs_fine for y in ys_fine]
            return float(max(errs))

        info = VGroup(
            VGroup(Tex(r"order $k=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"sup-error on $[-1.5, 1.5]^2=$", font_size=20),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=20).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"$k=1$: $f\approx x$",
                color=BLUE, font_size=20),
            Tex(r"$k=3$: $f\approx x-\frac{x^3}{6}-\frac{xy^2}{2}$",
                color=GREEN, font_size=20),
            Tex(r"$k=5$: extra quintic terms",
                color=ORANGE, font_size=20),
            Tex(r"GREEN: Taylor $>$ true, RED: Taylor $<$ true",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(order_now()))
        info[1][1].add_updater(lambda m: m.set_value(sup_err()))
        self.add(info)

        for target in [3, 5, 1]:
            self.play(order_tr.animate.set_value(float(target)),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
