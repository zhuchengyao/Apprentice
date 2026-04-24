from manim import *
import numpy as np


class SimilarTrianglesEquivalenceClass(Scene):
    """The moduli space of triangles identifies similar triangles (same
    shape, different size/orientation) as a single point.  Show that one
    shape -- a 3:4:5 right triangle -- can be drawn many ways (scaled,
    rotated, reflected) that all collapse to the same point in the
    (b/a, gamma) moduli plane."""

    def construct(self):
        title = Tex(
            r"Moduli space: similar triangles collapse to one point",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def make_triangle(s, angle, center, color=BLUE, reflect=False):
            a, b, c = 3 * s, 4 * s, 5 * s
            A = np.array([0, 0, 0])
            B = np.array([a, 0, 0])
            C = np.array([0, b, 0])
            if reflect:
                A, B, C = A, C, B
                A = np.array([0, 0, 0])
                B = np.array([a, 0, 0])
                C = np.array([0, -b, 0])
            rot = np.array([
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1],
            ])
            pts = [rot @ p for p in (A, B, C)]
            cen = np.mean(pts, axis=0)
            pts = [p - cen + center for p in pts]
            return Polygon(*pts, color=color, stroke_width=2.5,
                           fill_opacity=0.25)

        configs = [
            (0.35, 0.0, [-5.5, 1.5, 0]),
            (0.25, 0.6, [-3.8, 1.8, 0]),
            (0.5, -0.4, [-2.0, 1.2, 0]),
            (0.3, 1.5, [-0.2, 1.8, 0]),
            (0.4, 2.3, [1.6, 1.4, 0]),
        ]
        triangles = VGroup()
        for s, a, c in configs:
            triangles.add(make_triangle(s, a, c))
        self.play(LaggedStart(*[Create(t) for t in triangles],
                              lag_ratio=0.15))

        arrow_y = -0.5
        arrows = VGroup()
        for s, a, c in configs:
            arrows.add(Arrow(
                [c[0], c[1] - 0.8, 0], [3.5, arrow_y - 0.5, 0],
                buff=0.1, color=YELLOW, stroke_width=2,
                max_tip_length_to_length_ratio=0.05,
            ))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],
                              lag_ratio=0.1))

        plane = Axes(
            x_range=[0, 2, 0.5],
            y_range=[0, 3.2, 0.5],
            x_length=3.5, y_length=2.6,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        )
        plane.move_to([3.5, -2.0, 0])
        x_lab = MathTex("b/a", font_size=20).next_to(
            plane.x_axis.get_end(), DOWN, buff=0.1
        )
        y_lab = MathTex(r"\gamma", font_size=22).next_to(
            plane.y_axis.get_end(), LEFT, buff=0.1
        )
        self.play(Create(plane), FadeIn(x_lab), FadeIn(y_lab))

        moduli_point = Dot(plane.c2p(4 / 3, np.pi / 2),
                           radius=0.12,
                           color=RED).set_z_index(4)
        moduli_lab = MathTex(
            r"(b/a, \gamma) = (\tfrac{4}{3}, \tfrac{\pi}{2})",
            font_size=22, color=RED,
        ).next_to(moduli_point, DR, buff=0.15)
        self.play(FadeIn(moduli_point), Write(moduli_lab))

        note = Tex(
            r"All 5 triangles represent the same point in moduli space.",
            font_size=24, color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(note))
        self.wait(1.3)
