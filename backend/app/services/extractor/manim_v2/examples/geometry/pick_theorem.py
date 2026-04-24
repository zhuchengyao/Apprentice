from manim import *
import numpy as np


class PickTheoremExample(Scene):
    """
    Pick's theorem: area of a lattice polygon is A = I + B/2 - 1,
    where I is # interior lattice points and B is # boundary lattice
    points.

    SINGLE_FOCUS:
      Lattice grid with a polygon; ValueTracker v_tr slides one
      vertex through several positions; always_redraw highlights I
      (green) and B (red) lattice points, panel shows formula check.
    """

    def construct(self):
        title = Tex(r"Pick's theorem: $A = I + B/2 - 1$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                             x_length=8, y_length=6,
                             background_line_style={"stroke_opacity": 0.4}
                             ).move_to([-1, -0.3, 0])
        self.play(Create(plane))

        # Lattice dots
        lattice = VGroup()
        for xv in range(-4, 5):
            for yv in range(-3, 4):
                lattice.add(Dot(plane.c2p(xv, yv), color=GREY_B, radius=0.05))
        self.play(FadeIn(lattice))

        # Polygon with 5 vertices, 4 fixed, 1 variable
        fixed = [np.array([0, 0, 0]),
                 np.array([3, 0, 0]),
                 np.array([3, 2, 0]),
                 np.array([1, 2, 0])]
        vx_tr = ValueTracker(0.0)
        # Variable vertex at (vx, 3)

        def poly_verts():
            vx = int(round(vx_tr.get_value()))
            vx = max(-1, min(vx, 2))
            return fixed + [np.array([vx, 3, 0])]

        def poly_shape():
            verts = poly_verts()
            scene_pts = [plane.c2p(v[0], v[1]) for v in verts]
            return Polygon(*scene_pts, color=YELLOW,
                             fill_opacity=0.35, stroke_width=3)

        def point_in_polygon(px, py, poly_verts_xy):
            """Ray casting."""
            n = len(poly_verts_xy)
            inside = False
            j = n - 1
            for i in range(n):
                xi, yi = poly_verts_xy[i]
                xj, yj = poly_verts_xy[j]
                if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi + 1e-12) + xi):
                    inside = not inside
                j = i
            return inside

        def on_segment(px, py, sx, sy, tx, ty):
            """Is (px, py) on segment from (sx, sy) to (tx, ty)?"""
            # Cross product ≈ 0 and between endpoints
            cross = (tx - sx) * (py - sy) - (ty - sy) * (px - sx)
            if abs(cross) > 1e-6:
                return False
            dot = (px - sx) * (tx - sx) + (py - sy) * (ty - sy)
            len_sq = (tx - sx) ** 2 + (ty - sy) ** 2
            return 0 <= dot <= len_sq + 1e-6

        def classify_lattice():
            """Return (boundary_count, interior_count, boundary_pts, interior_pts)."""
            verts = poly_verts()
            poly_xy = [(v[0], v[1]) for v in verts]
            I_pts, B_pts = [], []
            for xv in range(-4, 5):
                for yv in range(-3, 4):
                    # On boundary?
                    on_b = False
                    for k in range(len(poly_xy)):
                        sx, sy = poly_xy[k]
                        tx, ty = poly_xy[(k + 1) % len(poly_xy)]
                        if on_segment(xv, yv, sx, sy, tx, ty):
                            on_b = True
                            break
                    if on_b:
                        B_pts.append((xv, yv))
                    elif point_in_polygon(xv, yv, poly_xy):
                        I_pts.append((xv, yv))
            return len(B_pts), len(I_pts), B_pts, I_pts

        def highlight_pts():
            _, _, B_pts, I_pts = classify_lattice()
            grp = VGroup()
            for (x, y) in B_pts:
                grp.add(Dot(plane.c2p(x, y), color=RED, radius=0.1))
            for (x, y) in I_pts:
                grp.add(Dot(plane.c2p(x, y), color=GREEN, radius=0.1))
            return grp

        self.add(always_redraw(poly_shape), always_redraw(highlight_pts))

        def shoelace_area(verts_xy):
            n = len(verts_xy)
            area = 0.0
            for i in range(n):
                x1, y1 = verts_xy[i]
                x2, y2 = verts_xy[(i + 1) % n]
                area += x1 * y2 - x2 * y1
            return abs(area) / 2

        def info():
            verts = poly_verts()
            B, I, _, _ = classify_lattice()
            A = shoelace_area([(v[0], v[1]) for v in verts])
            pick = I + B / 2 - 1
            return VGroup(
                MathTex(rf"I = {I}", color=GREEN, font_size=24),
                MathTex(rf"B = {B}", color=RED, font_size=24),
                MathTex(rf"A = {A:.3f}",
                         color=YELLOW, font_size=24),
                MathTex(rf"I + B/2 - 1 = {pick:.3f}",
                         color=YELLOW, font_size=22),
                Tex(rf"match: {abs(A - pick) < 1e-6}",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for vv in [1, 2, -1, 0]:
            self.play(vx_tr.animate.set_value(vv),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
