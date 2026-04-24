from manim import *
import numpy as np


class MatrixTrackPointExample(Scene):
    def construct(self):
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.4})
        matrix = [[1, 1], [0, 1]]
        v_start = np.array([1, 2, 0])

        dot = Dot(v_start, color=YELLOW, radius=0.1)
        v_lbl = MathTex(r"\vec{v}", color=YELLOW).next_to(dot, UR, buff=0.1)

        self.add(plane, dot, v_lbl)
        self.wait(0.3)

        new_pos = np.array([3, 2, 0])
        self.play(
            ApplyMatrix(matrix, plane),
            dot.animate.move_to(new_pos),
            v_lbl.animate.next_to(new_pos, UR, buff=0.1),
            run_time=2.5,
        )
        coords = MathTex(r"A\vec{v} = (3,\ 2)", font_size=34, color=YELLOW)
        coords.to_corner(UL).add_background_rectangle()
        self.play(Write(coords))
        self.wait(0.6)
