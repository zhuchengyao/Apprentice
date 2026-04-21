from manim import *


class RiemannRectanglesRefineExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 9, 2],
            x_length=7,
            y_length=4,
            tips=False,
        ).to_edge(DOWN, buff=0.6)
        graph = axes.plot(lambda x: 0.6 * x ** 2, color=BLUE)
        label = axes.get_graph_label(graph, label=r"f(x) = \tfrac{3}{5} x^{2}").shift(RIGHT)

        self.play(Create(axes), Create(graph), Write(label))

        rects_coarse = axes.get_riemann_rectangles(
            graph, x_range=[0.3, 3.7], dx=0.6, stroke_width=0.5, fill_opacity=0.55,
        )
        self.play(FadeIn(rects_coarse))
        self.wait(0.3)

        rects_medium = axes.get_riemann_rectangles(
            graph, x_range=[0.3, 3.7], dx=0.3, stroke_width=0.4, fill_opacity=0.6,
        )
        self.play(ReplacementTransform(rects_coarse, rects_medium))
        self.wait(0.3)

        rects_fine = axes.get_riemann_rectangles(
            graph, x_range=[0.3, 3.7], dx=0.1, stroke_width=0.2, fill_opacity=0.65,
        )
        self.play(ReplacementTransform(rects_medium, rects_fine))
        self.wait(0.6)
