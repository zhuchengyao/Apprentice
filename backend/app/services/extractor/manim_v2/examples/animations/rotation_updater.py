from manim import *


class RotationUpdaterExample(Scene):
    def construct(self):
        square = Square(side_length=1.3, color=BLUE, fill_opacity=0.6)
        label = Text("spinning", font_size=24).next_to(square, DOWN, buff=0.3)

        def spin(mob, dt):
            mob.rotate(dt * PI)

        self.add(square, label)
        square.add_updater(spin)
        self.wait(3)
        square.remove_updater(spin)
        self.play(label.animate.set_opacity(0.3))
        self.wait(0.4)
