from manim import *
import numpy as np


class LatticePointsVsCircleArea(Scene):
    """The number of lattice points in a disk of radius R tends to pi * R^2.
    Animate R growing, counting enclosed Gaussian integers, and compare to
    pi * R^2.  This is the bridge from the Z[i] ring-count formula to the
    Leibniz pi/4 identity."""

    def construct(self):
        title = Tex(
            r"Lattice points in a disk $\sim$ area = $\pi R^2$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-6, 6, 1], y_range=[-6, 6, 1],
            x_length=6.8, y_length=6.8,
            background_line_style={"stroke_opacity": 0.25},
        ).shift(LEFT * 2.3 + DOWN * 0.15)
        origin = plane.c2p(0, 0)
        unit = plane.c2p(1, 0)[0] - origin[0]
        self.play(Create(plane))

        dots = {}
        for a in range(-6, 7):
            for b in range(-6, 7):
                if a * a + b * b > 36:
                    continue
                d = Dot(plane.c2p(a, b), radius=0.05, color=BLUE)
                dots[(a, b)] = d
        self.play(LaggedStart(*[FadeIn(d) for d in dots.values()],
                              lag_ratio=0.003, run_time=1.5))

        R_tr = ValueTracker(0.5)

        def get_disk():
            R = R_tr.get_value()
            return Circle(radius=R * unit, color=YELLOW,
                          stroke_width=3).move_to(origin)

        disk = always_redraw(get_disk)
        self.add(disk)

        inside_group = VGroup()

        def refresh_inside(R):
            nonlocal inside_group
            new_grp = VGroup()
            for (a, b), d in dots.items():
                if a * a + b * b <= R * R + 1e-6:
                    nd = Dot(d.get_center(), radius=0.06,
                             color=YELLOW).set_z_index(4)
                    new_grp.add(nd)
            self.remove(inside_group)
            inside_group = new_grp
            self.add(inside_group)
            return len(inside_group)

        R_val = DecimalNumber(
            0.5, num_decimal_places=2, font_size=30, color=YELLOW,
        )
        count_val = Integer(1, font_size=30, color=YELLOW)
        area_val = DecimalNumber(
            np.pi * 0.25, num_decimal_places=2, font_size=30, color=GREEN,
        )
        ratio_val = DecimalNumber(
            1.0 / (np.pi * 0.25), num_decimal_places=3, font_size=30,
            color=BLUE,
        )

        R_row = VGroup(MathTex(r"R =", font_size=28), R_val).arrange(
            RIGHT, buff=0.1
        )
        count_row = VGroup(
            Tex("count:", font_size=28), count_val,
        ).arrange(RIGHT, buff=0.1)
        area_row = VGroup(
            MathTex(r"\pi R^2 =", font_size=28), area_val,
        ).arrange(RIGHT, buff=0.1)
        ratio_row = VGroup(
            Tex("count / $\\pi R^2$:", font_size=28), ratio_val,
        ).arrange(RIGHT, buff=0.1)
        panel = VGroup(R_row, count_row, area_row, ratio_row).arrange(
            DOWN, aligned_edge=LEFT, buff=0.28,
        )
        panel.to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        self.add(panel)

        for R_target in [1.0, 1.5, 2.5, 3.5, 4.5, 5.5, 6.0]:
            self.play(R_tr.animate.set_value(R_target), run_time=1.2)
            count = refresh_inside(R_target)
            area = np.pi * R_target * R_target
            R_val.set_value(R_target)
            count_val.set_value(count)
            area_val.set_value(area)
            ratio_val.set_value(count / area if area > 0 else 0)
            self.wait(0.2)

        self.wait(1.3)
