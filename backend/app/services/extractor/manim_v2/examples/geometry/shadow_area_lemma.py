from manim import *
import numpy as np


class ShadowAreaLemmaExample(ThreeDScene):
    """
    Cauchy's surface-area formula: for a convex body, the average
    area of its shadow (over all orientations) equals 1/4 of its
    surface area. Illustrated with a unit cube.

    3D scene:
      Cube with surface area 6 rotates via ValueTracker θ_tr about a
      generic axis. The projected silhouette onto the xy-plane is
      drawn (always_redraw); a running average of silhouette area
      approaches 6/4 = 1.5.
    """

    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=-40 * DEGREES)
        axes = ThreeDAxes(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                           z_range=[-2, 2, 1],
                           x_length=4, y_length=4, z_length=4)
        self.add(axes)

        # Unit cube vertices
        verts = [np.array([sx, sy, sz])
                 for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
        edges_idx = [(i, j) for i in range(8) for j in range(i + 1, 8)
                     if int(np.sum(np.abs(verts[i] - verts[j]))) == 2]

        # Rotation axis: normalized (0.6, 0.7, 0.4)
        axis = np.array([0.6, 0.7, 0.4])
        axis = axis / np.linalg.norm(axis)

        theta_tr = ValueTracker(0.0)

        def rot_pt(v, t):
            k = axis
            return (v * np.cos(t)
                    + np.cross(k, v) * np.sin(t)
                    + k * np.dot(k, v) * (1 - np.cos(t)))

        def cube_mob():
            t = theta_tr.get_value()
            rv = [rot_pt(v, t) for v in verts]
            grp = VGroup()
            for (i, j) in edges_idx:
                grp.add(Line(axes.c2p(*rv[i]), axes.c2p(*rv[j]),
                               color=BLUE_D, stroke_width=3))
            return grp

        def shadow_mob():
            # Projection of cube onto xy-plane (z=-2 for visual offset)
            t = theta_tr.get_value()
            rv = [rot_pt(v, t) for v in verts]
            # Project
            pv = [np.array([r[0], r[1]]) for r in rv]
            # Convex hull of projected points
            try:
                from scipy.spatial import ConvexHull
                hull = ConvexHull(np.array(pv))
                hull_pts = [np.array([pv[i][0], pv[i][1], -2])
                             for i in hull.vertices]
            except Exception:
                # Gift wrapping fallback
                pts = np.array(pv)
                # pick leftmost, walk around
                n = len(pts)
                start = int(np.argmin(pts[:, 0]))
                hull_idx = []
                p = start
                while True:
                    hull_idx.append(p)
                    q = (p + 1) % n
                    for r in range(n):
                        cross = ((pts[q][0] - pts[p][0]) * (pts[r][1] - pts[p][1])
                                  - (pts[q][1] - pts[p][1]) * (pts[r][0] - pts[p][0]))
                        if cross < 0:
                            q = r
                    p = q
                    if p == start:
                        break
                hull_pts = [np.array([pv[i][0], pv[i][1], -2])
                             for i in hull_idx]

            poly = Polygon(*[axes.c2p(*p) for p in hull_pts],
                            color=YELLOW, fill_opacity=0.5,
                            stroke_width=2)
            return poly

        def shadow_area(t):
            rv = [rot_pt(v, t) for v in verts]
            pv = [(r[0], r[1]) for r in rv]
            # Compute hull area via shoelace on gift-wrapped hull
            pts = np.array(pv)
            n = len(pts)
            start = int(np.argmin(pts[:, 0]))
            hull_idx = []
            p = start
            while True:
                hull_idx.append(p)
                q = (p + 1) % n
                for r in range(n):
                    cross = ((pts[q][0] - pts[p][0]) * (pts[r][1] - pts[p][1])
                              - (pts[q][1] - pts[p][1]) * (pts[r][0] - pts[p][0]))
                    if cross < 0:
                        q = r
                p = q
                if p == start:
                    break
            h = [pv[i] for i in hull_idx]
            area = 0.0
            for i in range(len(h)):
                x1, y1 = h[i]
                x2, y2 = h[(i + 1) % len(h)]
                area += x1 * y2 - x2 * y1
            return abs(area) / 2

        self.add(always_redraw(cube_mob), always_redraw(shadow_mob))

        # Precompute running-average area via Riemann sum over θ
        def running_avg(t_cur):
            if t_cur < 0.01:
                return 0.0
            n_samples = 80
            ts = np.linspace(0.001, t_cur, n_samples)
            vals = [shadow_area(t) for t in ts]
            return float(np.mean(vals))

        title = Tex(r"Cauchy's formula: $\overline{\text{shadow area}} = \tfrac{1}{4} \cdot $ surface area",
                    font_size=22).to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        def make_panel():
            t = theta_tr.get_value()
            cur = shadow_area(t) if t > 0.01 else 4.0
            avg = running_avg(t) if t > 0.1 else 0.0
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=WHITE, font_size=22),
                MathTex(rf"\text{{shadow area}} = {cur:.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"\text{{running avg}} = {avg:.3f}",
                         color=GREEN, font_size=22),
                MathTex(r"\text{target} = 6/4 = 1.5",
                         color=BLUE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_corner(DR, buff=0.4)

        panel = make_panel()
        self.add_fixed_in_frame_mobjects(panel)

        self.begin_ambient_camera_rotation(rate=0.1)
        for target in [PI / 2, PI, 3 * PI / 2, 2 * PI, 5 * PI / 2, 3 * PI]:
            self.play(theta_tr.animate.set_value(target),
                       run_time=1.6, rate_func=linear)
            new_panel = make_panel()
            self.add_fixed_in_frame_mobjects(new_panel)
            self.play(Transform(panel, new_panel), run_time=0.25)
        self.stop_ambient_camera_rotation()
        self.wait(0.4)
