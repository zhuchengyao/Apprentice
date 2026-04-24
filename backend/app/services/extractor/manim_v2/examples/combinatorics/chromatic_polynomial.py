from manim import *
import numpy as np


class ChromaticPolynomialExample(Scene):
    """
    Chromatic polynomial P(G, k) counts proper k-colorings of G.
    For K_3: P(K_3, k) = k(k-1)(k-2). For C_4 (4-cycle):
    P(C_4, k) = (k-1)^4 + (k-1).

    TWO_COLUMN:
      LEFT: two graphs K_3 and C_4. RIGHT: axes plotting both
      chromatic polynomials over k = 0..5; ValueTracker k_tr moves
      cursor; integer-k values marked.
    """

    def construct(self):
        title = Tex(r"Chromatic polynomial $P(G, k)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT: K_3 and C_4
        # K_3 positions
        k3_center = np.array([-4, 1.2, 0])
        k3_pos = [k3_center + np.array([np.cos(PI / 2 + 2 * PI * i / 3),
                                            np.sin(PI / 2 + 2 * PI * i / 3), 0]) * 0.7
                  for i in range(3)]
        k3_edges = VGroup(
            Line(k3_pos[0], k3_pos[1], color=BLUE, stroke_width=2),
            Line(k3_pos[1], k3_pos[2], color=BLUE, stroke_width=2),
            Line(k3_pos[2], k3_pos[0], color=BLUE, stroke_width=2),
        )
        k3_dots = VGroup(*[Dot(p, color=YELLOW, radius=0.1) for p in k3_pos])
        k3_lbl = MathTex(r"K_3", color=YELLOW, font_size=24
                           ).move_to(k3_center + np.array([0, -1.3, 0]))
        k3_formula = MathTex(r"P = k(k-1)(k-2)",
                                color=BLUE, font_size=18
                                ).move_to(k3_center + np.array([0, -1.7, 0]))
        self.play(Create(k3_edges), FadeIn(k3_dots), Write(k3_lbl),
                   Write(k3_formula))

        # C_4
        c4_center = np.array([-4, -1.5, 0])
        c4_pos = [c4_center + np.array([np.cos(PI / 4 + PI / 2 * i),
                                            np.sin(PI / 4 + PI / 2 * i), 0]) * 0.7
                  for i in range(4)]
        c4_edges = VGroup(
            Line(c4_pos[0], c4_pos[1], color=GREEN, stroke_width=2),
            Line(c4_pos[1], c4_pos[2], color=GREEN, stroke_width=2),
            Line(c4_pos[2], c4_pos[3], color=GREEN, stroke_width=2),
            Line(c4_pos[3], c4_pos[0], color=GREEN, stroke_width=2),
        )
        c4_dots = VGroup(*[Dot(p, color=YELLOW, radius=0.1) for p in c4_pos])
        c4_lbl = MathTex(r"C_4", color=YELLOW, font_size=24
                           ).move_to(c4_center + np.array([0, -1.3, 0]))
        c4_formula = MathTex(r"P = (k-1)^4 + (k-1)",
                                color=GREEN, font_size=18
                                ).move_to(c4_center + np.array([0, -1.7, 0]))
        self.play(Create(c4_edges), FadeIn(c4_dots), Write(c4_lbl),
                   Write(c4_formula))

        # RIGHT: polynomial plots
        ax = Axes(x_range=[0, 5, 1], y_range=[0, 300, 60],
                   x_length=5, y_length=4, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([3.5, -0.3, 0])
        xl = MathTex(r"k", font_size=20).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"P(G, k)", font_size=20).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        def P_K3(k):
            return k * (k - 1) * (k - 2)

        def P_C4(k):
            return (k - 1) ** 4 + (k - 1)

        k3_curve = ax.plot(P_K3, x_range=[0, 5, 0.02],
                             color=BLUE, stroke_width=3)
        c4_curve = ax.plot(P_C4, x_range=[0, 5, 0.02],
                             color=GREEN, stroke_width=3)
        self.play(Create(k3_curve), Create(c4_curve))

        k_tr = ValueTracker(0.5)

        def k3_rider():
            k = k_tr.get_value()
            return Dot(ax.c2p(k, min(P_K3(k), 300)),
                        color=BLUE, radius=0.1)

        def c4_rider():
            k = k_tr.get_value()
            return Dot(ax.c2p(k, min(P_C4(k), 300)),
                        color=GREEN, radius=0.1)

        self.add(always_redraw(k3_rider), always_redraw(c4_rider))

        def info():
            k = k_tr.get_value()
            return VGroup(
                MathTex(rf"k = {k:.2f}", color=YELLOW, font_size=22),
                MathTex(rf"P(K_3, k) = {P_K3(k):.0f}",
                         color=BLUE, font_size=20),
                MathTex(rf"P(C_4, k) = {P_C4(k):.0f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for kv in [1, 2, 3, 4, 5, 2.5]:
            self.play(k_tr.animate.set_value(kv),
                       run_time=1.2, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
