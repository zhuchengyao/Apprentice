from manim import *
import numpy as np


class RankIsOutputDimensionExample(Scene):
    """Rank as the dimension of the output space."""

    def disk_for_plane(self, plane: NumberPlane, color: ManimColor) -> Circle:
        radius = np.linalg.norm(plane.c2p(1, 0) - plane.c2p(0, 0))
        disk = Circle(radius=radius, color=color, stroke_width=2.5)
        disk.set_fill(color, opacity=0.2)
        disk.move_to(plane.c2p(0, 0))
        return disk

    def construct(self):
        full_rank = np.array([[1.2, 0.5], [-0.6, 1.1]])
        rank_one = np.array([[1.0, 0.5], [-1.0, -0.5]])

        title = Tex(r"Rank = dimension of the output space", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane_template = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=3.6,
            y_length=3.6,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.24, "stroke_width": 0.9},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.1, "stroke_width": 0.6},
            axis_config={"stroke_width": 1.8, "stroke_opacity": 0.8},
        )

        left_plane = plane_template.copy().move_to(LEFT * 3.25 + DOWN * 0.25)
        right_plane = plane_template.copy().move_to(RIGHT * 0.7 + DOWN * 0.25)
        left_disk = self.disk_for_plane(left_plane, TEAL)
        right_disk = self.disk_for_plane(right_plane, YELLOW_E)

        left_group = VGroup(left_plane, left_disk)
        right_group = VGroup(right_plane, right_disk)

        left_origin = left_plane.c2p(0, 0)
        right_origin = right_plane.c2p(0, 0)

        left_caption = VGroup(
            Tex("Rank 2", font_size=24, color=TEAL_A),
            Tex("outputs still fill area", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.12)
        left_caption.move_to(left_plane.get_bottom() + DOWN * 0.62)

        right_caption = VGroup(
            Tex("Rank 1", font_size=24, color=YELLOW_E),
            Tex("outputs collapse to a line", font_size=21, color=GREY_B),
        ).arrange(DOWN, buff=0.12)
        right_caption.move_to(right_plane.get_bottom() + DOWN * 0.62)

        self.play(Create(left_plane), Create(right_plane))
        self.play(FadeIn(left_disk), FadeIn(right_disk), FadeIn(left_caption), FadeIn(right_caption))
        self.play(
            ApplyMatrix(full_rank, left_group, about_point=left_origin),
            ApplyMatrix(rank_one, right_group, about_point=right_origin),
            run_time=2.8,
        )
        self.wait(0.8)
