from manim import *
import numpy as np


class EigenDirectionsStretchUnitDiskExample(Scene):
    """Eigen-directions stretch or shrink without turning."""

    def construct(self):
        A = np.array([[2.0, 2.0], [1.0, 2.0]])
        eigenvalues, eigenvectors = np.linalg.eig(A)
        order = np.argsort(-eigenvalues)
        eigenvalues = eigenvalues[order]
        eigenvectors = eigenvectors[:, order]
        e1 = eigenvectors[:, 0] / np.linalg.norm(eigenvectors[:, 0])
        e2 = eigenvectors[:, 1] / np.linalg.norm(eigenvectors[:, 1])

        title = Tex(r"Eigen-directions only stretch or shrink", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=6.0,
            y_length=4.5,
            background_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.16, "stroke_width": 0.8},
            faded_line_style={"stroke_color": BLUE_D, "stroke_opacity": 0.06, "stroke_width": 0.5},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        )
        plane.move_to(LEFT * 2.45 + DOWN * 0.25)
        origin = plane.c2p(0, 0)

        unit_radius = np.linalg.norm(plane.c2p(1, 0) - origin)
        disk = Circle(radius=unit_radius, color=YELLOW, stroke_width=1.8)
        disk.set_fill(YELLOW, opacity=0.09)
        disk.move_to(origin)

        eigenlines = VGroup(
            Line(origin - 3.4 * np.append(e1, 0.0), origin + 3.4 * np.append(e1, 0.0), color=TEAL_A),
            Line(origin - 3.0 * np.append(e2, 0.0), origin + 3.0 * np.append(e2, 0.0), color=MAROON_B),
        )
        eigenlines.set_stroke(width=2.0, opacity=0.85)

        eig_arrow_1 = Arrow(origin, origin + 1.35 * np.append(e1, 0.0), buff=0, color=TEAL_A, stroke_width=8)
        eig_arrow_2 = Arrow(origin, origin + 1.35 * np.append(e2, 0.0), buff=0, color=MAROON_B, stroke_width=8)

        panel = VGroup(
            MathTex(r"A\vec{u}_1=\lambda_1\vec{u}_1", font_size=28, color=TEAL_A),
            Tex(fr"stretch by {eigenvalues[0]:.2f}", font_size=22, color=TEAL_A),
            MathTex(r"A\vec{u}_2=\lambda_2\vec{u}_2", font_size=28, color=MAROON_B),
            Tex(fr"shrink by {eigenvalues[1]:.2f}", font_size=22, color=MAROON_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        panel.move_to(RIGHT * 3.25 + UP * 0.85)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)

        moving_group = VGroup(disk, eig_arrow_1, eig_arrow_2)

        self.play(Create(plane))
        self.play(FadeIn(disk), Create(eigenlines), GrowArrow(eig_arrow_1), GrowArrow(eig_arrow_2))
        self.play(FadeIn(panel_box), FadeIn(panel))
        self.play(ApplyMatrix(A, moving_group, about_point=origin), run_time=3.0)
        self.wait(0.8)
