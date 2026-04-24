from manim import *
import numpy as np


class WindingOdometerAccumulatedAngle(Scene):
    """The winding number of a closed curve around the origin is the total
    signed angle accumulated by f(z) / |f(z)| as z traverses the curve,
    divided by 2*pi.  Visualize with an 'odometer': an arrow on a unit
    dial that spins around and accumulates turns.  Use f(z) = z^2 on the
    unit circle — winding number 2."""

    def construct(self):
        title = Tex(
            r"Winding number as an accumulated-angle odometer",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(
            x_range=[-2, 2, 1], y_range=[-2, 2, 1],
            x_length=5, y_length=5,
            background_line_style={"stroke_opacity": 0.25},
        ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        self.play(Create(plane))

        dial = Circle(radius=1.6, color=WHITE, stroke_width=3).shift(
            RIGHT * 3.3 + DOWN * 0.3
        )
        dial_center = dial.get_center()
        dial_cap = Tex("odometer", font_size=22).next_to(dial, UP, buff=0.15)
        tick_marks = VGroup(*[
            Line(
                dial_center + rotate_vector(UP * 1.5, a),
                dial_center + rotate_vector(UP * 1.6, a),
                color=WHITE, stroke_width=1.5,
            )
            for a in np.arange(0, 2 * np.pi, np.pi / 6)
        ])
        self.play(Create(dial), Write(dial_cap), FadeIn(tick_marks))

        t_tr = ValueTracker(0.0)
        acc = [0.0]
        last_angle = [0.0]

        def get_gamma_dot():
            t = t_tr.get_value()
            z = np.exp(1j * t)
            return Dot(plane.n2p(z), radius=0.1, color=YELLOW).set_z_index(5)

        def get_gamma_curve():
            t = t_tr.get_value()
            return ParametricFunction(
                lambda s: plane.n2p(np.exp(1j * s)),
                t_range=[0, t, 0.02], color=YELLOW, stroke_width=3,
            )

        def get_dial_arrow():
            t = t_tr.get_value()
            z = np.exp(1j * t)
            w = z * z
            angle = np.angle(w)
            prev = last_angle[0]
            d = angle - prev
            while d > np.pi:
                d -= 2 * np.pi
            while d < -np.pi:
                d += 2 * np.pi
            acc[0] += d
            last_angle[0] = angle
            ang = acc[0]
            end = dial_center + rotate_vector(UP * 1.4, ang)
            return Arrow(dial_center, end, buff=0, color=RED,
                         stroke_width=4,
                         max_tip_length_to_length_ratio=0.12).set_z_index(3)

        def get_readout():
            w = acc[0] / (2 * np.pi)
            row = VGroup(
                Tex(r"revs so far:", font_size=22),
                DecimalNumber(w, num_decimal_places=3,
                              font_size=24, color=RED),
            ).arrange(RIGHT, buff=0.15).next_to(dial, DOWN, buff=0.4)
            return row

        gamma_curve = always_redraw(get_gamma_curve)
        gamma_dot = always_redraw(get_gamma_dot)
        dial_arrow = always_redraw(get_dial_arrow)
        readout = always_redraw(get_readout)
        self.add(gamma_curve, gamma_dot, dial_arrow, readout)

        f_tex = MathTex(r"f(z) = z^{2}", font_size=28,
                        color=BLUE).to_corner(UL, buff=0.4).shift(DOWN * 0.6)
        gamma_tex = MathTex(r"\gamma(t) = e^{it},\ t\in[0,2\pi]",
                            font_size=22).next_to(f_tex, DOWN,
                                                  aligned_edge=LEFT)
        self.play(FadeIn(f_tex), FadeIn(gamma_tex))

        self.play(t_tr.animate.set_value(2 * np.pi),
                  run_time=7, rate_func=linear)

        conclusion = MathTex(
            r"\text{winding}(f\circ\gamma, 0) = 2",
            font_size=30, color=YELLOW,
        ).to_edge(DOWN, buff=0.25)
        self.play(Write(conclusion))
        self.wait(1.3)
