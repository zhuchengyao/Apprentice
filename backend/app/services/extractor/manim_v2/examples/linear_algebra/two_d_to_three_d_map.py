from manim import *
import numpy as np


class TwoDToThreeDMapExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1])
        self.add(axes)

        # 3x2 matrix: columns land in R^3
        A = np.array([[1.0, 0.5],
                      [0.5, 1.2],
                      [1.0, 1.0]])

        grid_pts = []
        for ix in range(-3, 4):
            for iy in range(-3, 4):
                grid_pts.append((ix, iy))

        dots = VGroup()
        for ix, iy in grid_pts:
            d = Dot3D(point=np.array([ix, iy, 0.0]) * 0.6, color=BLUE, radius=0.045)
            dots.add(d)
        self.play(FadeIn(dots))

        def target_point(ix, iy):
            v = A @ np.array([ix * 0.6, iy * 0.6])
            return np.array([v[0], v[1], v[2]])

        new_dots = VGroup()
        for (ix, iy), d in zip(grid_pts, dots):
            new_dots.add(Dot3D(point=target_point(ix, iy), color=YELLOW, radius=0.045))
        self.play(Transform(dots, new_dots), run_time=2.5)
        self.wait(0.5)

        label = MathTex(
            r"A = \begin{bmatrix}1&0.5\\0.5&1.2\\1&1\end{bmatrix}:\;\mathbb{R}^2\to\mathbb{R}^3",
            font_size=32,
        )
        self.add_fixed_in_frame_mobjects(label)
        label.to_corner(UL)
        self.play(FadeIn(label))
        self.wait(0.6)
