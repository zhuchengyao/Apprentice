from manim import *
import numpy as np


class FourierSeriesAnimationExample(Scene):
    def construct(self):
        title = Text("Rotating vectors summing to a signal", font_size=28).to_edge(UP)
        self.play(Write(title))

        # Simple 3-term Fourier-like sum producing a square-ish wave at x=0
        freqs = [1, 3, 5]
        amps = [1.0, 1 / 3, 1 / 5]
        phases = [0, 0, 0]

        t_tracker = ValueTracker(0.0)
        anchor = LEFT * 4 + 0 * UP

        def circle_chain():
            group = VGroup()
            start = anchor.copy()
            for f, a, phi in zip(freqs, amps, phases):
                theta = t_tracker.get_value() * f + phi
                end = start + a * np.array([np.cos(theta), np.sin(theta), 0])
                circle = Circle(radius=a, color=BLUE, stroke_width=1).move_to(start)
                arm = Line(start, end, color=YELLOW, stroke_width=2)
                group.add(circle, arm)
                start = end
            return group

        tip_trace_points = []

        def tip():
            start = anchor.copy()
            for f, a, phi in zip(freqs, amps, phases):
                theta = t_tracker.get_value() * f + phi
                start = start + a * np.array([np.cos(theta), np.sin(theta), 0])
            return Dot(start, color=RED, radius=0.07)

        graph_origin = RIGHT * 1.3

        def traced_graph():
            start = anchor.copy()
            for f, a, phi in zip(freqs, amps, phases):
                theta = t_tracker.get_value() * f + phi
                start = start + a * np.array([np.cos(theta), np.sin(theta), 0])
            y = start[1]
            # Use t_tracker to advance the x coordinate
            x = graph_origin[0] + (t_tracker.get_value() % (2 * PI)) / (2 * PI) * 4
            tip_trace_points.append(np.array([x, y, 0]))
            if len(tip_trace_points) > 300:
                tip_trace_points.pop(0)
            path = VMobject(color=RED, stroke_width=2)
            path.set_points_as_corners(tip_trace_points if len(tip_trace_points) > 1 else [tip_trace_points[0]] * 2)
            return path

        chain = always_redraw(circle_chain)
        tip_dot = always_redraw(tip)
        graph = always_redraw(traced_graph)
        axis = Line(graph_origin + UP * 1.5, graph_origin + DOWN * 1.5, color=GREY_B)
        xax = Line(graph_origin + LEFT * 0.1, graph_origin + RIGHT * 4.2, color=GREY_B)
        self.play(Create(axis), Create(xax))
        self.add(chain, tip_dot, graph)

        self.play(t_tracker.animate.set_value(2 * PI), run_time=5, rate_func=linear)
        self.wait(0.3)

        formula = MathTex(r"f(t) = \sum_k A_k \cos(k\omega t + \varphi_k)",
                          font_size=30, color=YELLOW).to_edge(DOWN)
        self.play(Write(formula))
        self.wait(0.6)
