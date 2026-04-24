from manim import *
import numpy as np


class HouseholderReflectionExample(Scene):
    """
    Householder reflection: H = I − 2 u uᵀ / (uᵀu) reflects vectors
    across the hyperplane perpendicular to u. Apply H to reflect a
    GREEN source vector onto the x-axis via choice u = a ± |a|·e_1.

    SINGLE_FOCUS: NumberPlane. GREEN arrow a moves; ValueTracker t_tr
    animates applying H by linearly interpolating between a and Ha.
    always_redraw dashed perpendicular, reflection line, u arrow.
    """

    def construct(self):
        title = Tex(r"Householder: $H=I-\tfrac{2uu^T}{u^Tu}$ reflects across $u^\perp$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                            x_length=8, y_length=5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.2)
        self.play(Create(plane))

        configs = [np.array([2.5, 1.8]),
                   np.array([1.8, -2.1]),
                   np.array([-2.0, 1.3]),
                   np.array([2.8, 0.4])]

        idx_tr = ValueTracker(0.0)
        t_tr = ValueTracker(0.0)

        def a_vec():
            i = int(idx_tr.get_value())
            frac = idx_tr.get_value() - i
            i2 = min(len(configs) - 1, i + 1)
            return (1 - frac) * configs[i] + frac * configs[i2]

        def u_vec():
            a = a_vec()
            sign = 1.0 if a[0] >= 0 else -1.0
            return a + sign * np.linalg.norm(a) * np.array([1.0, 0.0])

        def Ha():
            a = a_vec()
            u = u_vec()
            return a - 2 * np.dot(u, a) / np.dot(u, u) * u

        def current():
            t = t_tr.get_value()
            return (1 - t) * a_vec() + t * Ha()

        def a_arrow():
            v = a_vec()
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=GREEN, buff=0, stroke_width=4)

        def h_arrow():
            v = current()
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=YELLOW, buff=0, stroke_width=4)

        def u_arrow():
            u = u_vec()
            un = u / np.linalg.norm(u) * 2.8
            return Arrow(plane.c2p(0, 0), plane.c2p(un[0], un[1]),
                          color=RED, buff=0, stroke_width=3)

        def u_perp_line():
            u = u_vec()
            un = u / np.linalg.norm(u)
            perp = np.array([-un[1], un[0]]) * 3.5
            return DashedLine(plane.c2p(-perp[0], -perp[1]),
                              plane.c2p(perp[0], perp[1]),
                              color=BLUE, stroke_width=2)

        self.add(always_redraw(u_perp_line), always_redraw(u_arrow),
                 always_redraw(a_arrow), always_redraw(h_arrow))

        # Labels
        lbl_a = always_redraw(lambda: Tex(r"$a$", color=GREEN, font_size=24).next_to(
            plane.c2p(*a_vec()), UP, buff=0.1))
        lbl_Ha = always_redraw(lambda: Tex(r"$Ha$", color=YELLOW, font_size=24).next_to(
            plane.c2p(*current()), UP, buff=0.1))
        lbl_u = always_redraw(lambda: Tex(r"$u$", color=RED, font_size=22).next_to(
            plane.c2p(*(u_vec() / np.linalg.norm(u_vec()) * 2.8)), UP, buff=0.1))
        self.add(lbl_a, lbl_Ha, lbl_u)

        # Info
        info = VGroup(
            Tex(r"$u=a+\mathrm{sign}(a_1)|a|e_1$", font_size=22),
            Tex(r"$Ha=\pm|a|e_1$", color=YELLOW, font_size=22),
            VGroup(Tex(r"$|a|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$|Ha|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"used for QR factorization",
                color=BLUE, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.3)
        info[2][1].add_updater(lambda m: m.set_value(float(np.linalg.norm(a_vec()))))
        info[3][1].add_updater(lambda m: m.set_value(float(np.linalg.norm(current()))))
        self.add(info)

        # Tour configs, reflecting each
        for k in range(len(configs)):
            self.play(idx_tr.animate.set_value(float(k)), run_time=0.8)
            self.wait(0.2)
            self.play(t_tr.animate.set_value(1.0),
                      run_time=1.2, rate_func=smooth)
            self.wait(0.3)
            self.play(t_tr.animate.set_value(0.0),
                      run_time=0.4, rate_func=smooth)
        self.wait(0.5)
