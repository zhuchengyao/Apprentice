from manim import *
import numpy as np


class LinearityAvPlusWExample(Scene):
    """
    Linearity: A(v + w) = Av + Aw. Add vectors tip-to-tail; apply A
    to each; result is the same as applying A to their sum.
    """

    def construct(self):
        title = Tex(r"$A(\vec v+\vec w)=A\vec v+A\vec w$ (additivity)",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 5, 1], y_range=[-3, 3, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        A = np.array([[1.0, 0.5], [-1.0, 1.0]])
        v = np.array([2.0, -1.0])
        w = np.array([1.0, 2.0])

        stage_tr = ValueTracker(0.0)

        def M_of():
            t = stage_tr.get_value()
            return (1 - t) * np.eye(2) + t * A

        def v_arrow():
            M = M_of()
            p = M @ v
            return Arrow(plane.c2p(0, 0), plane.c2p(p[0], p[1]),
                          color=YELLOW, buff=0, stroke_width=5)

        def w_arrow():
            M = M_of()
            Av = M @ v
            Aw = M @ w
            return Arrow(plane.c2p(Av[0], Av[1]),
                          plane.c2p(Av[0] + Aw[0], Av[1] + Aw[1]),
                          color=MAROON_B, buff=0, stroke_width=5)

        def sum_arrow():
            M = M_of()
            Avw = M @ (v + w)
            return Arrow(plane.c2p(0, 0), plane.c2p(Avw[0], Avw[1]),
                          color=PINK, buff=0, stroke_width=6)

        self.add(always_redraw(v_arrow), always_redraw(w_arrow), always_redraw(sum_arrow))

        # Labels — use updaters to keep in place
        v_lbl = always_redraw(lambda: Tex(r"$\vec v$", color=YELLOW, font_size=24).move_to(
            plane.c2p(*(M_of() @ v)) + UP * 0.3))
        w_lbl = always_redraw(lambda: Tex(r"$\vec w$", color=MAROON_B, font_size=24).move_to(
            plane.c2p(*(M_of() @ v + M_of() @ w)) + UP * 0.3 + RIGHT * 0.3))
        sum_lbl = always_redraw(lambda: Tex(r"$\vec v+\vec w$", color=PINK, font_size=22).move_to(
            plane.c2p(*(M_of() @ (v + w))) + DOWN * 0.3))
        self.add(v_lbl, w_lbl, sum_lbl)

        self.play(stage_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        # Display formula with colored terms
        formula = MathTex(r"A(\vec v + \vec w)", r"=", r"A\vec v", r"+", r"A\vec w",
                           font_size=36).to_edge(DOWN, buff=0.4)
        formula[0].set_color(PINK)
        formula[2].set_color(YELLOW)
        formula[4].set_color(MAROON_B)
        self.play(Write(formula))
        self.wait(1.0)
