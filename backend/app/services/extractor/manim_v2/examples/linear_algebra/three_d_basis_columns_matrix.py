from manim import *
import numpy as np


class ThreeDBasisColumnsMatrixExample(ThreeDScene):
    """A 3D matrix is assembled by recording where the basis vectors land."""

    def make_arrow(self, axes: ThreeDAxes, coords: np.ndarray, color: ManimColor) -> Arrow3D:
        return Arrow3D(
            start=axes.c2p(0, 0, 0),
            end=axes.c2p(*coords),
            color=color,
            thickness=0.04,
            height=0.25,
            base_radius=0.085,
            resolution=12,
        )

    def make_column(self, coords: np.ndarray, color: ManimColor) -> Matrix:
        column = Matrix([[str(int(value))] for value in coords], element_alignment_corner=ORIGIN)
        column.scale(0.58)
        column.set_color(color)
        return column

    def make_plane(self, width: float, height: float, color: ManimColor, rotations=()) -> Rectangle:
        plane = Rectangle(width=width, height=height)
        for angle, axis in rotations:
            plane.rotate(angle, axis=axis)
        plane.set_fill(color, opacity=0.07)
        plane.set_stroke(color, width=1, opacity=0.24)
        return plane

    def construct(self):
        title = Tex(r"A 3D matrix records where the basis vectors land", font_size=28)
        title.to_edge(UP, buff=0.2)

        output_columns = [
            np.array([1, 0, -1]),
            np.array([1, 1, 0]),
            np.array([1, 0, 1]),
        ]
        colors = [RED_C, GREEN_C, BLUE_C]
        basis_tex = [r"\hat{\imath}", r"\hat{\jmath}", r"\hat{k}"]
        basis_coords = [
            np.array([1, 0, 0]),
            np.array([0, 1, 0]),
            np.array([0, 0, 1]),
        ]

        axes = ThreeDAxes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-2.2, 2.2, 1],
            z_range=[-2.2, 2.2, 1],
            x_length=4.6,
            y_length=4.6,
            z_length=4.6,
            axis_config={
                "include_tip": True,
                "include_ticks": True,
                "tick_size": 0.055,
                "stroke_width": 2.4,
                "stroke_opacity": 0.72,
                "color": GREY_B,
            },
            z_axis_config={
                "include_tip": True,
                "include_ticks": True,
                "tick_size": 0.055,
                "stroke_width": 2.4,
                "stroke_opacity": 0.72,
                "color": GREY_B,
            },
        )

        planes = VGroup(
            self.make_plane(4.6, 4.6, YELLOW),
            self.make_plane(4.6, 4.6, BLUE, rotations=[(90 * DEGREES, RIGHT)]),
            self.make_plane(4.6, 4.6, GREEN, rotations=[(90 * DEGREES, UP)]),
        )

        basis_arrows = VGroup(*[
            self.make_arrow(axes, coords, color)
            for coords, color in zip(basis_coords, colors)
        ])
        basis_arrows.set_opacity(0.42)

        output_arrows = VGroup(*[
            self.make_arrow(axes, coords, color)
            for coords, color in zip(output_columns, colors)
        ])
        endpoints = VGroup(*[
            Dot3D(point=axes.c2p(*coords), radius=0.055, color=color)
            for coords, color in zip(output_columns, colors)
        ])

        axis_labels = VGroup(
            MathTex("x", color=GREY_B).move_to(axes.c2p(2.55, 0, 0)),
            MathTex("y", color=GREY_B).move_to(axes.c2p(0, 2.55, 0)),
            MathTex("z", color=GREY_B).move_to(axes.c2p(0, 0, 2.55)),
        )
        basis_labels = VGroup(*[
            MathTex(tex, color=color, font_size=28).move_to(axes.c2p(*(1.25 * coords + 0.08)))
            for tex, coords, color in zip(basis_tex, basis_coords, colors)
        ])
        output_labels = VGroup(*[
            MathTex(rf"L({tex})", color=color, font_size=27).move_to(axes.c2p(*(coords + 0.16)))
            for tex, coords, color in zip(basis_tex, output_columns, colors)
        ])
        VGroup(axis_labels, basis_labels, output_labels).set_opacity(0)

        scene_group = VGroup(
            planes,
            axes,
            basis_arrows,
            output_arrows,
            endpoints,
            axis_labels,
            basis_labels,
            output_labels,
        )
        scene_group.scale(0.86, about_point=ORIGIN)
        stage_origin = LEFT * 2.2
        scene_group.shift(stage_origin)
        axis_label_points = [label.get_center().copy() for label in axis_labels]
        basis_label_points = [label.get_center().copy() for label in basis_labels]
        output_label_points = [label.get_center().copy() for label in output_labels]

        panel_center = RIGHT * 4.05 + DOWN * 0.05
        panel_bg = RoundedRectangle(corner_radius=0.13, width=3.55, height=5.0)
        panel_bg.move_to(panel_center)
        panel_bg.set_fill(BLACK, opacity=0.9)
        panel_bg.set_stroke(GREY_B, width=1.2, opacity=0.55)

        legend = VGroup(*[
            VGroup(
                MathTex(rf"L({basis})", font_size=25, color=color),
                MathTex(r"\to", font_size=28, color=color),
                self.make_column(coords, color),
            ).arrange(RIGHT, buff=0.16)
            for basis, coords, color in zip(basis_tex, output_columns, colors)
        ]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        legend.scale(0.78)
        legend.move_to(panel_center + UP * 0.8)

        columns = VGroup(*[self.make_column(coords, color) for coords, color in zip(output_columns, colors)])
        columns.arrange(RIGHT, buff=0.12)
        columns.scale(0.9)
        bracket_l = MathTex(r"\left[", font_size=78)
        bracket_r = MathTex(r"\right]", font_size=78)
        matrix = VGroup(bracket_l, columns, bracket_r).arrange(RIGHT, buff=0.05)
        matrix.move_to(panel_center + DOWN * 0.8)
        matrix_title = VGroup(
            Tex("Landing points", font_size=20, color=BLUE_B),
            Tex("become matrix columns", font_size=20, color=BLUE_B),
        ).arrange(DOWN, buff=0.04)
        matrix_title.move_to(panel_center + UP * 0.18)

        note = VGroup(
            Tex("Column $j$ records", font_size=19, color=BLUE_B),
            Tex("where basis vector $j$ lands.", font_size=19, color=BLUE_B),
        ).arrange(DOWN, buff=0.04)
        note.move_to(panel_center + DOWN * 1.92)
        note_box = SurroundingRectangle(note, color=GREY_B, buff=0.18)
        note_box.set_fill(BLACK, opacity=0.84)

        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-45 * DEGREES,
            gamma=0,
            zoom=0.95,
        )
        self.add_fixed_in_frame_mobjects(title)
        self.add_fixed_orientation_mobjects(*axis_labels, *basis_labels, *output_labels)

        self.play(Write(title))
        stage_angle = ValueTracker(0)

        def rotate_stage(mobject: Mobject, dt: float) -> None:
            angle_step = 0.13 * dt
            mobject.rotate(angle_step, axis=Z_AXIS, about_point=stage_origin)

        def track_angle(mobject: Mobject, dt: float) -> None:
            stage_angle.increment_value(0.13 * dt)

        def rotated_label_position(point: np.ndarray) -> np.ndarray:
            angle = stage_angle.get_value()
            offset = point - stage_origin
            x = np.cos(angle) * offset[0] - np.sin(angle) * offset[1]
            y = np.sin(angle) * offset[0] + np.cos(angle) * offset[1]
            return stage_origin + np.array([x, y, offset[2]])

        def follow_point(point: np.ndarray):
            return lambda label: label.move_to(rotated_label_position(point))

        rotating_stage_parts = [
            axes,
            *planes,
            *basis_arrows,
            *output_arrows,
            *endpoints,
        ]
        for part in rotating_stage_parts:
            part.add_updater(rotate_stage)
        angle_driver = VMobject()
        angle_driver.add_updater(track_angle)
        self.add(angle_driver)
        for label, point in zip(axis_labels, axis_label_points):
            label.add_updater(follow_point(point))
        for label, point in zip(basis_labels, basis_label_points):
            label.add_updater(follow_point(point))
        for label, point in zip(output_labels, output_label_points):
            label.add_updater(follow_point(point))
        self.play(
            FadeIn(planes),
            Create(axes),
            axis_labels.animate.set_opacity(1),
            run_time=1.4,
        )
        self.play(
            LaggedStart(*[Create(arrow) for arrow in basis_arrows], lag_ratio=0.18),
            basis_labels.animate.set_opacity(1),
            run_time=1.2,
        )
        self.play(
            LaggedStart(*[
                TransformFromCopy(basis_arrow, output_arrow)
                for basis_arrow, output_arrow in zip(basis_arrows, output_arrows)
            ], lag_ratio=0.25),
            FadeIn(endpoints),
            output_labels.animate.set_opacity(1),
            run_time=2.0,
        )

        self.add_fixed_in_frame_mobjects(panel_bg)
        self.play(FadeIn(panel_bg), run_time=0.5, rate_func=linear)
        for arrow, row in zip(output_arrows, legend):
            self.add_fixed_in_frame_mobjects(row)
            self.play(
                Indicate(arrow, color=arrow.get_color(), scale_factor=1.08),
                FadeIn(row, shift=0.18 * RIGHT),
                run_time=1.0,
                rate_func=linear,
            )

        source_columns = [row[-1].copy() for row in legend]
        VGroup(*source_columns).arrange(RIGHT, buff=0.36).move_to(panel_center + UP * 0.58)
        for source_col in source_columns:
            source_col.set_opacity(0.25)

        self.play(
            FadeOut(legend, shift=0.18 * UP),
            run_time=0.75,
            rate_func=linear,
        )
        self.add_fixed_in_frame_mobjects(*source_columns)

        self.add_fixed_in_frame_mobjects(matrix_title, bracket_l, bracket_r)
        self.play(
            FadeIn(matrix_title),
            FadeIn(bracket_l),
            FadeIn(bracket_r),
            run_time=0.8,
            rate_func=linear,
        )
        for source_col, target_col in zip(source_columns, columns):
            self.add_fixed_in_frame_mobjects(target_col)
            self.play(
                TransformFromCopy(source_col, target_col),
                run_time=0.7,
                rate_func=linear,
            )

        self.remove(*source_columns)
        self.add_fixed_in_frame_mobjects(note_box, note)
        self.play(FadeIn(VGroup(note_box, note)), run_time=0.8, rate_func=linear)
        self.wait(1.8)
        for part in rotating_stage_parts:
            part.remove_updater(rotate_stage)
        self.remove(angle_driver)
        for label in VGroup(axis_labels, basis_labels, output_labels):
            label.clear_updaters()
        self.wait(0.4)
