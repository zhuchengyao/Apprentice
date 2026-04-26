from manim import *
import numpy as np


class CompositionRotationThenShearExample(Scene):
    """Composition of linear maps: first rotate, then shear."""

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
        x = np.array([1.35, 1.35])
        rot = np.array([[0.0, -1.0], [1.0, 0.0]])
        shear = np.array([[1.0, 1.0], [0.0, 1.0]])
        total = shear @ rot

        title = Tex(
            r"Compose transformations by applying them in order",
            font_size=29,
        ).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=6.0,
            y_length=4.5,
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
        plane.move_to(LEFT * 3.45 + DOWN * 0.25)
        origin = plane.c2p(0, 0)

        unit_square = Polygon(
            plane.c2p(0, 0),
            plane.c2p(1.35, 0),
            plane.c2p(1.35, 1.35),
            plane.c2p(0, 1.35),
            color=TEAL,
            fill_color=TEAL,
            fill_opacity=0.16,
            stroke_width=2.5,
        )
        x_vec = self.arrow_from_coords(plane, x, YELLOW, stroke_width=7)
        x_label = MathTex(r"\vec{x}", color=YELLOW, font_size=28)
        x_label.set_stroke(BLACK, width=5, background=True)
        x_label.next_to(x_vec.get_end(), RIGHT, buff=0.08)

        moving_group = VGroup(unit_square, x_vec)

        self.play(Create(plane), FadeIn(unit_square), GrowArrow(x_vec), FadeIn(x_label))

        order_note = Tex("First rotate, then shear", font_size=24, color=BLUE_B)
        rot_eq = MathTex(
            r"R=\begin{bmatrix}0&-1\\1&0\end{bmatrix}",
            font_size=28,
        )
        shear_eq = MathTex(
            r"S=\begin{bmatrix}1&1\\0&1\end{bmatrix}",
            font_size=28,
        )
        total_eq = MathTex(
            r"SR=\begin{bmatrix}1&-1\\1&0\end{bmatrix}",
            font_size=28,
        )
        chain_eq = MathTex(
            r"S(R\vec{x})=(SR)\vec{x}",
            font_size=30,
        )
        chain_eq.set_color_by_tex(r"\vec{x}", YELLOW)

        panel = VGroup(order_note, rot_eq, shear_eq, total_eq, chain_eq).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.22,
        )
        panel.move_to(RIGHT * 3.2 + UP * 0.85)
        panel_box = SurroundingRectangle(panel, color=GREY_B, buff=0.24)
        panel_box.set_fill(BLACK, opacity=0.84)
        self.play(FadeIn(panel_box), FadeIn(order_note), FadeIn(rot_eq), FadeIn(shear_eq))

        rotated_axes = VGroup(
            Line(origin + DOWN * 2.5, origin + UP * 2.5, color=GREY_B, stroke_width=2.0),
            Line(origin + LEFT * 2.5, origin + RIGHT * 2.5, color=GREY_B, stroke_width=2.0),
        ).set_opacity(0.45)
        self.play(ApplyMatrix(rot, moving_group, about_point=origin), FadeIn(rotated_axes), run_time=2.2)
        rx_label = MathTex(r"R\vec{x}", color=YELLOW, font_size=28)
        rx_label.set_stroke(BLACK, width=5, background=True)
        rx_label.next_to(x_vec.get_end(), LEFT, buff=0.08)
        self.play(FadeOut(x_label), FadeIn(rx_label))

        self.play(
            ApplyMatrix(shear, moving_group, about_point=origin),
            ApplyMatrix(shear, rotated_axes, about_point=origin),
            run_time=2.2,
        )
        srx_label = MathTex(r"S(R\vec{x})", color=YELLOW, font_size=28)
        srx_label.set_stroke(BLACK, width=5, background=True)
        srx_label.next_to(x_vec.get_end(), LEFT, buff=0.08)
        self.play(FadeOut(rx_label), FadeIn(srx_label))

        trace_dot = Dot(x_vec.get_end(), radius=0.06, color=YELLOW)
        trace_path = VMobject(color=YELLOW, stroke_width=3)
        trace_path.set_points_smoothly([origin, x_vec.get_end()])

        order_warning = Tex(
            r"Order matters: the second matrix acts on the already-rotated picture.",
            font_size=22,
            color=BLUE_B,
        ).move_to(RIGHT * 3.15 + DOWN * 1.95)
        warning_box = SurroundingRectangle(order_warning, color=GREY_B, buff=0.18)
        warning_box.set_fill(BLACK, opacity=0.8)
        self.play(FadeIn(total_eq), Write(chain_eq))
        self.play(Create(trace_path), FadeIn(trace_dot), FadeIn(warning_box), FadeIn(order_warning))
        self.wait(0.8)
