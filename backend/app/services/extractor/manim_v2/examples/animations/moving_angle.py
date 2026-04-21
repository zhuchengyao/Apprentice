from manim import *


class MovingAngleExample(Scene):
    def construct(self):
        rotation_center = LEFT * 1.5
        theta = ValueTracker(20 * DEGREES)

        line1 = Line(rotation_center, rotation_center + RIGHT * 2.5, color=BLUE)
        line_moving = Line(rotation_center, rotation_center + RIGHT * 2.5, color=YELLOW)
        line_moving.rotate(theta.get_value(), about_point=rotation_center)

        angle = always_redraw(
            lambda: Angle(line1, line_moving, radius=0.5, quadrant=(1, 1), color=RED)
        )
        value = always_redraw(
            lambda: DecimalNumber(theta.get_value() / DEGREES, num_decimal_places=0,
                                   unit=r"^{\circ}", font_size=28)
            .next_to(line_moving.get_end(), UR, buff=0.1)
        )

        self.add(line1, line_moving, angle, value)
        line_moving.add_updater(
            lambda m: m.become(
                Line(rotation_center, rotation_center + RIGHT * 2.5, color=YELLOW)
                .rotate(theta.get_value(), about_point=rotation_center)
            )
        )
        self.play(theta.animate.set_value(80 * DEGREES), run_time=3)
        self.wait(0.4)
