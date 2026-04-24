from manim import *
import numpy as np


class MorleyTrisectorTheoremExample(Scene):
    """
    Morley's theorem: the three adjacent pairs of angle trisectors of
    any triangle meet in an equilateral triangle.

    ValueTracker s_tr morphs triangle ABC through 5 configs
    (scalene, right, obtuse, nearly-equilateral, scalene again).
    always_redraw builds trisectors as rays from each vertex and
    intersects adjacent ones; the GREEN inner triangle is drawn from
    those 3 intersection points. Live readout shows its 3 side lengths
    which stay within ~1e-3 of each other.
    """

    def construct(self):
        title = Tex(r"Morley: trisectors $\Rightarrow$ equilateral",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        configs = [
            (np.array([-3.0, -1.5, 0]), np.array([3.0, -1.5, 0]),
             np.array([-1.2, 2.0, 0])),
            (np.array([-3.2, -1.6, 0]), np.array([3.0, -1.6, 0]),
             np.array([-3.2, 1.8, 0])),  # right
            (np.array([-3.0, -1.5, 0]), np.array([3.0, -1.5, 0]),
             np.array([1.6, 1.9, 0])),
            (np.array([-3.0, -1.6, 0]), np.array([3.0, -1.6, 0]),
             np.array([0.0, 2.2, 0])),
            (np.array([-2.8, -1.4, 0]), np.array([2.6, -1.7, 0]),
             np.array([-0.2, 1.9, 0])),
        ]

        A_tr = ValueTracker(0.0)

        def interp(idx):
            s = A_tr.get_value()
            k = int(s)
            frac = s - k
            k_next = min(k + 1, len(configs) - 1)
            return [(1 - frac) * configs[k][i] + frac * configs[k_next][i]
                    for i in range(3)]

        def triangle_v():
            A, B, C = interp(0)
            return Polygon(A, B, C, color=BLUE, stroke_width=4)

        def dots():
            A, B, C = interp(0)
            return VGroup(
                Dot(A, color=BLUE, radius=0.08),
                Dot(B, color=BLUE, radius=0.08),
                Dot(C, color=BLUE, radius=0.08),
            )

        def trisector_line(start, toward1, toward2, frac):
            # direction = rotate (toward1 - start) by frac * angle(toward2 - start)
            v1 = toward1 - start
            v2 = toward2 - start
            ang1 = np.arctan2(v1[1], v1[0])
            ang2 = np.arctan2(v2[1], v2[0])
            diff = ang2 - ang1
            # normalize to (-pi, pi]
            while diff > PI: diff -= 2 * PI
            while diff <= -PI: diff += 2 * PI
            ang = ang1 + frac * diff
            return start + 10 * np.array([np.cos(ang), np.sin(ang), 0.0])

        def line_intersect(p1, d1, p2, d2):
            # p + t*d ; solve p1 + t*d1 = p2 + s*d2
            A = np.array([[d1[0], -d2[0]], [d1[1], -d2[1]]])
            b = np.array([p2[0] - p1[0], p2[1] - p1[1]])
            try:
                sol = np.linalg.solve(A, b)
                return p1 + sol[0] * d1
            except np.linalg.LinAlgError:
                return (p1 + p2) / 2

        def trisectors_inner():
            A, B, C = interp(0)
            # for each vertex V the 2 trisectors split angle(V)/3 and 2·angle(V)/3
            # from edge to the CCW-adjacent edge
            # At A: adjacent edges AB and AC; split from AB toward AC by 1/3 and 2/3.
            # We need to pick sides so that "adjacent" trisectors from B & C meet.
            dA1 = trisector_line(A, B, C, 1 / 3) - A
            dA2 = trisector_line(A, B, C, 2 / 3) - A
            dB1 = trisector_line(B, C, A, 1 / 3) - B
            dB2 = trisector_line(B, C, A, 2 / 3) - B
            dC1 = trisector_line(C, A, B, 1 / 3) - C
            dC2 = trisector_line(C, A, B, 2 / 3) - C

            # Morley: the intersection of A's trisector closer to AB with
            # B's trisector closer to BA; etc.
            # trisector-A closer to AB = dA1 (since frac=1/3 is near AB)
            # trisector-B closer to BA = dB2 (far from BC means closer to BA)
            P_AB = line_intersect(A, dA1, B, dB2)
            P_BC = line_intersect(B, dB1, C, dC2)
            P_CA = line_intersect(C, dC1, A, dA2)

            ray_color = GREY_B
            rays = VGroup(
                Line(A, A + 2 * dA1 / np.linalg.norm(dA1),
                     color=ray_color, stroke_width=1.5, stroke_opacity=0.6),
                Line(A, A + 2 * dA2 / np.linalg.norm(dA2),
                     color=ray_color, stroke_width=1.5, stroke_opacity=0.6),
                Line(B, B + 2 * dB1 / np.linalg.norm(dB1),
                     color=ray_color, stroke_width=1.5, stroke_opacity=0.6),
                Line(B, B + 2 * dB2 / np.linalg.norm(dB2),
                     color=ray_color, stroke_width=1.5, stroke_opacity=0.6),
                Line(C, C + 2 * dC1 / np.linalg.norm(dC1),
                     color=ray_color, stroke_width=1.5, stroke_opacity=0.6),
                Line(C, C + 2 * dC2 / np.linalg.norm(dC2),
                     color=ray_color, stroke_width=1.5, stroke_opacity=0.6),
            )
            inner = Polygon(P_AB, P_BC, P_CA,
                            color=GREEN, stroke_width=4, fill_color=GREEN,
                            fill_opacity=0.2)
            inner_dots = VGroup(
                Dot(P_AB, color=GREEN, radius=0.07),
                Dot(P_BC, color=GREEN, radius=0.07),
                Dot(P_CA, color=GREEN, radius=0.07),
            )
            return VGroup(rays, inner, inner_dots)

        self.add(always_redraw(triangle_v),
                 always_redraw(dots),
                 always_redraw(trisectors_inner))

        # Live side lengths of inner triangle
        def side_lengths():
            A, B, C = interp(0)
            dA1 = trisector_line(A, B, C, 1 / 3) - A
            dA2 = trisector_line(A, B, C, 2 / 3) - A
            dB1 = trisector_line(B, C, A, 1 / 3) - B
            dB2 = trisector_line(B, C, A, 2 / 3) - B
            dC1 = trisector_line(C, A, B, 1 / 3) - C
            dC2 = trisector_line(C, A, B, 2 / 3) - C
            P_AB = line_intersect(A, dA1, B, dB2)
            P_BC = line_intersect(B, dB1, C, dC2)
            P_CA = line_intersect(C, dC1, A, dA2)
            return (np.linalg.norm(P_AB - P_BC),
                    np.linalg.norm(P_BC - P_CA),
                    np.linalg.norm(P_CA - P_AB))

        info = VGroup(
            Tex(r"inner sides:", color=GREEN, font_size=22),
            VGroup(Tex(r"$|s_1|=$", font_size=20),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=20).set_color(GREEN)
                   ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$|s_2|=$", font_size=20),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=20).set_color(GREEN)
                   ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$|s_3|=$", font_size=20),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=20).set_color(GREEN)
                   ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.4)

        info[1][1].add_updater(lambda m: m.set_value(side_lengths()[0]))
        info[2][1].add_updater(lambda m: m.set_value(side_lengths()[1]))
        info[3][1].add_updater(lambda m: m.set_value(side_lengths()[2]))
        self.add(info)

        for k in range(1, len(configs)):
            self.play(A_tr.animate.set_value(float(k)),
                      run_time=2.2, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.5)
