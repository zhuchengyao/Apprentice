from manim import *
import numpy as np


class VectorCurlDivergence2DExample(Scene):
    """
    Visualize curl and divergence of a 2D vector field
    F(x, y) = (a x − b y, c x + d y) for various (a, b, c, d).

    Curl = ∂F_y/∂x − ∂F_x/∂y = c + b
    Divergence = ∂F_x/∂x + ∂F_y/∂y = a + d

    TWO_COLUMN: LEFT shows field with arrows at grid points.
    ValueTracker s_tr tours 4 configs:
      (0, 1, -1, 0) — pure rotation: curl=-2, div=0
      (1, 0, 0, 1) — pure expansion: curl=0, div=2
      (1, 0, 0, -1) — hyperbolic: curl=0, div=0
      (0.5, -0.5, 0.5, 0.5) — mix: curl=1, div=1
    """

    def construct(self):
        title = Tex(r"Vector field: $\nabla\times F = c+b$, $\nabla\cdot F = a+d$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                            x_length=5.8, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 2.5 + DOWN * 0.2)
        self.play(Create(plane))

        configs = [
            (0, 1, -1, 0, "rotation"),
            (1, 0, 0, 1, "expansion"),
            (1, 0, 0, -1, "hyperbolic"),
            (0.5, -0.5, 0.5, 0.5, "spiral"),
        ]

        s_tr = ValueTracker(0.0)

        def coeffs():
            s = s_tr.get_value()
            k = int(s)
            frac = s - k
            k_next = min(len(configs) - 1, k + 1)
            c0 = configs[k][:4]
            c1 = configs[k_next][:4]
            return tuple((1 - frac) * c0[i] + frac * c1[i] for i in range(4))

        def name_now():
            s = s_tr.get_value()
            k = int(round(s))
            k = max(0, min(len(configs) - 1, k))
            return configs[k][4]

        def field_arrows():
            a, b, c, d = coeffs()
            grp = VGroup()
            for x in np.linspace(-1.7, 1.7, 8):
                for y in np.linspace(-1.7, 1.7, 8):
                    fx = a * x - b * y
                    fy = c * x + d * y
                    mag = np.sqrt(fx * fx + fy * fy)
                    if mag < 1e-4:
                        continue
                    scale = 0.3 / max(mag, 0.3)
                    col = interpolate_color(BLUE, RED, min(1, mag / 2))
                    grp.add(Arrow(plane.c2p(x, y),
                                   plane.c2p(x + fx * scale, y + fy * scale),
                                   color=col, buff=0, stroke_width=2,
                                   max_tip_length_to_length_ratio=0.25))
            return grp

        self.add(always_redraw(field_arrows))

        def curl_div():
            a, b, c, d = coeffs()
            return c + b, a + d

        info = VGroup(
            Tex(r"$F=(ax-by,\ cx+dy)$", font_size=22),
            VGroup(Tex(r"$a=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$b=$", font_size=22),
                   DecimalNumber(1.0, num_decimal_places=2,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$c=$", font_size=22),
                   DecimalNumber(-1.0, num_decimal_places=2,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$d=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"curl $= c+b =$", color=YELLOW, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"div $= a+d =$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.25)
        info[1][1].add_updater(lambda m: m.set_value(coeffs()[0]))
        info[2][1].add_updater(lambda m: m.set_value(coeffs()[1]))
        info[3][1].add_updater(lambda m: m.set_value(coeffs()[2]))
        info[4][1].add_updater(lambda m: m.set_value(coeffs()[3]))
        info[5][1].add_updater(lambda m: m.set_value(curl_div()[0]))
        info[6][1].add_updater(lambda m: m.set_value(curl_div()[1]))
        self.add(info)

        # Dynamic name label
        name_tex = Tex(name_now(), color=ORANGE, font_size=26).to_edge(DOWN, buff=0.5)
        self.add(name_tex)
        def update_name(mob, dt):
            new = Tex(name_now(), color=ORANGE, font_size=26).move_to(name_tex)
            name_tex.become(new)
            return name_tex
        name_tex.add_updater(update_name)

        for k in range(1, len(configs)):
            self.play(s_tr.animate.set_value(float(k)),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
