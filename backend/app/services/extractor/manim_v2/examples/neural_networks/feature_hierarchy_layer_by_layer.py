from manim import *
import numpy as np


class FeatureHierarchyLayerByLayer(Scene):
    """The classical pedagogical intuition (from 3b1b's nn series) that
    successive layers detect successively higher-level features: layer 1
    picks up short edges, layer 2 combines edges into strokes/loops, layer 3
    combines those into whole digits.  (Real MLPs rarely cluster this
    cleanly — the scene represents the teaching story.)"""

    def construct(self):
        title = Tex(
            r"Idealized feature hierarchy in a deep network",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def make_edge(kind, color=BLUE):
            box = Square(side_length=0.7, color=GREY_D, stroke_width=1.5,
                         fill_opacity=0.08, fill_color=WHITE)
            if kind == "horiz":
                bar = Line(LEFT * 0.25, RIGHT * 0.25, color=color,
                           stroke_width=6)
            elif kind == "vert":
                bar = Line(UP * 0.25, DOWN * 0.25, color=color,
                           stroke_width=6)
            elif kind == "diag1":
                bar = Line(DL * 0.25, UR * 0.25, color=color,
                           stroke_width=6)
            else:
                bar = Line(UL * 0.25, DR * 0.25, color=color,
                           stroke_width=6)
            return VGroup(box, bar)

        def make_loop(color=ORANGE):
            box = Square(side_length=0.85, color=GREY_D, stroke_width=1.5,
                         fill_opacity=0.08, fill_color=WHITE)
            circle = Circle(radius=0.25, color=color, stroke_width=5)
            return VGroup(box, circle)

        def make_stroke(color=ORANGE):
            box = Square(side_length=0.85, color=GREY_D, stroke_width=1.5,
                         fill_opacity=0.08, fill_color=WHITE)
            arc = ArcBetweenPoints(LEFT * 0.25, RIGHT * 0.25,
                                   angle=PI / 1.3, color=color,
                                   stroke_width=5)
            return VGroup(box, arc)

        def make_digit(text, color=YELLOW):
            box = Square(side_length=1.0, color=GREY_D, stroke_width=1.5,
                         fill_opacity=0.08, fill_color=WHITE)
            t = Tex(text, font_size=42, color=color)
            t.move_to(box)
            return VGroup(box, t)

        layer_titles = VGroup(
            Tex("Pixels\\\\(input)", font_size=22, color=WHITE),
            Tex("Edges\\\\(layer 1)", font_size=22, color=BLUE),
            Tex("Strokes\\\\(layer 2)", font_size=22, color=ORANGE),
            Tex("Digits\\\\(output)", font_size=22, color=YELLOW),
        )
        xs = [-5.2, -2.0, 1.5, 5.0]
        for t, x in zip(layer_titles, xs):
            t.move_to([x, 2.5, 0])
        self.play(LaggedStart(*[FadeIn(t) for t in layer_titles],
                              lag_ratio=0.1))

        pix_box = Square(side_length=1.6, color=WHITE, stroke_width=2,
                         fill_opacity=0.15)
        pix_box.move_to([xs[0], 0.6, 0])
        pix_tex = Tex("$\\mathbf{x}$", font_size=34).move_to(pix_box)
        self.play(FadeIn(pix_box), FadeIn(pix_tex))

        edges = VGroup(
            make_edge("horiz"), make_edge("vert"),
            make_edge("diag1"), make_edge("diag2"),
        )
        for e, y in zip(edges, [1.7, 0.7, -0.3, -1.3]):
            e.move_to([xs[1], y, 0])
        self.play(LaggedStart(*[FadeIn(e) for e in edges],
                              lag_ratio=0.15))

        strokes = VGroup(
            make_loop(), make_stroke(), make_loop(),
        )
        for s, y in zip(strokes, [1.2, 0, -1.2]):
            s.move_to([xs[2], y, 0])
        self.play(LaggedStart(*[FadeIn(s) for s in strokes],
                              lag_ratio=0.15))

        digits = VGroup(*[
            make_digit(str(d)) for d in [0, 8, 3]
        ])
        for d, y in zip(digits, [1.3, 0, -1.3]):
            d.move_to([xs[3], y, 0])
        self.play(LaggedStart(*[FadeIn(d) for d in digits],
                              lag_ratio=0.15))

        connectors = VGroup()
        for src in [pix_box]:
            for dst in edges:
                connectors.add(Line(src.get_right(), dst[0].get_left(),
                                    stroke_width=1, color=GREY_B))
        for src in edges:
            for dst in strokes:
                connectors.add(Line(src[0].get_right(), dst[0].get_left(),
                                    stroke_width=1, color=GREY_B))
        for src in strokes:
            for dst in digits:
                connectors.add(Line(src[0].get_right(), dst[0].get_left(),
                                    stroke_width=1, color=GREY_B))
        self.play(Create(connectors, lag_ratio=0.02, run_time=2.0))

        caption = Tex(
            r"The explanatory story: each layer composes the previous one's features.\\"
            r"(Empirically, real trained networks seldom decompose this cleanly.)",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(caption))
        self.wait(1.5)
