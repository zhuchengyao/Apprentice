from manim import *


class ComplexMultiplicationByIExample(Scene):
    def construct(self):
        plane = ComplexPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1]).add_coordinates()
        self.add(plane)

        z = 2 + 1j
        dot = Dot(plane.n2p(z), color=YELLOW)
        label = MathTex("z", color=YELLOW).next_to(dot, UR, buff=0.1)
        label.add_updater(lambda m: m.next_to(dot, UR, buff=0.1))

        eqn = MathTex(r"z \mapsto i \cdot z", font_size=40)
        eqn.to_corner(UL).add_background_rectangle()

        self.play(FadeIn(dot), Write(label), Write(eqn))
        self.play(Rotate(dot, PI / 2, about_point=plane.n2p(0)), run_time=2)
        label.clear_updaters()
        iz_lbl = MathTex(r"iz", color=YELLOW).next_to(dot, UL, buff=0.1)
        self.play(Transform(label, iz_lbl))
        self.wait(0.6)
