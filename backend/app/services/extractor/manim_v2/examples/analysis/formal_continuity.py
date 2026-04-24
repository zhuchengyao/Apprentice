from manim import *


class FormalContinuityExample(Scene):
    def construct(self):
        title = Text("Formal definition of continuity", font_size=28).to_edge(UP)
        self.play(Write(title))

        axes = Axes(
            x_range=[-1, 3.2, 1], y_range=[-1, 3, 1],
            x_length=6.5, y_length=4.2,
            axis_config={"include_tip": True},
        ).shift(0.4 * DOWN)

        graph = axes.plot(lambda x: 0.5 * x**2 + 0.3, x_range=[-0.8, 2.7], color=BLUE)
        self.play(Create(axes), Create(graph))

        x0 = 1.4
        y0 = 0.5 * x0**2 + 0.3
        p0 = Dot(axes.c2p(x0, y0), color=YELLOW)
        lbl = MathTex("f(x_0)", font_size=28, color=YELLOW).next_to(p0, UR, buff=0.1)
        self.play(FadeIn(p0), Write(lbl))

        eps = ValueTracker(0.8)
        delta = ValueTracker(0.9)

        eps_band = always_redraw(lambda: Rectangle(
            width=axes.x_length, height=abs(axes.c2p(0, y0 + eps.get_value())[1] - axes.c2p(0, y0 - eps.get_value())[1]),
            color=GREEN, fill_opacity=0.2, stroke_width=0,
        ).move_to(axes.c2p(axes.x_range[1] / 2 + axes.x_range[0] / 2, y0)))

        delta_band = always_redraw(lambda: Rectangle(
            width=abs(axes.c2p(x0 + delta.get_value(), 0)[0] - axes.c2p(x0 - delta.get_value(), 0)[0]),
            height=axes.y_length, color=ORANGE, fill_opacity=0.2, stroke_width=0,
        ).move_to(axes.c2p(x0, axes.y_range[1] / 2 + axes.y_range[0] / 2)))

        eps_tag = MathTex(r"\varepsilon", color=GREEN).to_corner(UL).shift(0.8 * DOWN + 0.5 * RIGHT)
        delta_tag = MathTex(r"\delta", color=ORANGE).next_to(eps_tag, RIGHT, buff=0.8)

        self.play(FadeIn(eps_band), Write(eps_tag))
        self.play(FadeIn(delta_band), Write(delta_tag))
        self.play(eps.animate.set_value(0.3), delta.animate.set_value(0.4), run_time=2)

        rule = MathTex(
            r"\forall\varepsilon > 0\;\exists\delta > 0:\;|x - x_0| < \delta \Rightarrow |f(x) - f(x_0)| < \varepsilon",
            font_size=28,
        ).to_edge(DOWN)
        self.play(Write(rule))
        self.wait(0.6)
