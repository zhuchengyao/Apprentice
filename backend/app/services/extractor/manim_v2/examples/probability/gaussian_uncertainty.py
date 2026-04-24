from manim import *
import numpy as np


class GaussianUncertaintyExample(Scene):
    def construct(self):
        title = Text("Position–momentum uncertainty (Gaussian)", font_size=28).to_edge(UP)
        self.play(Write(title))

        axes_x = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.8, 0.2],
            x_length=5.5, y_length=2.4,
            axis_config={"include_tip": True, "include_numbers": False},
        ).shift(LEFT * 3.2 + 0.4 * DOWN)
        axes_p = Axes(
            x_range=[-4, 4, 1], y_range=[0, 0.8, 0.2],
            x_length=5.5, y_length=2.4,
            axis_config={"include_tip": True, "include_numbers": False},
        ).shift(RIGHT * 3.2 + 0.4 * DOWN)

        lbl_x = MathTex(r"|\psi(x)|^2", font_size=28).next_to(axes_x, UP, buff=0.05)
        lbl_p = MathTex(r"|\hat{\psi}(p)|^2", font_size=28).next_to(axes_p, UP, buff=0.05)
        self.play(Create(axes_x), Create(axes_p), Write(lbl_x), Write(lbl_p))

        sigma = ValueTracker(0.6)

        def gauss_x():
            s = sigma.get_value()
            return axes_x.plot(lambda x: np.exp(-x**2 / (2 * s**2)) / (s * np.sqrt(2 * PI)),
                               x_range=[-3.8, 3.8], color=BLUE)

        def gauss_p():
            s_p = 1 / sigma.get_value()
            return axes_p.plot(lambda p: np.exp(-p**2 / (2 * s_p**2)) / (s_p * np.sqrt(2 * PI)),
                               x_range=[-3.8, 3.8], color=RED)

        gx = always_redraw(gauss_x)
        gp = always_redraw(gauss_p)
        self.play(Create(gx), Create(gp))
        self.wait(0.3)

        inequality = MathTex(r"\sigma_x \cdot \sigma_p \geq \tfrac{\hbar}{2}", font_size=34, color=YELLOW).to_edge(DOWN)
        self.play(Write(inequality))

        self.play(sigma.animate.set_value(1.4), run_time=2)
        self.play(sigma.animate.set_value(0.4), run_time=2)
        self.wait(0.5)
