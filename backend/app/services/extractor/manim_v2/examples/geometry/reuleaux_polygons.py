from manim import *
import numpy as np


class ReuleauxPolygonsExample(Scene):
    """
    Reuleaux polygons have constant width. Odd-sided regular
    polygons inscribed in equilateral k-gons with arcs from each
    vertex of radius = side length.

    SINGLE_FOCUS: ValueTracker k_tr ∈ {3, 5, 7, 9} morphs between
    Reuleaux triangle, pentagon, heptagon, nonagon. always_redraw
    rebuilds the curve of constant width + rotating calipers
    confirming width is invariant.
    """

    def construct(self):
        title = Tex(r"Reuleaux polygons: constant-width curves (odd $k$)",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        k_tr = ValueTracker(3.0)
        theta_tr = ValueTracker(0.0)
        R = 1.6

        def reuleaux_arcs():
            k = int(round(k_tr.get_value()))
            k = max(3, min(9, 2 * (k // 2) + 1))  # ensure odd
            # Vertices of regular k-gon on unit circle radius R (centered at origin)
            verts = [R * np.array([np.cos(2 * PI * j / k - PI / 2), np.sin(2 * PI * j / k - PI / 2), 0])
                     for j in range(k)]
            s = np.linalg.norm(verts[0] - verts[(k + 1) // 2])
            grp = VGroup()
            for j in range(k):
                # arc centered at vertex j, connecting the two vertices "opposite"
                center = verts[j]
                # far vertices from j
                v1 = verts[(j + (k - 1) // 2) % k]
                v2 = verts[(j + (k + 1) // 2) % k]
                a1 = np.arctan2(v1[1] - center[1], v1[0] - center[0])
                a2 = np.arctan2(v2[1] - center[1], v2[0] - center[0])
                # choose the short arc between a1 and a2
                diff = a2 - a1
                while diff > PI: diff -= 2 * PI
                while diff < -PI: diff += 2 * PI
                pts = []
                for t in np.linspace(0, 1, 30):
                    ang = a1 + t * diff
                    pts.append(center + s * np.array([np.cos(ang), np.sin(ang), 0]))
                grp.add(VMobject().set_points_as_corners(pts)
                         .set_color(YELLOW).set_stroke(width=3))
            return grp

        def verts_dots():
            k = int(round(k_tr.get_value()))
            k = max(3, min(9, 2 * (k // 2) + 1))
            verts = [R * np.array([np.cos(2 * PI * j / k - PI / 2), np.sin(2 * PI * j / k - PI / 2), 0])
                     for j in range(k)]
            return VGroup(*[Dot(v, color=BLUE, radius=0.08) for v in verts])

        # Compute support width for a given direction
        def support_in_dir(theta, k):
            k = max(3, min(9, 2 * (k // 2) + 1))
            verts = [R * np.array([np.cos(2 * PI * j / k - PI / 2), np.sin(2 * PI * j / k - PI / 2), 0])
                     for j in range(k)]
            s = np.linalg.norm(verts[0] - verts[(k + 1) // 2])
            # Sample curve
            pts = []
            for j in range(k):
                center = verts[j]
                v1 = verts[(j + (k - 1) // 2) % k]
                v2 = verts[(j + (k + 1) // 2) % k]
                a1 = np.arctan2(v1[1] - center[1], v1[0] - center[0])
                a2 = np.arctan2(v2[1] - center[1], v2[0] - center[0])
                diff = a2 - a1
                while diff > PI: diff -= 2 * PI
                while diff < -PI: diff += 2 * PI
                for t in np.linspace(0, 1, 30):
                    ang = a1 + t * diff
                    pts.append(center + s * np.array([np.cos(ang), np.sin(ang), 0]))
            proj_vals = [p[0] * np.cos(theta) + p[1] * np.sin(theta) for p in pts]
            return max(proj_vals) - min(proj_vals), s

        def calipers():
            theta = theta_tr.get_value()
            k = int(round(k_tr.get_value()))
            width, _ = support_in_dir(theta, k)
            # Two parallel lines perpendicular to direction theta
            dir_vec = np.array([np.cos(theta), np.sin(theta), 0])
            perp = np.array([-np.sin(theta), np.cos(theta), 0])
            # Find points on curve with max and min projections
            return VGroup(
                DashedLine(-dir_vec * 5 + perp * 4,
                            -dir_vec * 5 - perp * 4, color=GREEN, stroke_width=1),
                # Approximate caliper pair
                Line(dir_vec * (width / 2) + perp * 3,
                      dir_vec * (width / 2) - perp * 3,
                      color=ORANGE, stroke_width=3),
                Line(-dir_vec * (width / 2) + perp * 3,
                      -dir_vec * (width / 2) - perp * 3,
                      color=ORANGE, stroke_width=3),
            )

        self.add(always_redraw(reuleaux_arcs), always_redraw(verts_dots),
                 always_redraw(calipers))

        # Info
        def k_now():
            k = int(round(k_tr.get_value()))
            return max(3, min(9, 2 * (k // 2) + 1))

        def width_now():
            w, s = support_in_dir(theta_tr.get_value(), k_now())
            return w

        info = VGroup(
            VGroup(Tex(r"$k=$", font_size=22),
                   DecimalNumber(3, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\theta=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"width $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"width constant across $\theta$",
                color=YELLOW, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(k_now()))
        info[1][1].add_updater(lambda m: m.set_value(theta_tr.get_value()))
        info[2][1].add_updater(lambda m: m.set_value(width_now()))
        self.add(info)

        self.play(theta_tr.animate.set_value(TAU),
                  run_time=4, rate_func=linear)
        self.wait(0.4)

        for kval in [5, 7, 9, 3]:
            self.play(k_tr.animate.set_value(float(kval)), run_time=1.0)
            self.play(theta_tr.animate.set_value(theta_tr.get_value() + TAU),
                      run_time=3, rate_func=linear)
            self.wait(0.3)
        self.wait(0.5)
