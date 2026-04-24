from manim import *
import numpy as np


class PythagorasRearrangementExample(Scene):
    """
    Pythagoras a²+b²=c² via the classic two-arrangement proof.

    The same outer (a+b)×(a+b) square is filled with four identical right
    triangles in TWO arrangements:
      Arrangement 1 — triangles sit in the four corners as 'L' pieces
                      around two squares of side a and side b.
                      Free area = a² + b².
      Arrangement 2 — triangles sit in the four corners pointing inward,
                      leaving a tilted square of side c.
                      Free area = c².

    Animate triangles smoothly sliding from arrangement 1 to arrangement 2
    via Transform. The total area is fixed (the outer square never moves);
    only the triangles move. So a² + b² must equal c².
    """

    def construct(self):
        title = Tex(r"$a^2 + b^2 = c^2$: same square, two ways to fill it",
                    font_size=32).to_edge(UP, buff=0.4)
        self.play(Write(title))

        a, b = 1.5, 2.0
        s = a + b

        # Center the (a+b)×(a+b) square at origin
        center = np.array([0.0, -0.4, 0])
        bl = center + np.array([-s / 2, -s / 2, 0])
        br = center + np.array([+s / 2, -s / 2, 0])
        tr = center + np.array([+s / 2, +s / 2, 0])
        tl = center + np.array([-s / 2, +s / 2, 0])

        outer = Polygon(bl, br, tr, tl, color=WHITE, stroke_width=3)
        side_lbl = MathTex("a + b", font_size=26, color=WHITE).next_to(outer, UP, buff=0.15)
        self.play(Create(outer), Write(side_lbl))

        # === ARRANGEMENT 1 ===
        # Four triangles tucked into corners, leaving an a×a square + a b×b square.
        # Each triangle has legs a (horizontal/vertical) and b.
        # Bottom-left corner: triangle with right angle at bl, legs going right (b) and up (a).
        # That leaves an a×a square in the top-left and a b×b square in the bottom-right.

        # Let's place them so:
        #   T1 (BL): right angle at bl, legs RIGHT b, UP a → vertices: bl, bl + (b, 0), bl + (0, a)
        #   T2 (BR): right angle at br, legs LEFT a, UP b → vertices: br, br + (-a, 0), br + (0, b)
        #   T3 (TR): right angle at tr, legs LEFT b, DOWN a → vertices: tr, tr + (-b, 0), tr + (0, -a)
        #   T4 (TL): right angle at tl, legs RIGHT a, DOWN b → vertices: tl, tl + (a, 0), tl + (0, -b)

        T1_a = [bl, bl + np.array([b, 0, 0]), bl + np.array([0, a, 0])]
        T2_a = [br, br + np.array([-a, 0, 0]), br + np.array([0, b, 0])]
        T3_a = [tr, tr + np.array([-b, 0, 0]), tr + np.array([0, -a, 0])]
        T4_a = [tl, tl + np.array([a, 0, 0]), tl + np.array([0, -b, 0])]

        triangles_arr1 = VGroup(*[
            Polygon(*pts, color=BLUE_D, fill_opacity=0.7, stroke_width=2)
            for pts in [T1_a, T2_a, T3_a, T4_a]
        ])

        # The two free squares:
        # a²-square sits in the top-left between T1 and T4
        a_sq_bl = bl + np.array([0, a, 0])
        a_sq = Polygon(
            a_sq_bl,
            a_sq_bl + np.array([a, 0, 0]),
            a_sq_bl + np.array([a, b, 0]),  # actually side a, but b leg of T1, hmm let's reconsider
            a_sq_bl + np.array([0, b, 0]),
            color=GREEN, fill_opacity=0.6, stroke_width=2,
        )

        # Let me reconsider. With a=1.5, b=2, the square's geometry:
        # The free region in arrangement 1 has two parts:
        # - a square of side a (top-left rectangle: width a, height b? no, side a × side a)
        # - a square of side b (bottom-right square: side b × side b)
        # The triangles cover an L shape between them.

        # Actually the cleanest decomposition: divide the (a+b) square with a horizontal line at
        # height a from the bottom and a vertical line at width a from the left.
        # That gives 4 sub-rectangles: bl=(a×a), br=(b×a), tl=(a×b), tr=(b×b).
        # We want T1+T2+T3+T4 to cover regions whose total area = 2ab, leaving a²+b² free.

        # Let me redefine triangles cleanly using inscribed-tilted-square positioning instead.
        # Place 4 triangles with right angle at each corner, legs (a, b) outward.
        # Specifically: T1 BL corner has legs going RIGHT a + UP b.
        T1_a = [bl, bl + np.array([a, 0, 0]), bl + np.array([0, b, 0])]
        T2_a = [br, br + np.array([-b, 0, 0]), br + np.array([0, a, 0])]
        T3_a = [tr, tr + np.array([-a, 0, 0]), tr + np.array([0, -b, 0])]
        T4_a = [tl, tl + np.array([b, 0, 0]), tl + np.array([0, -a, 0])]

        triangles_arr1 = VGroup(*[
            Polygon(*pts, color=BLUE_D, fill_opacity=0.7, stroke_width=2)
            for pts in [T1_a, T2_a, T3_a, T4_a]
        ])

        # The remaining area is the "L" between them. With this triangle placement,
        # the central uncovered region is a tilted parallelogram, not a clean a²+b² split.
        # For a clean a²+b² visual we need a different placement.

        # Use the *standard* proof: triangles align to form a rectangular L:
        # T1 BL: (bl, bl+(a,0), bl+(a,b))  — right angle at bl+(a,0)? No, at bl+(a,b)? Hmm.
        #
        # Let me just use the classical setup where triangles tile so that the FREE region
        # is the union of an a×a square and a b×b square sitting side by side along the bottom.

        # Setup: bottom edge has length a+b. Place T1 at the top-left and T2 at the top-right
        # such that their hypotenuses go from top-left to (a, a+b vertical?) ...
        # Easier: let me just draw the two sub-squares directly and place 4 triangles as the
        # complement, computing geometry from scratch.

        # CLEAN ARRANGEMENT 1 (a²+b²-revealing):
        #   - a×a square in the top-left corner: vertices tl, tl+(a,0), tl+(a,-a), tl+(0,-a)
        #   - b×b square in the bottom-right corner: vertices bl+(a,0), br, br+(0,b), bl+(a, b)
        #   - Two rectangles a×b filling the remaining L; each rectangle is split into 2 triangles
        #     so we get 4 triangles total.
        # The 4 triangles all have legs a and b.

        a_square = Polygon(
            tl,
            tl + np.array([a, 0, 0]),
            tl + np.array([a, -a, 0]),
            tl + np.array([0, -a, 0]),
            color=GREEN, fill_opacity=0.6, stroke_width=2,
        )
        a_lbl = MathTex("a^2", color=GREEN, font_size=30).move_to(
            tl + np.array([a / 2, -a / 2, 0])
        )

        b_square = Polygon(
            bl + np.array([a, 0, 0]),
            br,
            br + np.array([0, b, 0]),
            bl + np.array([a, b, 0]),
            color=ORANGE, fill_opacity=0.6, stroke_width=2,
        )
        b_lbl = MathTex("b^2", color=ORANGE, font_size=30).move_to(
            bl + np.array([a + b / 2, b / 2, 0])
        )

        # Two a×b rectangles fill the rest:
        #   R1 (bottom-left): vertices bl, bl+(a,0), bl+(a,b), bl+(0,b)
        #   R2 (top-right):   vertices tl+(a,0), tr, tr+(0,-a), tl+(a,-a)
        # Split each rectangle into two triangles by a diagonal.
        T1_pts = [bl, bl + np.array([a, 0, 0]), bl + np.array([a, b, 0])]
        T2_pts = [bl, bl + np.array([a, b, 0]), bl + np.array([0, b, 0])]
        T3_pts = [tl + np.array([a, 0, 0]), tr, tr + np.array([0, -a, 0])]
        T4_pts = [tl + np.array([a, 0, 0]), tr + np.array([0, -a, 0]), tl + np.array([a, -a, 0])]

        triangles_arr1 = VGroup(*[
            Polygon(*pts, color=BLUE_D, fill_opacity=0.7, stroke_width=2)
            for pts in [T1_pts, T2_pts, T3_pts, T4_pts]
        ])

        self.play(FadeIn(a_square), Write(a_lbl), FadeIn(b_square), Write(b_lbl))
        self.play(LaggedStart(*[FadeIn(t) for t in triangles_arr1], lag_ratio=0.15))
        self.wait(0.6)

        eq1 = MathTex(r"\text{Free area} = a^2 + b^2", font_size=28, color=YELLOW).move_to(
            [-4.5, +2.4, 0]
        )
        self.play(Write(eq1))
        self.wait(0.6)

        # === ARRANGEMENT 2 ===
        # Move the 4 triangles to surround a tilted c×c square.
        # New triangle positions: each in a corner with right angle at that corner,
        # legs (a, b) along the two adjacent sides of the outer square.
        T1_b_pts = [bl, bl + np.array([a, 0, 0]), bl + np.array([0, b, 0])]
        T2_b_pts = [br, br + np.array([-b, 0, 0]), br + np.array([0, a, 0])]
        T3_b_pts = [tr, tr + np.array([-a, 0, 0]), tr + np.array([0, -b, 0])]
        T4_b_pts = [tl, tl + np.array([b, 0, 0]), tl + np.array([0, -a, 0])]

        triangles_arr2 = VGroup(*[
            Polygon(*pts, color=BLUE_D, fill_opacity=0.7, stroke_width=2)
            for pts in [T1_b_pts, T2_b_pts, T3_b_pts, T4_b_pts]
        ])

        # The center tilted square has vertices:
        #   bl + (a, 0), br + (0, a), tr + (-a, 0), tl + (0, -a)
        # ... actually we need the tilted-square vertices at the inner ends of T1..T4 hypotenuses.
        # T1 hypotenuse: from bl+(a,0) to bl+(0,b)
        # T2 hypotenuse: from br+(-b,0) to br+(0,a)
        # T3 hypotenuse: from tr+(-a,0) to tr+(0,-b)
        # T4 hypotenuse: from tl+(b,0) to tl+(0,-a)
        # The tilted square's vertices are the points shared between consecutive triangles' hypotenuse ends:
        c_p1 = bl + np.array([a, 0, 0])      # shared with T2's leg base? Let's check
        c_p2 = br + np.array([0, a, 0])
        c_p3 = tr + np.array([-a, 0, 0])
        c_p4 = tl + np.array([0, -a, 0])

        c_square = Polygon(c_p1, c_p2, c_p3, c_p4,
                           color=YELLOW, fill_opacity=0.6, stroke_width=2)
        c_lbl = MathTex("c^2", color=YELLOW, font_size=36).move_to(c_square.get_center())

        # Animate: fade out the a², b² squares and the triangles morph into arrangement 2
        self.play(
            FadeOut(a_square), FadeOut(a_lbl),
            FadeOut(b_square), FadeOut(b_lbl),
            Transform(triangles_arr1, triangles_arr2),
            run_time=2.5, rate_func=smooth,
        )
        self.play(FadeIn(c_square), Write(c_lbl))
        self.wait(0.4)

        eq2 = MathTex(r"\text{Free area} = c^2", font_size=28, color=YELLOW).move_to(
            [-4.5, +2.4, 0]
        )
        self.play(Transform(eq1, eq2))
        self.wait(0.6)

        # Side label change — now the triangles' legs along outer edges spell "a, b"
        leg_labels = VGroup(
            MathTex("a", font_size=22, color=BLUE_D).next_to(
                bl + np.array([a / 2, 0, 0]), DOWN, buff=0.1),
            MathTex("b", font_size=22, color=BLUE_D).next_to(
                bl + np.array([a + b / 2, 0, 0]), DOWN, buff=0.1),
        )
        self.play(Write(leg_labels))

        conclusion = MathTex(r"a^2 + b^2 = c^2", font_size=44, color=YELLOW).move_to(
            [+4.5, +1.8, 0]
        )
        self.play(Write(conclusion))
        self.wait(1.2)
