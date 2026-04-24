from manim import *
import numpy as np


class DxSquaredViaSquareExample(Scene):
    """
    Geometric derivation: d(x²)/dx = 2x.
    Consider a square of side x, area x². Nudge the side by dx:
    new area (x+dx)² = x² + 2x·dx + dx².
    The added region is: two strips of dimensions x·dx, plus a tiny
    corner dx·dx. dx² is negligible → dA ≈ 2x·dx → dA/dx = 2x.
    """

    def construct(self):
        title = Tex(r"$\frac{d(x^2)}{dx}=2x$ via square",
                    font_size=30).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Main square
        x = 2.0
        dx_tr = ValueTracker(0.4)

        origin = LEFT * 2.0 + DOWN * 0.3

        def main_square():
            return Square(side_length=x * 1.3,
                           color=BLUE, fill_color=BLUE,
                           fill_opacity=0.45).move_to(
                origin + RIGHT * x / 2 * 1.3 + UP * x / 2 * 1.3)

        def right_strip():
            dx = dx_tr.get_value()
            if dx < 0.02: return VMobject()
            return Rectangle(width=dx * 1.3, height=x * 1.3,
                              color=GREEN, fill_color=GREEN,
                              fill_opacity=0.7).move_to(
                origin + RIGHT * (x + dx / 2) * 1.3 + UP * x / 2 * 1.3)

        def top_strip():
            dx = dx_tr.get_value()
            if dx < 0.02: return VMobject()
            return Rectangle(width=x * 1.3, height=dx * 1.3,
                              color=GREEN, fill_color=GREEN,
                              fill_opacity=0.7).move_to(
                origin + RIGHT * x / 2 * 1.3 + UP * (x + dx / 2) * 1.3)

        def corner():
            dx = dx_tr.get_value()
            if dx < 0.02: return VMobject()
            return Rectangle(width=dx * 1.3, height=dx * 1.3,
                              color=RED, fill_color=RED,
                              fill_opacity=0.8).move_to(
                origin + RIGHT * (x + dx / 2) * 1.3 + UP * (x + dx / 2) * 1.3)

        self.add(main_square(), always_redraw(right_strip),
                 always_redraw(top_strip), always_redraw(corner))

        # Labels
        self.add(Tex(r"$x$", color=BLUE, font_size=24).move_to(origin + RIGHT * x / 2 * 1.3 + DOWN * 0.35))
        self.add(Tex(r"$x$", color=BLUE, font_size=24).move_to(origin + LEFT * 0.4 + UP * x / 2 * 1.3))
        self.add(Tex(r"area $=x^2$", color=BLUE, font_size=22).move_to(
            origin + RIGHT * x / 2 * 1.3 + UP * x / 2 * 1.3))

        # Right: algebraic expansion
        algebra = VGroup(
            MathTex(r"(x+dx)^2=x^2+2x\,dx+dx^2", font_size=26),
            MathTex(r"dA = 2x\,dx+dx^2", font_size=26),
            MathTex(r"\frac{dA}{dx}=2x+dx", font_size=28, color=YELLOW),
            MathTex(r"\lim_{dx\to 0}: \frac{dA}{dx}=2x", font_size=32, color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        self.play(Write(algebra[0]))
        self.wait(0.3)
        self.play(Write(algebra[1]))

        # Strip labels
        self.add(Tex(r"$x\,dx$", color=GREEN, font_size=18).move_to(
            origin + RIGHT * (x + 0.2) * 1.3 + UP * x / 2 * 1.3))
        self.add(Tex(r"$dx^2$", color=RED, font_size=18).move_to(
            origin + RIGHT * (x + 0.4) * 1.3 + UP * (x + 0.4) * 1.3))

        self.wait(0.5)
        self.play(Write(algebra[2]))
        self.wait(0.3)
        # Shrink dx to show limit
        self.play(dx_tr.animate.set_value(0.08), run_time=3, rate_func=smooth)
        self.play(Write(algebra[3]))
        self.wait(1.0)
