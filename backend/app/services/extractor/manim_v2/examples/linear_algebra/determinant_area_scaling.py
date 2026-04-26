from manim import *
import numpy as np


class DeterminantAreaScalingExample(Scene):
    """det(A) measures the area scaling of the unit square."""

    def arrow_from_coords(
        self,
        plane: NumberPlane,
        coords: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 6,
    ) -> Arrow:
        return Arrow(
            plane.c2p(0, 0),
            plane.c2p(float(coords[0]), float(coords[1])),
            buff=0,
            color=color,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.18,
        )

    def construct(self):
        matrix = np.array([[3.0, 0.0], [0.0, 2.0]])
        det = int(round(np.linalg.det(matrix)))

        title = Tex(
            r"Determinant = signed area scaling",
            font_size=30,
        ).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-1, 4, 1],
            y_range=[-1, 3, 1],
            x_length=5.7,
            y_length=4.56,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.26,
                "stroke_width": 1.0,
            },
            faded_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.1,
                "stroke_width": 0.7,
            },
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        )
        plane.move_to(LEFT * 3.2 + DOWN * 0.35)
        origin = plane.c2p(0, 0)

        square = Polygon(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            plane.c2p(1, 1),
            plane.c2p(0, 1),
            color=TEAL,
            fill_color=TEAL,
            fill_opacity=0.24,
            stroke_width=3,
        )
        e1 = self.arrow_from_coords(plane, np.array([1.0, 0.0]), RED)
        e2 = self.arrow_from_coords(plane, np.array([0.0, 1.0]), GREEN)
        label_1 = Tex("area = 1", font_size=24, color=TEAL_A).move_to(square.get_center())
        label_1.set_stroke(BLACK, width=5, background=True)

        moving_group = VGroup(square, e1, e2)

        self.play(Create(plane), FadeIn(square), GrowArrow(e1), GrowArrow(e2), FadeIn(label_1))

        matrix_eq = MathTex(
            r"A=\begin{bmatrix}3&0\\0&2\end{bmatrix}",
            font_size=30,
        )
        det_eq = MathTex(
            r"\det(A)=6",
            font_size=30,
        )
        area_eq = MathTex(
            r"\text{new area}=|6|\cdot 1 = 6",
            font_size=28,
        )
        read_note = Tex("Stretch x by 3 and y by 2", font_size=24, color=BLUE_B)
        panel = VGroup(matrix_eq, det_eq, area_eq, read_note).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.24,
        )
        panel.move_to(RIGHT * 3.05 + UP * 0.95)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.24)
        panel_box.set_fill(BLACK, opacity=0.84)
        self.play(FadeIn(panel_box), FadeIn(matrix_eq), FadeIn(read_note))

        self.play(FadeOut(label_1), ApplyMatrix(matrix, moving_group, about_point=origin), run_time=2.6)

        width_edge = Line(square.get_vertices()[0], square.get_vertices()[1])
        height_edge = Line(square.get_vertices()[1], square.get_vertices()[2])
        bottom_brace = Brace(width_edge, DOWN)
        right_brace = Brace(height_edge, RIGHT)
        width_tex = MathTex("3", font_size=26).next_to(bottom_brace, DOWN, buff=0.08)
        height_tex = MathTex("2", font_size=26).next_to(right_brace, RIGHT, buff=0.08)
        area_label = Tex("area = 6", font_size=24, color=YELLOW).move_to(square.get_center())
        area_label.set_stroke(BLACK, width=5, background=True)
        for mob in (bottom_brace, right_brace, width_tex, height_tex):
            mob.set_z_index(3)

        self.play(FadeIn(det_eq))
        self.play(Create(bottom_brace), FadeIn(width_tex), Create(right_brace), FadeIn(height_tex))
        self.play(FadeIn(area_label), Write(area_eq))
        self.wait(0.8)
