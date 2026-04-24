from manim import *
import numpy as np


class GaussianIntegerSquaresLattice(Scene):
    """Squaring each Gaussian integer z = u+vi yields a Pythagorean triple
    (u^2-v^2, 2uv, u^2+v^2). Show the input lattice mapping to output points."""

    def construct(self):
        title = Tex(
            r"Squaring Gaussian integers produces Pythagorean triples",
            font_size=26,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1],
            x_length=5.5, y_length=5.5,
            background_line_style={"stroke_opacity": 0.3},
        ).shift(LEFT * 3.3 + DOWN * 0.3)
        right = NumberPlane(
            x_range=[-16, 16, 4], y_range=[-16, 16, 4],
            x_length=5.5, y_length=5.5,
            background_line_style={"stroke_opacity": 0.3},
        ).shift(RIGHT * 3.3 + DOWN * 0.3)
        l_label = Tex(r"$z$-plane", font_size=22).next_to(left, DOWN, buff=0.1)
        r_label = Tex(r"$z^{2}$-plane", font_size=22).next_to(right, DOWN, buff=0.1)
        self.play(Create(left), Create(right), FadeIn(l_label), FadeIn(r_label))

        pairs = [
            (u, v)
            for u in range(-3, 4)
            for v in range(-3, 4)
            if (u, v) != (0, 0)
        ]
        dots_in = VGroup()
        dots_out = VGroup()
        for u, v in pairs:
            z = complex(u, v)
            z2 = z * z
            dots_in.add(Dot(left.c2p(u, v), radius=0.04, color=BLUE))
            dots_out.add(
                Dot(right.c2p(z2.real, z2.imag), radius=0.04, color=YELLOW)
            )
        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_in], lag_ratio=0.015),
            run_time=1.5,
        )
        self.wait(0.3)

        z_in_hi = Dot(left.c2p(2, 1), radius=0.1, color=RED, z_index=5)
        z_in_lab = MathTex("2+i", font_size=26, color=RED).next_to(
            z_in_hi, UR, buff=0.05
        )
        z_out_hi = Dot(right.c2p(3, 4), radius=0.1, color=RED, z_index=5)
        z_out_lab = MathTex("3+4i", font_size=26, color=RED).next_to(
            z_out_hi, UR, buff=0.05
        )
        self.play(Create(z_in_hi), Write(z_in_lab))
        self.wait(0.3)
        self.play(
            TransformFromCopy(z_in_hi, z_out_hi), Write(z_out_lab)
        )
        self.wait(0.3)

        formula = MathTex(
            r"(2+i)^{2} = 4 - 1 + 4i = 3 + 4i,\quad |2+i|^{2} = 5",
            font_size=26, color=YELLOW,
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(formula))
        self.wait(0.4)

        self.play(
            LaggedStart(*[FadeIn(d) for d in dots_out], lag_ratio=0.015),
            run_time=2.0,
        )
        self.wait(1.0)
