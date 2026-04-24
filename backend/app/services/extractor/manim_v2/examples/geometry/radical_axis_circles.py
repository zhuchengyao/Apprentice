from manim import *
import numpy as np


class RadicalAxisCirclesExample(Scene):
    """
    Radical axis of two circles: locus of points with equal power
    with respect to both. For two non-concentric circles it's a line
    perpendicular to the line of centers.

    SINGLE_FOCUS:
      Two circles (configurable); ValueTracker c_tr moves the
      second circle's center. always_redraw radical axis (line of
      equal power) + midpoint/verification dot.
    """

    def construct(self):
        title = Tex(r"Radical axis: locus of equal power w.r.t.\ two circles",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Circle 1 fixed
        C1 = np.array([-2.5, 0, 0])
        r1 = 1.5
        circle1 = Circle(radius=r1, color=BLUE, stroke_width=2.5,
                           fill_opacity=0.15).move_to(C1)
        C1_dot = Dot(C1, color=BLUE, radius=0.08)
        self.play(Create(circle1), FadeIn(C1_dot))

        # Circle 2: position varies
        C2_x_tr = ValueTracker(2.0)
        r2 = 1.2

        def circle2():
            c2 = np.array([C2_x_tr.get_value(), 0.5, 0])
            return Circle(radius=r2, color=ORANGE, stroke_width=2.5,
                            fill_opacity=0.15).move_to(c2)

        def C2_dot():
            c2 = np.array([C2_x_tr.get_value(), 0.5, 0])
            return Dot(c2, color=ORANGE, radius=0.08)

        self.add(always_redraw(circle2), always_redraw(C2_dot))

        def radical_axis():
            c2 = np.array([C2_x_tr.get_value(), 0.5, 0])
            # Power wrt circle i at point P: |P - C_i|² - r_i²
            # Equal: |P - C1|² - r1² = |P - C2|² - r2²
            # Expand: P² - 2P·C1 + C1² - r1² = P² - 2P·C2 + C2² - r2²
            # 2P · (C2 - C1) = C2² - C1² - r2² + r1²
            # Line equation: (P - midpoint) · (C2 - C1) = const
            d = c2 - C1
            # Point on axis: midpoint shifted toward center with bigger radius
            mid = (C1 + c2) / 2
            # Actually: along line C1C2, at distance d_axis = (|C1C2|² + r1² - r2²)/(2|C1C2|)
            # from C1
            dist = np.linalg.norm(d)
            if dist < 1e-4:
                return VGroup()
            d_axis = (dist ** 2 + r1 ** 2 - r2 ** 2) / (2 * dist)
            # Point on axis
            axis_pt = C1 + d_axis * d / dist
            # Perpendicular direction
            perp = np.array([-d[1], d[0], 0]) / dist
            start = axis_pt - 3 * perp
            end = axis_pt + 3 * perp
            line = Line(start, end, color=RED, stroke_width=3)
            dot = Dot(axis_pt, color=YELLOW, radius=0.1)
            return VGroup(line, dot)

        self.add(always_redraw(radical_axis))

        def info():
            c2 = np.array([C2_x_tr.get_value(), 0.5, 0])
            return VGroup(
                MathTex(rf"C_1 = (-2.5, 0),\ r_1 = {r1}",
                         color=BLUE, font_size=20),
                MathTex(rf"C_2 = ({c2[0]:.2f}, 0.5),\ r_2 = {r2}",
                         color=ORANGE, font_size=20),
                Tex(r"RED line: radical axis $\perp C_1 C_2$",
                     color=RED, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for cv in [3.0, 0.5, 4.0, 2.0]:
            self.play(C2_x_tr.animate.set_value(cv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
