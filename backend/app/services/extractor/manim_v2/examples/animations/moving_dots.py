from manim import *


class MovingDotsExample(Scene):
    def construct(self):
        d1 = Dot(color=BLUE).shift(LEFT * 2)
        d2 = Dot(color=RED).shift(RIGHT * 2)
        line = always_redraw(lambda: Line(d1.get_center(), d2.get_center(), color=YELLOW))
        label = always_redraw(
            lambda: DecimalNumber(
                (d1.get_center()[0] - d2.get_center()[0]) ** 2
                + (d1.get_center()[1] - d2.get_center()[1]) ** 2,
                num_decimal_places=2, font_size=28,
            ).next_to(line.get_center(), UP, buff=0.15)
        )

        self.add(d1, d2, line, label)
        self.play(d1.animate.shift(UP * 2 + RIGHT), d2.animate.shift(DOWN + LEFT), run_time=2.5)
        self.play(d1.animate.shift(DOWN * 2), d2.animate.shift(UP * 2), run_time=2.5)
        self.wait(0.4)
