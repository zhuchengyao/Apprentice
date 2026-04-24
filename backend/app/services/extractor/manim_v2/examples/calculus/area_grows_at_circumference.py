from manim import *
import numpy as np


class AreaGrowsAtCircumferenceExample(Scene):
    """
    As the radius R grows, the disk's area grows at rate 2πR:
      A(R) = π R²,   A'(R) = 2πR = circumference.

    This is the infinitesimal insight behind integrating rings
    to get total area.

    SINGLE_FOCUS: animate a disk whose radius grows; a thin annular
    ring of width dr is highlighted. Its area ≈ 2πR · dr — exactly
    the infinitesimal contribution dA.
    """

    def construct(self):
        title = Tex(r"Disk area grows at rate circumference: $\frac{dA}{dR}=2\pi R$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT: disk with growing radius
        disk_center = LEFT * 2.7 + DOWN * 0.4
        R_tr = ValueTracker(1.2)
        dr = 0.08

        def disk():
            R = R_tr.get_value()
            return Circle(radius=R, color=BLUE, stroke_width=2,
                           fill_color=BLUE, fill_opacity=0.4).move_to(disk_center)

        def outer_ring():
            R = R_tr.get_value()
            outer = Circle(radius=R + dr, color=YELLOW).move_to(disk_center)
            inner = Circle(radius=R).move_to(disk_center)
            ring = Difference(outer, inner, color=YELLOW, fill_color=YELLOW, fill_opacity=0.85)
            return ring

        def radius_arrow():
            R = R_tr.get_value()
            end = disk_center + R * RIGHT
            return Arrow(disk_center, end, color=RED, buff=0, stroke_width=3,
                          max_tip_length_to_length_ratio=0.15)

        def R_label():
            R = R_tr.get_value()
            return Tex(rf"$R={R:.2f}$", color=RED,
                        font_size=22).move_to(disk_center + R / 2 * RIGHT + DOWN * 0.35)

        self.add(always_redraw(disk), always_redraw(outer_ring),
                 always_redraw(radius_arrow), always_redraw(R_label))

        # RIGHT: area vs R plot
        axes = Axes(x_range=[0, 3, 0.5], y_range=[0, 30, 10],
                    x_length=5, y_length=4,
                    axis_config={"include_numbers": True, "font_size": 14}
                    ).shift(RIGHT * 2.8 + DOWN * 0.3)
        self.play(Create(axes))

        area_curve = axes.plot(lambda r: PI * r * r, x_range=[0, 3],
                                color=BLUE, stroke_width=3)
        self.add(area_curve)
        self.add(Tex(r"$A(R)=\pi R^2$", color=BLUE, font_size=22).next_to(axes, UP, buff=0.15))

        def area_dot():
            R = R_tr.get_value()
            return Dot(axes.c2p(R, PI * R * R), color=YELLOW, radius=0.1)

        # Tangent line = circumference
        def tangent():
            R = R_tr.get_value()
            A = PI * R * R
            slope = 2 * PI * R
            dx = 0.4
            return Line(axes.c2p(R - dx, A - slope * dx),
                         axes.c2p(R + dx, A + slope * dx),
                         color=GREEN, stroke_width=3)

        self.add(always_redraw(area_dot), always_redraw(tangent))

        info = VGroup(
            VGroup(Tex(r"$A=\pi R^2=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"slope $=2\pi R=$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"= circumference of circle",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(PI * R_tr.get_value() ** 2))
        info[1][1].add_updater(lambda m: m.set_value(2 * PI * R_tr.get_value()))
        self.add(info)

        self.play(R_tr.animate.set_value(2.5), run_time=5, rate_func=smooth)
        self.wait(0.8)
