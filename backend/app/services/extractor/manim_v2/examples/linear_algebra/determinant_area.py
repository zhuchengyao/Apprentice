from manim import *


class DeterminantAreaExample(Scene):
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.35})
        unit_sq = Polygon(
            ORIGIN, RIGHT, RIGHT + UP, UP,
            color=YELLOW, fill_opacity=0.5, stroke_width=3,
        )
        matrix = [[2, 1], [0, 2]]
        self.add(plane, unit_sq)

        label0 = MathTex(r"\text{Area} = 1", font_size=34).to_corner(UL).add_background_rectangle()
        self.play(Write(label0))
        self.wait(0.3)

        self.play(ApplyMatrix(matrix, plane), ApplyMatrix(matrix, unit_sq), run_time=2)

        label1 = MathTex(r"\text{Area} = |\det A| = 4", font_size=34)
        label1.to_corner(UL).add_background_rectangle()
        self.play(Transform(label0, label1))
        self.wait(0.6)
