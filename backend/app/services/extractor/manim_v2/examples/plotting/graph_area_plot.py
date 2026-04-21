from manim import *


class GraphAreaPlotExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 6, 1],
            x_length=7,
            y_length=4,
            tips=False,
        ).to_edge(DOWN, buff=0.5)
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        graph = axes.plot(lambda x: 0.1 * x ** 2 + 0.5, color=BLUE)
        label = axes.get_graph_label(graph, label=r"f(x) = 0.1 x^{2} + \tfrac{1}{2}")

        area = axes.get_area(graph, x_range=[0.8, 4.2], color=GREEN, opacity=0.45)

        self.play(Create(axes), Write(labels))
        self.play(Create(graph), Write(label))
        self.play(FadeIn(area))
        self.wait(0.4)

        riemann = axes.get_riemann_rectangles(
            graph, x_range=[0.8, 4.2], dx=0.4, stroke_width=0.5, fill_opacity=0.6,
        )
        self.play(ReplacementTransform(area, riemann))
        self.wait(0.6)
