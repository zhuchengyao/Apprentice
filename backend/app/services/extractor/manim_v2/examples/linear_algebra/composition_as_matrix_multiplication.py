from manim import *
import numpy as np


class CompositionAsMatrixMultiplicationExample(Scene):
    """
    Why is composition matrix multiplication? Expand:
       S · (R · v)  =  (SR) · v
    where (SR) is the composed matrix. Notation: the LEFT matrix
    acts LAST, like f(g(x)) — read right-to-left.

    SINGLE_FOCUS: write S(Rv), then transform it into (SR)v by
    grouping, labeled with "composition" and "read right to left",
    with f(g(x)) analogy written above.
    """

    def construct(self):
        title = Tex(r"Why is composition matrix multiplication?",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Stage 1: show S(Rv)
        eq1 = MathTex(r"S", r"\Big(", r"R", r"v", r"\Big)",
                       font_size=54)
        eq1.shift(UP * 1.3)
        eq1[0].set_color(PINK)
        eq1[2].set_color(TEAL)
        eq1[3].set_color(YELLOW)

        # Stage 2: rearrange to (SR)v
        eq2 = MathTex(r"\Big(", r"S", r"R", r"\Big)", r"v",
                       font_size=54)
        eq2.shift(DOWN * 0.3)
        eq2[1].set_color(PINK)
        eq2[2].set_color(TEAL)
        eq2[4].set_color(YELLOW)

        # Stage 3: define composition as matrix product
        eq3 = MathTex(r"SR", r"=", r"\text{``composition''}",
                       font_size=42)
        eq3.shift(DOWN * 1.8)
        eq3[0].set_submobject_colors_by_gradient(PINK, TEAL)

        arrow = Arrow(eq1.get_bottom(), eq2.get_top(), color=WHITE)

        # Stage 4: read right-to-left
        rtl_arrow = Arrow(eq2.get_right() + RIGHT * 0.3 + UP * 0.1,
                            eq2.get_left() + LEFT * 0.3 + UP * 0.1,
                            color=GREEN)
        rtl_lbl = Tex(r"read right-to-left", color=GREEN, font_size=24).next_to(
            rtl_arrow, UP, buff=0.15)

        # Stage 5: f(g(x)) analogy
        fg_tex = MathTex(r"\text{like } f(g(x))", font_size=32)
        fg_tex.set_color(ORANGE)
        fg_tex.to_corner(DR, buff=0.5)

        t_tr = ValueTracker(0.0)

        self.play(Write(eq1))
        self.wait(0.6)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.play(Write(eq2))
        self.wait(0.6)
        self.play(Write(eq3))
        self.wait(0.5)
        self.play(GrowArrow(rtl_arrow), Write(rtl_lbl))
        self.wait(0.5)
        self.play(Write(fg_tex))
        self.wait(0.8)

        # Animate: vector moving along rtl arrow
        def moving_dot():
            t = t_tr.get_value()
            start = eq2.get_right() + RIGHT * 0.3 + UP * 0.1
            end = eq2.get_left() + LEFT * 0.3 + UP * 0.1
            return Dot((1 - t) * start + t * end, color=GREEN, radius=0.12)

        self.add(always_redraw(moving_dot))

        for _ in range(3):
            self.play(t_tr.animate.set_value(1.0), run_time=1.5, rate_func=smooth)
            self.play(t_tr.animate.set_value(0.0), run_time=0.8)

        self.wait(0.5)
