from manim import *
import numpy as np


class CauchyIntegralFormulaVisualExample(Scene):
    """
    Cauchy integral formula: for f holomorphic inside contour γ,
        f(z_0) = (1/2πi) ∮_γ f(z)/(z − z_0) dz.
    Apply to f(z) = z² − 2z + 3 with contour |z|=2 and z_0 = 1+0.5i:
    evaluates to f(z_0) = (1+0.5i)² − 2(1+0.5i) + 3 = 1.75 + i·(-1).

    Wait let me compute: (1+0.5i)² = 1 + i - 0.25 = 0.75 + i.
    −2(1+0.5i) = -2 - i
    + 3: 0.75 + i - 2 - i + 3 = 1.75 + 0i

    So f(z_0) = 1.75 + 0i.

    TWO_COLUMN: LEFT ComplexPlane with contour + z_0 marked. RIGHT
    shows live numerical integral converging to 2πi·f(z_0) via
    ValueTracker N_tr (number of sample points).
    """

    def construct(self):
        title = Tex(r"Cauchy: $f(z_0)=\frac{1}{2\pi i}\oint \frac{f(z)}{z-z_0}dz$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                             x_length=6, y_length=5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(plane))

        # Contour |z|=2
        contour = Circle(radius=2 * plane.x_length / (plane.x_range[1] - plane.x_range[0]),
                         color=BLUE, stroke_width=3).move_to(plane.n2p(0))
        self.add(contour)

        # z_0
        z0 = complex(1, 0.5)
        z0_dot = Dot(plane.n2p(z0), color=RED, radius=0.14)
        z0_lbl = Tex(r"$z_0=1+0.5i$", color=RED, font_size=22).next_to(z0_dot, UR, buff=0.1)
        self.add(z0_dot, z0_lbl)

        def f(z):
            return z * z - 2 * z + 3

        f_z0 = f(z0)  # 1.75 + 0i

        # Sample contour
        N_tr = ValueTracker(4.0)

        def k_now():
            return max(2, min(100, int(round(N_tr.get_value()))))

        def sample_dots():
            n = k_now()
            grp = VGroup()
            for k in range(n):
                theta = 2 * PI * k / n
                z = 2 * np.exp(1j * theta)
                grp.add(Dot(plane.n2p(z), color=YELLOW, radius=0.06))
            return grp

        self.add(always_redraw(sample_dots))

        # Numerical integral
        def compute_integral():
            n = k_now()
            thetas = np.linspace(0, TAU, n, endpoint=False)
            dtheta = TAU / n
            total = 0 + 0j
            for t in thetas:
                z = 2 * np.exp(1j * t)
                dz = 2 * 1j * np.exp(1j * t) * dtheta
                integrand = f(z) / (z - z0)
                total += integrand * dz
            return total / (2 * PI * 1j)

        # Right panel
        info = VGroup(
            Tex(r"$f(z)=z^2-2z+3$", color=BLUE, font_size=22),
            VGroup(Tex(r"$N=$", font_size=22),
                   DecimalNumber(4, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"numeric $f(z_0)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN),
                   Tex(r"$+$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN),
                   Tex(r"$i$", font_size=22),
                   ).arrange(RIGHT, buff=0.05),
            Tex(r"exact: $f(z_0)=1.75+0i$",
                color=RED, font_size=22),
            VGroup(Tex(r"error $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=6,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[1][1].add_updater(lambda m: m.set_value(k_now()))
        info[2][1].add_updater(lambda m: m.set_value(compute_integral().real))
        info[2][3].add_updater(lambda m: m.set_value(compute_integral().imag))
        info[4][1].add_updater(lambda m: m.set_value(abs(compute_integral() - f_z0)))
        self.add(info)

        self.play(N_tr.animate.set_value(100.0),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
