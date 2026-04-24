from manim import *
import numpy as np


class SchwarzChristoffelMapExample(Scene):
    """
    Schwarz-Christoffel maps the upper half-plane to a polygon.
    For a rectangle with corners at ±K, ±K + iK', the map is
    f(z) = ∫_0^z dt / √((1-t²)(1-k²t²))  (incomplete elliptic).

    Simplified demo: upper half-plane z = x + iy (y > 0) → interior
    of a square. Use Möbius approximation z ↦ z/(1 + i z) + tweak.

    Actually show classical SC with 3 corners mapped to equilateral
    triangle: f(z) = ∫_0^z t^{-2/3}(1-t)^{-2/3} dt.
    """

    def construct(self):
        title = Tex(r"Schwarz-Christoffel: upper half-plane $\to$ triangle",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-2, 2, 1], y_range=[0, 2, 1],
                            x_length=4.5, y_length=2.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.2 + UP * 0.2)
        right = ComplexPlane(x_range=[-2, 2, 1], y_range=[-1, 2, 1],
                             x_length=4.8, y_length=3.5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).shift(RIGHT * 2.5 + DOWN * 0.4)
        self.play(Create(left), Create(right))

        # Real axis highlighted
        real_line = Line(left.n2p(-2, 0), left.n2p(2, 0),
                          color=RED, stroke_width=3)
        self.add(real_line)

        # Corners at z = 0, 1 (+ ∞): maps to vertices of equilateral triangle
        A_z = Dot(left.n2p(0, 0), color=GREEN, radius=0.1)
        B_z = Dot(left.n2p(1, 0), color=ORANGE, radius=0.1)
        self.add(A_z, B_z)

        # Numerical SC: f(z) = ∫_0^z s^(-2/3) (1-s)^(-2/3) ds
        # For simplicity, precompute the triangle image
        def sc_map(z):
            # numerically integrate from 0 to z along straight line
            # avoid singularities at 0 and 1
            N = 200
            eps = 1e-3
            if abs(z) < 1e-6:
                return 0 + 0j
            ss = np.linspace(0, 1, N)
            path = [eps + s * (z - eps) for s in ss]
            ds = path[1] - path[0]
            total = 0 + 0j
            for p in path:
                if abs(p) < 1e-6 or abs(p - 1) < 1e-6:
                    continue
                integrand = (p ** (-2 / 3)) * ((1 - p) ** (-2 / 3))
                total += integrand * ds
            return total

        # Draw images of horizontal lines on upper half
        grid_lines = VGroup()
        image_lines = VGroup()
        for y0 in [0.1, 0.4, 0.8, 1.3]:
            pts_z = [left.n2p(x, y0) for x in np.linspace(-1.5, 1.5, 30)]
            grid_lines.add(VMobject().set_points_as_corners(pts_z)
                            .set_color(GREY_B).set_stroke(width=1.5, opacity=0.7))
            pts_w = []
            for x in np.linspace(-1.5, 1.5, 30):
                w = sc_map(complex(x, y0))
                pts_w.append(right.n2p(complex(w.real, w.imag)))
            image_lines.add(VMobject().set_points_as_corners(pts_w)
                             .set_color(interpolate_color(BLUE, YELLOW, y0 / 1.5))
                             .set_stroke(width=2))

        self.add(grid_lines)
        self.play(Create(image_lines), run_time=3)

        # Triangle vertices on right
        v_A = sc_map(complex(1e-3, 0))  # z=0+ → triangle corner
        v_B = sc_map(complex(1, 1e-3))  # z=1
        v_C = sc_map(complex(5, 0.1))   # z=∞ approximation

        self.add(Dot(right.n2p(complex(v_A.real, v_A.imag)), color=GREEN, radius=0.12))
        self.add(Dot(right.n2p(complex(v_B.real, v_B.imag)), color=ORANGE, radius=0.12))

        # Probe dot mapping
        t_tr = ValueTracker(-1.5)

        def probe_left():
            t = t_tr.get_value()
            return Dot(left.n2p(t, 0.3), color=YELLOW, radius=0.1)

        def probe_right():
            t = t_tr.get_value()
            w = sc_map(complex(t, 0.3))
            return Dot(right.n2p(complex(w.real, w.imag)),
                        color=YELLOW, radius=0.1)

        self.add(always_redraw(probe_left), always_redraw(probe_right))

        info = VGroup(
            Tex(r"$f'(z)=z^{-2/3}(1-z)^{-2/3}$",
                font_size=22),
            Tex(r"corners at $z=0,1,\infty$",
                color=GREY_B, font_size=20),
            Tex(r"maps upper half $\to$ equilateral triangle",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3).shift(LEFT * 2)
        self.add(info)

        self.play(t_tr.animate.set_value(1.5),
                  run_time=6, rate_func=linear)
        self.wait(0.5)
