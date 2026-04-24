from manim import *
import numpy as np


class SecantToTangentExample(Scene):
    def construct(self):
        title = Text("Secant approaches tangent as dt → 0", font_size=28).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 4, 1], y_range=[-1, 8, 2],
            x_length=7, y_length=4.2,
            axis_config={"include_tip": True},
        ).shift(0.3 * DOWN)
        graph = axes.plot(lambda t: 0.5 * t**2 + 0.2, x_range=[0.1, 3.8], color=BLUE)
        self.play(Create(axes), Create(graph))

        t0 = 1.6
        f = lambda t: 0.5 * t**2 + 0.2
        p0 = Dot(axes.c2p(t0, f(t0)), color=YELLOW)
        self.play(FadeIn(p0))

        dt = ValueTracker(1.6)

        def secant():
            a = axes.c2p(t0, f(t0))
            b = axes.c2p(t0 + dt.get_value(), f(t0 + dt.get_value()))
            direction = np.array(b) - np.array(a)
            unit = direction / np.linalg.norm(direction)
            extended_left = np.array(a) - unit * 1.2
            extended_right = np.array(b) + unit * 0.8
            return Line(extended_left, extended_right, color=ORANGE, stroke_width=3)

        def moving_dot():
            return Dot(axes.c2p(t0 + dt.get_value(), f(t0 + dt.get_value())), color=RED)

        sec = always_redraw(secant)
        md = always_redraw(moving_dot)
        self.play(Create(sec), FadeIn(md))
        self.wait(0.3)

        slope_txt = always_redraw(lambda: MathTex(
            rf"\text{{slope}} \approx {(f(t0 + dt.get_value()) - f(t0)) / dt.get_value():.3f}",
            font_size=30, color=ORANGE,
        ).to_corner(DL))
        self.add(slope_txt)

        self.play(dt.animate.set_value(0.05), run_time=3)
        self.wait(0.4)

        exact = MathTex(r"f'(t_0) = t_0 = 1.6", color=YELLOW, font_size=32).to_corner(DR)
        self.play(Write(exact))
        self.wait(0.6)
