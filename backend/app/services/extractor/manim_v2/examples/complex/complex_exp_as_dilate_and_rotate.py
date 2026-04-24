from manim import *
import numpy as np


class ComplexExpAsDilateAndRotate(Scene):
    """exp: (C, +) -> (C^*, ×).  e^{a + bi} = e^a * (cos b + i sin b).
    Show a z = a + bi point on the additive plane and its image e^z on the
    multiplicative plane.  Adding a (real) stretches by e^a, adding bi
    (imaginary) rotates by angle b."""

    def construct(self):
        title = MathTex(
            r"e^{a + b\,i} = e^{a}\bigl(\cos b + i\sin b\bigr)",
            font_size=32,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane_add = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5.2, y_length=5.2,
            background_line_style={"stroke_opacity": 0.25},
        ).to_edge(LEFT, buff=0.35).shift(DOWN * 0.3)
        plane_mul = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1],
            x_length=5.2, y_length=5.2,
            background_line_style={"stroke_opacity": 0.25},
        ).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.3)
        add_lab = MathTex(r"(\mathbb{C}, +)", font_size=28,
                          color=GREEN).next_to(plane_add, UP, buff=0.1)
        mul_lab = MathTex(r"(\mathbb{C}^{*}, \times)", font_size=28,
                          color=ORANGE).next_to(plane_mul, UP, buff=0.1)
        self.play(Create(plane_add), Create(plane_mul),
                  Write(add_lab), Write(mul_lab))

        a_tr = ValueTracker(0.0)
        b_tr = ValueTracker(0.0)

        def z_point():
            return plane_add.c2p(a_tr.get_value(), b_tr.get_value())

        def w_point():
            a = a_tr.get_value()
            b = b_tr.get_value()
            return plane_mul.c2p(np.exp(a) * np.cos(b),
                                 np.exp(a) * np.sin(b))

        def get_z_dot():
            return Dot(z_point(), radius=0.1, color=YELLOW).set_z_index(4)

        def get_w_dot():
            return Dot(w_point(), radius=0.1, color=RED).set_z_index(4)

        def get_z_vec():
            return Arrow(plane_add.c2p(0, 0), z_point(),
                         buff=0, color=GREEN, stroke_width=3,
                         max_tip_length_to_length_ratio=0.12)

        def get_w_vec():
            return Arrow(plane_mul.c2p(0, 0), w_point(),
                         buff=0, color=RED, stroke_width=3,
                         max_tip_length_to_length_ratio=0.12)

        def get_unit_circle_ghost():
            r = np.exp(a_tr.get_value())
            origin = plane_mul.c2p(0, 0)
            unit = plane_mul.c2p(1, 0)[0] - origin[0]
            return Circle(radius=r * unit, color=BLUE,
                          stroke_opacity=0.4, stroke_width=2).move_to(origin)

        z_dot = always_redraw(get_z_dot)
        w_dot = always_redraw(get_w_dot)
        z_vec = always_redraw(get_z_vec)
        w_vec = always_redraw(get_w_vec)
        ghost = always_redraw(get_unit_circle_ghost)
        self.add(z_dot, w_dot, z_vec, w_vec, ghost)

        readout = always_redraw(lambda: VGroup(
            MathTex("a=", font_size=24, color=GREEN),
            DecimalNumber(a_tr.get_value(), num_decimal_places=2,
                          font_size=24, color=GREEN),
            MathTex(r",\ b=", font_size=24, color=GREEN),
            DecimalNumber(b_tr.get_value(), num_decimal_places=2,
                          font_size=24, color=GREEN),
            MathTex(r"\ \to\ |e^z|=", font_size=24, color=RED),
            DecimalNumber(np.exp(a_tr.get_value()), num_decimal_places=2,
                          font_size=24, color=RED),
        ).arrange(RIGHT, buff=0.08).to_edge(DOWN, buff=0.25))
        self.add(readout)

        self.play(a_tr.animate.set_value(0.8), run_time=2)
        self.play(b_tr.animate.set_value(np.pi / 2), run_time=2)
        self.play(b_tr.animate.set_value(np.pi), run_time=2)
        self.play(a_tr.animate.set_value(0.0), run_time=1.5)
        self.play(b_tr.animate.set_value(2 * np.pi), run_time=2)
        self.wait(1.3)
