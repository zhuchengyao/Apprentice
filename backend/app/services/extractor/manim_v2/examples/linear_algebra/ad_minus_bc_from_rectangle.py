from manim import *
import numpy as np


class AdMinusBcFromRectangleExample(Scene):
    """
    Derive det=ad-bc formula by specializing to diagonal (b=c=0):
    In that case columns are (a, 0) and (0, d), forming an axis-aligned
    rectangle of area a·d. Then show -bc correction.

    SINGLE_FOCUS: ValueTracker b_tr, c_tr sweep b and c from 0 to
    nonzero values; formula "a·d" updates to "ad - bc".
    """

    def construct(self):
        title = Tex(r"Derive $\det=ad-bc$: start from diagonal ($b=c=0$)",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-1, 5, 1], y_range=[-1, 4, 1],
                            x_length=8, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        a_val, d_val = 3.0, 2.0
        bc_tr = ValueTracker(0.0)  # 0 → b=c=0; 1 → b, c at target values

        b_target, c_target = 1.5, 0.8

        def cols():
            s = bc_tr.get_value()
            return np.array([a_val, c_target * s]), np.array([b_target * s, d_val])

        def parallelogram():
            v1, v2 = cols()
            pts = [plane.c2p(*p) for p in [np.zeros(2), v1, v1 + v2, v2]]
            return Polygon(*pts, color=YELLOW, stroke_width=3,
                            fill_color=YELLOW, fill_opacity=0.4)

        def v1_arrow():
            v1, _ = cols()
            return Arrow(plane.c2p(0, 0), plane.c2p(v1[0], v1[1]),
                          color=GREEN, buff=0, stroke_width=5)

        def v2_arrow():
            _, v2 = cols()
            return Arrow(plane.c2p(0, 0), plane.c2p(v2[0], v2[1]),
                          color=RED, buff=0, stroke_width=5)

        self.add(always_redraw(parallelogram), always_redraw(v1_arrow), always_redraw(v2_arrow))

        # Dynamic formula
        def formula_str():
            s = bc_tr.get_value()
            b = s * b_target
            c = s * c_target
            det = a_val * d_val - b * c
            if s < 0.05:
                return rf"$\det=a\cdot d={a_val:.0f}\cdot{d_val:.0f}={a_val * d_val:.1f}$"
            return rf"$\det=ad-bc={a_val:.0f}\cdot{d_val:.0f}-{b:.2f}\cdot{c:.2f}={det:.3f}$"

        formula_tex = Tex(formula_str(), color=YELLOW, font_size=26).to_edge(DOWN, buff=0.3)
        self.add(formula_tex)
        def update_formula(mob, dt):
            new = Tex(formula_str(), color=YELLOW, font_size=26).move_to(formula_tex)
            formula_tex.become(new)
            return formula_tex
        formula_tex.add_updater(update_formula)

        info = VGroup(
            VGroup(Tex(r"$a=3, d=2$; $b=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(RED),
                   Tex(r", $c=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.05),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(bc_tr.get_value() * b_target))
        info[0][3].add_updater(lambda m: m.set_value(bc_tr.get_value() * c_target))
        self.add(info)

        self.play(bc_tr.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(0.8)
