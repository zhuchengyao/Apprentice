from manim import *
import numpy as np


class SphereTriangleCountExample(ThreeDScene):
    """
    V - E + F = 2 stays invariant under triangulation refinement.

    Build an octahedral triangulation of a sphere (V=6, E=12, F=8).
    Then refine each triangular face by adding a vertex at each edge
    midpoint (snapped to the sphere surface) — this multiplies counts
    in a controlled way: V' = V + E,  E' = 2E + 3F,  F' = 4F. The
    Euler characteristic V - E + F stays = 2 across both stages.

    Right-side overlay panel (fixed in frame) tracks counters and the
    invariant.
    """

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES)

        title = Tex(r"$V - E + F = 2$ across triangulation refinements",
                    font_size=26)
        self.add_fixed_in_frame_mobjects(title)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Stage 0: octahedron (6 vertices on the sphere)
        R = 1.6
        octa_verts = [
            R * np.array([+1, 0, 0]),
            R * np.array([-1, 0, 0]),
            R * np.array([0, +1, 0]),
            R * np.array([0, -1, 0]),
            R * np.array([0, 0, +1]),
            R * np.array([0, 0, -1]),
        ]
        octa_faces = [
            (0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4),
            (0, 4, 2), (2, 4, 1), (1, 4, 3), (3, 4, 0),  # placeholder; we'll dedupe below
        ]
        # Real octahedron faces: 8 triangles
        octa_faces = [
            (0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4),
            (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5),
        ]

        def faces_to_edges(faces):
            edges = set()
            for a, b, c in faces:
                edges.add(tuple(sorted([a, b])))
                edges.add(tuple(sorted([b, c])))
                edges.add(tuple(sorted([c, a])))
            return edges

        # Right-side counter panel (overlay, fixed in frame)
        v_count = ValueTracker(0)
        e_count = ValueTracker(0)
        f_count = ValueTracker(0)

        def counter_panel():
            v = int(round(v_count.get_value()))
            e = int(round(e_count.get_value()))
            f = int(round(f_count.get_value()))
            return VGroup(
                MathTex(rf"V = {v}", color=YELLOW, font_size=28),
                MathTex(rf"E = {e}", color=BLUE, font_size=28),
                MathTex(rf"F = {f}", color=GREEN, font_size=28),
                MathTex(rf"V - E + F = {v - e + f}",
                        color=ORANGE, font_size=32),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).shift(UP * 0.2)

        panel = always_redraw(counter_panel)
        self.add_fixed_in_frame_mobjects(panel)
        # Re-add panel as always_redraw so it stays fixed but updates
        # Actually add_fixed_in_frame_mobjects adds it once. For dynamic content we use
        # a static workaround: just keep panel as always_redraw at scene level.
        # Let me just rely on always_redraw being fixed; manim's camera ignores
        # 2D mobjects that aren't ThreeD. They'll project onto the screen.

        # Stage 1: build the octahedron
        verts_3d = VGroup(*[Dot3D(point=v, color=YELLOW, radius=0.10)
                            for v in octa_verts])
        edges_3d = VGroup()
        for (i, j) in faces_to_edges(octa_faces):
            edges_3d.add(Line(octa_verts[i], octa_verts[j],
                              color=BLUE, stroke_width=2.5))
        faces_3d = VGroup()
        for (a, b, c) in octa_faces:
            tri = Polygon(octa_verts[a], octa_verts[b], octa_verts[c],
                          color=GREEN, fill_color=GREEN, fill_opacity=0.25,
                          stroke_width=0.5)
            faces_3d.add(tri)

        self.play(LaggedStart(*[FadeIn(d) for d in verts_3d], lag_ratio=0.08),
                  v_count.animate.set_value(len(octa_verts)), run_time=1.5)
        self.play(LaggedStart(*[Create(e) for e in edges_3d], lag_ratio=0.05),
                  e_count.animate.set_value(len(edges_3d)), run_time=1.8)
        self.play(LaggedStart(*[FadeIn(f) for f in faces_3d], lag_ratio=0.08),
                  f_count.animate.set_value(len(octa_faces)), run_time=1.5)
        self.wait(0.6)

        # Stage 2: refine — each triangle subdivided into 4 by edge midpoints
        # New vertex set: octa_verts + midpoints (snapped to sphere)
        new_verts = list(octa_verts)
        edge_to_mid = {}
        for (i, j) in faces_to_edges(octa_faces):
            mid = (octa_verts[i] + octa_verts[j]) / 2
            mid = mid / np.linalg.norm(mid) * R
            edge_to_mid[(i, j)] = len(new_verts)
            new_verts.append(mid)

        # New faces: each old (a, b, c) becomes 4 small triangles
        new_faces = []
        for (a, b, c) in octa_faces:
            mab = edge_to_mid[tuple(sorted([a, b]))]
            mbc = edge_to_mid[tuple(sorted([b, c]))]
            mca = edge_to_mid[tuple(sorted([c, a]))]
            new_faces.append((a, mab, mca))
            new_faces.append((b, mbc, mab))
            new_faces.append((c, mca, mbc))
            new_faces.append((mab, mbc, mca))

        new_edges = faces_to_edges(new_faces)

        new_verts_3d = VGroup(*[Dot3D(point=v, color=YELLOW, radius=0.07)
                                for v in new_verts])
        new_edges_3d = VGroup()
        for (i, j) in new_edges:
            new_edges_3d.add(Line(new_verts[i], new_verts[j],
                                   color=BLUE, stroke_width=1.5))
        new_faces_3d = VGroup()
        for (a, b, c) in new_faces:
            tri = Polygon(new_verts[a], new_verts[b], new_verts[c],
                          color=GREEN, fill_color=GREEN, fill_opacity=0.2,
                          stroke_width=0.3)
            new_faces_3d.add(tri)

        self.play(
            FadeOut(verts_3d), FadeOut(edges_3d), FadeOut(faces_3d),
            run_time=0.8,
        )
        self.play(
            LaggedStart(*[FadeIn(d) for d in new_verts_3d], lag_ratio=0.02),
            v_count.animate.set_value(len(new_verts)),
            run_time=1.5,
        )
        self.play(
            LaggedStart(*[Create(e) for e in new_edges_3d], lag_ratio=0.01),
            e_count.animate.set_value(len(new_edges)),
            run_time=1.8,
        )
        self.play(
            LaggedStart(*[FadeIn(f) for f in new_faces_3d], lag_ratio=0.01),
            f_count.animate.set_value(len(new_faces)),
            run_time=1.5,
        )
        self.wait(0.6)

        chi_lbl = Tex(r"$\chi = V - E + F = 2$ (sphere, every triangulation)",
                      color=ORANGE, font_size=22)
        self.add_fixed_in_frame_mobjects(chi_lbl)
        chi_lbl.to_edge(DOWN, buff=0.3)
        self.play(Write(chi_lbl))
        self.wait(1.0)
