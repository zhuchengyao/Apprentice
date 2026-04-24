from manim import *
import numpy as np


class WindingPolynomialZerosExample(Scene):
    """
    For polynomial p(z) of degree n, winding number of p(γ) around 0
    equals the number of zeros of p enclosed by γ (argument principle).

    Example: p(z) = z³ - 2z + 1 has 3 zeros. Sweep contour radius r
    via ValueTracker; winding count matches zeros inside.

    TWO_COLUMN: LEFT z-plane with contour + zero markers. RIGHT plot
    of p(γ) image tracing around origin.
    """

    def construct(self):
        title = Tex(r"Argument principle: winding of $p(\gamma)$ $=\#$ zeros inside",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Zeros of p(z) = z^3 - 2z + 1
        roots = np.roots([1, 0, -2, 1])  # complex roots

        left = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                            x_length=4.5, y_length=4.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.3)
        right = ComplexPlane(x_range=[-8, 8, 2], y_range=[-8, 8, 2],
                             x_length=4.8, y_length=4.8,
                             background_line_style={"stroke_opacity": 0.3}
                             ).shift(RIGHT * 2.5)
        self.play(Create(left), Create(right))

        # Mark zeros
        for z in roots:
            self.add(Dot(left.n2p(complex(z.real, z.imag)),
                         color=RED, radius=0.1))

        r_tr = ValueTracker(0.4)

        def p(z):
            return z ** 3 - 2 * z + 1

        def input_circle():
            r = r_tr.get_value()
            unit = left.x_length / (left.x_range[1] - left.x_range[0])
            return Circle(radius=r * unit, color=YELLOW,
                          stroke_width=3).move_to(left.n2p(0))

        def image_curve():
            r = r_tr.get_value()
            pts = []
            for t in np.linspace(0, TAU, 200):
                z = r * np.exp(1j * t)
                w = p(z)
                if abs(w) < 10:
                    pts.append(right.n2p(complex(w.real, w.imag)))
            if len(pts) < 3:
                return VMobject()
            return VMobject().set_points_smoothly(pts + [pts[0]])\
                .set_color(YELLOW).set_stroke(width=3)

        self.add(always_redraw(input_circle), always_redraw(image_curve))
        self.add(Dot(right.n2p(0), color=RED, radius=0.1))

        def n_inside():
            r = r_tr.get_value()
            return sum(1 for z in roots if abs(z) < r)

        def winding():
            r = r_tr.get_value()
            ts = np.linspace(0, TAU, 400, endpoint=False)
            zs = r * np.exp(1j * ts)
            ws = p(zs)
            ang = np.angle(ws)
            d = np.diff(np.concatenate([ang, [ang[0]]]))
            d = np.where(d > PI, d - 2 * PI, d)
            d = np.where(d < -PI, d + 2 * PI, d)
            return int(round(np.sum(d) / TAU))

        info = VGroup(
            VGroup(Tex(r"$r=$", font_size=22),
                   DecimalNumber(0.4, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"zeros inside $=$", color=RED, font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"winding $=$", color=YELLOW, font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(rf"$p(z)=z^3-2z+1$", font_size=22),
            Tex(rf"roots: $\approx\pm 1.62, {roots[2].real:.2f}$",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3).shift(LEFT * 3)
        info[0][1].add_updater(lambda m: m.set_value(r_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(n_inside()))
        info[2][1].add_updater(lambda m: m.set_value(winding()))
        self.add(info)

        for r_val in [0.9, 1.8, 0.5, 1.3, 1.9]:
            self.play(r_tr.animate.set_value(r_val),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
