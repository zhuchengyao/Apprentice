from manim import *


class PointMovingOnShapesExample(Scene):
    def construct(self):
        circle = Circle(radius=1.2, color=BLUE)
        dot = Dot(color=YELLOW).move_to(circle.point_from_proportion(0))
        self.play(Create(circle), FadeIn(dot))
        self.play(MoveAlongPath(dot, circle), run_time=2.5, rate_func=linear)

        square = Square(side_length=2, color=GREEN)
        self.play(ReplacementTransform(circle, square))
        self.play(Rotating(square, radians=PI, about_point=ORIGIN, run_time=2))
        self.wait(0.4)
