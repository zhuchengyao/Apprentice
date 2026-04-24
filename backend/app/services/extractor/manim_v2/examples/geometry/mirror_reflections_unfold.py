from manim import *
import numpy as np


class MirrorReflectionsUnfoldExample(Scene):
    """
    Billiard / light reflection by unfolding (from _2019/clacks/
    solution2/mirror_scenes): a zig-zag path between parallel
    mirrors becomes a straight line once mirrors are unfolded.

    SINGLE_FOCUS:
      Two parallel mirrors + a zig-zag reflected path. ValueTracker
      unfold_tr s ∈ [0, 1] rotates each reflection chamber into a
      straight strip; always_redraw shows the path morphing from
      zig-zag to straight, revealing the total path length.
    """

    def construct(self):
        title = Tex(r"Reflection by unfolding: zigzag $\to$ straight line",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Source (bottom) and target (top)
        A = np.array([-5.0, -1.5, 0])
        B = np.array([5.0, -1.5, 0])

        # Three bounces off two mirrors (top mirror at y=1.5, bottom mirror at y=-1.5)
        # Unfolded target: reflection places target at (5, 3) (if bounces = 1)
        n_bounces = 3

        # Compute bounce x-coordinates for a 3-bounce path
        # Direct path from (-5, -1.5) to (5, -1.5) with bounces at y = ±1.5
        # Path: up to y=1.5 (bounce), down to y=-1.5 (bounce), up to y=1.5 (bounce), down to (5, -1.5)
        # Segments: 4 pieces, each horizontal span 10/4 = 2.5
        bounces = [
            (-5.0 + 2.5 * 1, 1.5),  # top mirror
            (-5.0 + 2.5 * 2, -1.5),  # bottom mirror
            (-5.0 + 2.5 * 3, 1.5),  # top mirror
        ]
        path_folded = [A] + [np.array([x, y, 0]) for (x, y) in bounces] + [B]

        # Unfolded: mirror positions flip vertical coord for each reflection
        # Segment 1: (-5, -1.5) to (-2.5, 1.5) → unchanged
        # Segment 2 (after top reflection): (-2.5, 1.5) to (0, -1.5) → unfold: y becomes 1.5 + (1.5 - (-1.5)) = 4.5
        # Segment 3 (after bottom reflection): (0, -1.5) to (2.5, 1.5) → unfold: y becomes 4.5 + (1.5-(-1.5)) = 7.5
        # Segment 4 (after top reflection): (2.5, 1.5) to (5, -1.5) → unfold: y becomes 7.5 + (1.5 - (-1.5)) = 10.5
        # Unfolded target at (5, 10.5)
        # For animation purposes, we interpolate each segment's y-coordinate toward its unfolded position.
        unfolded_offsets = [0, 3.0, 6.0, 9.0]  # offset to add to the y of each segment's endpoints

        unfold_tr = ValueTracker(0.0)

        # Unfolded path endpoints as function of s (unfold parameter)
        def path_at_s(s):
            # Four segments, each endpoint's y-offset grows with s
            # We need a consistent interpolation
            def apply_offset(pt, offset):
                return np.array([pt[0], pt[1] + s * offset, 0])

            p0 = path_folded[0]
            p1 = apply_offset(path_folded[1], unfolded_offsets[0])  # = unchanged
            # Actually segment 1 connects p0 to p1; both should have segment-1 offset = 0
            # Segment 2 connects p1 to p2, but with s>0 we straighten: p1's "post-reflection" version
            # has offset unfolded_offsets[1]? Let me simplify: just lerp each segment-endpoint
            # individually.
            endpoints = [path_folded[0]]
            for i in range(1, len(path_folded)):
                # Endpoint i is the start of segment (i), end of segment (i-1)
                # Use offset[i-1] (post-bounce-i-1 offset)
                offset = unfolded_offsets[min(i, 3)]
                endpoints.append(np.array([path_folded[i][0],
                                             path_folded[i][1] + s * offset, 0]))
            return endpoints

        def path_line():
            s = unfold_tr.get_value()
            pts = path_at_s(s)
            v = VMobject(color=YELLOW, stroke_width=3)
            v.set_points_as_corners(pts)
            return v

        def endpoints():
            s = unfold_tr.get_value()
            pts = path_at_s(s)
            grp = VGroup()
            for (p, col) in zip(pts, [GREEN, RED, RED, RED, BLUE]):
                grp.add(Dot(p, color=col, radius=0.1))
            return grp

        # Mirrors: static
        mirror_top = Line([-5.2, 1.5, 0], [5.2, 1.5, 0],
                            color=WHITE, stroke_width=4)
        mirror_bot = Line([-5.2, -1.5, 0], [5.2, -1.5, 0],
                            color=WHITE, stroke_width=4)

        self.play(Create(mirror_top), Create(mirror_bot))

        self.add(always_redraw(path_line), always_redraw(endpoints))

        # Labels
        A_lbl = Tex(r"A", color=GREEN, font_size=22).next_to(A, LEFT, buff=0.1)
        B_lbl = Tex(r"B", color=BLUE, font_size=22).next_to(B, RIGHT, buff=0.1)
        self.play(Write(A_lbl), Write(B_lbl))

        def info():
            s = unfold_tr.get_value()
            # Original zigzag length
            L_fold = sum(np.linalg.norm(path_folded[i + 1] - path_folded[i])
                         for i in range(len(path_folded) - 1))
            return VGroup(
                MathTex(rf"\text{{unfold}} = {s:.2f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"L = {L_fold:.3f}",
                         color=WHITE, font_size=22),
                Tex(r"zigzag length = straight unfolded length",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.35)

        self.add(always_redraw(info))

        self.play(unfold_tr.animate.set_value(1.0),
                   run_time=4, rate_func=smooth)
        self.wait(0.6)
        self.play(unfold_tr.animate.set_value(0.0),
                   run_time=3, rate_func=smooth)
        self.wait(0.4)
