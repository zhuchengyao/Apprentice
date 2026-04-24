from manim import *
import numpy as np


class MobiusStressTestExample(Scene):
    """
    Möbius transformation f(z) = (az + b)/(cz + d) applied to a grid
    of circles + radial lines shows circle-to-circle mapping (circles
    and lines go to circles/lines).

    TWO_COLUMN: LEFT ComplexPlane with 5 concentric unit circles +
    12 radials; RIGHT shows image under f(z) = (z + 1)/(z - 1) with
    ValueTracker t_tr interpolating from identity to the map.
    """

    def construct(self):
        title = Tex(r"Möbius $f(z)=\frac{z+1}{z-1}$: circles/lines $\to$ circles/lines",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                            x_length=5.0, y_length=5.0,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.2)
        right = ComplexPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=5.2, y_length=3.6,
                             background_line_style={"stroke_opacity": 0.3}
                             ).shift(RIGHT * 2.4)
        self.play(Create(left), Create(right))

        # Input circles and radials
        def f(z):
            return (z + 1) / (z - 1) if abs(z - 1) > 1e-4 else complex(1e6, 0)

        t_tr = ValueTracker(0.0)

        def morph(z):
            t = t_tr.get_value()
            return (1 - t) * z + t * f(z)

        def input_circles():
            grp = VGroup()
            for r in [0.4, 0.8, 1.2, 1.6]:
                pts_l = []
                pts_r = []
                for theta in np.linspace(0, TAU, 80):
                    z = r * np.exp(1j * theta)
                    w = morph(z)
                    pts_l.append(left.n2p(complex(z.real, z.imag)))
                    if abs(w) < 20:
                        pts_r.append(right.n2p(complex(w.real, w.imag)))
                col = interpolate_color(BLUE, PURPLE, r / 2)
                grp.add(VMobject().set_points_smoothly(pts_l + [pts_l[0]])
                         .set_color(col).set_stroke(width=2))
                if len(pts_r) > 2:
                    grp.add(VMobject().set_points_smoothly(pts_r + [pts_r[0]])
                             .set_color(col).set_stroke(width=2))
            return grp

        def radial_lines():
            grp = VGroup()
            for phi in np.linspace(0, TAU, 8, endpoint=False):
                pts_l = []
                pts_r = []
                for r in np.linspace(0.01, 1.9, 40):
                    z = r * np.exp(1j * phi)
                    w = morph(z)
                    pts_l.append(left.n2p(complex(z.real, z.imag)))
                    if abs(w) < 20:
                        pts_r.append(right.n2p(complex(w.real, w.imag)))
                col = interpolate_color(ORANGE, YELLOW, phi / TAU)
                grp.add(VMobject().set_points_smoothly(pts_l)
                         .set_color(col).set_stroke(width=1.5))
                if len(pts_r) > 2:
                    grp.add(VMobject().set_points_smoothly(pts_r)
                             .set_color(col).set_stroke(width=1.5))
            return grp

        self.add(always_redraw(input_circles), always_redraw(radial_lines))

        # Pole marker at z=1
        self.add(Dot(left.n2p(1 + 0j), color=RED, radius=0.1))
        self.add(Tex(r"pole $z=1$", color=RED,
                     font_size=20).next_to(left.n2p(1 + 0j), UP, buff=0.15))

        info = VGroup(
            VGroup(Tex(r"morph $t=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"pole $z=1\to \infty$",
                color=RED, font_size=20),
            Tex(r"$z=-1\to 0$ (fixed zero)",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3).shift(LEFT * 3)
        info[0][1].add_updater(lambda m: m.set_value(t_tr.get_value()))
        self.add(info)

        self.play(t_tr.animate.set_value(1.0),
                  run_time=4, rate_func=smooth)
        self.wait(0.8)
        self.play(t_tr.animate.set_value(0.0),
                  run_time=2.5, rate_func=smooth)
        self.wait(0.5)
