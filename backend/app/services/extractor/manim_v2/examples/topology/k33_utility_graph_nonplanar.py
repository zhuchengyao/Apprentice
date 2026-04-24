from manim import *
import numpy as np


class K33UtilityGraphNonplanar(Scene):
    """Three houses (top row) connect to three utilities (bottom row).  The
    complete bipartite graph K_{3,3} has V=6, E=9.  If it were planar,
    Euler gives F = 2 + E - V = 5, and bipartiteness forces every face to
    be bounded by at least 4 edges, so 2E >= 4F, i.e. E >= 2F = 10.  But
    E = 9 < 10 — contradiction.  So K_{3,3} is non-planar."""

    def construct(self):
        title = Tex(
            r"Why $K_{3,3}$ (three utilities puzzle) is not planar",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        house_positions = [
            np.array([-3, 1.8, 0]),
            np.array([0, 1.8, 0]),
            np.array([3, 1.8, 0]),
        ]
        util_positions = [
            np.array([-3, -1.8, 0]),
            np.array([0, -1.8, 0]),
            np.array([3, -1.8, 0]),
        ]

        houses = VGroup(*[
            VGroup(
                Square(side_length=0.65, color=BLUE, stroke_width=2,
                       fill_opacity=0.25),
                Polygon(
                    np.array([-0.35, 0, 0]),
                    np.array([0.35, 0, 0]),
                    np.array([0, 0.35, 0]),
                    color=BLUE, stroke_width=2, fill_opacity=0.25,
                ).shift(UP * 0.3),
            ).move_to(p)
            for p in house_positions
        ])
        utils = VGroup(*[
            Circle(radius=0.33, color=color, stroke_width=2,
                   fill_opacity=0.25).move_to(p)
            for p, color in zip(util_positions, [YELLOW, TEAL, ORANGE])
        ])
        util_tex = VGroup(*[
            Tex(name, font_size=20).move_to(p)
            for p, name in zip(util_positions,
                               ["water", "gas", "elec"])
        ])
        self.play(LaggedStart(*[FadeIn(h) for h in houses], lag_ratio=0.1))
        self.play(LaggedStart(*[FadeIn(u) for u in utils], lag_ratio=0.1),
                  LaggedStart(*[Write(t) for t in util_tex],
                              lag_ratio=0.1))

        edges = VGroup()
        for hp in house_positions:
            for up_ in util_positions:
                edges.add(Line(hp + DOWN * 0.35, up_ + UP * 0.35,
                               color=WHITE, stroke_width=2))
        self.play(LaggedStart(*[Create(e) for e in edges],
                              lag_ratio=0.08, run_time=3))

        counts = VGroup(
            MathTex(r"V = 6", font_size=30),
            MathTex(r"E = 9", font_size=30),
        ).arrange(RIGHT, buff=1.0)
        counts.to_edge(LEFT, buff=0.4).shift(UP * 0.1)
        self.play(FadeIn(counts))

        argument = VGroup(
            MathTex(r"\text{If planar: } F = 2 + E - V = 5",
                    font_size=26),
            MathTex(r"\text{Bipartite} \Rightarrow \text{every face has}\ \ge 4\ \text{edges}",
                    font_size=26),
            MathTex(r"2E \ge 4F \Rightarrow E \ge 10",
                    font_size=28, color=YELLOW),
            MathTex(r"\text{but } E = 9.\ \ \Longrightarrow\ \text{contradiction}",
                    font_size=28, color=RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        argument.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.3)
        self.play(FadeIn(argument[0]))
        self.wait(0.3)
        self.play(FadeIn(argument[1]))
        self.wait(0.3)
        self.play(Write(argument[2]))
        self.wait(0.3)
        self.play(Write(argument[3]))
        self.wait(1.5)
