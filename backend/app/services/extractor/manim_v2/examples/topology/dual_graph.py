from manim import *
import numpy as np


class DualGraphExample(Scene):
    """
    Planar dual: each face of a planar graph → a dual vertex;
    each primal edge → a dual edge crossing it exactly once.

    SINGLE_FOCUS animation of dual emergence:
      Primal = rectangle with one diagonal (V=4, E=5, F=3 incl. outer).
      ValueTracker s ∈ [0, 1] moves 3 dual vertices from the
      midpoints of an adjacent primal edge to their face centroids.
      always_redraw keeps the dual edges glued to the moving dual
      vertices; a second ValueTracker opacity_tr fades dual edges
      in as s → 1. The Euler count panel V − E + F = 2 is shown
      for both primal and dual graphs.
    """

    def construct(self):
        title = Tex(r"Planar dual: face $\leftrightarrow$ vertex, edge $\leftrightarrow$ edge",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Primal (rectangle + one diagonal)
        p1 = np.array([-2.2, -1.2, 0])
        p2 = np.array([2.2, -1.2, 0])
        p3 = np.array([2.2, 1.2, 0])
        p4 = np.array([-2.2, 1.2, 0])

        primal_edges = VGroup(
            Line(p1, p2, color=BLUE),
            Line(p2, p3, color=BLUE),
            Line(p3, p4, color=BLUE),
            Line(p4, p1, color=BLUE),
            Line(p1, p3, color=BLUE),
        )
        primal_dots = VGroup(*[Dot(p, color=BLUE, radius=0.1)
                                for p in [p1, p2, p3, p4]])
        primal_lbls = VGroup(*[
            MathTex(f"v_{i+1}", color=BLUE, font_size=22).next_to(
                p, direction, buff=0.1)
            for i, (p, direction) in enumerate(
                [(p1, DL), (p2, DR), (p3, UR), (p4, UL)])
        ])

        self.play(Create(primal_edges), FadeIn(primal_dots),
                  Write(primal_lbls))

        # Face centroids
        f_lower = (p1 + p2 + p3) / 3          # lower-right triangle
        f_upper = (p1 + p3 + p4) / 3          # upper-left triangle
        f_outer = np.array([0.0, 2.6, 0.0])   # outer face dual vertex

        # Emergence-start positions (on primal edges adjacent to each face)
        start_lower = (p1 + p2) / 2           # edge p1-p2
        start_upper = (p3 + p4) / 2           # edge p3-p4
        start_outer = (p3 + p4) / 2 + UP * 0.15

        s_tr = ValueTracker(0.0)

        def pos_lower():
            s = s_tr.get_value()
            return (1 - s) * start_lower + s * f_lower

        def pos_upper():
            s = s_tr.get_value()
            return (1 - s) * start_upper + s * f_upper

        def pos_outer():
            s = s_tr.get_value()
            return (1 - s) * start_outer + s * f_outer

        def dual_lower():
            return Dot(pos_lower(), color=RED, radius=0.13)

        def dual_upper():
            return Dot(pos_upper(), color=RED, radius=0.13)

        def dual_outer():
            return Dot(pos_outer(), color=RED, radius=0.13)

        def dual_edges():
            pl = pos_lower()
            pu = pos_upper()
            po = pos_outer()
            s = s_tr.get_value()
            alpha = min(1.0, max(0.0, (s - 0.3) / 0.7))
            grp = VGroup(
                # diag (p1,p3) separates lower ↔ upper
                DashedLine(pl, pu, color=RED, stroke_width=3,
                            stroke_opacity=alpha),
                # edge (p1,p2) lower ↔ outer (via bottom-left)
                DashedLine(pl, po, color=RED, stroke_width=3,
                            stroke_opacity=alpha),
                # edge (p2,p3) lower ↔ outer (via right) — a parallel dual edge
                DashedLine(pl + np.array([0.18, 0, 0]),
                            po + np.array([0.18, 0, 0]),
                            color=RED, stroke_width=3,
                            stroke_opacity=alpha),
                # edge (p3,p4) upper ↔ outer (via top)
                DashedLine(pu, po, color=RED, stroke_width=3,
                            stroke_opacity=alpha),
                # edge (p4,p1) upper ↔ outer (via left)
                DashedLine(pu + np.array([-0.18, 0, 0]),
                            po + np.array([-0.18, 0, 0]),
                            color=RED, stroke_width=3,
                            stroke_opacity=alpha),
            )
            return grp

        self.add(always_redraw(dual_lower),
                 always_redraw(dual_upper),
                 always_redraw(dual_outer),
                 always_redraw(dual_edges))

        # Dual vertex hints at the start positions (faded away via s)
        hint_lbl = Tex(r"dual vertices emerge from edges into face centers",
                       color=GREY_B, font_size=20).move_to([0, -2.0, 0])
        self.play(Write(hint_lbl))

        # Phase 1: grow dual vertices + edges
        self.play(s_tr.animate.set_value(1.0),
                  run_time=4, rate_func=smooth)
        self.wait(0.5)

        self.play(FadeOut(hint_lbl))

        # Euler panel
        count_panel = VGroup(
            Tex(r"primal: $V=4,\ E=5,\ F=3$", color=BLUE, font_size=22),
            Tex(r"dual:\ $V^*=3,\ E^*=5,\ F^*=4$", color=RED, font_size=22),
            Tex(r"$V - E + F = 2$", color=YELLOW, font_size=24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        count_panel.to_edge(DOWN, buff=0.3)
        self.play(Write(count_panel))
        self.wait(0.8)

        # Phase 2: oscillate s to show the dual-from-edges intuition
        self.play(s_tr.animate.set_value(0.0),
                  run_time=1.6, rate_func=smooth)
        self.play(s_tr.animate.set_value(1.0),
                  run_time=1.6, rate_func=smooth)
        self.wait(0.5)
