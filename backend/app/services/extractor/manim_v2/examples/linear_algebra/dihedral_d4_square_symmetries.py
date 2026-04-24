from manim import *
import numpy as np


class DihedralD4SquareSymmetries(Scene):
    """Visit all 8 elements of the dihedral group D_4 acting on a square with
    labeled corners A, B, C, D.  Four rotations (0, 90°, 180°, 270°) and four
    reflections (about horizontal, vertical, two diagonals)."""

    def construct(self):
        title = Tex(
            r"Dihedral group $D_4$: 8 symmetries of a square",
            font_size=30,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def make_labeled_square():
            square = Square(side_length=2.0, color=BLUE,
                            fill_opacity=0.2, stroke_width=3)
            labels = VGroup(
                Tex("A", font_size=30, color=YELLOW),
                Tex("B", font_size=30, color=GREEN),
                Tex("C", font_size=30, color=ORANGE),
                Tex("D", font_size=30, color=PURPLE),
            )
            corners = [UL, UR, DR, DL]
            for lab, corner in zip(labels, corners):
                lab.move_to(square.get_corner(corner) + 0.25 * corner)
            return VGroup(square, labels)

        positions = [
            (-4.5, 1.6), (-1.5, 1.6), (1.5, 1.6), (4.5, 1.6),
            (-4.5, -1.8), (-1.5, -1.8), (1.5, -1.8), (4.5, -1.8),
        ]
        op_labels = [
            r"$e$", r"$r$", r"$r^2$", r"$r^3$",
            r"$s$", r"$rs$", r"$r^2 s$", r"$r^3 s$",
        ]
        op_names = [
            "identity", r"$90^\circ$", r"$180^\circ$", r"$270^\circ$",
            "horiz flip", "vert flip", "diag /", "diag \\",
        ]

        squares = []
        for (x, y), op, name in zip(positions, op_labels, op_names):
            sq = make_labeled_square().scale(0.55).move_to([x, y, 0])
            tex_op = Tex(op, font_size=28, color=YELLOW).next_to(
                sq, DOWN, buff=0.12
            )
            tex_nm = Tex(name, font_size=20).next_to(
                tex_op, DOWN, buff=0.05
            )
            squares.append(VGroup(sq, tex_op, tex_nm))

        identity, r1, r2, r3, s, rs, r2s, r3s = squares
        self.play(FadeIn(identity))

        def rotate_copy(base, angle):
            target = base.copy()
            target[0].rotate(angle, about_point=target[0][0].get_center())
            return target

        def flip_copy(base, axis):
            target = base.copy()
            target[0].flip(axis, about_point=target[0][0].get_center())
            return target

        self.play(TransformFromCopy(identity[0], r1[0]), FadeIn(r1[1:]))
        self.play(Rotate(r1[0], angle=-PI / 2,
                         about_point=r1[0][0].get_center()))
        self.wait(0.2)

        self.play(TransformFromCopy(identity[0], r2[0]), FadeIn(r2[1:]))
        self.play(Rotate(r2[0], angle=-PI,
                         about_point=r2[0][0].get_center()))
        self.wait(0.2)

        self.play(TransformFromCopy(identity[0], r3[0]), FadeIn(r3[1:]))
        self.play(Rotate(r3[0], angle=-3 * PI / 2,
                         about_point=r3[0][0].get_center()))
        self.wait(0.2)

        self.play(TransformFromCopy(identity[0], s[0]), FadeIn(s[1:]))
        self.play(s[0].animate.flip(axis=RIGHT))

        self.play(TransformFromCopy(identity[0], rs[0]), FadeIn(rs[1:]))
        self.play(rs[0].animate.flip(axis=UP))

        self.play(TransformFromCopy(identity[0], r2s[0]), FadeIn(r2s[1:]))
        self.play(r2s[0].animate.flip(axis=UR))

        self.play(TransformFromCopy(identity[0], r3s[0]), FadeIn(r3s[1:]))
        self.play(r3s[0].animate.flip(axis=UL))

        order_note = Tex(
            r"$|D_4| = 8 = 4\text{ rotations} + 4\text{ reflections}$",
            font_size=28, color=YELLOW,
        ).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(order_note))
        self.wait(1.5)
