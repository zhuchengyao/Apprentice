from manim import *


class ThreeDCameraRotationExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        cube = Cube(side_length=1.2, fill_opacity=0.6, fill_color=BLUE)
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        self.play(Create(axes), FadeIn(cube))
        self.begin_ambient_camera_rotation(rate=0.4)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
