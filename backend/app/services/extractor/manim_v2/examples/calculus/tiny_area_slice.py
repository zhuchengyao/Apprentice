from manim import *
import numpy as np


class TinyAreaSliceExample(Scene):
    def construct(self):
        title = Text("dA/dx: a thin slice of the area under a curve", font_size=26).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 4, 1], y_range=[0, 3, 1],
            x_length=8, y_length=4,
            axis_config={"include_tip": True, "include_numbers": True},
        ).shift(0.3 * DOWN)
        graph = axes.plot(lambda x: 0.4 * x * x + 0.3, x_range=[0, 3.9], color=BLUE)
        self.play(Create(axes), Create(graph))

        x0 = 2.2
        dx_tracker = ValueTracker(0.55)

        def area_under():
            return axes.get_area(graph, x_range=[0, x0], color=BLUE, opacity=0.35)

        def slice_rect():
            dx = dx_tracker.get_value()
            fx = 0.4 * x0 * x0 + 0.3
            return Polygon(
                axes.c2p(x0, 0),
                axes.c2p(x0 + dx, 0),
                axes.c2p(x0 + dx, fx),
                axes.c2p(x0, fx),
                color=YELLOW, fill_color=YELLOW, fill_opacity=0.7, stroke_width=2,
            )

        a = area_under()
        self.play(FadeIn(a))

        slice_m = always_redraw(slice_rect)
        self.add(slice_m)

        readout = always_redraw(lambda: MathTex(
            rf"dx = {dx_tracker.get_value():.2f},\;\; f(x_0)\cdot dx = {(0.4 * x0 * x0 + 0.3) * dx_tracker.get_value():.3f}",
            font_size=26,
        ).to_edge(DOWN).shift(UP * 0.4))
        self.add(readout)

        self.play(dx_tracker.animate.set_value(0.05), run_time=3)
        self.wait(0.3)

        rule = MathTex(r"\frac{dA}{dx} = f(x)", font_size=38, color=YELLOW).to_edge(DOWN)
        self.remove(readout)
        self.play(Write(rule))
        self.wait(0.6)
