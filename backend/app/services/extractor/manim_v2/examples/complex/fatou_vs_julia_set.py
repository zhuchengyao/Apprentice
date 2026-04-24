from manim import *
import numpy as np


class FatouVsJuliaSet(Scene):
    """For a rational map f(z), the Fatou set is where iteration is stable
    (nearby points stay nearby), while the Julia set is where iteration
    is chaotic.  Visualize for f(z) = z^2 - 1.  Three sample orbits:
    BLUE attracts to a fixed point (Fatou), GREEN lies on a 2-cycle
    (Fatou), RED starts on the Julia-set boundary and shows chaotic
    behavior."""

    def construct(self):
        title = Tex(
            r"Fatou vs Julia: stable vs chaotic iteration of $f(z)=z^2-1$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(
            x_range=[-2, 2, 1], y_range=[-1.5, 1.5, 1],
            x_length=9, y_length=5.5,
            background_line_style={"stroke_opacity": 0.25},
        ).shift(DOWN * 0.3)
        self.play(Create(plane))

        def f(z):
            return z * z - 1

        def orbit(z0, n=15):
            orb = [z0]
            z = z0
            for _ in range(n):
                z = f(z)
                orb.append(z)
            return orb

        def draw_orbit(orb, color, radius_factor=1.0):
            dots = VGroup()
            lines = VGroup()
            for i, z in enumerate(orb):
                d = Dot(plane.n2p(z), radius=0.06 * radius_factor,
                        color=color).set_z_index(4)
                dots.add(d)
                if i > 0:
                    lines.add(Line(
                        plane.n2p(orb[i - 1]), plane.n2p(z),
                        color=color, stroke_width=2,
                        stroke_opacity=0.5,
                    ))
            return dots, lines

        fatou_fixed = orbit(0.3 + 0.05j, 20)
        fatou_dots1, fatou_lines1 = draw_orbit(fatou_fixed, BLUE)

        fatou_2cycle = orbit(-0.7 + 0.0j, 20)
        fatou_dots2, fatou_lines2 = draw_orbit(fatou_2cycle, GREEN)

        julia_edge = orbit(0.6180 + 0.01j, 12)
        julia_dots, julia_lines = draw_orbit(julia_edge, RED)

        self.play(Create(fatou_lines1),
                  LaggedStart(*[FadeIn(d) for d in fatou_dots1],
                              lag_ratio=0.05, run_time=1.5))
        self.play(Create(fatou_lines2),
                  LaggedStart(*[FadeIn(d) for d in fatou_dots2],
                              lag_ratio=0.05, run_time=1.5))
        self.play(Create(julia_lines),
                  LaggedStart(*[FadeIn(d) for d in julia_dots],
                              lag_ratio=0.05, run_time=1.5))

        legend = VGroup(
            VGroup(Dot(radius=0.08, color=BLUE),
                   Tex(r"Fatou: attracted to fixed point $\tfrac{1-\sqrt{5}}{2}$",
                       font_size=20)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(radius=0.08, color=GREEN),
                   Tex(r"Fatou: on a 2-cycle $0 \leftrightarrow -1$",
                       font_size=20)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(radius=0.08, color=RED),
                   Tex(r"Julia: near boundary $\to$ chaotic",
                       font_size=20)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        self.play(FadeIn(legend))

        principle = Tex(
            r"Fatou = where iteration is predictable; Julia = where arbitrarily close starts diverge wildly.",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(principle))
        self.wait(1.5)
