from manim import *


class FixedInFrameTextExample(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        sphere = Sphere(radius=1, color=BLUE).set_opacity(0.7)

        self.set_camera_orientation(phi=65 * DEGREES, theta=30 * DEGREES)
        self.play(Create(axes), FadeIn(sphere))

        # `add_fixed_in_frame_mobjects` pins the mobject to camera space so
        # it doesn't rotate with the 3D scene.
        title = Text("Unit sphere", font_size=32).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
