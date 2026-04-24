from manim import *
import numpy as np


class MassScalingIntegerVsFractional(Scene):
    """Four shapes (line, square, cube, Sierpinski) each scaled by 1/2. Line
    mass halves, square quarters (= (1/2)^2), cube eighths (= (1/2)^3),
    Sierpinski thirds — which does not fit any integer power, demanding a
    fractional dimension log 3 / log 2 ≈ 1.585."""

    def construct(self):
        title = Tex(
            r"Scale each shape by $\tfrac{1}{2}$: how does mass change?",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        col_xs = [-5.0, -1.7, 1.7, 5.0]
        col_titles = ["Line", "Square", "Cube", "Sierpinski"]
        label_rows = VGroup(*[
            Tex(t, font_size=28) for t in col_titles
        ])
        for lab, x in zip(label_rows, col_xs):
            lab.move_to([x, 2.3, 0])
        self.play(LaggedStart(*[FadeIn(m) for m in label_rows], lag_ratio=0.1))

        def make_line():
            return Line(LEFT, RIGHT, color=BLUE, stroke_width=6)

        def make_square():
            return Square(side_length=1.6, color=BLUE,
                          fill_opacity=0.6, stroke_width=2)

        def make_cube():
            sq_back = Square(side_length=1.5, color=BLUE_E,
                             fill_opacity=0.5, stroke_width=2)
            sq_front = Square(side_length=1.5, color=BLUE,
                              fill_opacity=0.55, stroke_width=2)
            sq_front.shift(0.25 * (RIGHT + UP))
            connectors = VGroup(*[
                Line(sq_back.get_corner(c),
                     sq_front.get_corner(c),
                     color=BLUE_E, stroke_width=2)
                for c in [UL, UR, DL, DR]
            ])
            return VGroup(sq_back, connectors, sq_front)

        def make_sierpinski(order=4, size=1.8):
            A = np.array([-size / 2, -size * np.sqrt(3) / 6, 0])
            B = np.array([size / 2, -size * np.sqrt(3) / 6, 0])
            C = np.array([0, size * np.sqrt(3) / 3, 0])

            def recurse(a, b, c, depth):
                if depth == 0:
                    return [Polygon(a, b, c, color=YELLOW,
                                    fill_opacity=0.8, stroke_width=0)]
                ab = (a + b) / 2
                bc = (b + c) / 2
                ca = (c + a) / 2
                return (
                    recurse(a, ab, ca, depth - 1)
                    + recurse(ab, b, bc, depth - 1)
                    + recurse(ca, bc, c, depth - 1)
                )

            return VGroup(*recurse(A, B, C, order))

        big_line = make_line().scale(1.4).move_to([col_xs[0], 0.9, 0])
        big_sq = make_square().move_to([col_xs[1], 0.9, 0])
        big_cube = make_cube().move_to([col_xs[2], 0.9, 0])
        big_sier = make_sierpinski(order=4, size=1.8).move_to(
            [col_xs[3], 0.9, 0]
        )
        shapes_top = VGroup(big_line, big_sq, big_cube, big_sier)
        self.play(LaggedStart(
            Create(big_line),
            FadeIn(big_sq),
            FadeIn(big_cube),
            FadeIn(big_sier),
            lag_ratio=0.15,
        ))

        small_line = make_line().scale(0.7).move_to([col_xs[0], -1.4, 0])
        small_sq = make_square().scale(0.5).move_to([col_xs[1], -1.4, 0])
        small_cube = make_cube().scale(0.5).move_to([col_xs[2], -1.4, 0])
        small_sier = make_sierpinski(order=4, size=0.9).move_to(
            [col_xs[3], -1.4, 0]
        )
        smalls = VGroup(small_line, small_sq, small_cube, small_sier)
        self.play(*[
            TransformFromCopy(big, small, run_time=1.5)
            for big, small in zip(shapes_top, smalls)
        ])

        mass_labels = VGroup(
            MathTex(r"\tfrac{1}{2}\, M", font_size=30, color=GREEN),
            MathTex(r"\tfrac{1}{4}\, M", font_size=30, color=GREEN),
            MathTex(r"\tfrac{1}{8}\, M", font_size=30, color=GREEN),
            MathTex(r"\tfrac{1}{3}\, M", font_size=30, color=RED),
        )
        for lab, x in zip(mass_labels, col_xs):
            lab.move_to([x, -2.6, 0])
        self.play(LaggedStart(*[Write(m) for m in mass_labels],
                              lag_ratio=0.2))

        power_labels = VGroup(
            MathTex(r"\left(\tfrac{1}{2}\right)^{1}", font_size=26),
            MathTex(r"\left(\tfrac{1}{2}\right)^{2}", font_size=26),
            MathTex(r"\left(\tfrac{1}{2}\right)^{3}", font_size=26),
            MathTex(r"\left(\tfrac{1}{2}\right)^{?}", font_size=26,
                    color=YELLOW),
        )
        for lab, x in zip(power_labels, col_xs):
            lab.move_to([x, -3.2, 0])
        self.play(LaggedStart(*[FadeIn(m) for m in power_labels],
                              lag_ratio=0.2))

        self.play(
            Indicate(mass_labels[3], color=YELLOW, scale_factor=1.25),
            Indicate(power_labels[3], color=YELLOW, scale_factor=1.25),
            run_time=1.5,
        )
        self.wait(1.5)
