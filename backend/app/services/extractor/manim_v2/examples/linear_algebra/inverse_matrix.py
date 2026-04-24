from manim import *


class InverseMatrixExample(Scene):
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.35})
        unit_sq = Polygon(ORIGIN, RIGHT, RIGHT + UP, UP,
                          color=YELLOW, fill_opacity=0.5, stroke_width=3)
        self.add(plane, unit_sq)

        A = [[2, 1], [1, 1]]
        A_inv = [[1, -1], [-1, 2]]

        label_a = MathTex(r"\text{apply }A", font_size=32)
        label_a.to_corner(UL).add_background_rectangle()
        self.play(Write(label_a))
        self.play(ApplyMatrix(A, plane), ApplyMatrix(A, unit_sq), run_time=2)

        label_ai = MathTex(r"\text{apply }A^{-1}", font_size=32)
        label_ai.to_corner(UL).add_background_rectangle()
        self.play(Transform(label_a, label_ai))
        self.play(ApplyMatrix(A_inv, plane), ApplyMatrix(A_inv, unit_sq), run_time=2)

        eqn = MathTex(r"A A^{-1} = I", font_size=36).to_edge(DOWN).add_background_rectangle()
        self.play(Write(eqn))
        self.wait(0.6)
