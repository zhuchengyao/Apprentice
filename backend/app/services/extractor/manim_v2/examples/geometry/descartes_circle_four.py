from manim import *
import numpy as np


class DescartesCircleFourExample(Scene):
    """
    Descartes circle theorem: 4 mutually tangent circles with
    curvatures k_i satisfy (k_1+k_2+k_3+k_4)² = 2(k_1²+k_2²+k_3²+k_4²).

    Use a symmetric setup: 3 congruent circles of curvature 2
    tangent to each other, enclosed by a larger circle of curvature
    -(2(√3-1))/... and a small inner circle. Show Apollonian gasket
    extension with ValueTracker.
    """

    def construct(self):
        title = Tex(r"Descartes: $(\sum k_i)^2=2\sum k_i^2$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 3 congruent circles tangent to each other, all curvature 1
        R = 1.0  # each has radius 1
        r_set = R
        # Centers: equilateral triangle with side 2R
        offsets = [R * np.array([np.cos(t), np.sin(t), 0])
                    for t in [-PI / 2, PI / 6, 5 * PI / 6]]
        side = 2 * R
        height = side * np.sqrt(3) / 2
        centers = [
            np.array([0, height / 1.5, 0]),
            np.array([-side / 2, -height / 3, 0]),
            np.array([side / 2, -height / 3, 0]),
        ]
        c1 = Circle(radius=R, color=BLUE, stroke_width=3).move_to(centers[0])
        c2 = Circle(radius=R, color=GREEN, stroke_width=3).move_to(centers[1])
        c3 = Circle(radius=R, color=ORANGE, stroke_width=3).move_to(centers[2])
        self.play(Create(c1), Create(c2), Create(c3))

        # For 3 unit circles, k_1 = k_2 = k_3 = 1 (curvature 1/r=1)
        k1 = k2 = k3 = 1.0
        # Descartes: k_4 = k_1+k_2+k_3 ± 2√(k_1 k_2+k_2 k_3+k_3 k_1)
        # = 3 ± 2√3
        k4_out = 3 - 2 * np.sqrt(3)  # negative (large outer enclosing circle)
        k4_in = 3 + 2 * np.sqrt(3)   # positive (small inner circle)

        r4_out = 1 / abs(k4_out)  # radius ≈ 2.155
        r4_in = 1 / k4_in           # radius ≈ 0.155

        # Outer circle center: by symmetry at centroid of 3 circles
        center_gasket = (centers[0] + centers[1] + centers[2]) / 3

        s_tr = ValueTracker(0.0)

        def outer_circle():
            s = s_tr.get_value()
            alpha = min(1.0, s)
            return Circle(radius=r4_out * alpha, color=RED,
                          stroke_width=4, stroke_opacity=alpha).move_to(center_gasket)

        def inner_circle():
            s = s_tr.get_value()
            if s < 1:
                return VMobject()
            alpha = min(1.0, s - 1)
            return Circle(radius=r4_in * alpha, color=PURPLE,
                          stroke_width=3, stroke_opacity=alpha,
                          fill_color=PURPLE,
                          fill_opacity=0.3 * alpha).move_to(center_gasket)

        self.add(always_redraw(outer_circle), always_redraw(inner_circle))

        info = VGroup(
            VGroup(Tex(r"$k_1=k_2=k_3=$", font_size=22),
                   Tex(r"$1$", color=BLUE, font_size=22)
                   ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$k_4^-=3-2\sqrt 3=$", color=RED, font_size=22),
                   DecimalNumber(k4_out, num_decimal_places=3,
                                 font_size=22).set_color(RED)
                   ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$k_4^+=3+2\sqrt 3=$", color=PURPLE, font_size=22),
                   DecimalNumber(k4_in, num_decimal_places=3,
                                 font_size=22).set_color(PURPLE)
                   ).arrange(RIGHT, buff=0.1),
            Tex(r"Apollonian gasket starts here",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.3)
        self.add(info)

        self.play(s_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)
        self.play(s_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(1.0)
