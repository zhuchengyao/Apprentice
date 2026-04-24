from manim import *
import numpy as np


class IncircleExcirclesTriangleExample(Scene):
    """
    Every triangle has one inscribed circle (incircle) and three
    escribed circles (excircles), each tangent to one side and the
    extensions of the other two.

    SINGLE_FOCUS: ValueTracker s_tr morphs ABC through 4 configs;
    always_redraw recomputes incircle (GREEN) + 3 excircles (BLUE/
    RED/ORANGE) with tangent points. Uses formulas:
      r = Area/s (s=semi-perimeter), r_A = Area/(s-a), ...
      incenter I = (a·A+b·B+c·C)/(a+b+c)
      excenter I_A = (-a·A + b·B + c·C)/(-a+b+c)
    """

    def construct(self):
        title = Tex(r"Incircle + 3 excircles of a triangle",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        configs = [
            (np.array([-2.8, -1.4, 0]), np.array([2.6, -1.4, 0]), np.array([-1.0, 1.7, 0])),
            (np.array([-2.5, -1.3, 0]), np.array([2.5, -1.3, 0]), np.array([0.0, 2.0, 0])),
            (np.array([-2.8, -1.4, 0]), np.array([2.6, -1.4, 0]), np.array([2.0, 1.9, 0])),
            (np.array([-2.4, -1.2, 0]), np.array([2.4, -1.2, 0]), np.array([-0.4, 2.2, 0])),
        ]

        s_tr = ValueTracker(0.0)

        def ABC():
            s = s_tr.get_value()
            k = int(s)
            frac = s - k
            k_next = min(k + 1, len(configs) - 1)
            return [(1 - frac) * configs[k][i] + frac * configs[k_next][i]
                    for i in range(3)]

        def circle_of(center, r, color, stroke):
            return Circle(radius=r, color=color, stroke_width=stroke,
                          fill_color=color, fill_opacity=0.08).move_to(center)

        def build():
            A, B, C = ABC()
            a = np.linalg.norm(B - C)
            b = np.linalg.norm(C - A)
            c = np.linalg.norm(A - B)
            s = (a + b + c) / 2
            area = 0.5 * abs((B[0] - A[0]) * (C[1] - A[1])
                              - (C[0] - A[0]) * (B[1] - A[1]))
            r_in = area / s
            I = (a * A + b * B + c * C) / (a + b + c)
            r_A = area / (s - a)
            I_A = (-a * A + b * B + c * C) / (-a + b + c)
            r_B = area / (s - b)
            I_B = (a * A - b * B + c * C) / (a - b + c)
            r_C = area / (s - c)
            I_C = (a * A + b * B - c * C) / (a + b - c)

            tri = Polygon(A, B, C, color=YELLOW, stroke_width=3)
            inc = circle_of(I, r_in, GREEN, 3)
            ex_A = circle_of(I_A, r_A, BLUE, 2)
            ex_B = circle_of(I_B, r_B, RED, 2)
            ex_C = circle_of(I_C, r_C, ORANGE, 2)

            centers = VGroup(
                Dot(I, color=GREEN, radius=0.06),
                Dot(I_A, color=BLUE, radius=0.06),
                Dot(I_B, color=RED, radius=0.06),
                Dot(I_C, color=ORANGE, radius=0.06),
            )

            # Extensions of sides (rays) for excircle tangency visualization
            def extended(P, Q):
                d = Q - P
                return Line(P - 3 * d, Q + 3 * d, color=GREY_D,
                             stroke_width=1, stroke_opacity=0.5)

            rays = VGroup(extended(A, B), extended(B, C), extended(C, A))

            return VGroup(rays, tri, inc, ex_A, ex_B, ex_C, centers)

        self.add(always_redraw(build))

        def props():
            A, B, C = ABC()
            a = np.linalg.norm(B - C)
            b = np.linalg.norm(C - A)
            c = np.linalg.norm(A - B)
            s = (a + b + c) / 2
            area = 0.5 * abs((B[0] - A[0]) * (C[1] - A[1])
                              - (C[0] - A[0]) * (B[1] - A[1]))
            return a, b, c, s, area, area / s

        info = VGroup(
            VGroup(Tex(r"$a=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$b=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$c=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"area $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$r=\frac{\mathrm{area}}{s}=$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DL, buff=0.3)

        info[0][1].add_updater(lambda m: m.set_value(props()[0]))
        info[1][1].add_updater(lambda m: m.set_value(props()[1]))
        info[2][1].add_updater(lambda m: m.set_value(props()[2]))
        info[3][1].add_updater(lambda m: m.set_value(props()[4]))
        info[4][1].add_updater(lambda m: m.set_value(props()[5]))
        self.add(info)

        for k in range(1, len(configs)):
            self.play(s_tr.animate.set_value(float(k)),
                      run_time=2.2, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
