from manim import *
import numpy as np


class GradientEvaluatedAtPoint(Scene):
    """Symbolic gradient (df/dx, df/dy) of e^(-x^2+cos(2y)),
    then plug (x, y) = (1, 3) to get a concrete numerical vector."""

    def construct(self):
        title = Tex(
            r"The gradient at a point is a concrete vector",
            font_size=26,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        lhs = MathTex(r"\nabla f(x, y) =", font_size=38)
        formula = Matrix(
            [
                [r"e^{-x^{2}+\cos(2y)}(-2x)"],
                [r"e^{-x^{2}+\cos(2y)}(-2\sin(2y))"],
            ],
            v_buff=1.2,
            element_alignment_corner=ORIGIN,
            h_buff=1.0,
        )
        symbolic = VGroup(lhs, formula).arrange(RIGHT, buff=0.2)
        symbolic.scale(0.75).shift(1.4 * UP)
        self.play(FadeIn(lhs), FadeIn(formula))
        self.wait(0.4)

        lhs_at = MathTex(r"\nabla f(1, 3) =", font_size=38)
        formula_at = Matrix(
            [
                [r"e^{-1+\cos(6)}(-2)"],
                [r"e^{-1+\cos(6)}(-2\sin(6))"],
            ],
            v_buff=1.2,
            element_alignment_corner=ORIGIN,
            h_buff=1.0,
        )
        evaluated = VGroup(lhs_at, formula_at).arrange(RIGHT, buff=0.2)
        evaluated.scale(0.75).shift(0.5 * DOWN)
        self.play(
            TransformFromCopy(lhs, lhs_at),
            TransformFromCopy(formula, formula_at),
        )
        self.wait(0.6)

        base = np.exp(-1 + np.cos(6.0))
        nx = base * (-2)
        ny = base * (-2 * np.sin(6.0))

        approx_eq = MathTex(r"\approx", font_size=38)
        numeric = DecimalMatrix(
            [[nx], [ny]],
            element_to_mobject_config={"num_decimal_places": 2},
            v_buff=1.2,
        )
        numeric_grp = VGroup(approx_eq, numeric).arrange(RIGHT, buff=0.2)
        numeric_grp.scale(0.75).next_to(formula_at, RIGHT, buff=0.2)
        self.play(Write(approx_eq), FadeIn(numeric))

        hi = SurroundingRectangle(numeric, color=YELLOW, buff=0.1)
        caption = Tex(
            r"The gradient at $(1,3)$ points in this direction",
            font_size=24, color=YELLOW,
        ).next_to(hi, DOWN, buff=0.4)
        self.play(Create(hi), Write(caption))
        self.wait(1.2)
