from manim import *
import numpy as np


class EigenvectorStaysExample(Scene):
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.3})
        self.add(plane)

        matrix = [[2, 1], [0, 3]]
        eig1_dir = np.array([1, 0, 0])
        eig2_dir = np.array([1, 1, 0]) / np.sqrt(2)

        line1 = Line(-5 * eig1_dir, 5 * eig1_dir, color=YELLOW, stroke_width=4)
        line2 = Line(-5 * eig2_dir, 5 * eig2_dir, color=PINK, stroke_width=4)
        self.play(Create(line1), Create(line2))

        self.play(
            ApplyMatrix(matrix, plane),
            ApplyMatrix(matrix, line1),
            ApplyMatrix(matrix, line2),
            run_time=2.5,
        )

        caption = Text("Eigenvector lines stay on themselves", font_size=26)
        caption.to_edge(UP).add_background_rectangle()
        self.play(Write(caption))
        self.wait(0.6)
