from manim import *
import numpy as np


class EulersFormulaCubeExample(Scene):
    """
    Euler's formula V - E + F = 2 built up incrementally.

    TWO_COLUMN:
      LEFT  — a 3D cube wireframe is constructed in stages: vertices
              first (8 of them), then edges (12, animated in batches),
              then "faces" highlighted by colored polygons (6 of them).
      RIGHT — running counters V, E, F, and the live invariant V - E + F.

    The right-side V - E + F counter never drops to weird intermediate
    values — we only display it once a stage completes — and locks at 2
    by the end. Tex used for math symbols.
    """

    def construct(self):
        title = Tex(r"Euler's formula on a cube: $V - E + F = 2$",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Use 3D cube projected to 2D ("isometric-ish")
        # Front-face square + back-face square offset by (0.7, 0.5)
        offs = np.array([1.0, 0.7, 0])
        front = [
            np.array([-1.5, -1.5, 0]),
            np.array([+1.5, -1.5, 0]),
            np.array([+1.5, +1.5, 0]),
            np.array([-1.5, +1.5, 0]),
        ]
        back = [p + offs for p in front]
        verts = front + back  # 8 vertices total

        anchor = np.array([-3.4, -0.4, 0])
        verts_world = [v + anchor for v in verts]

        edge_pairs = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # front face
            (4, 5), (5, 6), (6, 7), (7, 4),  # back face
            (0, 4), (1, 5), (2, 6), (3, 7),  # connectors
        ]

        face_specs = [
            (front, BLUE_E, "front"),
            (back, GREEN_E, "back"),
            ([front[0], front[1], back[1], back[0]], YELLOW_E, "bottom"),
            ([front[2], front[3], back[3], back[2]], ORANGE, "top"),
            ([front[1], front[2], back[2], back[1]], RED_E, "right"),
            ([front[0], front[3], back[3], back[0]], PURPLE, "left"),
        ]

        # RIGHT COLUMN counters (these are mutated as stages complete)
        rcol_x = +3.6
        V_count = ValueTracker(0)
        E_count = ValueTracker(0)
        F_count = ValueTracker(0)

        def info_panel():
            v = int(round(V_count.get_value()))
            e = int(round(E_count.get_value()))
            f = int(round(F_count.get_value()))
            return VGroup(
                MathTex(rf"V = {v}", color=YELLOW, font_size=32),
                MathTex(rf"E = {e}", color=BLUE, font_size=32),
                MathTex(rf"F = {f}", color=GREEN, font_size=32),
                MathTex(rf"V - E + F = {v - e + f}",
                        color=ORANGE, font_size=36),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(info_panel))

        # Stage 1: drop in vertices
        vertex_dots = VGroup(*[
            Dot(v, color=YELLOW, radius=0.10) for v in verts_world
        ])
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in vertex_dots],
                              lag_ratio=0.12), V_count.animate.set_value(8),
                  run_time=2.5)
        self.wait(0.4)

        # Stage 2: build edges, in three groups (front, back, connectors)
        edge_lines = []
        for (i, j) in edge_pairs:
            edge_lines.append(Line(verts_world[i], verts_world[j],
                                    color=BLUE, stroke_width=3))
        edge_groups = [edge_lines[:4], edge_lines[4:8], edge_lines[8:12]]
        cumulative_E = 0
        for grp in edge_groups:
            cumulative_E += len(grp)
            self.play(LaggedStart(*[Create(e) for e in grp], lag_ratio=0.15),
                      E_count.animate.set_value(cumulative_E),
                      run_time=1.6)
            self.wait(0.25)

        # Stage 3: light up the faces
        for f_pts, f_color, _ in face_specs:
            face = Polygon(*f_pts, color=f_color, fill_color=f_color,
                           fill_opacity=0.35, stroke_width=2)
            face.shift(anchor)
            self.play(FadeIn(face),
                      F_count.animate.increment_value(1),
                      run_time=0.55)

        self.wait(0.5)

        conclusion = Tex(r"$V - E + F = 8 - 12 + 6 = 2$",
                         font_size=32, color=ORANGE).move_to([rcol_x, -3.0, 0])
        self.play(Write(conclusion))
        self.wait(1.0)
