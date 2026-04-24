from manim import *
import numpy as np


class BlobGridSquaresDetExample(Scene):
    """
    Cover a blob with a grid of small squares of side ε. After
    transforming, each square scales by |det|. Total = |det| · blob_area.
    Take ε → 0 to see that continuous blob area also scales by |det|.

    ValueTracker eps_tr shrinks square size from 0.5 → 0.1. Number
    of squares grows, visual approximation to blob area improves.
    """

    def construct(self):
        title = Tex(r"Blob $\approx$ sum of squares; each scales by $|\det A|$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-1, 6, 1], y_range=[-1, 5, 1],
                            x_length=9, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        # Blob shape (teardrop-like, irregular)
        np.random.seed(3)
        blob_center = np.array([2.0, 2.0])
        blob_pts = []
        for theta in np.linspace(0, TAU, 80, endpoint=False):
            r = 1.2 + 0.3 * np.sin(2 * theta) + 0.15 * np.cos(4 * theta)
            blob_pts.append(blob_center + np.array([r * np.cos(theta),
                                                     r * np.sin(theta)]))

        A = np.array([[1.0, -1.0], [0.5, 1.0]])
        eps_tr = ValueTracker(0.5)

        def inside_blob(pt):
            # Simple angular check: compare distance to center vs blob at that angle
            d = pt - blob_center
            theta = np.arctan2(d[1], d[0])
            r = 1.2 + 0.3 * np.sin(2 * theta) + 0.15 * np.cos(4 * theta)
            return np.linalg.norm(d) < r

        def blob_polygon():
            M = A  # fully applied in RIGHT side only
            pts_left = [plane.c2p(*p) for p in blob_pts]
            return Polygon(*pts_left, color=BLUE, stroke_width=3,
                            fill_color=BLUE, fill_opacity=0.25)

        def squares():
            eps = eps_tr.get_value()
            grp = VGroup()
            xs = np.arange(0.2, 4.2, eps)
            ys = np.arange(0.2, 4.0, eps)
            for x in xs:
                for y in ys:
                    pt = np.array([x + eps / 2, y + eps / 2])
                    if inside_blob(pt):
                        corners = [np.array([x, y]),
                                   np.array([x + eps, y]),
                                   np.array([x + eps, y + eps]),
                                   np.array([x, y + eps])]
                        poly_pts = [plane.c2p(*c) for c in corners]
                        grp.add(Polygon(*poly_pts, color=YELLOW,
                                         stroke_width=0.5,
                                         fill_color=YELLOW,
                                         fill_opacity=0.45))
            return grp

        self.add(blob_polygon(), always_redraw(squares))

        def n_squares():
            eps = eps_tr.get_value()
            cnt = 0
            xs = np.arange(0.2, 4.2, eps)
            ys = np.arange(0.2, 4.0, eps)
            for x in xs:
                for y in ys:
                    pt = np.array([x + eps / 2, y + eps / 2])
                    if inside_blob(pt):
                        cnt += 1
            return cnt

        info = VGroup(
            VGroup(Tex(r"$\varepsilon=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$N$ squares $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"approx area $=N\varepsilon^2\approx$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"each $\varepsilon^2$ square $\to |\det A|\cdot\varepsilon^2$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(eps_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(n_squares()))
        info[2][1].add_updater(lambda m: m.set_value(n_squares() * eps_tr.get_value() ** 2))
        self.add(info)

        for eps_val in [0.3, 0.18, 0.1]:
            self.play(eps_tr.animate.set_value(eps_val),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
