from manim import *
import numpy as np


class ComplexFunctionGridExample(Scene):
    def construct(self):
        title = MathTex(r"z \mapsto z^2", font_size=40).to_corner(UL).add_background_rectangle()
        plane = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1]).add_coordinates()
        self.add(plane)
        self.play(Write(title))

        def squared_point(p):
            z = complex(p[0], p[1])
            w = z * z
            return np.array([w.real, w.imag, 0])

        self.play(ApplyPointwiseFunction(squared_point, plane), run_time=3)
        self.wait(0.6)
