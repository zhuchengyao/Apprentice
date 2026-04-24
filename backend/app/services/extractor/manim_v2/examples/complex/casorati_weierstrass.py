from manim import *
import numpy as np


class CasoratiWeierstrassExample(Scene):
    """
    Casorati–Weierstrass: near an essential singularity, a function's
    image on any punctured neighborhood is dense in ℂ.

    f(z) = exp(1/z) near z=0. SINGLE_FOCUS ComplexPlane on right shows
    the image cloud of a small disk |z−0|<r; left has the input plane
    with a shrinking circle. ValueTracker r_tr sweeps r: 0.6 → 0.05;
    always_redraw recomputes 400 sample points on |z|=r (and interior
    ring |z|=r/2) and maps them through exp(1/z). Image cloud
    visibly spreads to cover most of ℂ as r → 0.
    """

    def construct(self):
        title = Tex(r"Casorati–Weierstrass: $f(z)=e^{1/z}$ near $z=0$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-1.5, 1.5], y_range=[-1.5, 1.5],
                            x_length=4.8, y_length=4.8,
                            background_line_style={"stroke_opacity": 0.35}
                            ).shift(LEFT * 3.4)
        right = ComplexPlane(x_range=[-6, 6, 2], y_range=[-6, 6, 2],
                             x_length=5.6, y_length=5.6,
                             background_line_style={"stroke_opacity": 0.35}
                             ).shift(RIGHT * 2.3)

        lbl_l = Tex(r"input $z$, $|z|<r$", font_size=22).next_to(left, UP, buff=0.1)
        lbl_r = Tex(r"output $e^{1/z}$", font_size=22).next_to(right, UP, buff=0.1)
        self.play(Create(left), Create(right), Write(lbl_l), Write(lbl_r))

        origin_dot = Dot(left.n2p(0), color=RED, radius=0.1)
        origin_lbl = Tex(r"$0$", color=RED, font_size=22).next_to(origin_dot, DL, buff=0.05)
        self.play(FadeIn(origin_dot), Write(origin_lbl))

        r_tr = ValueTracker(0.6)

        def input_circle():
            r = r_tr.get_value()
            return Circle(radius=r, color=YELLOW, stroke_width=3).move_to(left.n2p(0)).scale(
                (left.x_length / (left.x_range[1] - left.x_range[0])) / 1.0
                if False else 1
            )

        # Scale circle explicitly: left axes give 1 unit = (x_length/3)
        def input_circle2():
            r = r_tr.get_value()
            unit = left.x_length / (left.x_range[1] - left.x_range[0])
            return Circle(radius=r * unit, color=YELLOW,
                          stroke_width=3).move_to(left.n2p(0))

        def image_cloud():
            r = r_tr.get_value()
            pts = []
            for rr in [r, r * 0.7, r * 0.4]:
                thetas = np.linspace(0, TAU, 160, endpoint=False)
                z = rr * np.exp(1j * thetas)
                w = np.exp(1 / z)
                for wi in w:
                    if abs(wi) < 6.5:
                        pts.append(Dot(right.n2p(complex(wi.real, wi.imag)),
                                       color=ORANGE, radius=0.02))
            return VGroup(*pts)

        self.add(always_redraw(input_circle2), always_redraw(image_cloud))

        info = VGroup(
            VGroup(Tex(r"$r=$", font_size=22),
                   DecimalNumber(0.6, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)
                   ).arrange(RIGHT, buff=0.1),
            Tex(r"image dense in $\mathbb{C}$", color=ORANGE, font_size=22),
            Tex(r"essential singularity at $0$", color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.4)
        info[0][1].add_updater(lambda m: m.set_value(r_tr.get_value()))
        self.add(info)

        self.play(r_tr.animate.set_value(0.05), run_time=6, rate_func=smooth)
        self.wait(0.8)
        self.play(r_tr.animate.set_value(0.6), run_time=2, rate_func=smooth)
        self.play(r_tr.animate.set_value(0.08), run_time=3, rate_func=smooth)
        self.wait(0.8)
