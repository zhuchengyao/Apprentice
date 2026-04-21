from manim import *


class PolygonOnAxesExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 8, 1],
            x_length=6,
            y_length=4,
            tips=False,
        ).to_edge(DOWN, buff=0.5)
        self.play(Create(axes))

        scale = ValueTracker(1.0)

        def make_polygon():
            s = scale.get_value()
            return Polygon(
                axes.c2p(1 * s, 2 * s),
                axes.c2p(4 * s, 1 * s),
                axes.c2p(5 * s, 5 * s),
                axes.c2p(2 * s, 6 * s),
                color=YELLOW,
                fill_color=ORANGE,
                fill_opacity=0.45,
            )

        poly = always_redraw(make_polygon)
        self.add(poly)
        self.play(scale.animate.set_value(1.3), run_time=2)
        self.play(scale.animate.set_value(0.7), run_time=2)
        self.wait(0.4)
