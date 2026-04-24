from manim import *
import numpy as np


class ResidueTheoremContourExample(Scene):
    """
    Residue theorem: ∮_γ f(z) dz = 2πi Σ Res(f, z_k) for z_k poles
    inside γ.

    f(z) = 1/(z² + 1) has simple poles at ±i with residues ±1/(2i).

    TWO_COLUMN: LEFT ComplexPlane with contour (circle |z|=r) that
    grows via ValueTracker r_tr; RIGHT shows live count of poles
    inside and computed integral value 2πi Σ res. For r > 1, integral
    equals π; for r < 1, integral equals 0.
    """

    def construct(self):
        title = Tex(r"Residue theorem: $f(z)=1/(z^2+1)$, poles at $\pm i$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                             x_length=6.5, y_length=6.5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).shift(LEFT * 1.8 + DOWN * 0.2)
        self.play(Create(plane))

        # Poles
        pole_i = Dot(plane.n2p(0 + 1j), color=RED, radius=0.12)
        pole_neg_i = Dot(plane.n2p(0 - 1j), color=RED, radius=0.12)
        self.add(pole_i, pole_neg_i)
        self.add(Tex(r"$+i$", color=RED, font_size=22).next_to(pole_i, UR, buff=0.05))
        self.add(Tex(r"$-i$", color=RED, font_size=22).next_to(pole_neg_i, DR, buff=0.05))

        r_tr = ValueTracker(0.5)

        def contour_circle():
            r = r_tr.get_value()
            unit = plane.x_length / (plane.x_range[1] - plane.x_range[0])
            return Circle(radius=r * unit, color=YELLOW, stroke_width=3).move_to(plane.n2p(0))

        self.add(always_redraw(contour_circle))

        def n_inside():
            r = r_tr.get_value()
            count = 0
            for z0 in [1j, -1j]:
                if abs(z0) < r:
                    count += 1
            return count

        # Numerical integral
        def integral():
            r = r_tr.get_value()
            ts = np.linspace(0, TAU, 500, endpoint=False)
            dt = TAU / 500
            total = 0 + 0j
            for t in ts:
                z = r * np.exp(1j * t)
                dz = 1j * r * np.exp(1j * t) * dt
                f = 1 / (z * z + 1)
                total += f * dz
            return total

        info = VGroup(
            VGroup(Tex(r"$r=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"poles inside $=$", color=RED, font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\oint dz/(z^2+1)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN),
                   Tex(r"$+$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN),
                   Tex(r"$i$", font_size=22),
                   ).arrange(RIGHT, buff=0.05),
            Tex(r"$2\pi i\cdot \tfrac{1}{2i}=\pi$ for $r>1$",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(r_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(n_inside()))
        info[2][1].add_updater(lambda m: m.set_value(integral().real))
        info[2][3].add_updater(lambda m: m.set_value(integral().imag))
        self.add(info)

        for r_val in [1.5, 0.5, 2.0, 0.8, 1.2]:
            self.play(r_tr.animate.set_value(r_val),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
