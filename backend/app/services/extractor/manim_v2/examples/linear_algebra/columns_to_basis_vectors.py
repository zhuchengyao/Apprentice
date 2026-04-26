from manim import *
import numpy as np


class ColumnsToBasisVectorsExample(Scene):
    """Rebuild the core EOLA chapter 3 idea in ManimCE:
    the columns of A are the images of the basis vectors e1 and e2.
    """

    def _arrow(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: ManimColor,
        *,
        stroke_width: float = 6,
        opacity: float = 1.0,
    ) -> Arrow:
        arrow = Arrow(
            start,
            end,
            buff=0,
            color=color,
            stroke_width=stroke_width,
            max_tip_length_to_length_ratio=0.18,
        )
        arrow.set_opacity(opacity)
        return arrow

    def construct(self):
        matrix = np.array([[3.0, 1.0], [1.0, 2.0]])
        x_coords = np.array([-1.0, 2.0])

        title = Tex(
            r"Columns of $A$ tell you where the basis vectors land",
            font_size=30,
        ).to_edge(UP, buff=0.2)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=5.0,
            y_length=5.0,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.38,
                "stroke_width": 1.0,
            },
            faded_line_style={
                "stroke_color": BLUE_E,
                "stroke_opacity": 0.15,
                "stroke_width": 0.7,
            },
            axis_config={"stroke_opacity": 0.8, "stroke_width": 2},
        )
        plane.move_to(LEFT * 3.8 + DOWN * 0.5)
        plane_origin = plane.c2p(0, 0)

        unit_square = Polygon(
            plane.c2p(0, 0),
            plane.c2p(1, 0),
            plane.c2p(1, 1),
            plane.c2p(0, 1),
            color=BLUE_D,
            fill_color=BLUE_D,
            fill_opacity=0.16,
            stroke_width=2.5,
        )
        origin_dot = Dot(plane_origin, radius=0.05, color=WHITE)

        e1 = self._arrow(plane_origin, plane.c2p(1, 0), RED)
        e2 = self._arrow(plane_origin, plane.c2p(0, 1), GREEN)
        x_vec = self._arrow(
            plane_origin,
            plane.c2p(float(x_coords[0]), float(x_coords[1])),
            YELLOW,
            stroke_width=7,
        )

        moving_group = VGroup(plane, unit_square, e1, e2, x_vec)

        e1_label = MathTex(r"\vec{e}_1", color=RED, font_size=28)
        e2_label = MathTex(r"\vec{e}_2", color=GREEN, font_size=28)
        x_label = MathTex(r"\vec{x}", color=YELLOW, font_size=30)
        for label in (e1_label, e2_label, x_label):
            label.set_stroke(BLACK, width=6, background=True)

        e1_label.add_updater(lambda m: m.next_to(e1.get_end(), RIGHT, buff=0.1))
        e2_label.add_updater(lambda m: m.next_to(e2.get_end(), UP, buff=0.1))
        x_label.add_updater(lambda m: m.next_to(x_vec.get_end(), LEFT + DOWN, buff=0.12))

        self.play(Create(plane), FadeIn(unit_square), FadeIn(origin_dot))
        self.play(
            GrowArrow(e1),
            GrowArrow(e2),
            GrowArrow(x_vec),
        )
        self.add(e1_label, e2_label, x_label)

        matrix_mob = Matrix([[3, 1], [1, 2]], h_buff=0.8, v_buff=0.8)
        matrix_mob.scale(0.82)
        entries = matrix_mob.get_entries()
        col1_entries = VGroup(entries[0], entries[2]).set_color(RED)
        col2_entries = VGroup(entries[1], entries[3]).set_color(GREEN)
        matrix_eq = VGroup(
            MathTex("A=", font_size=34),
            matrix_mob,
        ).arrange(RIGHT, buff=0.12)

        read_note = Tex("Read by columns", font_size=25, color=BLUE_B)
        col1_eq = MathTex(
            r"A\vec{e}_1=\begin{bmatrix}3\\1\end{bmatrix}",
            font_size=31,
        )
        col2_eq = MathTex(
            r"A\vec{e}_2=\begin{bmatrix}1\\2\end{bmatrix}",
            font_size=31,
        )
        for line in (col1_eq, col2_eq):
            line.set_color_by_tex(r"\vec{e}_1", RED)
            line.set_color_by_tex(r"\vec{e}_2", GREEN)

        info_block = VGroup(
            read_note,
            matrix_eq,
            col1_eq,
            col2_eq,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        info_block.move_to(RIGHT * 3.35 + UP * 1.05)

        info_box = SurroundingRectangle(
            info_block,
            corner_radius=0.12,
            color=GREY_B,
            buff=0.22,
        )
        info_box.set_fill(BLACK, opacity=0.85)

        col1_box = SurroundingRectangle(col1_entries, color=RED, buff=0.08)
        col2_box = SurroundingRectangle(col2_entries, color=GREEN, buff=0.08)

        self.play(FadeIn(info_box), FadeIn(matrix_eq), FadeIn(read_note))
        self.play(Create(col1_box), Indicate(e1, color=RED), Write(col1_eq))
        self.play(ReplacementTransform(col1_box, col2_box), Indicate(e2, color=GREEN), Write(col2_eq))
        self.play(FadeOut(col2_box))

        transform_note = Tex(
            r"Apply $A$ to the whole plane",
            font_size=24,
            color=YELLOW_B,
        ).move_to(RIGHT * 3.3 + DOWN * 1.35)
        self.play(FadeIn(transform_note))

        self.play(
            ApplyMatrix(matrix, moving_group, about_point=plane_origin),
            run_time=3.0,
        )
        self.play(
            plane.animate.set_stroke(opacity=0.16),
            FadeOut(transform_note, shift=DOWN * 0.08),
            run_time=0.6,
        )

        x_label.clear_updaters()
        ax_label = MathTex(r"A\vec{x}", color=YELLOW, font_size=30)
        ax_label.set_stroke(BLACK, width=6, background=True)
        ax_label.move_to(x_vec.get_end() + RIGHT * 0.55 + DOWN * 0.22)

        ae1_coords = MathTex(r"(3,1)", color=RED, font_size=25)
        ae2_coords = MathTex(r"(1,2)", color=GREEN, font_size=25)
        ae1_coords.set_stroke(BLACK, width=5, background=True)
        ae2_coords.set_stroke(BLACK, width=5, background=True)
        ae1_coords.next_to(e1.get_end(), UR, buff=0.08)
        ae2_coords.next_to(e2.get_end(), RIGHT + UP, buff=0.12)

        x_formula = MathTex(
            r"\vec{x}=\begin{bmatrix}-1\\2\end{bmatrix}=-1\vec{e}_1+2\vec{e}_2",
            font_size=29,
        )
        x_formula.set_color_by_tex(r"\vec{x}", YELLOW)
        x_formula.set_color_by_tex(r"\vec{e}_1", RED)
        x_formula.set_color_by_tex(r"\vec{e}_2", GREEN)

        ax_formula = MathTex(
            r"A\vec{x}=-1A\vec{e}_1+2A\vec{e}_2=\begin{bmatrix}-1\\3\end{bmatrix}",
            font_size=29,
        )
        ax_formula.set_color_by_tex(r"\vec{x}", YELLOW)
        ax_formula.set_color_by_tex(r"\vec{e}_1", RED)
        ax_formula.set_color_by_tex(r"\vec{e}_2", GREEN)

        formula_block = VGroup(x_formula, ax_formula).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.18,
        )
        formula_block.move_to(RIGHT * 3.25 + DOWN * 2.2)
        formula_box = SurroundingRectangle(
            formula_block,
            color=GREY_B,
            buff=0.18,
        )
        formula_box.set_fill(BLACK, opacity=0.82)

        self.play(
            FadeOut(x_label),
            FadeIn(ax_label),
            FadeIn(ae1_coords),
            FadeIn(ae2_coords),
            FadeIn(formula_box),
        )
        self.play(Write(x_formula))
        self.play(Write(ax_formula))

        p1 = e1.get_end()
        p2 = e2.get_end()
        neg_ae1 = self._arrow(
            plane_origin,
            plane_origin - (p1 - plane_origin),
            RED_E,
            stroke_width=5,
            opacity=0.55,
        )
        two_ae2 = self._arrow(
            plane_origin,
            plane_origin + 2 * (p2 - plane_origin),
            GREEN_E,
            stroke_width=5,
            opacity=0.55,
        )
        two_ae2_shifted = two_ae2.copy().shift(neg_ae1.get_end() - plane_origin)

        coeff1 = MathTex("-1", color=RED_E, font_size=24)
        coeff2 = MathTex("2", color=GREEN_E, font_size=24)
        coeff1.set_stroke(BLACK, width=5, background=True)
        coeff2.set_stroke(BLACK, width=5, background=True)
        coeff1.move_to((plane_origin + neg_ae1.get_end()) / 2 + DOWN * 0.28)
        coeff2.move_to((two_ae2.get_start() + two_ae2.get_end()) / 2 + RIGHT * 0.18)

        self.play(FadeIn(neg_ae1), FadeIn(coeff1))
        self.play(FadeIn(two_ae2), FadeIn(coeff2))
        self.play(
            two_ae2.animate.shift(neg_ae1.get_end() - plane_origin),
            coeff2.animate.shift(neg_ae1.get_end() - plane_origin),
        )
        self.play(Indicate(x_vec, color=YELLOW), Flash(x_vec.get_end(), color=YELLOW))
        self.wait(1.0)
