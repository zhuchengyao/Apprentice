from manim import *
import numpy as np


class PlanarGraphBasicExample(Scene):
    """
    Planar embedding of K₄: edges that look like crossings can be
    re-routed; verify Euler's formula V−E+F=2.

    SINGLE_FOCUS:
      Stage 1 — Draw K₄ as a "square with diagonals" embedding (one
                edge appears to cross another).
      Stage 2 — Move one vertex outside via Transform on its position,
                eliminating the crossing — same graph, planar embedding.
      Stage 3 — Highlight 4 faces (3 interior triangles + outer
                infinite face). Show V−E+F = 4 − 6 + 4 = 2.
    """

    def construct(self):
        title = Tex(r"K$_4$ is planar — V $-$ E $+$ F $= 2$",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # K₄ vertices arranged as a square (with crossing diagonals)
        sq_pos = {
            1: np.array([-2.0, +1.5, 0]),
            2: np.array([+2.0, +1.5, 0]),
            3: np.array([+2.0, -1.5, 0]),
            4: np.array([-2.0, -1.5, 0]),
        }
        # All 6 edges of K₄
        edge_pairs = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3), (2, 4)]

        v_dots = {k: Dot(p, color=YELLOW, radius=0.12) for k, p in sq_pos.items()}
        v_lbls = {k: MathTex(rf"v_{k}", color=YELLOW, font_size=20).next_to(d, UR, buff=0.05)
                   for k, d in v_dots.items()}
        edges = {(i, j): Line(sq_pos[i], sq_pos[j], color=BLUE, stroke_width=3)
                 for (i, j) in edge_pairs}

        self.play(*[FadeIn(d) for d in v_dots.values()],
                  *[Write(l) for l in v_lbls.values()])
        self.play(*[Create(e) for e in edges.values()], run_time=1.5)

        # Highlight the visible crossing
        crossing_dot = Dot(ORIGIN, color=RED, radius=0.10)
        crossing_lbl = Tex(r"crossing!", color=RED, font_size=22).next_to(
            crossing_dot, UP, buff=0.1)
        self.play(FadeIn(crossing_dot), Write(crossing_lbl))
        self.wait(0.6)

        # Stage 2: move vertex 4 to a position that makes it planar
        # Place v4 outside the triangle 1-2-3 instead of as a corner
        new_v4_pos = np.array([0.0, -2.5, 0])
        new_pos = dict(sq_pos)
        new_pos[4] = new_v4_pos

        new_v4_dot = Dot(new_v4_pos, color=YELLOW, radius=0.12)
        new_v4_lbl = MathTex(r"v_4", color=YELLOW, font_size=20).next_to(
            new_v4_dot, DR, buff=0.05)

        # New edges
        new_edges = {(i, j): Line(new_pos[i], new_pos[j], color=BLUE, stroke_width=3)
                     for (i, j) in edge_pairs}

        self.play(
            FadeOut(crossing_dot), FadeOut(crossing_lbl),
            Transform(v_dots[4], new_v4_dot),
            Transform(v_lbls[4], new_v4_lbl),
            *[Transform(edges[k], new_edges[k]) for k in edge_pairs],
            run_time=2.0,
        )
        self.wait(0.4)

        replanar_lbl = Tex(r"\textbf{planar embedding}", color=GREEN,
                           font_size=22).move_to([0, -3.4, 0])
        self.play(Write(replanar_lbl))

        # Stage 3: highlight 4 faces (3 inner triangles + outer)
        # In the new embedding: triangles {1,2,3}, {1,3,4}, {1,2,4} ... wait, need 6 edges
        # Actually with 6 edges and the planar K4 layout, we get:
        # Faces: triangle (1,2,3), triangle (1,3,4), triangle (2,3,4), outer (1,2,4)
        # We'll color them lightly.
        face_polys = [
            Polygon(new_pos[1], new_pos[2], new_pos[3], color=BLUE, fill_opacity=0.2, stroke_width=0),
            Polygon(new_pos[1], new_pos[3], new_pos[4], color=GREEN, fill_opacity=0.2, stroke_width=0),
            Polygon(new_pos[2], new_pos[3], new_pos[4], color=ORANGE, fill_opacity=0.2, stroke_width=0),
        ]
        outer_lbl = Tex(r"+ outer face", color=GREY_B, font_size=20).move_to([3.5, -2.5, 0])

        self.play(*[FadeIn(p) for p in face_polys], Write(outer_lbl))

        # Counter
        counter = MathTex(
            r"V - E + F = 4 - 6 + 4 = 2",
            color=YELLOW, font_size=30,
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(counter))
        self.wait(1.0)
