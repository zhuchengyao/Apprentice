from manim import *
import numpy as np


class OriginFixedLinearTransformExample(Scene):
    """A linear transformation can move the grid, but not the origin."""

    def _plane(self, center: np.ndarray) -> NumberPlane:
        return NumberPlane(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            x_length=4.3,
            y_length=4.3,
            background_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.25, "stroke_width": 1.0},
            faded_line_style={"stroke_color": BLUE_E, "stroke_opacity": 0.1, "stroke_width": 0.7},
            axis_config={"stroke_width": 2, "stroke_opacity": 0.75},
        ).move_to(center)

    def construct(self):
        title = Tex(r"Linear transformations keep the origin fixed", font_size=30).to_edge(UP, buff=0.2)
        self.play(Write(title))

        linear_plane = self._plane(LEFT * 3.05 + DOWN * 0.1)
        shifted_plane = self._plane(RIGHT * 3.05 + DOWN * 0.1)
        linear_origin = linear_plane.c2p(0, 0)
        shifted_origin = shifted_plane.c2p(0, 0)

        origin_dot_linear = Dot(linear_origin, color=YELLOW, radius=0.08)
        origin_dot_shifted = Dot(shifted_origin, color=YELLOW, radius=0.08)
        old_origin_dot = Dot(shifted_origin, color=GREY_B, radius=0.05)
        linear_group = VGroup(linear_plane, origin_dot_linear)
        shifted_group = VGroup(shifted_plane, origin_dot_shifted)

        linear_label = Tex("linear shear", font_size=23, color=BLUE_B).next_to(linear_plane, UP, buff=0.16)
        shifted_label = Tex("translation", font_size=23, color=BLUE_B).next_to(shifted_plane, UP, buff=0.16)
        origin_label_left = MathTex(r"\vec{0}\mapsto\vec{0}", font_size=29, color=YELLOW)
        origin_label_right = MathTex(r"\vec{0}\mapsto\vec{b}\neq\vec{0}", font_size=29, color=ORANGE)
        origin_label_left.next_to(linear_plane, DOWN, buff=0.16)
        origin_label_right.next_to(shifted_plane, DOWN, buff=0.16)

        shear = np.array([[1.0, 0.75], [0.0, 1.0]])
        offset = RIGHT * 0.9 + UP * 0.55
        displacement_arrow = Arrow(
            shifted_origin,
            shifted_origin + offset,
            buff=0.08,
            color=ORANGE,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.22,
        )

        self.play(
            Create(linear_plane),
            Create(shifted_plane),
            FadeIn(origin_dot_linear),
            FadeIn(origin_dot_shifted),
            FadeIn(old_origin_dot),
        )
        self.play(FadeIn(linear_label), FadeIn(shifted_label))
        self.play(
            ApplyMatrix(shear, linear_group, about_point=linear_origin),
            ApplyPointwiseFunction(lambda p: p + offset, shifted_group),
            run_time=2.0,
        )
        self.play(
            GrowArrow(displacement_arrow),
            Write(origin_label_left),
            Write(origin_label_right),
            Circumscribe(origin_dot_linear, color=YELLOW),
        )
        self.wait(0.8)
