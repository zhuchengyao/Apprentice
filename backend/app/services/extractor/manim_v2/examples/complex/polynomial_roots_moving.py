from manim import *
import numpy as np


class PolynomialRootsMovingExample(Scene):
    def construct(self):
        title = Text("Moving polynomial coefficient shifts roots continuously", font_size=26).to_edge(UP)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                             background_line_style={"stroke_opacity": 0.4}).shift(0.2 * DOWN)
        self.play(Create(plane))

        c = ValueTracker(-2.0)

        # p(z) = z^3 + c*z + 1, roots depend on c
        def roots_of(c_val):
            coeffs = [1, 0, c_val, 1]
            return np.roots(coeffs)

        def roots_dots():
            rs = roots_of(c.get_value())
            group = VGroup()
            for r in rs:
                group.add(Dot(plane.n2p(complex(r)), color=YELLOW, radius=0.11))
            return group

        dots = always_redraw(roots_dots)
        self.add(dots)

        readout = always_redraw(lambda: MathTex(
            rf"p(z) = z^3 + ({c.get_value():.2f})z + 1", font_size=30,
        ).to_edge(DOWN))
        self.add(readout)

        self.play(c.animate.set_value(2.0), run_time=4, rate_func=smooth)
        self.play(c.animate.set_value(-2.0), run_time=4, rate_func=smooth)
        self.wait(0.3)

        cap = Text("Real roots become complex conjugate pairs at a bifurcation.",
                   font_size=22, color=YELLOW).to_edge(UP).shift(DOWN * 0.55)
        self.play(Write(cap))
        self.wait(0.6)
