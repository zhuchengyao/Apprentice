from manim import *
import numpy as np


class DOneOverXRectangleExample(Scene):
    """
    d(1/x)/dx = -1/x² via rectangle with area 1.
    Rectangle of width x and height 1/x (so area = 1). Nudge width
    to x+dx. Height must shrink to 1/(x+dx) to keep area = 1.
    Change in height: 1/(x+dx) - 1/x = -dx/(x(x+dx)).
    So d(1/x)/dx = -1/x².
    """

    def construct(self):
        title = Tex(r"$\frac{d(1/x)}{dx}=-\frac{1}{x^2}$: rectangle of area $1$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane_center = DOWN * 0.4 + LEFT * 1.5
        x0 = 2.0

        x_tr = ValueTracker(x0)

        def rect():
            x = x_tr.get_value()
            h = 1 / x
            return Rectangle(width=x * 1.3, height=h * 2.5,
                              color=BLUE, stroke_width=2,
                              fill_color=BLUE, fill_opacity=0.5).move_to(
                plane_center + RIGHT * x / 2 * 1.3 + UP * h / 2 * 2.5)

        def width_lbl():
            x = x_tr.get_value()
            return Tex(rf"$x={x:.2f}$", color=BLUE, font_size=22).move_to(
                plane_center + RIGHT * x / 2 * 1.3 + DOWN * 0.3)

        def height_lbl():
            x = x_tr.get_value()
            h = 1 / x
            return Tex(rf"$1/x={h:.3f}$", color=GREEN, font_size=20).move_to(
                plane_center + LEFT * 0.5 + UP * h / 2 * 2.5)

        def area_lbl():
            return Tex(r"area $=1$", color=YELLOW, font_size=22).move_to(
                plane_center + RIGHT * x_tr.get_value() / 2 * 1.3 + UP * 0.3)

        self.add(always_redraw(rect), always_redraw(width_lbl),
                 always_redraw(height_lbl), always_redraw(area_lbl))

        # Derivation
        derivation = VGroup(
            MathTex(r"\text{area}=x\cdot \frac{1}{x}=1", font_size=22),
            MathTex(r"d(1/x)=\frac{1}{x+dx}-\frac{1}{x}",
                      font_size=22),
            MathTex(r"=\frac{-dx}{x(x+dx)}",
                      font_size=22),
            MathTex(r"\frac{d(1/x)}{dx}=-\frac{1}{x^2}",
                      font_size=28, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.3)
        self.play(Write(derivation))
        self.wait(0.4)

        # Animate x → larger (height shrinks)
        self.play(x_tr.animate.set_value(3.5), run_time=3, rate_func=smooth)
        self.play(x_tr.animate.set_value(1.3), run_time=3, rate_func=smooth)
        self.wait(0.5)
