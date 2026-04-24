from manim import *
import numpy as np


class InverseSquareLawLightSpread(Scene):
    """Light from a point source spreads over a sphere of radius r; total
    luminous power is conserved, so intensity I(r) = L/(4*pi*r^2) falls
    off as 1/r^2.  Visualize by expanding concentric spheres and an
    intensity DecimalNumber that decays with 1/r^2."""

    def construct(self):
        title = Tex(
            r"Inverse-square law: $I(r) \propto 1/r^2$",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        source = Dot([-3.5, 0, 0], radius=0.16, color=YELLOW).set_z_index(5)
        glow = Circle(radius=0.35, color=YELLOW, fill_opacity=0.4,
                      stroke_width=0).move_to(source)
        self.play(FadeIn(glow), FadeIn(source))

        r_tr = ValueTracker(0.5)

        def get_ring():
            r = r_tr.get_value()
            return Circle(
                radius=r, color=BLUE, stroke_width=3,
                stroke_opacity=0.8, fill_opacity=0.0,
            ).move_to(source)

        def get_intensity_panel():
            r = r_tr.get_value()
            I = 1.0 / (r * r)
            row = VGroup(
                MathTex("r = ", font_size=28),
                DecimalNumber(r, num_decimal_places=2,
                              font_size=28, color=BLUE),
                MathTex(r"\quad I(r) = \tfrac{L}{4\pi r^2} \propto",
                        font_size=28),
                DecimalNumber(I, num_decimal_places=3,
                              font_size=28, color=RED),
            ).arrange(RIGHT, buff=0.12)
            row.to_edge(DOWN, buff=0.6)
            return row

        ring = always_redraw(get_ring)
        panel = always_redraw(get_intensity_panel)
        self.add(ring, panel)

        sample_rs = [0.5, 1.0, 1.5, 2.0, 3.0, 4.5]
        trail_rings = VGroup()
        for r in sample_rs:
            trail_rings.add(Circle(
                radius=r, color=BLUE, stroke_opacity=0.3,
                stroke_width=1.5,
            ).move_to(source))
        self.add(trail_rings)

        table = VGroup(
            Tex("r", font_size=26, color=BLUE),
            Tex(r"I $\propto 1/r^2$", font_size=26, color=RED),
        ).arrange(RIGHT, buff=1.6)
        table.to_corner(UR, buff=0.5).shift(DOWN * 0.5)
        rows = [table]
        for r in [0.5, 1.0, 2.0, 3.0, 4.5]:
            row = VGroup(
                DecimalNumber(r, num_decimal_places=1,
                              font_size=24, color=BLUE),
                DecimalNumber(1 / (r * r), num_decimal_places=3,
                              font_size=24, color=RED),
            ).arrange(RIGHT, buff=2.2)
            row.next_to(rows[-1], DOWN, buff=0.2, aligned_edge=LEFT)
            rows.append(row)
        self.play(LaggedStart(*[FadeIn(r) for r in rows],
                              lag_ratio=0.15, run_time=2))

        for r in sample_rs:
            self.play(r_tr.animate.set_value(r), run_time=0.8)
            self.wait(0.2)

        power_note = Tex(
            r"Total luminous power $L$ is conserved across every sphere.",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.15)
        self.play(FadeIn(power_note))
        self.wait(1.2)
