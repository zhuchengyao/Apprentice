from manim import *
import numpy as np


class DotProductSymmetricSwapExample(Scene):
    """
    v·w = w·v (commutativity/symmetry). Visual: projecting v onto w
    gives |v|cos θ · |w|; projecting w onto v gives |w|cos θ · |v|.
    Both equal |v||w|cos θ — same answer.
    """

    def construct(self):
        title = Tex(r"Symmetry: $\vec v\cdot\vec w=\vec w\cdot\vec v$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Two planes side by side
        left = NumberPlane(x_range=[-2, 3, 1], y_range=[-1, 3, 1],
                           x_length=4.5, y_length=4.5,
                           background_line_style={"stroke_opacity": 0.3}
                           ).shift(LEFT * 3.3)
        right = NumberPlane(x_range=[-2, 3, 1], y_range=[-1, 3, 1],
                            x_length=4.5, y_length=4.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(RIGHT * 2.5)
        self.play(Create(left), Create(right))

        v = np.array([2.5, 0.5])
        w = np.array([1.0, 2.0])

        # Left plane: project v onto w direction
        v_arrow_l = Arrow(left.c2p(0, 0), left.c2p(v[0], v[1]),
                           color=BLUE, buff=0, stroke_width=5)
        w_arrow_l = Arrow(left.c2p(0, 0), left.c2p(w[0], w[1]),
                           color=ORANGE, buff=0, stroke_width=5)
        # Projection of v onto w
        w_hat = w / np.linalg.norm(w)
        proj_v_on_w = np.dot(v, w_hat) * w_hat
        proj_v_arrow = Arrow(left.c2p(0, 0), left.c2p(proj_v_on_w[0], proj_v_on_w[1]),
                              color=YELLOW, buff=0, stroke_width=4)
        drop_v = DashedLine(left.c2p(v[0], v[1]),
                             left.c2p(proj_v_on_w[0], proj_v_on_w[1]),
                             color=GREY_B, stroke_width=2)
        self.add(v_arrow_l, w_arrow_l, proj_v_arrow, drop_v)
        self.add(Tex(r"$\vec v$", color=BLUE, font_size=22).next_to(v_arrow_l.get_end(), UR, buff=0.05))
        self.add(Tex(r"$\vec w$", color=ORANGE, font_size=22).next_to(w_arrow_l.get_end(), UL, buff=0.05))
        self.add(Tex(r"proj$_{\vec w}\vec v$", color=YELLOW, font_size=20).next_to(proj_v_arrow.get_end(), DR, buff=0.05))

        # Right plane: project w onto v direction
        v_arrow_r = Arrow(right.c2p(0, 0), right.c2p(v[0], v[1]),
                           color=BLUE, buff=0, stroke_width=5)
        w_arrow_r = Arrow(right.c2p(0, 0), right.c2p(w[0], w[1]),
                           color=ORANGE, buff=0, stroke_width=5)
        v_hat = v / np.linalg.norm(v)
        proj_w_on_v = np.dot(w, v_hat) * v_hat
        proj_w_arrow = Arrow(right.c2p(0, 0), right.c2p(proj_w_on_v[0], proj_w_on_v[1]),
                              color=YELLOW, buff=0, stroke_width=4)
        drop_w = DashedLine(right.c2p(w[0], w[1]),
                             right.c2p(proj_w_on_v[0], proj_w_on_v[1]),
                             color=GREY_B, stroke_width=2)
        self.add(v_arrow_r, w_arrow_r, proj_w_arrow, drop_w)
        self.add(Tex(r"$\vec v$", color=BLUE, font_size=22).next_to(v_arrow_r.get_end(), UR, buff=0.05))
        self.add(Tex(r"$\vec w$", color=ORANGE, font_size=22).next_to(w_arrow_r.get_end(), UL, buff=0.05))
        self.add(Tex(r"proj$_{\vec v}\vec w$", color=YELLOW, font_size=20).next_to(proj_w_arrow.get_end(), DR, buff=0.05))

        # Titles above each plane
        self.add(Tex(r"$\vec v\cdot\vec w=|\vec w|\cdot|\text{proj}_{\vec w}\vec v|$",
                     font_size=20).move_to(left.get_top() + UP * 0.3))
        self.add(Tex(r"$\vec w\cdot\vec v=|\vec v|\cdot|\text{proj}_{\vec v}\vec w|$",
                     font_size=20).move_to(right.get_top() + UP * 0.3))

        # Numeric value
        val = float(np.dot(v, w))
        self.play(Write(
            Tex(rf"both equal $|\vec v||\vec w|\cos\theta={val:.2f}$",
                color=GREEN, font_size=24).to_edge(DOWN, buff=0.4)
        ))
        self.wait(1.0)
