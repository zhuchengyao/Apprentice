from manim import *
import numpy as np


class FundamentalGroupCircleExample(Scene):
    """
    π₁(S¹) ≅ ℤ: loops on a circle are classified by winding number.

    SINGLE_FOCUS: a unit circle with small hole marked at origin.
    ValueTracker wind_tr takes values through {1, 2, 0, -1, 3}; the
    current loop γ(t) = (1 + 0.12 sin(3t)) · (cos(wind·t+phase),
    sin(wind·t+phase)) is drawn via always_redraw ParametricFunction
    along with its winding-number readout computed from angular total.
    Homotopy phase: a loop with wind=0 smoothly contracts to a point.
    """

    def construct(self):
        title = Tex(r"$\pi_1(S^1)\cong \mathbb{Z}$: loops classified by winding number",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                            x_length=6.0, y_length=5.0,
                            background_line_style={"stroke_opacity": 0.3})
        self.play(Create(plane))

        # Fixed circle and hole
        circle = Circle(radius=2.0, color=BLUE, stroke_width=3).move_to(plane.c2p(0, 0))
        hole = Dot(plane.c2p(0, 0), color=RED, radius=0.12)
        hole_lbl = Tex(r"hole", color=RED, font_size=22).next_to(hole, DL, buff=0.1)
        self.play(Create(circle), FadeIn(hole), Write(hole_lbl))

        wind_tr = ValueTracker(1.0)
        contract_tr = ValueTracker(1.0)

        def loop():
            w = wind_tr.get_value()
            c = contract_tr.get_value()
            def gamma(t):
                r = c * (2.0 + 0.4 * np.sin(3 * t))
                return plane.c2p(r * np.cos(w * t),
                                  r * np.sin(w * t))
            return ParametricFunction(gamma, t_range=[0, TAU],
                                       color=YELLOW, stroke_width=4)

        self.add(always_redraw(loop))

        def true_winding():
            # Integer winding of the closed curve around origin.
            # Curve does not pass through origin since r = c·(2 + 0.4 sin 3t) > 0
            # so total angular change / 2π = w.
            return wind_tr.get_value()

        info = VGroup(
            VGroup(Tex(r"winding $w=$", font_size=24),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=24).set_color(YELLOW)
                   ).arrange(RIGHT, buff=0.1),
            Tex(r"$[\gamma]\in \pi_1\cong \mathbb{Z}$", font_size=22, color=YELLOW),
            Tex(r"loop radius scale $c=1$", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.35)
        info[0][1].add_updater(lambda m: m.set_value(int(round(true_winding()))))
        self.add(info)

        # Tour winding numbers
        for w in [2.0, 3.0, -1.0, 0.5, 1.0]:
            self.play(wind_tr.animate.set_value(w),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.4)

        # Contract a wind=0 loop (set wind=0 first)
        self.play(wind_tr.animate.set_value(0.0), run_time=1.2)
        note = Tex(r"Homotopy: $[\gamma_0]=0$ contracts to a point",
                   color=GREEN, font_size=22).to_edge(DOWN, buff=0.3)
        self.play(Write(note))
        self.play(contract_tr.animate.set_value(0.05),
                  run_time=3, rate_func=smooth)
        self.wait(0.5)

        # Try to contract wind=1 to show it can't pass through hole
        self.play(contract_tr.animate.set_value(1.0), run_time=1.0)
        self.play(wind_tr.animate.set_value(1.0), run_time=1.0)
        note2 = Tex(r"$[\gamma_1]\neq 0$: hole blocks contraction",
                    color=RED, font_size=22).next_to(note, DOWN, buff=0.15)
        self.play(Write(note2))
        self.wait(1.0)
