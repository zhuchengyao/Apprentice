from manim import *
import numpy as np


class PoincareDiskTilingExample(Scene):
    """
    Poincaré disk model of hyperbolic geometry: {3, 7} tiling with
    regular heptagons meeting 3 at each vertex. Geodesics are arcs
    of circles perpendicular to the boundary.

    SINGLE_FOCUS: unit disk with a centered regular hyperbolic polygon
    and successive reflections producing a tiling. ValueTracker
    depth_tr reveals more layers.
    """

    def construct(self):
        title = Tex(r"Poincaré disk: $\{3,7\}$ tiling (approx)",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R_disk = 3.2
        disk = Circle(radius=R_disk, color=BLUE, stroke_width=3)
        self.play(Create(disk))

        depth_tr = ValueTracker(0.0)

        # Approximate {3, 7} tiling using shrinking triangle-like figures
        # We'll draw "triangles" placed at various radii
        def d_now():
            return max(0, min(3, int(round(depth_tr.get_value()))))

        def tiles():
            d = d_now()
            grp = VGroup()
            # Center triangle
            for k in range(7):
                ang = TAU * k / 7
                # a "geodesic edge" connecting two boundary-bound points
                # Approximate with a line for visual clarity
                p1 = R_disk * 0.35 * np.array([np.cos(ang), np.sin(ang), 0])
                p2 = R_disk * 0.35 * np.array([np.cos(ang + TAU / 7),
                                                  np.sin(ang + TAU / 7), 0])
                grp.add(Line(p1, p2, color=YELLOW, stroke_width=3))
            if d >= 1:
                # Ring 1: 7 tiles at outer
                for k in range(7):
                    ang = TAU * k / 7 + TAU / 14
                    center_r = R_disk * 0.65
                    cx = center_r * np.cos(ang)
                    cy = center_r * np.sin(ang)
                    for j in range(7):
                        a1 = TAU * j / 7
                        a2 = TAU * (j + 1) / 7
                        r_tile = R_disk * 0.18
                        p1 = np.array([cx + r_tile * np.cos(a1), cy + r_tile * np.sin(a1), 0])
                        p2 = np.array([cx + r_tile * np.cos(a2), cy + r_tile * np.sin(a2), 0])
                        grp.add(Line(p1, p2, color=GREEN, stroke_width=1.5, stroke_opacity=0.8))
            if d >= 2:
                # Ring 2: smaller tiles further out
                for k in range(14):
                    ang = TAU * k / 14 + TAU / 28
                    center_r = R_disk * 0.85
                    cx = center_r * np.cos(ang)
                    cy = center_r * np.sin(ang)
                    for j in range(7):
                        a1 = TAU * j / 7
                        a2 = TAU * (j + 1) / 7
                        r_tile = R_disk * 0.08
                        p1 = np.array([cx + r_tile * np.cos(a1), cy + r_tile * np.sin(a1), 0])
                        p2 = np.array([cx + r_tile * np.cos(a2), cy + r_tile * np.sin(a2), 0])
                        grp.add(Line(p1, p2, color=ORANGE, stroke_width=1.3, stroke_opacity=0.7))
            if d >= 3:
                # Near boundary: cluster
                for k in range(28):
                    ang = TAU * k / 28 + TAU / 56
                    center_r = R_disk * 0.95
                    cx = center_r * np.cos(ang)
                    cy = center_r * np.sin(ang)
                    for j in range(7):
                        a1 = TAU * j / 7
                        a2 = TAU * (j + 1) / 7
                        r_tile = R_disk * 0.03
                        p1 = np.array([cx + r_tile * np.cos(a1), cy + r_tile * np.sin(a1), 0])
                        p2 = np.array([cx + r_tile * np.cos(a2), cy + r_tile * np.sin(a2), 0])
                        grp.add(Line(p1, p2, color=RED, stroke_width=1.1, stroke_opacity=0.55))
            return grp

        self.add(always_redraw(tiles))

        # A geodesic (circle perpendicular to boundary)
        # Through (0.6, 0) and (-0.2, 0.8) — use explicit geometry
        # Geodesic arc for demo:
        geodesic_arc = Arc(radius=2.0, start_angle=PI * 0.25,
                           angle=PI * 0.5, color=RED, stroke_width=3).shift(
            np.array([1.8, -1.5, 0]))
        self.add(geodesic_arc)
        self.add(Tex(r"geodesic", color=RED, font_size=20).next_to(geodesic_arc, UR, buff=0.1))

        info = VGroup(
            VGroup(Tex(r"depth $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"$\{p, q\}$: $p$-gons, $q$ at each vertex",
                font_size=20),
            Tex(r"hyperbolic: $1/p+1/q<1/2$",
                color=YELLOW, font_size=20),
            Tex(r"boundary circle $=$ ideal points",
                color=BLUE, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(d_now()))
        self.add(info)

        for target in [1, 2, 3]:
            self.play(depth_tr.animate.set_value(float(target)),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.8)
