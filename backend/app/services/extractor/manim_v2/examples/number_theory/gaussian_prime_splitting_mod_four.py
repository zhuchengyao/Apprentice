from manim import *
import numpy as np


class GaussianPrimeSplittingModFour(Scene):
    """Integer primes split in Z[i] based on their residue mod 4:
    p ≡ 1 (mod 4) -> factors as (a+bi)(a-bi) in Z[i].
    p ≡ 3 (mod 4) -> remains prime (inert).
    p = 2         -> ramifies:  2 = -i (1+i)^2.
    Visualize on the complex plane: put each p on the real axis, then for the
    1 mod 4 primes animate the split by drawing arrows to (a+bi) and (a-bi)."""

    def construct(self):
        title = Tex(
            r"Which integer primes split in $\mathbb{Z}[i]$?",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-1, 18, 2], y_range=[-5, 5, 1],
            x_length=11, y_length=5.5,
            background_line_style={"stroke_opacity": 0.25},
        ).shift(DOWN * 0.3)
        self.play(Create(plane))

        primes_split = [(5, 2, 1), (13, 3, 2), (17, 4, 1)]
        primes_inert = [3, 7, 11]

        real_dots = {}
        all_primes = sorted(
            [p for p, _, _ in primes_split] + primes_inert
        )
        for p in all_primes:
            color = GREEN if any(p == q for q, _, _ in primes_split) else RED
            d = Dot(plane.c2p(p, 0), radius=0.09, color=color)
            d.set_z_index(4)
            real_dots[p] = d
            lab = MathTex(str(p), font_size=26, color=color).next_to(
                d, DOWN, buff=0.15
            )
            self.play(FadeIn(d), Write(lab), run_time=0.35)

        legend = VGroup(
            VGroup(Dot(radius=0.09, color=GREEN),
                   Tex(r"$p \equiv 1 \pmod 4$ (splits)",
                       font_size=24)).arrange(RIGHT, buff=0.2),
            VGroup(Dot(radius=0.09, color=RED),
                   Tex(r"$p \equiv 3 \pmod 4$ (inert)",
                       font_size=24)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UL, buff=0.4).shift(DOWN * 0.6)
        self.play(FadeIn(legend))

        for p, a, b in primes_split:
            up_dot = Dot(plane.c2p(a, b), radius=0.09,
                         color=YELLOW).set_z_index(5)
            down_dot = Dot(plane.c2p(a, -b), radius=0.09,
                           color=YELLOW).set_z_index(5)
            up_lab = MathTex(
                rf"{a}+{b}i", font_size=24, color=YELLOW,
            ).next_to(up_dot, UP, buff=0.1)
            down_lab = MathTex(
                rf"{a}-{b}i", font_size=24, color=YELLOW,
            ).next_to(down_dot, DOWN, buff=0.1)
            arrow_up = Arrow(
                real_dots[p].get_center(), up_dot.get_center(),
                buff=0.12, color=YELLOW, stroke_width=3,
                max_tip_length_to_length_ratio=0.12,
            )
            arrow_down = Arrow(
                real_dots[p].get_center(), down_dot.get_center(),
                buff=0.12, color=YELLOW, stroke_width=3,
                max_tip_length_to_length_ratio=0.12,
            )
            eq = MathTex(
                rf"{p} = ({a}+{b}i)({a}-{b}i)",
                font_size=26, color=YELLOW,
            )
            eq.move_to(plane.c2p(p, 3.2))
            self.play(
                GrowArrow(arrow_up), GrowArrow(arrow_down),
                FadeIn(up_dot), FadeIn(down_dot),
                Write(up_lab), Write(down_lab),
                Write(eq),
                run_time=1.4,
            )
            self.wait(0.4)

        caption = Tex(
            r"(2 ramifies: $2 = -i(1+i)^2$)",
            font_size=24, color=BLUE,
        ).to_corner(DR, buff=0.4)
        self.play(FadeIn(caption))
        self.wait(1.3)
