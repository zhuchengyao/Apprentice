from manim import *
import numpy as np


class ViralSpreadCurvesExample(Scene):
    def construct(self):
        title = Text("Exponential growth vs logistic saturation", font_size=26).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 25, 5], y_range=[0, 1.1, 0.2],
            x_length=9, y_length=4.2,
            axis_config={"include_tip": True},
        ).shift(0.2 * DOWN)
        xlbl = Text("time (days)", font_size=22).next_to(axes, DOWN, buff=0.1)
        ylbl = Text("fraction infected", font_size=22).next_to(axes, LEFT, buff=0.1).rotate(PI / 2)
        self.play(Create(axes), Write(xlbl), Write(ylbl))

        r = 0.35
        I0 = 0.002
        exp_curve = axes.plot(lambda t: min(1.0, I0 * np.exp(r * t)),
                              x_range=[0, 24.5], color=RED)
        logistic = axes.plot(lambda t: 1 / (1 + (1 - I0) / I0 * np.exp(-r * t)),
                             x_range=[0, 24.5], color=GREEN)

        lbl_exp = MathTex(r"I(t) = I_0 e^{r t}", font_size=28, color=RED)
        lbl_log = MathTex(r"I(t) = \frac{1}{1 + A e^{-r t}}", font_size=28, color=GREEN)
        legend = VGroup(lbl_exp, lbl_log).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL).shift(DOWN * 0.6)

        self.play(Create(exp_curve), Write(lbl_exp))
        self.wait(0.2)
        self.play(Create(logistic), Write(lbl_log))

        caption = Text("Real epidemics eventually saturate; early exponential fit overestimates the peak.",
                       font_size=20, color=YELLOW).to_edge(DOWN)
        self.play(Write(caption))
        self.wait(0.6)
