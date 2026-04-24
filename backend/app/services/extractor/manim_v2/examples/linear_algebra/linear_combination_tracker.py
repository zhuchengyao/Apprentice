from manim import *
import numpy as np


class LinearCombinationTrackerExample(Scene):
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.35})
        self.add(plane)

        v = np.array([2, 0.5, 0])
        w = np.array([0.5, 2, 0])
        a = ValueTracker(1)
        b = ValueTracker(1)

        v_arrow = always_redraw(
            lambda: Arrow(ORIGIN, a.get_value() * v, buff=0, color=GREEN, stroke_width=5)
        )
        w_arrow = always_redraw(
            lambda: Arrow(
                a.get_value() * v,
                a.get_value() * v + b.get_value() * w,
                buff=0, color=RED, stroke_width=5,
            )
        )
        result = always_redraw(
            lambda: Arrow(
                ORIGIN,
                a.get_value() * v + b.get_value() * w,
                buff=0, color=YELLOW, stroke_width=6,
            )
        )
        label = MathTex(r"a\vec{v} + b\vec{w}", font_size=38, color=YELLOW)
        label.to_corner(UL).add_background_rectangle()

        self.add(v_arrow, w_arrow, result, label)
        self.play(a.animate.set_value(-1), b.animate.set_value(0.5), run_time=2)
        self.play(a.animate.set_value(1.5), b.animate.set_value(-1), run_time=2)
        self.wait(0.4)
