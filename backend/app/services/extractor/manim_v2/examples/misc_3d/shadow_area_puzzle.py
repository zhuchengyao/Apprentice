from manim import *
import numpy as np


class ShadowAreaPuzzleExample(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES)

        cube = Cube(side_length=1.6, fill_opacity=0.7, stroke_width=1).set_color(BLUE)
        self.play(FadeIn(cube))

        # Shadow on z = -1 plane as a filled polygon based on cube silhouette when rotated
        floor = Surface(
            lambda u, v: np.array([u, v, -1.2]),
            u_range=[-2, 2], v_range=[-2, 2], resolution=(4, 4),
            fill_opacity=0.35, checkerboard_colors=[GREY_C, GREY_D], stroke_width=0.2,
        )
        self.play(FadeIn(floor))

        rotations = [
            np.array([0, 0, 0]),
            np.array([0.6, 0.3, 0]),
            np.array([0.9, 1.1, 0.2]),
            np.array([0.4, -0.7, 0.3]),
        ]
        shadow = None
        for r in rotations:
            cube.generate_target()
            cube.target = Cube(side_length=1.6, fill_opacity=0.7, stroke_width=1).set_color(BLUE)
            cube.target.rotate(r[0], axis=RIGHT).rotate(r[1], axis=UP).rotate(r[2], axis=OUT)

            unit = np.array([[x, y, z] for x in [-0.8, 0.8] for y in [-0.8, 0.8] for z in [-0.8, 0.8]])
            Rx = np.array([[1, 0, 0], [0, np.cos(r[0]), -np.sin(r[0])], [0, np.sin(r[0]), np.cos(r[0])]])
            Ry = np.array([[np.cos(r[1]), 0, np.sin(r[1])], [0, 1, 0], [-np.sin(r[1]), 0, np.cos(r[1])]])
            Rz = np.array([[np.cos(r[2]), -np.sin(r[2]), 0], [np.sin(r[2]), np.cos(r[2]), 0], [0, 0, 1]])
            rotated = unit @ Rx.T @ Ry.T @ Rz.T
            xy = rotated[:, :2]
            hull_pts = _convex_hull(xy)
            hull_3d = [np.array([x, y, -1.15]) for x, y in hull_pts]
            new_shadow = Polygon(*hull_3d, color=BLACK, fill_opacity=0.7, stroke_width=0)

            anims = [MoveToTarget(cube)]
            if shadow is None:
                self.play(*anims, FadeIn(new_shadow), run_time=1.2)
            else:
                self.play(*anims, Transform(shadow, new_shadow), run_time=1.2)
            shadow = new_shadow
            self.wait(0.3)

        label = MathTex(r"\mathbb{E}[\text{shadow area}] = \tfrac{1}{4}\cdot \text{surface area}",
                        font_size=28, color=YELLOW)
        self.add_fixed_in_frame_mobjects(label)
        label.to_edge(DOWN)
        self.play(Write(label))
        self.wait(0.6)


def _convex_hull(points):
    # 2D gift-wrapping (Jarvis march) — returns ordered hull points
    pts = [tuple(p) for p in points]
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts
    start = min(pts, key=lambda p: (p[1], p[0]))
    hull = [start]
    cur = start
    while True:
        nxt = pts[0]
        for p in pts[1:]:
            if p == cur:
                continue
            if nxt == cur:
                nxt = p
                continue
            cross = ((nxt[0] - cur[0]) * (p[1] - cur[1])
                     - (nxt[1] - cur[1]) * (p[0] - cur[0]))
            if cross < 0 or (cross == 0 and
                             ((p[0] - cur[0]) ** 2 + (p[1] - cur[1]) ** 2)
                             > ((nxt[0] - cur[0]) ** 2 + (nxt[1] - cur[1]) ** 2)):
                nxt = p
        cur = nxt
        if cur == start:
            break
        hull.append(cur)
    return hull
