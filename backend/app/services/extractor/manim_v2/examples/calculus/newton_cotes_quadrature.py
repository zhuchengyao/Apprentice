from manim import *
import numpy as np


class NewtonCotesQuadratureExample(Scene):
    """
    Newton-Cotes quadrature rules approximate ∫_a^b f dx by fitting
    polynomials through n+1 equally-spaced nodes.
      n=1: trapezoidal rule
      n=2: Simpson's 1/3 rule
      n=3: Simpson's 3/8 rule
      n=4: Boole's rule

    TWO_COLUMN: LEFT axes with f(x) = e^(-x²) on [0, 2]; overlaid
    ValueTracker rule_tr cycles through the 4 rules with always_redraw
    polynomial fit + error. RIGHT shows each rule's error and scaling.
    """

    def construct(self):
        title = Tex(r"Newton-Cotes: fit polynomial through $n+1$ nodes",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 2.1, 0.5], y_range=[0, 1.1, 0.2],
                    x_length=6.0, y_length=4.0,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(axes))

        def f(x):
            return np.exp(-x * x)

        f_curve = axes.plot(f, x_range=[0, 2], color=BLUE, stroke_width=3)
        self.play(Create(f_curve))

        rule_tr = ValueTracker(1.0)

        def n_now():
            return max(1, min(4, int(round(rule_tr.get_value()))))

        def rule_name():
            n = n_now()
            return {1: "trapezoidal", 2: "Simpson 1/3", 3: "Simpson 3/8", 4: "Boole"}[n]

        def nodes_and_poly():
            n = n_now()
            a, b = 0, 2
            xs_nodes = np.linspace(a, b, n + 1)
            ys_nodes = f(xs_nodes)
            # Fit polynomial
            coeffs = np.polyfit(xs_nodes, ys_nodes, n)
            poly = lambda x: float(np.polyval(coeffs, x))
            # Draw polynomial
            poly_curve = axes.plot(poly, x_range=[0, 2],
                                    color=YELLOW, stroke_width=3)
            # Node dots
            dots = VGroup(*[Dot(axes.c2p(x, f(x)),
                                color=RED, radius=0.1)
                            for x in xs_nodes])
            # Error region
            xs_fine = np.linspace(0, 2, 60)
            pts_top = [axes.c2p(x, max(f(x), poly(x))) for x in xs_fine]
            pts_bot = [axes.c2p(x, min(f(x), poly(x))) for x in xs_fine]
            error_band = Polygon(*pts_top, *reversed(pts_bot),
                                  color=GREEN, stroke_width=0,
                                  fill_color=GREEN, fill_opacity=0.35)
            return VGroup(error_band, poly_curve, dots)

        self.add(always_redraw(nodes_and_poly))

        # Rule integral and error
        from scipy.integrate import quad
        true_val, _ = quad(f, 0, 2)

        def rule_integral():
            n = n_now()
            a, b = 0, 2
            xs_nodes = np.linspace(a, b, n + 1)
            ys_nodes = f(xs_nodes)
            # Newton-Cotes coefficients
            if n == 1:
                return 0.5 * (b - a) * (ys_nodes[0] + ys_nodes[1])
            if n == 2:
                h = (b - a) / 2
                return h / 3 * (ys_nodes[0] + 4 * ys_nodes[1] + ys_nodes[2])
            if n == 3:
                h = (b - a) / 3
                return 3 * h / 8 * (ys_nodes[0] + 3 * ys_nodes[1]
                                     + 3 * ys_nodes[2] + ys_nodes[3])
            if n == 4:
                h = (b - a) / 4
                return 2 * h / 45 * (7 * ys_nodes[0] + 32 * ys_nodes[1]
                                      + 12 * ys_nodes[2] + 32 * ys_nodes[3]
                                      + 7 * ys_nodes[4])

        # Right
        name_tex = Tex(rule_name(), color=ORANGE, font_size=26).to_corner(UR, buff=0.5)
        self.add(name_tex)
        def update_name(mob, dt):
            new = Tex(rule_name(), color=ORANGE, font_size=26).move_to(name_tex)
            name_tex.become(new)
            return name_tex
        name_tex.add_updater(update_name)

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\int_0^2 e^{-x^2}\,dx=$", font_size=22),
                   DecimalNumber(true_val, num_decimal_places=5,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"rule gives $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=5,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"error $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=6,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"error $\sim h^{n+2}$ (odd $n$: $h^{n+3}$)",
                color=GREY_B, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2).shift(DOWN * 0.8)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        info[2][1].add_updater(lambda m: m.set_value(rule_integral()))
        info[3][1].add_updater(lambda m: m.set_value(abs(rule_integral() - true_val)))
        self.add(info)

        for n in [2, 3, 4, 1]:
            self.play(rule_tr.animate.set_value(float(n)),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
