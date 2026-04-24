from manim import *
import numpy as np


class SecondDerivativeConcavityExample(Scene):
    def construct(self):
        title = Text("Second derivative = concavity", font_size=30).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-3, 5, 2],
            x_length=8, y_length=4.2,
            axis_config={"include_tip": True},
        ).shift(0.3 * DOWN)
        self.play(Create(axes))

        f = lambda x: x**3 - 2 * x
        fpp = lambda x: 6 * x

        graph = axes.plot(f, x_range=[-2.1, 2.1], color=BLUE)
        self.play(Create(graph))

        x_tracker = ValueTracker(-1.7)

        def osc_circle():
            x = x_tracker.get_value()
            curv = fpp(x)
            if abs(curv) < 0.5:
                curv = 0.5 * np.sign(curv) if curv != 0 else 0.5
            radius_world = 1.0 / abs(curv)
            sign = -1 if curv > 0 else 1  # circle sits on the concavity side
            center = axes.c2p(x, f(x) + sign * radius_world)
            color = RED if curv > 0 else GREEN
            scale = (axes.c2p(1, 0)[0] - axes.c2p(0, 0)[0])
            return Circle(radius=radius_world * scale, color=color, stroke_width=3).move_to(center)

        def pt():
            x = x_tracker.get_value()
            return Dot(axes.c2p(x, f(x)), color=YELLOW, radius=0.09)

        def readout():
            x = x_tracker.get_value()
            return MathTex(
                rf"x = {x:.2f},\; f''(x) = {fpp(x):+.2f}",
                font_size=28,
            ).to_corner(DR)

        oc = always_redraw(osc_circle)
        p = always_redraw(pt)
        r = always_redraw(readout)
        self.add(oc, p, r)

        self.play(x_tracker.animate.set_value(1.7), run_time=4, rate_func=linear)
        self.wait(0.3)

        caption = Text("red = concave down (f'' < 0), green = concave up (f'' > 0)",
                       font_size=22, color=YELLOW).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
