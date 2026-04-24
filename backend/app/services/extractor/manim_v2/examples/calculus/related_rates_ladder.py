from manim import *
import numpy as np


class RelatedRatesLadderExample(Scene):
    """
    Related rates: ladder of length L slides down a wall. If foot is
    at distance x from wall and top at height y, then x²+y²=L².
    Differentiate: 2x x' + 2y y' = 0, so y' = -(x/y) x'.
    Given x' > 0 (foot moves away), y' is negative (top falls).
    """

    def construct(self):
        title = Tex(r"Related rates: sliding ladder, $x^2+y^2=L^2$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-0.5, 5, 1], y_range=[-0.5, 5, 1],
                            x_length=5.5, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 2.8 + DOWN * 0.3)
        self.play(Create(plane))

        # Wall and floor
        wall = Line(plane.c2p(0, 0), plane.c2p(0, 5), color=WHITE, stroke_width=3)
        floor = Line(plane.c2p(0, 0), plane.c2p(5, 0), color=WHITE, stroke_width=3)
        self.add(wall, floor)

        L = 4.0
        x_tr = ValueTracker(1.0)

        def ladder():
            x = x_tr.get_value()
            y = np.sqrt(max(0, L ** 2 - x ** 2))
            return Line(plane.c2p(x, 0), plane.c2p(0, y),
                         color=ORANGE, stroke_width=6)

        def foot_dot():
            x = x_tr.get_value()
            return Dot(plane.c2p(x, 0), color=GREEN, radius=0.12)

        def top_dot():
            x = x_tr.get_value()
            y = np.sqrt(max(0, L ** 2 - x ** 2))
            return Dot(plane.c2p(0, y), color=RED, radius=0.12)

        self.add(always_redraw(ladder), always_redraw(foot_dot),
                 always_redraw(top_dot))

        # Right column: equations
        x_prime = 0.5  # foot speed
        info = VGroup(
            Tex(rf"$L={L:.0f}$, $x'={x_prime}$ m/s", font_size=22),
            VGroup(Tex(r"$x=$", color=GREEN, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=2,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$y=\sqrt{L^2-x^2}=$", color=RED, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$y'=-\frac{x}{y}x'=$", color=YELLOW, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"(top falls faster as $x$ grows)",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)

        def y_of():
            x = x_tr.get_value()
            return np.sqrt(max(0.001, L * L - x * x))

        info[1][1].add_updater(lambda m: m.set_value(x_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(y_of()))
        info[3][1].add_updater(lambda m: m.set_value(-x_tr.get_value() / y_of() * x_prime))
        self.add(info)

        self.play(x_tr.animate.set_value(L - 0.1),
                  run_time=6, rate_func=smooth)
        self.wait(0.5)
