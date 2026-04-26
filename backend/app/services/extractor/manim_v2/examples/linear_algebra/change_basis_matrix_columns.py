from manim import *
import numpy as np


class ChangeBasisMatrixColumnsExample(Scene):
    """A change-of-basis matrix moves basis vectors and preserves coordinate scalars."""

    def fixed_tip_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 6,
        tip_length: float = 0.2,
        tip_width: float = 0.2,
    ) -> Line:
        arrow = Line(start, end, color=color, stroke_width=stroke_width)
        length = np.linalg.norm(end - start)
        if length > 0.08:
            arrow.add_tip(
                tip_length=min(tip_length, 0.45 * length),
                tip_width=min(tip_width, 0.45 * length),
            )
        return arrow

    def panel_card(self, *mobjects: Mobject) -> VGroup:
        card = VGroup(*mobjects).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        card.move_to(RIGHT * 3.05 + UP * 0.1)
        return card

    def construct(self):
        b1 = np.array([1.4, 0.6])
        b2 = np.array([-0.5, 1.2])
        matrix = np.column_stack([b1, b2])
        coords = np.array([2.0, -1.0])
        standard_image = matrix @ coords

        title = Tex(r"A change-of-basis matrix moves the whole coordinate system", font_size=28)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-1.5, 2.5, 1],
            y_range=[-1.7, 1.7, 1],
            x_length=3.2,
            y_length=2.72,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.24, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.1, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.78},
        ).move_to(LEFT * 4.0 + DOWN * 0.25)
        origin = plane.c2p(0, 0)

        e1 = self.fixed_tip_arrow(origin, plane.c2p(1, 0), GREY_B, stroke_width=5, tip_length=0.16)
        e2 = self.fixed_tip_arrow(origin, plane.c2p(0, 1), GREY_B, stroke_width=5, tip_length=0.16)
        e1_label = MathTex(r"\hat{\imath}", font_size=24, color=GREY_B).next_to(e1.get_end(), DOWN, buff=0.06)
        e2_label = MathTex(r"\hat{\jmath}", font_size=24, color=GREY_B).next_to(e2.get_end(), LEFT, buff=0.06)

        two_e1 = self.fixed_tip_arrow(origin, plane.c2p(2, 0), ORANGE, stroke_width=5)
        neg_e2 = self.fixed_tip_arrow(plane.c2p(2, 0), plane.c2p(2, -1), ORANGE, stroke_width=5)
        u_arrow = self.fixed_tip_arrow(origin, plane.c2p(*coords), YELLOW, stroke_width=8, tip_length=0.23, tip_width=0.23)
        u_label = MathTex(r"\vec u", font_size=28, color=YELLOW).next_to(u_arrow.get_end(), RIGHT, buff=0.08)
        scalar_label = MathTex(r"[\,2,-1\,]", font_size=24, color=YELLOW).next_to(u_arrow.get_center(), DOWN, buff=0.12)

        for label in (e1_label, e2_label, u_label, scalar_label):
            label.set_stroke(BLACK, width=5, background=True)

        target_grid = plane.copy()
        target_grid.apply_matrix(matrix, about_point=origin)
        target_grid.set_stroke(opacity=0.2)
        target_grid.set_color(BLUE_B)

        b1_arrow = e1.copy().set_color(RED)
        b1_arrow.apply_matrix(matrix, about_point=origin)
        b2_arrow = e2.copy().set_color(GREEN)
        b2_arrow.apply_matrix(matrix, about_point=origin)
        target_x = u_arrow.copy().set_color(YELLOW)
        target_x.apply_matrix(matrix, about_point=origin)

        b1_label = MathTex(r"\vec b_1=P\hat{\imath}", font_size=24, color=RED)
        b1_label.next_to(b1_arrow.get_end(), RIGHT, buff=0.08).set_stroke(BLACK, width=5, background=True)
        b2_label = MathTex(r"\vec b_2=P\hat{\jmath}", font_size=24, color=GREEN)
        b2_label.next_to(b2_arrow.get_end(), UP, buff=0.08).set_stroke(BLACK, width=5, background=True)
        x_label = MathTex(r"\vec x=P\vec u", font_size=27, color=YELLOW)
        x_label.next_to(target_x.get_end(), RIGHT, buff=0.08).set_stroke(BLACK, width=5, background=True)

        two_b1 = self.fixed_tip_arrow(origin, plane.c2p(*(2 * b1)), RED_E, stroke_width=5)
        minus_b2 = self.fixed_tip_arrow(plane.c2p(*(2 * b1)), plane.c2p(*standard_image), GREEN_E, stroke_width=5)
        two_b1_label = MathTex(r"2\vec b_1", font_size=24, color=RED_E)
        two_b1_label.next_to(two_b1.get_end(), UP, buff=0.06).set_stroke(BLACK, width=5, background=True)
        minus_b2_label = MathTex(r"-\vec b_2", font_size=24, color=GREEN_E)
        minus_b2_label.next_to(minus_b2.get_center(), RIGHT, buff=0.06).set_stroke(BLACK, width=5, background=True)

        matrix_tex = Matrix(
            [[r"1.4", r"-0.5"], [r"0.6", r"1.2"]],
            element_to_mobject=MathTex,
            h_buff=1.45,
            v_buff=0.72,
            bracket_h_buff=0.12,
        )
        p_label = MathTex("P=", font_size=32).next_to(matrix_tex, LEFT, buff=0.12)
        p_matrix = VGroup(p_label, matrix_tex)
        p_matrix.move_to(RIGHT * 3.05 + UP * 1.65)
        entries = matrix_tex.get_entries()
        VGroup(entries[0], entries[2]).set_color(RED)
        VGroup(entries[1], entries[3]).set_color(GREEN)
        first_column_box = SurroundingRectangle(VGroup(entries[0], entries[2]), color=RED, buff=0.08)
        second_column_box = SurroundingRectangle(VGroup(entries[1], entries[3]), color=GREEN, buff=0.08)

        panel_box = RoundedRectangle(corner_radius=0.12, width=5.75, height=4.95, color=GREY_B, stroke_width=1.4)
        panel_box.set_fill(BLACK, opacity=0.84)
        panel_box.move_to(RIGHT * 3.05 + DOWN * 0.08)

        card_scalars = self.panel_card(
            MathTex(r"\vec u=2\hat{\imath}-\hat{\jmath}", font_size=31, color=YELLOW),
            MathTex(r"[\vec u]_{\rm std}=\begin{bmatrix}2\\-1\end{bmatrix}", font_size=31),
            Tex("The coordinates are scalars on the current basis.", font_size=22, color=BLUE_B),
        )
        card_columns = self.panel_card(
            MathTex(r"P\hat{\imath}=\vec b_1", r"\qquad", r"P\hat{\jmath}=\vec b_2", font_size=30),
            MathTex(r"P=[\,\vec b_1\ \vec b_2\,]", font_size=32),
            Tex("The columns say where the basis vectors land.", font_size=22, color=BLUE_B),
        )
        card_columns[0][0].set_color(RED)
        card_columns[0][2].set_color(GREEN)
        card_columns[1].set_color_by_tex(r"\vec b_1", RED)
        card_columns[1].set_color_by_tex(r"\vec b_2", GREEN)

        card_same_scalars = self.panel_card(
            MathTex(r"P\begin{bmatrix}2\\-1\end{bmatrix}", r"=", r"2\vec b_1-\vec b_2", font_size=28),
            Tex("Keep scalars 2 and -1; swap in the moved basis.", font_size=20, color=BLUE_B),
        )
        card_same_scalars[0][2].set_color(YELLOW)
        card_transform = self.panel_card(
            MathTex(r"P[\vec u]_{\rm std}=\vec x_{\rm standard}", font_size=32, color=YELLOW),
            Tex("Apply P to the whole grid: matching objects overlap.", font_size=22, color=BLUE_B),
        )

        self.play(Create(plane), Create(e1), Create(e2), FadeIn(e1_label), FadeIn(e2_label))
        self.play(FadeIn(panel_box), FadeIn(card_scalars))
        self.play(Create(two_e1), Create(neg_e2), Create(u_arrow), FadeIn(u_label), FadeIn(scalar_label))
        self.wait(0.25)

        self.play(FadeOut(card_scalars), FadeIn(p_matrix), FadeIn(card_columns))
        self.play(Create(first_column_box), Create(b1_arrow), FadeIn(b1_label))
        self.play(ReplacementTransform(first_column_box, second_column_box), Create(b2_arrow), FadeIn(b2_label))
        self.play(FadeOut(second_column_box), FadeIn(target_grid), b1_arrow.animate.set_opacity(0.45), b2_arrow.animate.set_opacity(0.45))

        self.play(FadeOut(card_columns), FadeIn(card_same_scalars))
        self.play(Create(two_b1), FadeIn(two_b1_label))
        self.play(Create(minus_b2), FadeIn(minus_b2_label))
        self.play(Create(target_x), FadeIn(x_label))
        self.play(Circumscribe(target_x, color=YELLOW), run_time=1.0)

        moving_group = VGroup(plane, e1, e2, u_arrow, two_e1, neg_e2)
        target_group = VGroup(target_grid, b1_arrow, b2_arrow, target_x)
        self.play(
            FadeOut(card_same_scalars),
            FadeIn(card_transform),
            FadeOut(e1_label),
            FadeOut(e2_label),
            FadeOut(u_label),
            FadeOut(scalar_label),
            FadeOut(two_b1_label),
            FadeOut(minus_b2_label),
            target_group.animate.set_opacity(0.35),
            run_time=0.8,
        )
        self.play(ApplyMatrix(matrix, moving_group, about_point=origin), run_time=2.5)
        self.play(target_group.animate.set_opacity(0.75), Circumscribe(card_transform[0], color=YELLOW))
        self.wait(0.8)
