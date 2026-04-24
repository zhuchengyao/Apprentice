from manim import *
import numpy as np


class CubeSymmetriesExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        cube = Cube(side_length=1.6, fill_opacity=0.6, stroke_width=1).set_color(BLUE)
        self.play(FadeIn(cube))
        self.wait(0.3)

        # Three orthogonal 90-degree rotations (axes through face centers)
        self.play(Rotate(cube, angle=PI / 2, axis=RIGHT), run_time=1.2)
        self.wait(0.2)
        self.play(Rotate(cube, angle=PI / 2, axis=UP), run_time=1.2)
        self.wait(0.2)
        self.play(Rotate(cube, angle=PI / 2, axis=OUT), run_time=1.2)
        self.wait(0.2)

        # Diagonal axis (vertex-to-vertex), 120-degree rotation
        axis = np.array([1, 1, 1]) / np.sqrt(3)
        self.play(Rotate(cube, angle=2 * PI / 3, axis=axis), run_time=1.5)
        self.wait(0.2)

        counts = VGroup(
            Text("Cube rotation group: 24 orientations", font_size=24),
            MathTex(r"6 \times 4 = 24\;\;\text{(6 faces on top} \times \text{4 rotations of the top face)}",
                    font_size=22, color=YELLOW),
        ).arrange(DOWN, buff=0.15)
        self.add_fixed_in_frame_mobjects(counts)
        counts.to_edge(DOWN)
        self.play(Write(counts))
        self.wait(0.6)
