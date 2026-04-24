from manim import *
import numpy as np


class ArgumentPrincipleWindingExample(Scene):
    """
    Argument principle: for meromorphic f and contour γ,
        (1/2πi) ∮ f'/f dz = Z − P,
    i.e. winding of f(γ) around 0 equals (#zeros − #poles) inside γ.

    f(z) = z·(z−1)·(z+1). 3 simple zeros. Contour = circle of radius
    r_tr via ValueTracker; first r=0.5 (1 zero inside → wind 1),
    then r=1.3 (all 3 zeros inside → wind 3), then r=2.0 (still 3).
    Right: ComplexPlane of image f(γ) tracing around origin.
    """

    def construct(self):
        title = Tex(r"Argument principle: $\frac{1}{2\pi i}\oint \frac{f'}{f}\,dz = Z - P$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
                            x_length=5.0, y_length=5.0,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.4)
        right = ComplexPlane(x_range=[-6, 6, 2], y_range=[-6, 6, 2],
                             x_length=5.2, y_length=5.2,
                             background_line_style={"stroke_opacity": 0.3}
                             ).shift(RIGHT * 2.3)
        left_lbl = Tex(r"input: contour $\gamma$", font_size=22).next_to(left, UP, buff=0.1)
        right_lbl = Tex(r"output: $f(\gamma)$", font_size=22).next_to(right, UP, buff=0.1)
        self.play(Create(left), Create(right), Write(left_lbl), Write(right_lbl))

        # Zeros: -1, 0, 1
        zero_dots = VGroup(
            Dot(left.n2p(-1), color=RED, radius=0.1),
            Dot(left.n2p(0), color=RED, radius=0.1),
            Dot(left.n2p(1), color=RED, radius=0.1),
        )
        zero_lbls = VGroup(
            Tex(r"$-1$", font_size=20).next_to(left.n2p(-1), DL, buff=0.05),
            Tex(r"$0$", font_size=20).next_to(left.n2p(0), DL, buff=0.05),
            Tex(r"$1$", font_size=20).next_to(left.n2p(1), DR, buff=0.05),
        )
        self.play(FadeIn(zero_dots), Write(zero_lbls))

        def f(z):
            return z * (z - 1) * (z + 1)

        r_tr = ValueTracker(0.5)

        def input_circle():
            r = r_tr.get_value()
            unit = left.x_length / (left.x_range[1] - left.x_range[0])
            return Circle(radius=r * unit, color=YELLOW,
                          stroke_width=3).move_to(left.n2p(0))

        def output_image():
            r = r_tr.get_value()
            pts = []
            for t in np.linspace(0, TAU, 300):
                z = r * np.exp(1j * t)
                w = f(z)
                pts.append(right.n2p(complex(w.real, w.imag)))
            return VMobject().set_points_as_corners(pts + [pts[0]])\
                .set_color(YELLOW).set_stroke(width=3)

        def origin_right():
            return Dot(right.n2p(0), color=RED, radius=0.1)

        self.add(always_redraw(input_circle),
                 always_redraw(output_image),
                 origin_right())

        # Count zeros inside radius r
        def zeros_inside():
            r = r_tr.get_value()
            count = 0
            for z0 in [-1, 0, 1]:
                if abs(z0) < r:
                    count += 1
            return count

        # Compute winding of f(γ) around 0 via discrete angular change
        def winding():
            r = r_tr.get_value()
            ts = np.linspace(0, TAU, 400, endpoint=False)
            zs = r * np.exp(1j * ts)
            ws = f(zs)
            ang = np.angle(ws)
            dang = np.diff(np.concatenate([ang, [ang[0]]]))
            dang = np.where(dang > PI, dang - 2 * PI, dang)
            dang = np.where(dang < -PI, dang + 2 * PI, dang)
            return int(round(np.sum(dang) / TAU))

        info = VGroup(
            VGroup(Tex(r"$r=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"zeros inside $Z=$", color=RED, font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"winding of $f(\gamma)=$", color=YELLOW, font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"$Z-P=\mathrm{wind}$", color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.3)

        info[0][1].add_updater(lambda m: m.set_value(r_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(zeros_inside()))
        info[2][1].add_updater(lambda m: m.set_value(winding()))
        self.add(info)

        for r_val in [1.3, 2.0, 0.5, 1.8]:
            self.play(r_tr.animate.set_value(r_val),
                      run_time=2.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
