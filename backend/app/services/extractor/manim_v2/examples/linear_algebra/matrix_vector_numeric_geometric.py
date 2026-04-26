from manim import *
import numpy as np


class MatrixVectorNumericGeometricExample(Scene):
    """Matrix-vector multiplication as both arithmetic and a geometric action."""

    def fixed_tip_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 7,
        tip_length: float = 0.2,
        tip_width: float = 0.2,
        opacity: float = 1.0,
    ) -> Line:
        arrow = Line(start, end, color=color, stroke_width=stroke_width)
        length = np.linalg.norm(end - start)
        if length > 0.08:
            arrow.add_tip(
                tip_length=min(tip_length, 0.45 * length),
                tip_width=min(tip_width, 0.45 * length),
            )
        arrow.set_opacity(opacity)
        return arrow

    def arrow_from_coords(
        self,
        plane: NumberPlane,
        coords: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 7,
        opacity: float = 1.0,
    ) -> Line:
        return self.fixed_tip_arrow(
            plane.c2p(0, 0),
            plane.c2p(float(coords[0]), float(coords[1])),
            color,
            stroke_width=stroke_width,
            opacity=opacity,
        )

    def construct(self):
        A = np.array([[0.0, 1.0], [-1.0, 1.0]])
        x = np.array([1.0, 2.0])
        Ax = A @ x

        title = Tex(r"Matrix-vector product: arithmetic and geometry", font_size=29).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5.0,
            y_length=5.0,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.26, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.1, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.82},
        ).move_to(LEFT * 3.25 + DOWN * 0.25)
        origin = plane.c2p(0, 0)

        moved_grid = plane.copy()
        moved_grid.set_color(TEAL_A)
        moved_grid.set_stroke(opacity=0.34)

        vec = self.arrow_from_coords(plane, x, YELLOW, stroke_width=8)
        vec_label = MathTex(r"\vec{x}", font_size=28, color=YELLOW)
        vec_label.set_stroke(BLACK, width=5, background=True)
        vec_label.next_to(vec.get_end(), RIGHT, buff=0.08)

        input_coord_label = MathTex(r"[1,2]_{\rm moving}", font_size=24, color=TEAL_A)
        input_coord_label.set_stroke(BLACK, width=5, background=True)
        input_coord_label.next_to(vec.get_center(), LEFT, buff=0.12)

        static_result_dot = Dot(plane.c2p(*Ax), color=PINK, radius=0.075)
        static_result_label = MathTex(r"[2,1]_{\rm original}", font_size=25, color=PINK)
        static_result_label.set_stroke(BLACK, width=5, background=True)
        static_result_label.next_to(static_result_dot, RIGHT, buff=0.08)

        matrix_product = MathTex(
            r"\begin{bmatrix}0&1\\-1&1\end{bmatrix}",
            r"\begin{bmatrix}1\\2\end{bmatrix}",
            r"=",
            r"\begin{bmatrix}2\\1\end{bmatrix}_{\rm original}",
            font_size=28,
        )
        matrix_product[1].set_color(TEAL_A)
        matrix_product[3].set_color(PINK)
        note_1 = Tex("Keep the original grid: it reads the output as [2, 1].", font_size=22, color=PINK)
        note_2 = Tex("The moved grid reads the same arrow with coordinates [1, 2].", font_size=22, color=TEAL_A)
        panel = VGroup(matrix_product, note_1, note_2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        panel.scale(min(5.25 / panel.width, 2.05 / panel.height, 1.0))
        panel.move_to(RIGHT * 3.05 + UP * 0.82)
        panel_box = RoundedRectangle(corner_radius=0.12, width=5.7, height=2.55, color=GREY_B, stroke_width=1.4)
        panel_box.set_fill(BLACK, opacity=0.84)
        panel_box.move_to(panel)

        self.play(Create(plane), Create(vec), FadeIn(vec_label), FadeIn(input_coord_label))
        self.play(FadeIn(panel_box), FadeIn(panel[0]))
        self.play(FadeIn(static_result_dot), FadeIn(static_result_label), FadeIn(note_1))

        moving_group = VGroup(moved_grid, vec)
        moved_grid.set_z_index(-1)
        plane.set_z_index(-2)
        self.play(FadeIn(moved_grid), run_time=0.5)
        self.play(
            FadeOut(vec_label),
            FadeOut(input_coord_label),
            ApplyMatrix(A, moving_group, about_point=origin),
            run_time=2.4,
        )

        out_label = MathTex(r"A\vec{x}", font_size=28, color=YELLOW)
        out_label.set_stroke(BLACK, width=5, background=True)
        out_label.next_to(vec.get_end(), UP, buff=0.08)
        moved_coord_label = MathTex(r"[1,2]_{\rm moved\ grid}", font_size=24, color=TEAL_A)
        moved_coord_label.set_stroke(BLACK, width=5, background=True)
        moved_coord_label.next_to(vec.get_center(), LEFT, buff=0.12)
        self.play(FadeIn(out_label), FadeIn(moved_coord_label), FadeIn(note_2))
        self.play(Circumscribe(matrix_product[3], color=PINK), Circumscribe(moved_coord_label, color=TEAL_A))
        self.wait(0.8)
