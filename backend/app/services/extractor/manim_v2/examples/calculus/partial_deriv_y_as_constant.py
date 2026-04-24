from manim import *
import numpy as np


class PartialDerivYAsConstant(Scene):
    """Compute d f/dx of f(x, y) = e^(-x^2 + cos(2y)) by pinning every
    occurrence of y with a 'constant' arrow before differentiating."""

    def construct(self):
        title = Tex(
            r"Partial $\partial/\partial x$: every $y$ is frozen",
            font_size=26,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        f = MathTex(
            "f(", "x", ",", "y", ")", "=",
            "e^{", "-", "x", "^{2}", "+", r"\cos(", "2", "y", ")}",
            font_size=40,
        )
        f.shift(UP * 1.2)
        for idx in (1, 8):
            f[idx].set_color(BLUE)
        for idx in (3, 13):
            f[idx].set_color(RED)
        self.play(FadeIn(f))
        self.wait(0.4)

        frozen_arrows = VGroup()
        for yterm in (f[3], f[13]):
            a = Arrow(
                yterm.get_top() + UP * 0.55,
                yterm.get_top() + UP * 0.08,
                buff=0,
                color=RED,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.35,
            )
            frozen_arrows.add(a)
        const_txt = Tex(
            "constant", font_size=24, color=RED
        ).next_to(frozen_arrows, UP, buff=0.05)
        self.play(
            LaggedStart(*[GrowArrow(a) for a in frozen_arrows], lag_ratio=0.3),
            Write(const_txt),
        )
        self.wait(0.8)

        moving_arrows = VGroup()
        for xterm in (f[1], f[8]):
            a = Arrow(
                xterm.get_bottom() + DOWN * 0.55,
                xterm.get_bottom() + DOWN * 0.08,
                buff=0,
                color=BLUE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.35,
            )
            moving_arrows.add(a)
        var_txt = Tex(
            "variable", font_size=24, color=BLUE
        ).next_to(moving_arrows, DOWN, buff=0.05)
        self.play(
            LaggedStart(*[GrowArrow(a) for a in moving_arrows], lag_ratio=0.3),
            Write(var_txt),
        )
        self.wait(0.6)

        deriv = MathTex(
            r"\frac{\partial f}{\partial x}", "=",
            r"e^{-x^{2}+\cos(2y)}", r"\cdot", "(-2x)",
            font_size=40,
        )
        deriv[0][-1].set_color(BLUE)
        deriv.shift(1.6 * DOWN)
        self.play(Write(deriv[0:2]))
        self.wait(0.3)
        self.play(ReplacementTransform(f[6:].copy(), deriv[2]))
        self.wait(0.5)
        self.play(Write(deriv[3]), FadeIn(deriv[4]))
        self.wait(0.6)

        note = Tex(
            r"Chain rule: outer $\times$ derivative of $-x^{2}$",
            font_size=26, color=YELLOW,
        ).next_to(deriv, DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(1.0)
