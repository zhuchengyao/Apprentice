from manim import *
import numpy as np


class TriangleModuliSpaceExample(Scene):
    """
    Moduli space of triangles up to similarity, parametrized by
    (side ratio b/a, included angle γ at vertex A).

    TWO_COLUMN:
      LEFT  — a live triangle with sides a=1, b=ratio, included
              angle γ at vertex A, recomputed each frame from
              ValueTrackers ratio_tr and gamma_tr. Above it, a
              scaled copy (green) confirms similarity is invariant
              under rescaling.
      RIGHT — moduli-space axes (b/a ∈ [0, 1.2], γ ∈ [0, π]) with
              a GREY cloud of 36 sample similarity classes, a RED
              tracked dot, and a live (b/a, γ) panel. The 5-point
              tour steps through 5 (b/a, γ) configurations.
    """

    def construct(self):
        title = Tex(r"Moduli space of triangles $\sim (b/a,\ \gamma)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        ratio_tr = ValueTracker(0.7)
        gamma_tr = ValueTracker(PI / 3)

        # LEFT: live triangle at scale S
        tri_origin = np.array([-4.0, -0.8, 0])
        S = 1.8

        def tri_verts(origin, scale):
            r = ratio_tr.get_value()
            g = gamma_tr.get_value()
            A = origin.copy()
            B = A + scale * np.array([1.0, 0.0, 0.0])
            C = A + scale * r * np.array([np.cos(g), np.sin(g), 0.0])
            return A, B, C

        def big_triangle():
            A, B, C = tri_verts(tri_origin, S)
            return Polygon(A, B, C, color=YELLOW,
                           fill_opacity=0.3, stroke_width=3)

        def side_labels():
            A, B, C = tri_verts(tri_origin, S)
            r = ratio_tr.get_value()
            g = gamma_tr.get_value()
            a_lbl = MathTex(r"a", font_size=24,
                            color=WHITE).move_to((A + B) / 2 + DOWN * 0.3)
            b_lbl = MathTex(rf"b={r:.2f}", font_size=22,
                            color=WHITE).move_to((A + C) / 2
                                                  + np.array([-0.45, 0.05, 0]))
            g_lbl = MathTex(rf"\gamma={np.degrees(g):.0f}^\circ",
                            font_size=22, color=BLUE).move_to(
                A + 0.7 * np.array([np.cos(g / 2), np.sin(g / 2), 0]))
            return VGroup(a_lbl, b_lbl, g_lbl)

        self.add(always_redraw(big_triangle),
                 always_redraw(side_labels))

        # A scaled similar copy above
        sim_origin = np.array([-4.8, 2.0, 0])
        sim_S = 0.9

        def sim_copy():
            A, B, C = tri_verts(sim_origin, sim_S)
            return Polygon(A, B, C, color=GREEN_B,
                           fill_opacity=0.25, stroke_width=2)

        self.add(always_redraw(sim_copy))

        sim_lbl = Tex(r"$\sim$ similar (rescaled)", color=GREEN_B,
                      font_size=18).move_to([-4.0, 3.1, 0])
        self.play(Write(sim_lbl))

        # RIGHT: moduli axes
        axes = Axes(
            x_range=[0, 1.2, 0.25], y_range=[0, PI + 0.05, PI / 4],
            x_length=4.5, y_length=3.8,
            axis_config={"font_size": 16, "include_numbers": True,
                         "decimal_number_config": {"num_decimal_places": 2}},
            tips=False,
        ).move_to([3.3, -0.6, 0])
        xlbl = MathTex(r"b/a", font_size=22).next_to(axes, DOWN, buff=0.15)
        ylbl = MathTex(r"\gamma", font_size=24).next_to(axes, LEFT, buff=0.15)
        self.play(Create(axes), Write(xlbl), Write(ylbl))

        # Background cloud
        np.random.seed(4)
        cloud = VGroup()
        for _ in range(36):
            rv = np.random.uniform(0.1, 1.15)
            gv = np.random.uniform(0.2, PI - 0.2)
            cloud.add(Dot(axes.c2p(rv, gv), color=GREY_B, radius=0.03))
        self.play(FadeIn(cloud))

        def tracked_dot():
            r = ratio_tr.get_value()
            g = gamma_tr.get_value()
            return Dot(axes.c2p(r, g), color=RED, radius=0.12)

        self.add(always_redraw(tracked_dot))

        def info_panel():
            r = ratio_tr.get_value()
            g = gamma_tr.get_value()
            return VGroup(
                MathTex(rf"b/a = {r:.2f}", color=WHITE, font_size=22),
                MathTex(rf"\gamma = {np.degrees(g):.0f}^\circ",
                        color=BLUE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.3, 2.2, 0])

        self.add(always_redraw(info_panel))

        # Tour through 5 configs
        tour = [(1.0, PI / 2),
                (0.4, 2 * PI / 5),
                (0.9, PI / 6),
                (0.6, 5 * PI / 6),
                (0.7, PI / 3)]
        for (r, g) in tour:
            self.play(ratio_tr.animate.set_value(r),
                      gamma_tr.animate.set_value(g),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.35)
        self.wait(0.4)
