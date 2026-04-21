from manim import *


class PointWithTraceExample(Scene):
    def construct(self):
        dot = Dot(color=YELLOW).shift(RIGHT * 2)
        trace = VMobject(color=RED)
        trace.set_points_as_corners([dot.get_center(), dot.get_center() + UP * 0.001])

        def update_trace(t: VMobject) -> None:
            prev = t.get_points()
            new_points = list(prev) + [dot.get_center()]
            t.set_points_as_corners(new_points)

        trace.add_updater(update_trace)

        self.add(trace, dot)
        self.play(Rotating(dot, radians=TAU, about_point=ORIGIN, run_time=4, rate_func=linear))
        trace.clear_updaters()
        self.wait(0.4)
