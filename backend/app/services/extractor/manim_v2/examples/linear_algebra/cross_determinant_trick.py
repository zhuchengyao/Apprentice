from manim import *
import numpy as np


class CrossDeterminantTrickExample(Scene):
    """
    Determinant trick for 3D cross product: write
      v × w = det |i  j  k |
                 |v_1 v_2 v_3|
                 |w_1 w_2 w_3|
    Expanding along the first row gives the component formula.
    """

    def construct(self):
        title = Tex(r"Determinant mnemonic for 3D $\vec v\times\vec w$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Show the determinant form
        det_form = MathTex(
            r"\vec v\times\vec w=",
            r"\det",
            r"\begin{pmatrix}\hat\imath&\hat\jmath&\hat k\\v_1&v_2&v_3\\w_1&w_2&w_3\end{pmatrix}",
            font_size=36,
        )
        det_form.shift(UP * 1.2)
        # Color basis row
        self.play(Write(det_form))
        self.wait(0.5)

        # Expand: Laplace along first row
        expand = MathTex(
            r"=\hat\imath(v_2w_3-v_3w_2)",
            r"-\hat\jmath(v_1w_3-v_3w_1)",
            r"+\hat k(v_1w_2-v_2w_1)",
            font_size=26,
        )
        expand.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        expand.next_to(det_form, DOWN, buff=0.5)
        for e in expand:
            self.play(Write(e), run_time=0.9)
            self.wait(0.3)

        # Concrete example
        example = Tex(r"e.g.\ for $\vec v=(1, 2, 3), \vec w=(4,-1,2)$: $\vec v\times\vec w=(7, 10, -9)$",
                       color=YELLOW, font_size=22).to_edge(DOWN, buff=0.4)
        self.play(Write(example))
        self.wait(1.0)
