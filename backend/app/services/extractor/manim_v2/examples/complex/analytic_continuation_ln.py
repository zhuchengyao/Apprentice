from manim import *
import numpy as np


class AnalyticContinuationLnExample(Scene):
    """
    Analytic continuation of ln(z) along a path encircling the
    origin: after one loop, the value shifts by 2πi. Multi-valued
    logarithm has Riemann surface with infinitely many sheets.

    TWO_COLUMN: LEFT ComplexPlane of z with ValueTracker θ_tr
    moving dot along path z(θ)=e^{iθ} for θ ∈ [0, 4π]; RIGHT
    shows ln(z) = ln|z| + i θ with θ continuously increasing (no
    principal-branch wrap); the GREEN trace spirals up.
    """

    def construct(self):
        title = Tex(r"Analytic continuation: $\ln z$ around origin picks up $2\pi i$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-1.8, 1.8, 1], y_range=[-1.8, 1.8, 1],
                            x_length=4.5, y_length=4.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.3)
        right = ComplexPlane(x_range=[-3, 3, 1], y_range=[-4, 14, 2],
                             x_length=4.5, y_length=5.2,
                             background_line_style={"stroke_opacity": 0.3}
                             ).shift(RIGHT * 2.5)
        l_lbl = Tex(r"$z=e^{i\theta}$ on unit circle", font_size=22).next_to(left, UP, buff=0.1)
        r_lbl = Tex(r"$\ln z = \ln|z| + i\theta$", font_size=22).next_to(right, UP, buff=0.1)
        self.play(Create(left), Create(right), Write(l_lbl), Write(r_lbl))

        unit_circ = Circle(radius=left.x_length / (left.x_range[1] - left.x_range[0]),
                            color=GREY_B, stroke_width=2).move_to(left.n2p(0))
        self.play(Create(unit_circ))

        theta_tr = ValueTracker(0.0)

        def z_dot():
            t = theta_tr.get_value()
            z = np.exp(1j * t)
            return Dot(left.n2p(complex(z.real, z.imag)),
                        color=YELLOW, radius=0.1)

        def z_radial():
            t = theta_tr.get_value()
            z = np.exp(1j * t)
            return Line(left.n2p(0),
                         left.n2p(complex(z.real, z.imag)),
                         color=ORANGE, stroke_width=2)

        def ln_trace():
            t = theta_tr.get_value()
            if t < 0.02:
                return VMobject()
            ts = np.linspace(0, t, max(5, int(200 * t / (4 * PI))))
            pts = []
            for tk in ts:
                w = np.log(abs(1)) + 1j * tk  # = i·tk
                pts.append(right.n2p(complex(w.real, w.imag)))
            return VMobject().set_points_as_corners(pts)\
                .set_color(GREEN).set_stroke(width=3)

        def ln_dot():
            t = theta_tr.get_value()
            w = 1j * t
            return Dot(right.n2p(complex(w.real, w.imag)),
                        color=GREEN, radius=0.1)

        self.add(always_redraw(z_dot), always_redraw(z_radial),
                 always_redraw(ln_trace), always_redraw(ln_dot))

        # Sheet markers on right
        sheet_lines = VGroup()
        sheet_lbls = VGroup()
        for k, yv in enumerate([0, 2 * PI, 4 * PI]):
            if yv <= 13:
                sheet_lines.add(DashedLine(right.n2p(-3, yv),
                                            right.n2p(3, yv),
                                            color=BLUE,
                                            stroke_width=1.5,
                                            stroke_opacity=0.5))
                sheet_lbls.add(Tex(rf"$2\pi\cdot {k}$", color=BLUE,
                                    font_size=18).next_to(right.n2p(3, yv),
                                                           RIGHT, buff=0.1))
        self.add(sheet_lines, sheet_lbls)

        # Info
        info = VGroup(
            VGroup(Tex(r"$\theta=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"Im $\ln z=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"after each full loop: +$2\pi$",
                color=BLUE, font_size=22),
            Tex(r"principal branch: $-\pi<\theta\le\pi$",
                color=GREY_B, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3).shift(LEFT * 3.2)
        info[0][1].add_updater(lambda m: m.set_value(theta_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(theta_tr.get_value()))
        self.add(info)

        self.play(theta_tr.animate.set_value(4 * PI),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
