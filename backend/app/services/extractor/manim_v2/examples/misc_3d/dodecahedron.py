from manim import *


class DodecahedronExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-30 * DEGREES)
        title = Text("Dodecahedron", font_size=32)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP)

        dodec = Dodecahedron(edge_length=1).set_fill(GREEN, opacity=0.5).set_stroke(WHITE, width=2)
        self.play(Create(dodec))
        self.play(Rotate(dodec, 2 * PI, axis=UP, run_time=4, rate_func=linear))
