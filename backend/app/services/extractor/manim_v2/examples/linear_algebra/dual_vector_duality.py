from manim import *
import numpy as np


class DualVectorDualityExample(Scene):
    """
    Duality: every vector v = (a, b) corresponds to a linear map
    ℝ² → ℝ via dot product: L_v(x) = v·x = ax + by. The 1×2 matrix
    form of L_v is just [a b].

    Visualize: a vector v in the plane ↔ a functional L_v on vectors.
    """

    def construct(self):
        title = Tex(r"Vector-functional duality: $\vec v \leftrightarrow L_{\vec v}(\vec x)=\vec v\cdot\vec x$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                            x_length=5.5, y_length=4.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.0 + DOWN * 0.2)
        self.play(Create(plane))

        # Right side: symbolic duality
        v = np.array([2.0, 1.0])
        v_arrow = Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                         color=BLUE, buff=0, stroke_width=5)
        v_lbl = Tex(r"$\vec v=(2, 1)$", color=BLUE, font_size=22).next_to(v_arrow.get_end(), UR, buff=0.05)
        self.play(Create(v_arrow), Write(v_lbl))

        # Arrow pointing right
        big_arrow = Arrow(plane.get_right() + RIGHT * 0.3,
                           plane.get_right() + RIGHT * 1.5,
                           color=YELLOW, stroke_width=5)
        big_arrow_lbl = Tex(r"dual", color=YELLOW, font_size=22).next_to(big_arrow, UP, buff=0.1)
        self.play(Create(big_arrow), Write(big_arrow_lbl))

        # Right: functional form
        functional = VGroup(
            MathTex(r"L_{\vec v}", color=BLUE, font_size=36),
            MathTex(r"=", font_size=36),
            Matrix([["2", "1"]]).set_color(BLUE).scale(0.9),
        ).arrange(RIGHT, buff=0.2).shift(RIGHT * 3.5 + UP * 1.0)
        self.play(Write(functional))
        self.wait(0.4)

        # Show action on a sample vector
        sample_note = VGroup(
            MathTex(r"L_{\vec v}(3, -2)=2\cdot 3+1\cdot(-2)=4",
                      color=YELLOW, font_size=28),
            Tex(r"i.e. $\vec v\cdot (3, -2)=4$",
                 color=YELLOW, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(RIGHT * 3.0 + DOWN * 1.0)
        self.play(Write(sample_note))
        self.wait(0.5)

        # Explanation
        expl = Tex(r"every 2D vector is a 1$\times$2 matrix in disguise",
                    color=GREEN, font_size=24).to_edge(DOWN, buff=0.4)
        self.play(Write(expl))
        self.wait(1.0)
