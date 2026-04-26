from manim import *
import numpy as np


class ChangeOfBasisSameVectorExample(Scene):
    """The same geometric vector can be constructed from different bases."""

    def fixed_tip_arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 6,
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
        end_coords: np.ndarray,
        color: ManimColor,
        *,
        start_coords: np.ndarray | None = None,
        stroke_width: float = 6,
        opacity: float = 1.0,
    ) -> Line:
        start_coords = np.array([0.0, 0.0]) if start_coords is None else start_coords
        return self.fixed_tip_arrow(
            plane.c2p(float(start_coords[0]), float(start_coords[1])),
            plane.c2p(float(end_coords[0]), float(end_coords[1])),
            color,
            stroke_width=stroke_width,
            opacity=opacity,
        )

    def card(self, *mobjects: Mobject) -> VGroup:
        group = VGroup(*mobjects).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        group.move_to(RIGHT * 3.05 + UP * 0.35)
        return group

    def construct(self):
        b1 = np.array([1.0, 0.5])
        b2 = np.array([-0.5, 1.5])
        std_coords = np.array([1.5, 2.5])
        b_coords = np.array([2.0, 1.0])

        title = Tex(r"Change the basis, not the vector", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-1.5, 3.5, 1],
            y_range=[-0.5, 3.5, 1],
            x_length=4.8,
            y_length=4.1,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.24, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.1, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.78},
        ).move_to(LEFT * 3.55 + DOWN * 0.25)

        e1 = self.arrow_from_coords(plane, np.array([1.0, 0.0]), RED, stroke_width=5)
        e2 = self.arrow_from_coords(plane, np.array([0.0, 1.0]), GREEN, stroke_width=5)
        e1_label = MathTex(r"\hat{\imath}", color=RED, font_size=25).next_to(e1.get_end(), DOWN, buff=0.06)
        e2_label = MathTex(r"\hat{\jmath}", color=GREEN, font_size=25).next_to(e2.get_end(), LEFT, buff=0.06)

        b1_arrow = self.arrow_from_coords(plane, b1, RED, stroke_width=5, opacity=0.9)
        b2_arrow = self.arrow_from_coords(plane, b2, GREEN, stroke_width=5, opacity=0.9)
        b1_label = MathTex(r"\vec b_1", color=RED, font_size=25).next_to(b1_arrow.get_end(), RIGHT, buff=0.06)
        b2_label = MathTex(r"\vec b_2", color=GREEN, font_size=25).next_to(b2_arrow.get_end(), UP, buff=0.06)

        std_x = self.arrow_from_coords(plane, std_coords, YELLOW, stroke_width=8)
        std_x_label = MathTex(r"\vec x", color=YELLOW, font_size=29).next_to(std_x.get_end(), RIGHT, buff=0.08)
        target_dot = Dot(plane.c2p(*std_coords), radius=0.075, color=YELLOW)

        std_part_1 = self.arrow_from_coords(plane, np.array([1.5, 0.0]), RED_E, stroke_width=5)
        std_part_2 = self.arrow_from_coords(plane, std_coords, GREEN_E, start_coords=np.array([1.5, 0.0]), stroke_width=5)
        std_part_1_label = MathTex(r"1.5\hat{\imath}", color=RED_E, font_size=24).next_to(std_part_1.get_center(), DOWN, buff=0.08)
        std_part_2_label = MathTex(r"2.5\hat{\jmath}", color=GREEN_E, font_size=24).next_to(std_part_2.get_center(), RIGHT, buff=0.08)

        b_part_1 = self.arrow_from_coords(plane, 2 * b1, RED_E, stroke_width=5)
        b_part_2 = self.arrow_from_coords(plane, std_coords, GREEN_E, start_coords=2 * b1, stroke_width=5)
        b_part_1_label = MathTex(r"2\vec b_1", color=RED_E, font_size=24).next_to(b_part_1.get_center(), UP, buff=0.08)
        b_part_2_label = MathTex(r"1\vec b_2", color=GREEN_E, font_size=24).next_to(b_part_2.get_center(), RIGHT, buff=0.08)

        for label in (
            e1_label,
            e2_label,
            b1_label,
            b2_label,
            std_x_label,
            std_part_1_label,
            std_part_2_label,
            b_part_1_label,
            b_part_2_label,
        ):
            label.set_stroke(BLACK, width=5, background=True)

        panel_box = RoundedRectangle(corner_radius=0.12, width=5.75, height=4.75, color=GREY_B, stroke_width=1.4)
        panel_box.set_fill(BLACK, opacity=0.84)
        panel_box.move_to(RIGHT * 3.05 + DOWN * 0.05)

        std_card = self.card(
            MathTex(r"\vec x", r"=", r"1.5\hat{\imath}", r"+", r"2.5\hat{\jmath}", font_size=31),
            MathTex(r"[\vec x]_{\rm std}=\begin{bmatrix}1.5\\2.5\end{bmatrix}", font_size=30),
            Tex("First construct x using the standard basis.", font_size=22, color=BLUE_B),
        )
        std_card[0][2].set_color(RED)
        std_card[0][4].set_color(GREEN)

        basis_card = self.card(
            MathTex(r"\vec b_1=\begin{bmatrix}1\\0.5\end{bmatrix}", r"\qquad", r"\vec b_2=\begin{bmatrix}-0.5\\1.5\end{bmatrix}", font_size=27),
            Tex("Now use a different pair of basis vectors.", font_size=22, color=BLUE_B),
        )
        basis_card[0][0].set_color(RED)
        basis_card[0][2].set_color(GREEN)

        b_card = self.card(
            MathTex(r"\vec x", r"=", r"2\vec b_1", r"+", r"1\vec b_2", font_size=31),
            MathTex(r"[\vec x]_{B}=\begin{bmatrix}2\\1\end{bmatrix}", font_size=30),
            Tex("Different basis, different coordinates; same endpoint.", font_size=22, color=BLUE_B),
        )
        b_card[0][2].set_color(RED)
        b_card[0][4].set_color(GREEN)

        equality_card = self.card(
            MathTex(r"1.5\hat{\imath}+2.5\hat{\jmath}", font_size=27, color=BLUE_B),
            MathTex(r"=", r"2\vec b_1+1\vec b_2", font_size=27, color=YELLOW),
            MathTex(
                r"\begin{bmatrix}1.5\\2.5\end{bmatrix}_{\rm std}",
                r"\quad\leftrightarrow\quad",
                r"\begin{bmatrix}2\\1\end{bmatrix}_{B}",
                font_size=25,
            ),
            Tex("Two coordinate columns, one geometric vector.", font_size=21, color=BLUE_B),
        )

        self.play(Create(plane), FadeIn(panel_box))
        self.play(Create(e1), Create(e2), FadeIn(e1_label), FadeIn(e2_label), FadeIn(std_card))
        self.play(Create(std_part_1), FadeIn(std_part_1_label))
        self.play(Create(std_part_2), FadeIn(std_part_2_label))
        self.play(Create(std_x), FadeIn(std_x_label), FadeIn(target_dot))
        self.play(Circumscribe(std_x, color=YELLOW), run_time=1.0)

        self.play(FadeOut(std_card), FadeIn(basis_card))
        self.play(Create(b1_arrow), Create(b2_arrow), FadeIn(b1_label), FadeIn(b2_label))
        self.play(FadeOut(std_part_1), FadeOut(std_part_2), FadeOut(std_part_1_label), FadeOut(std_part_2_label))

        self.play(FadeOut(basis_card), FadeIn(b_card))
        self.play(Create(b_part_1), FadeIn(b_part_1_label))
        self.play(Create(b_part_2), FadeIn(b_part_2_label))
        self.play(Circumscribe(target_dot, color=YELLOW), Circumscribe(std_x, color=YELLOW), run_time=1.0)

        std_x.set_opacity(0.55)
        self.play(FadeOut(b_card), FadeIn(equality_card))
        self.play(
            b_part_1.animate.set_opacity(0.55),
            b_part_2.animate.set_opacity(0.55),
            Circumscribe(equality_card[0], color=YELLOW),
            run_time=1.2,
        )
        self.wait(0.8)
