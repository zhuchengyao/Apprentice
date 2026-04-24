from manim import *
import numpy as np


class ThreeDLinearTransformExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1])
        self.add(axes)

        M = np.array([[1, 1, 0],
                      [0, 1, 1],
                      [1, 0, 1]], dtype=float)

        def basis_arrow(vec, color):
            return Arrow3D(start=ORIGIN, end=vec, color=color, thickness=0.03, height=0.3, base_radius=0.08)

        i_hat = basis_arrow(RIGHT, GREEN)
        j_hat = basis_arrow(UP, RED)
        k_hat = basis_arrow(OUT, BLUE)
        self.play(Create(i_hat), Create(j_hat), Create(k_hat))

        i_end = M @ np.array([1, 0, 0])
        j_end = M @ np.array([0, 1, 0])
        k_end = M @ np.array([0, 0, 1])

        new_i = basis_arrow(i_end, GREEN)
        new_j = basis_arrow(j_end, RED)
        new_k = basis_arrow(k_end, BLUE)

        self.play(
            Transform(i_hat, new_i),
            Transform(j_hat, new_j),
            Transform(k_hat, new_k),
            run_time=2.5,
        )
        self.wait(0.5)

        label = MathTex(
            r"M = \begin{bmatrix}1&1&0\\0&1&1\\1&0&1\end{bmatrix}",
            font_size=36,
        )
        self.add_fixed_in_frame_mobjects(label)
        label.to_corner(UL)
        self.play(FadeIn(label))
        self.wait(0.6)
