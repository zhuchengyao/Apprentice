from manim import *
import numpy as np


class HallMarriageTheoremExample(Scene):
    """
    Hall's marriage theorem: a bipartite graph has a perfect matching
    iff for every subset S of one side, |N(S)| >= |S|. Visualize with
    a specific bipartite graph on 4+4 vertices.

    SINGLE_FOCUS:
      Left 4 vertices (L_1..L_4), right 4 vertices (R_1..R_4), edges
      form preference graph. ValueTracker step_tr reveals perfect
      matching edge by edge; Hall's condition visually verified.
    """

    def construct(self):
        title = Tex(r"Hall's theorem: $|N(S)| \ge |S|$ for all $S \Leftrightarrow$ perfect matching",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Left and right positions
        N = 4
        left_xs = [-3.5] * N
        left_ys = [2 - i * 1.3 for i in range(N)]
        right_xs = [1.5] * N
        right_ys = [2 - i * 1.3 for i in range(N)]

        # Edges
        edges = [
            (0, 0), (0, 1),
            (1, 1), (1, 2),
            (2, 0), (2, 3),
            (3, 2), (3, 3),
        ]
        # Perfect matching: (0, 0), (1, 1), (2, 3), (3, 2)
        matching = [(0, 0), (1, 1), (2, 3), (3, 2)]

        # Dots + labels
        L_dots = VGroup()
        R_dots = VGroup()
        for i in range(N):
            L_dots.add(Circle(radius=0.25, color=BLUE,
                                 fill_opacity=0.5, stroke_width=2
                                 ).move_to([left_xs[i], left_ys[i], 0]))
            L_dots.add(MathTex(rf"L_{i + 1}", font_size=18, color=BLACK
                                  ).move_to([left_xs[i], left_ys[i], 0]))
            R_dots.add(Circle(radius=0.25, color=GREEN,
                                 fill_opacity=0.5, stroke_width=2
                                 ).move_to([right_xs[i], right_ys[i], 0]))
            R_dots.add(MathTex(rf"R_{i + 1}", font_size=18, color=BLACK
                                  ).move_to([right_xs[i], right_ys[i], 0]))
        self.play(FadeIn(L_dots), FadeIn(R_dots))

        # Static all edges (faint)
        all_edges = VGroup()
        for (l, r) in edges:
            all_edges.add(Line([left_xs[l], left_ys[l], 0],
                                 [right_xs[r], right_ys[r], 0],
                                 color=GREY_B, stroke_width=1.5,
                                 stroke_opacity=0.5))
        self.play(Create(all_edges))

        step_tr = ValueTracker(0)

        def matching_edges():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(matching)))
            grp = VGroup()
            for i in range(s):
                l, r = matching[i]
                grp.add(Line([left_xs[l], left_ys[l], 0],
                               [right_xs[r], right_ys[r], 0],
                               color=RED, stroke_width=4))
            return grp

        self.add(always_redraw(matching_edges))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(matching)))
            return VGroup(
                MathTex(rf"\text{{matched}} = {s}/{N}",
                         color=RED, font_size=22),
                Tex(r"|N(\{L_1\})| = 2 \ge 1",
                     color=GREEN, font_size=18),
                Tex(r"|N(\{L_1, L_2\})| = 3 \ge 2",
                     color=GREEN, font_size=18),
                Tex(r"all Hall conditions pass",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for s in range(1, len(matching) + 1):
            self.play(step_tr.animate.set_value(s),
                       run_time=0.9, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
