from manim import *


class CompositionOfTransformationsExample(Scene):
    def construct(self):
        title = Text("Matrix multiplication = composition of transformations",
                     font_size=24).to_edge(UP)
        self.play(Write(title))

        plane = NumberPlane(background_line_style={"stroke_opacity": 0.35})
        self.add(plane)

        A = [[1, 1], [0, 1]]  # shear
        B = [[0, -1], [1, 0]]  # rotation 90°

        label_a = MathTex(r"\text{apply } A\ (\text{shear})", font_size=28)
        label_a.to_corner(UL).add_background_rectangle()
        self.play(Write(label_a))
        self.play(ApplyMatrix(A, plane), run_time=2)

        label_b = MathTex(r"\text{then apply } B\ (\text{rotation})", font_size=28)
        label_b.to_corner(UL).add_background_rectangle()
        self.play(Transform(label_a, label_b))
        self.play(ApplyMatrix(B, plane), run_time=2)

        product = MathTex(r"BA = \begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}"
                          r"\begin{bmatrix}1 & 1 \\ 0 & 1\end{bmatrix}"
                          r" = \begin{bmatrix}0 & -1 \\ 1 & 1\end{bmatrix}",
                          font_size=28)
        product.to_edge(DOWN).add_background_rectangle()
        self.play(Write(product))
        self.wait(0.6)
