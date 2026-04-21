from manim import *


class ArgMinExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 10, 2],
            x_length=7,
            y_length=4,
            tips=False,
        ).to_edge(DOWN, buff=0.5)
        self.play(Create(axes))

        func = lambda x: (x - 1.5) ** 2 + 1
        graph = axes.plot(func, color=BLUE)
        self.play(Create(graph))

        x_tracker = ValueTracker(-2.5)
        dot = always_redraw(
            lambda: Dot(color=YELLOW).move_to(
                axes.c2p(x_tracker.get_value(), func(x_tracker.get_value()))
            )
        )
        value = always_redraw(
            lambda: MathTex(f"x = {x_tracker.get_value():.2f}", font_size=32)
            .to_edge(UP).shift(LEFT * 2)
        )
        fvalue = always_redraw(
            lambda: MathTex(f"f(x) = {func(x_tracker.get_value()):.2f}", font_size=32)
            .to_edge(UP).shift(RIGHT * 2)
        )
        self.add(dot, value, fvalue)

        self.play(x_tracker.animate.set_value(1.5), run_time=3)
        self.wait(0.4)
