from manim import *


class OctahedronExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-30 * DEGREES)
        title = Text("Octahedron", font_size=32)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP)

        oct_ = Octahedron(edge_length=2).set_fill(MAROON_D, opacity=0.55).set_stroke(WHITE, width=2)
        self.play(Create(oct_))
        self.play(Rotate(oct_, 2 * PI, axis=UP, run_time=3.5, rate_func=linear))
