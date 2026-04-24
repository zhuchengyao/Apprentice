from manim import *


class ComplexMultiplicationScaleRotateExample(Scene):
    def construct(self):
        plane = ComplexPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1]).add_coordinates()
        self.add(plane)

        multiplier = 1 + 1j
        start = 2 + 0j
        end = multiplier * start

        dot = Dot(plane.n2p(start), color=YELLOW, radius=0.1)
        trail = TracedPath(dot.get_center, stroke_color=YELLOW, stroke_width=3)
        self.add(trail)

        start_lbl = MathTex("p", color=YELLOW).next_to(dot, DR, buff=0.1)
        eqn = MathTex(r"p \mapsto (1+i)\, p", font_size=38)
        eqn.to_corner(UL).add_background_rectangle()

        self.play(FadeIn(dot), Write(start_lbl), Write(eqn))

        end_dot = Dot(plane.n2p(end), color=YELLOW, radius=0.1)
        end_lbl = MathTex(r"(1+i)\,p", color=YELLOW).next_to(end_dot, UR, buff=0.1)
        self.play(
            Transform(dot, end_dot, path_arc=PI / 4),
            Transform(start_lbl, end_lbl, path_arc=PI / 4),
            run_time=2.5,
        )
        self.wait(0.6)
