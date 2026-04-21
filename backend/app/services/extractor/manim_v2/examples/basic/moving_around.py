from manim import *


class MovingAroundExample(Scene):
    def construct(self):
        square = Square(side_length=1.4, color=BLUE, fill_opacity=0.6)
        self.play(FadeIn(square))

        self.play(square.animate.shift(LEFT * 2))
        self.play(square.animate.set_fill(GREEN, opacity=0.6))
        self.play(square.animate.scale(1.5))
        self.play(square.animate.rotate(PI / 4))
        self.play(square.animate.shift(RIGHT * 4))
        self.wait(0.4)
