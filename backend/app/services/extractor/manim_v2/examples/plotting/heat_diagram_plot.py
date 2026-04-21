from manim import *


class HeatDiagramPlotExample(Scene):
    def construct(self):
        energies = [1, 2, 3, 4, 5, 6]
        temps = [30, 35, 55, 70, 72, 74]

        axes = Axes(
            x_range=[0, 7, 1],
            y_range=[0, 100, 20],
            x_length=7,
            y_length=4,
            tips=False,
            axis_config={"include_numbers": True},
        ).to_edge(DOWN, buff=0.5)
        labels = axes.get_axis_labels(x_label=r"Q\,(\mathrm{kJ})", y_label=r"T\,(^{\circ}C)")

        graph = axes.plot_line_graph(
            x_values=energies,
            y_values=temps,
            line_color=BLUE,
            vertex_dot_style={"stroke_width": 3, "fill_color": YELLOW},
        )

        self.play(Create(axes), Write(labels))
        self.play(Create(graph), run_time=2.5)
        self.wait(0.5)
