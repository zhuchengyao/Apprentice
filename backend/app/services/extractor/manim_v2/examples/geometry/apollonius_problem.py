from manim import *
import numpy as np


class ApolloniusProblemExample(Scene):
    """
    Apollonius' problem: find all circles tangent to 3 given circles.
    For simple config with 3 mutually tangent circles, there are 2
    solution circles — "inner" Soddy circle (tangent internally to
    all 3) and "outer" Soddy circle.

    Descartes' circle theorem:
      (k_1 + k_2 + k_3 + k_4)² = 2(k_1² + k_2² + k_3² + k_4²).

    3 fixed circles with radii 2, 2, 1.5 arranged so they're mutually
    tangent. ValueTracker reveals inner + outer Soddy circles.
    """

    def construct(self):
        title = Tex(r"Apollonius: Soddy circles from Descartes' $(\sum k)^2=2\sum k^2$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 3 mutually tangent circles: use radii r1=2, r2=2, r3=1.5
        r1, r2, r3 = 2.0, 2.0, 1.5
        # Compute centers so circles are externally tangent
        # Use triangle with side lengths r_i+r_j
        a12 = r1 + r2
        a13 = r1 + r3
        a23 = r2 + r3
        C1 = np.array([-a12 / 2, -0.5, 0])
        C2 = np.array([a12 / 2, -0.5, 0])
        # C3: intersection of circles radius a13 around C1 and a23 around C2
        d = a12
        x = (a13 ** 2 - a23 ** 2 + d ** 2) / (2 * d)
        y = np.sqrt(max(0, a13 ** 2 - x ** 2))
        C3 = C1 + np.array([x, y, 0])

        # Scale to fit
        scale = 0.85
        C1 *= scale; C2 *= scale; C3 *= scale
        r1 *= scale; r2 *= scale; r3 *= scale

        c1 = Circle(radius=r1, color=BLUE, stroke_width=3).move_to(C1)
        c2 = Circle(radius=r2, color=GREEN, stroke_width=3).move_to(C2)
        c3 = Circle(radius=r3, color=ORANGE, stroke_width=3).move_to(C3)
        self.play(Create(c1), Create(c2), Create(c3))

        # Descartes' theorem: k_4 = k_1 + k_2 + k_3 ± 2√(k_1 k_2 + k_2 k_3 + k_3 k_1)
        k1, k2, k3 = 1 / r1, 1 / r2, 1 / r3
        disc = k1 * k2 + k2 * k3 + k3 * k1
        k4_plus = k1 + k2 + k3 + 2 * np.sqrt(disc)
        k4_minus = k1 + k2 + k3 - 2 * np.sqrt(disc)
        r4_plus = 1 / k4_plus    # inner (smaller)
        r4_minus = 1 / abs(k4_minus) if k4_minus != 0 else None
        sign_minus = np.sign(k4_minus)

        # Center of Soddy circles via complex-coordinate version of theorem:
        # (k_1 z_1 + k_2 z_2 + k_3 z_3 + k_4 z_4)² = 2(k_1² z_1² + ...)
        # Solve for z_4.
        z1, z2, z3 = complex(*C1[:2]), complex(*C2[:2]), complex(*C3[:2])
        term = k1 * k2 * z1 * z2 + k2 * k3 * z2 * z3 + k3 * k1 * z3 * z1
        disc_c = 2 * np.sqrt(term)
        kz_sum = k1 * z1 + k2 * z2 + k3 * z3
        z4_plus = (kz_sum + disc_c) / k4_plus
        z4_minus = (kz_sum - disc_c) / k4_minus if k4_minus != 0 else None

        s_tr = ValueTracker(0.0)

        # Phase 1: inner Soddy grows
        def inner_soddy():
            s = s_tr.get_value()
            if s < 0.01:
                return VMobject()
            alpha = min(1.0, s / 0.5)
            return Circle(radius=r4_plus * alpha, color=YELLOW,
                          stroke_width=4, stroke_opacity=alpha,
                          fill_color=YELLOW,
                          fill_opacity=0.2 * alpha).move_to(
                np.array([z4_plus.real, z4_plus.imag, 0]))

        def outer_soddy():
            s = s_tr.get_value()
            if s < 0.5:
                return VMobject()
            alpha = min(1.0, (s - 0.5) / 0.5)
            if k4_minus < 0:
                r4 = 1 / (-k4_minus)
                return Circle(radius=r4 * alpha, color=RED,
                              stroke_width=3, stroke_opacity=alpha,
                              fill_opacity=0).move_to(
                    np.array([z4_minus.real, z4_minus.imag, 0]))
            return VMobject()

        self.add(always_redraw(inner_soddy), always_redraw(outer_soddy))

        info = VGroup(
            VGroup(Tex(r"$k_1=$", color=BLUE, font_size=22),
                   DecimalNumber(k1, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$k_2=$", color=GREEN, font_size=22),
                   DecimalNumber(k2, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$k_3=$", color=ORANGE, font_size=22),
                   DecimalNumber(k3, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$k_4^+=$", color=YELLOW, font_size=22),
                   DecimalNumber(k4_plus, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$k_4^-=$", color=RED, font_size=22),
                   DecimalNumber(k4_minus, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            Tex(r"$(\sum k)^2 = 2\sum k^2$",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DL, buff=0.3)
        self.add(info)

        self.play(s_tr.animate.set_value(1.0),
                  run_time=5, rate_func=smooth)
        self.wait(1.0)
