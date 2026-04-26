from manim import *
import numpy as np


class ColumnSpaceNullSpaceExample(Scene):
    """Rank-deficient maps collapse null-space offsets to the same output."""

    def _plane(self, center: np.ndarray, x_range: list[float], y_range: list[float]) -> NumberPlane:
        return NumberPlane(
            x_range=x_range,
            y_range=y_range,
            x_length=4.45,
            y_length=3.95,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.22, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.09, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.75},
        ).move_to(center)

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

    def panel_card(self, *mobjects: Mobject) -> VGroup:
        card = VGroup(*mobjects).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        max_width = 8.05
        max_height = 1.22
        scale_factor = min(max_width / card.width, max_height / card.height, 1.0)
        card.scale(scale_factor)
        card.move_to(DOWN * 2.82)
        return card

    def construct(self):
        matrix = np.array([[1.0, 2.0], [0.5, 1.0]])
        n_vec = np.array([2.0, -1.0])
        x0 = np.array([0.8, 0.4])

        def output_of(v: np.ndarray) -> np.ndarray:
            return matrix @ v

        title = Tex(r"Null-space offsets do not change the output", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        input_plane = self._plane(LEFT * 3.05 + DOWN * 0.25, [-1.4, 3.4, 1], [-2, 2, 1])
        output_plane = self._plane(RIGHT * 3.05 + DOWN * 0.25, [-0.8, 4.2, 1], [-0.8, 2.4, 1])
        input_origin = input_plane.c2p(0, 0)
        output_origin = output_plane.c2p(0, 0)

        input_label = Tex("input space", font_size=22, color=BLUE_B).next_to(input_plane, UP, buff=0.12)
        output_label = Tex("output space", font_size=22, color=BLUE_B).next_to(output_plane, UP, buff=0.12)

        null_line = Line(input_plane.c2p(-1.2, 0.6), input_plane.c2p(3.2, -1.6), color=PURPLE_B, stroke_width=4)
        null_line_label = Tex("null-space direction", font_size=19, color=PURPLE_B)
        null_line_label.next_to(null_line, UP, buff=0.08).shift(LEFT * 0.2)
        column_line = Line(output_plane.c2p(-0.6, -0.3), output_plane.c2p(4.0, 2.0), color=TEAL_A, stroke_width=4)
        column_line_label = Tex("column space", font_size=20, color=TEAL_A).next_to(column_line, UP, buff=0.08)

        n_arrow = self.arrow_from_coords(input_plane, n_vec, PURPLE_B, stroke_width=7)
        n_label = MathTex(r"\vec n", font_size=28, color=PURPLE_B)
        n_label.next_to(n_arrow.get_end(), DOWN, buff=0.08).set_stroke(BLACK, width=5, background=True)
        zero_dot = Dot(output_origin, color=PURPLE_B, radius=0.08)
        zero_label = MathTex(r"\vec 0", font_size=26, color=PURPLE_B)
        zero_label.next_to(zero_dot, DOWN, buff=0.08).set_stroke(BLACK, width=5, background=True)

        x_arrow = self.arrow_from_coords(input_plane, x0, YELLOW, stroke_width=7)
        x_label = MathTex(r"\vec x", font_size=28, color=YELLOW)
        x_label.next_to(x_arrow.get_end(), UP, buff=0.08).set_stroke(BLACK, width=5, background=True)
        shifted_n_arrow = self.arrow_from_coords(input_plane, x0 + n_vec, PURPLE_B, start_coords=x0, stroke_width=5)
        shifted_n_label = MathTex(r"\vec n", font_size=25, color=PURPLE_B)
        shifted_n_label.next_to(shifted_n_arrow.get_center(), DOWN, buff=0.08).set_stroke(BLACK, width=5, background=True)
        x_plus_n_arrow = self.arrow_from_coords(input_plane, x0 + n_vec, ORANGE, stroke_width=7)
        x_plus_n_label = MathTex(r"\vec x+\vec n", font_size=27, color=ORANGE)
        x_plus_n_label.next_to(x_plus_n_arrow.get_end(), RIGHT, buff=0.08).set_stroke(BLACK, width=5, background=True)

        ax = output_of(x0)
        ax_arrow = self.arrow_from_coords(output_plane, ax, YELLOW, stroke_width=7)
        ax_label = MathTex(r"A\vec x", font_size=27, color=YELLOW)
        ax_label.next_to(ax_arrow.get_end(), UP, buff=0.08).set_stroke(BLACK, width=5, background=True)
        axn_arrow = self.arrow_from_coords(output_plane, ax, ORANGE, stroke_width=4, opacity=0.75)
        axn_label = MathTex(r"A(\vec x+\vec n)", font_size=25, color=ORANGE)
        axn_label.next_to(axn_arrow.get_end(), DOWN, buff=0.08).set_stroke(BLACK, width=5, background=True)
        output_dot = Dot(output_plane.c2p(*ax), color=WHITE, radius=0.08)

        matrix_tex = MathTex(r"A=\begin{bmatrix}1&2\\0.5&1\end{bmatrix}", font_size=27)
        card_null = self.panel_card(
            matrix_tex,
            MathTex(r"\vec n=\begin{bmatrix}2\\-1\end{bmatrix}", r"\quad\Rightarrow\quad", r"A\vec n=\vec 0", font_size=27),
            Tex("A null-space direction disappears under A.", font_size=21, color=BLUE_B),
        )
        card_null[1][2].set_color(PURPLE_B)

        card_sum = self.panel_card(
            MathTex(r"\vec x+\vec n", r"\text{ is a different input}", font_size=28),
            MathTex(r"\vec x", r"\quad+\quad", r"\vec n", font_size=28),
            Tex("Move along the null-space direction from x.", font_size=21, color=BLUE_B),
        )
        card_sum[0][0].set_color(ORANGE)
        card_sum[1][0].set_color(YELLOW)
        card_sum[1][2].set_color(PURPLE_B)

        card_same_output = self.panel_card(
            MathTex(r"A(\vec x+\vec n)", r"=", r"A\vec x+A\vec n", font_size=28),
            MathTex(r"=", r"A\vec x+\vec 0", r"=", r"A\vec x", font_size=28, color=YELLOW),
            Tex("The two different inputs land on the same output.", font_size=21, color=BLUE_B),
        )

        card_dynamic = self.panel_card(
            MathTex(r"\vec x\ \text{changes}", r"\quad\Longrightarrow\quad", r"A\vec x\ \text{changes}", font_size=28),
            Tex("But adding n still stays invisible to A.", font_size=21, color=BLUE_B),
            Tex("All outputs remain on the column space line.", font_size=21, color=TEAL_A),
        )
        card_dynamic[0][0].set_color(YELLOW)
        card_dynamic[0][2].set_color(YELLOW)

        panel_box = RoundedRectangle(corner_radius=0.08, width=8.85, height=1.68, color=GREY_B, stroke_width=1.4)
        panel_box.set_fill(BLACK, opacity=0.86)
        panel_box.move_to(DOWN * 2.82)

        self.play(Create(input_plane), Create(output_plane), FadeIn(input_label), FadeIn(output_label))
        self.play(Create(null_line), FadeIn(null_line_label), FadeIn(panel_box), FadeIn(card_null))
        self.play(Create(n_arrow), FadeIn(n_label))
        moving_n = n_arrow.copy()
        self.add(moving_n)
        self.play(Transform(moving_n, Dot(output_origin, color=PURPLE_B, radius=0.08)), FadeIn(zero_dot), FadeIn(zero_label), run_time=1.5)
        self.play(Circumscribe(zero_dot, color=PURPLE_B), run_time=0.9)

        self.play(FadeOut(card_null, shift=DOWN * 0.08), run_time=0.35)
        self.play(FadeIn(card_sum, shift=DOWN * 0.08), run_time=0.45)
        self.play(Create(x_arrow), FadeIn(x_label))
        self.play(Create(shifted_n_arrow), FadeIn(shifted_n_label))
        self.play(Create(x_plus_n_arrow), FadeIn(x_plus_n_label))
        self.play(Circumscribe(x_plus_n_arrow, color=ORANGE), run_time=0.9)

        self.play(FadeOut(card_sum, shift=DOWN * 0.08), run_time=0.35)
        self.play(FadeIn(card_same_output, shift=DOWN * 0.08), Create(column_line), FadeIn(column_line_label), run_time=0.65)
        moving_x = x_arrow.copy()
        moving_xn = x_plus_n_arrow.copy()
        self.add(moving_x, moving_xn)
        self.play(
            Transform(moving_x, ax_arrow),
            Transform(moving_xn, axn_arrow),
            FadeIn(output_dot),
            run_time=1.8,
        )
        self.play(FadeIn(ax_label), FadeIn(axn_label), Circumscribe(output_dot, color=WHITE), run_time=1.0)

        t = ValueTracker(0.0)

        def live_x() -> np.ndarray:
            s = t.get_value()
            return np.array([0.7 + 0.65 * np.cos(s), 0.75 + 0.35 * np.sin(1.1 * s)])

        live_input_arrow = always_redraw(lambda: self.arrow_from_coords(input_plane, live_x(), YELLOW, stroke_width=7))
        live_input_label = always_redraw(
            lambda: MathTex(r"\vec x", font_size=27, color=YELLOW)
            .next_to(live_input_arrow.get_end(), UP, buff=0.08)
            .set_stroke(BLACK, width=5, background=True)
        )
        live_output_arrow = always_redraw(lambda: self.arrow_from_coords(output_plane, output_of(live_x()), YELLOW, stroke_width=7))
        live_output_label = always_redraw(
            lambda: MathTex(r"A\vec x", font_size=26, color=YELLOW)
            .next_to(live_output_arrow.get_end(), UP, buff=0.08)
            .set_stroke(BLACK, width=5, background=True)
        )
        live_output_dot = always_redraw(lambda: Dot(output_plane.c2p(*output_of(live_x())), color=WHITE, radius=0.07))
        live_coset = always_redraw(
            lambda: Line(
                input_plane.c2p(*(live_x() - 1.2 * n_vec)),
                input_plane.c2p(*(live_x() + 1.2 * n_vec)),
                color=YELLOW_E,
                stroke_width=3,
                stroke_opacity=0.45,
            )
        )

        self.play(
            FadeOut(card_same_output, shift=DOWN * 0.08),
            FadeOut(x_arrow),
            FadeOut(x_label),
            FadeOut(x_plus_n_arrow),
            FadeOut(x_plus_n_label),
            FadeOut(shifted_n_arrow),
            FadeOut(shifted_n_label),
            FadeOut(moving_x),
            FadeOut(moving_xn),
            FadeOut(ax_label),
            FadeOut(axn_label),
            FadeOut(output_dot),
            FadeOut(null_line_label),
        )
        self.play(FadeIn(card_dynamic, shift=DOWN * 0.08), run_time=0.45)
        self.add(live_coset, live_input_arrow, live_input_label, live_output_arrow, live_output_label, live_output_dot)
        self.play(t.animate.set_value(2.3), run_time=2.2)
        self.play(t.animate.set_value(4.6), run_time=2.2)
        self.wait(0.8)
