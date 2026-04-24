from manim import *
import numpy as np


class PutnamTriangleContainsCenterTrials(Scene):
    """Three points uniformly at random on a unit circle form a triangle.
    How often does the triangle contain the center of the circle?  Empirical
    trial counter converges toward the theoretical answer 1/4."""

    def construct(self):
        title = Tex(
            r"3 random points: does the triangle contain the center?",
            font_size=26,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-1.8, 1.8, 1], y_range=[-1.8, 1.8, 1],
            x_length=5.5, y_length=5.5,
            background_line_style={"stroke_opacity": 0.2},
        ).shift(LEFT * 2.5 + DOWN * 0.2)
        origin = plane.c2p(0, 0)
        unit = plane.c2p(1, 0)[0] - origin[0]
        circle = Circle(radius=unit, color=BLUE).move_to(origin)
        center_dot = Dot(origin, radius=0.08, color=WHITE).set_z_index(5)
        self.play(Create(plane), Create(circle), FadeIn(center_dot))

        rng = np.random.default_rng(7)

        def triangle_contains_origin(pts):
            def sign(p1, p2, p3):
                return (p1[0] - p3[0]) * (p2[1] - p3[1]) \
                    - (p2[0] - p3[0]) * (p1[1] - p3[1])
            zero = np.array([0.0, 0.0])
            d1 = sign(zero, pts[0], pts[1])
            d2 = sign(zero, pts[1], pts[2])
            d3 = sign(zero, pts[2], pts[0])
            neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
            pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
            return not (neg and pos)

        trial_num = Integer(0, font_size=30)
        contained_num = Integer(0, font_size=30)
        frac = DecimalNumber(0.0, num_decimal_places=3, font_size=30)
        expected = MathTex(
            r"\text{theory:}\; 1/4 = 0.25",
            font_size=26, color=YELLOW,
        )
        panel = VGroup(
            VGroup(Tex("trials: ", font_size=28), trial_num).arrange(
                RIGHT, buff=0.1
            ),
            VGroup(
                Tex("contain center: ", font_size=28), contained_num,
            ).arrange(RIGHT, buff=0.1),
            VGroup(Tex("fraction: ", font_size=28), frac).arrange(
                RIGHT, buff=0.1
            ),
            expected,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        panel.to_edge(RIGHT, buff=0.3).shift(UP * 0.3)
        self.add(panel)

        contained = 0
        total = 0
        n_trials = 60
        for i in range(n_trials):
            angles = rng.uniform(0, 2 * np.pi, size=3)
            pts = np.array([[np.cos(a), np.sin(a)] for a in angles])
            contains = triangle_contains_origin(pts)
            total += 1
            if contains:
                contained += 1
            tri_color = GREEN if contains else RED
            dots = VGroup(*[
                Dot(plane.c2p(p[0], p[1]),
                    radius=0.05, color=YELLOW).set_z_index(4)
                for p in pts
            ])
            tri = Polygon(
                plane.c2p(pts[0][0], pts[0][1]),
                plane.c2p(pts[1][0], pts[1][1]),
                plane.c2p(pts[2][0], pts[2][1]),
                color=tri_color, fill_opacity=0.3, stroke_width=2,
            )
            trial_num.set_value(total)
            contained_num.set_value(contained)
            frac.set_value(contained / total)
            self.add(dots, tri)
            self.wait(0.08)
            if i < n_trials - 1:
                self.remove(dots, tri)
        self.wait(2.0)
