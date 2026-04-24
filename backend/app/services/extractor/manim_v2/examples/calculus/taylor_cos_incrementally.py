from manim import *
import numpy as np
from math import factorial


class TaylorCosIncrementallyExample(Scene):
    """
    Build Taylor series for cos(x) around 0 by adding terms:
      P_0 = 1
      P_2 = 1 - x²/2
      P_4 = 1 - x²/2 + x⁴/24
      P_6 = 1 - x²/2 + x⁴/24 - x⁶/720
    Each added term improves approximation near 0.
    """

    def construct(self):
        title = Tex(r"Build Taylor series for $\cos x$ incrementally",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-PI, PI, PI / 2], y_range=[-2.5, 2, 1],
                    x_length=9, y_length=4.5,
                    axis_config={"include_numbers": True, "font_size": 14}
                    ).shift(DOWN * 0.3)
        self.play(Create(axes))

        cos_curve = axes.plot(np.cos, x_range=[-PI, PI], color=BLUE, stroke_width=3)
        self.add(cos_curve)
        self.add(Tex(r"$\cos x$", color=BLUE, font_size=22).next_to(axes, UP, buff=0.1).shift(LEFT * 3))

        order_tr = ValueTracker(0.0)  # 0 for P_0, 1 for P_2, 2 for P_4, 3 for P_6

        def P(x, order):
            result = 0.0
            for k in range(order + 1):
                result += (-1) ** k * x ** (2 * k) / factorial(2 * k)
            return result

        def n_now():
            return max(0, min(3, int(round(order_tr.get_value()))))

        def approx_curve():
            n = n_now()
            return axes.plot(lambda x: P(x, n), x_range=[-PI, PI],
                             color=YELLOW, stroke_width=3)

        self.add(always_redraw(approx_curve))

        # Term list
        def term_list():
            n = n_now()
            terms = [
                r"$1$",
                r"$1-\tfrac{x^2}{2}$",
                r"$1-\tfrac{x^2}{2}+\tfrac{x^4}{24}$",
                r"$1-\tfrac{x^2}{2}+\tfrac{x^4}{24}-\tfrac{x^6}{720}$",
            ]
            return Tex(terms[n], color=YELLOW, font_size=26).to_edge(DOWN, buff=0.5)

        terms_tex = term_list()
        self.add(terms_tex)
        def update_terms(mob, dt):
            new = term_list().move_to(terms_tex)
            terms_tex.become(new)
            return terms_tex
        terms_tex.add_updater(update_terms)

        info = VGroup(
            VGroup(Tex(r"order $2n=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(2 * n_now()))
        self.add(info)

        for n in [1, 2, 3]:
            self.play(order_tr.animate.set_value(float(n)),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
