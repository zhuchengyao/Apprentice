from manim import *
import numpy as np


class RotationMatrixPowersCycleExample(Scene):
    """Powers of the quarter-turn matrix cycle every four steps."""

    def arrow_from_coords(
        self,
        plane: NumberPlane,
        coords: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 6,
        opacity: float = 1.0,
    ) -> Arrow:
        arrow = Arrow(
            plane.c2p(0, 0),
            plane.c2p(float(coords[0]), float(coords[1])),
            buff=0,
            color=color,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.18,
        )
        arrow.set_opacity(opacity)
        return arrow

    def construct(self):
        R = np.array([[0.0, -1.0], [1.0, 0.0]])
        x = np.array([1.6, 0.8])

        title = Tex(
            r"Powers of a 90-degree rotation cycle every four steps",
            font_size=27,
        ).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5.8,
            y_length=5.8,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.28,
                "stroke_width": 1.0,
            },
            faded_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.12,
                "stroke_width": 0.7,
            },
            axis_config={"stroke_width": 2, "stroke_opacity": 0.8},
        )
        plane.move_to(LEFT * 3.2 + DOWN * 0.25)
        origin = plane.c2p(0, 0)

        x_vec = self.arrow_from_coords(plane, x, YELLOW, stroke_width=7)
        x_label = MathTex(r"\vec{x}", color=YELLOW, font_size=28)
        x_label.set_stroke(BLACK, width=5, background=True)
        x_label.next_to(x_vec.get_end(), RIGHT, buff=0.08)
        self.play(Create(plane), GrowArrow(x_vec), FadeIn(x_label))

        matrix_eq = MathTex(r"R=\begin{bmatrix}0&-1\\1&0\end{bmatrix}", font_size=29)
        cycle_eq = MathTex(r"R^4=I", font_size=30)
        step_eq = MathTex(r"\vec{x}\to R\vec{x}\to R^2\vec{x}\to R^3\vec{x}\to \vec{x}", font_size=25)
        step_eq.set_color_by_tex(r"\vec{x}", YELLOW)
        panel = VGroup(matrix_eq, cycle_eq, step_eq).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        panel.move_to(RIGHT * 3.12 + UP * 0.95)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.22)
        panel_box.set_fill(BLACK, opacity=0.84)
        self.play(FadeIn(panel_box), FadeIn(panel))

        labels = [
            MathTex(r"R\vec{x}", color=TEAL_A, font_size=24),
            MathTex(r"R^2\vec{x}", color=BLUE_B, font_size=24),
            MathTex(r"R^3\vec{x}", color=GREEN_B, font_size=24),
            MathTex(r"R^4\vec{x}=\vec{x}", color=YELLOW, font_size=24),
        ]
        colors = [TEAL_A, BLUE_B, GREEN_B, YELLOW]

        for k, (lab, color) in enumerate(zip(labels, colors), start=1):
            self.play(ApplyMatrix(R, x_vec, about_point=origin), run_time=1.3)
            ghost = x_vec.copy().set_color(color).set_opacity(0.55)
            self.add(ghost)
            lab.set_stroke(BLACK, width=5, background=True)
            lab.next_to(x_vec.get_end(), RIGHT, buff=0.08)
            if k == 1:
                self.play(FadeOut(x_label), FadeIn(lab))
            else:
                self.play(ReplacementTransform(labels[k - 2], lab))
            labels[k - 1] = lab

        self.wait(0.8)
