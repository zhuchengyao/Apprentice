from manim import *


class DeterminantNegativeExample(Scene):
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.35})
        i_hat = Arrow(ORIGIN, RIGHT, buff=0, color=GREEN, stroke_width=6)
        j_hat = Arrow(ORIGIN, UP, buff=0, color=RED, stroke_width=6)
        unit_sq = Polygon(
            ORIGIN, RIGHT, RIGHT + UP, UP,
            color=YELLOW, fill_opacity=0.5, stroke_width=3,
        )
        self.add(plane, unit_sq, i_hat, j_hat)

        matrix = [[1, 2], [2, 1]]
        label = MathTex(r"\det A = 1\cdot 1 - 2\cdot 2 = -3", font_size=34)
        label.to_corner(UL).add_background_rectangle()
        self.play(Write(label))

        new_i = Arrow(ORIGIN, RIGHT + 2 * UP, buff=0, color=GREEN, stroke_width=6)
        new_j = Arrow(ORIGIN, 2 * RIGHT + UP, buff=0, color=RED, stroke_width=6)
        self.play(
            ApplyMatrix(matrix, plane),
            ApplyMatrix(matrix, unit_sq),
            Transform(i_hat, new_i),
            Transform(j_hat, new_j),
            run_time=2.5,
        )
        caption = Text("Orientation flipped", font_size=28, color=RED)
        caption.to_edge(UP).add_background_rectangle()
        self.play(Write(caption))
        self.wait(0.6)
