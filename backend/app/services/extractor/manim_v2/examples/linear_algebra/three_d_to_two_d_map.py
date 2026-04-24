from manim import *
import numpy as np


class ThreeDToTwoDMapExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1])
        self.add(axes)

        # 2x3 matrix: columns in R^2, viewed as vectors in the xy-plane
        A = np.array([[1.0, 0.5, -0.4],
                      [0.2, 1.0, 0.8]])

        source_pts = []
        for ix in [-2, -1, 0, 1, 2]:
            for iy in [-2, -1, 0, 1, 2]:
                for iz in [-2, -1, 0, 1, 2]:
                    source_pts.append(np.array([ix, iy, iz]) * 0.5)

        src = VGroup(*[Dot3D(point=p, color=BLUE, radius=0.03) for p in source_pts])
        self.play(FadeIn(src))

        def target(p):
            v = A @ p
            return np.array([v[0], v[1], 0.0])

        tgt = VGroup(*[Dot3D(point=target(p), color=YELLOW, radius=0.03) for p in source_pts])
        self.play(Transform(src, tgt), run_time=2.5)
        self.wait(0.4)

        label = MathTex(
            r"A:\;\mathbb{R}^3\to\mathbb{R}^2\quad (\text{image: plane})",
            font_size=32,
        )
        self.add_fixed_in_frame_mobjects(label)
        label.to_corner(UL)
        self.play(FadeIn(label))
        self.wait(0.6)
