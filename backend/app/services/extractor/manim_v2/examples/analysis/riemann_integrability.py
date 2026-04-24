from manim import *
import numpy as np


class RiemannIntegrabilityExample(Scene):
    """
    Riemann integrability: f is Riemann integrable iff U_N - L_N → 0.
    Dirichlet function (1 on rationals, 0 elsewhere) has U_N - L_N = 1
    for all N, so NOT Riemann integrable. Continuous f has U_N - L_N → 0.

    COMPARISON:
      LEFT  — continuous f(x) = x²; upper and lower sums converge.
      RIGHT — Dirichlet-like function; upper stays 1, lower stays 0.
    """

    def construct(self):
        title = Tex(r"Riemann integrable iff $U_N - L_N \to 0$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT: continuous function
        ax_L = Axes(x_range=[0, 1, 0.25], y_range=[0, 1.2, 0.25],
                     x_length=5, y_length=3.5, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([-3.3, -0.3, 0])
        f_curve = ax_L.plot(lambda x: x ** 2, x_range=[0, 1, 0.01],
                              color=BLUE, stroke_width=3)
        L_lbl = MathTex(r"f(x) = x^2", color=BLUE, font_size=20
                          ).next_to(ax_L, UP, buff=0.1)
        self.play(Create(ax_L), Write(L_lbl), Create(f_curve))

        ax_R = Axes(x_range=[0, 1, 0.25], y_range=[0, 1.2, 0.25],
                     x_length=5, y_length=3.5, tips=False,
                     axis_config={"font_size": 12, "include_numbers": True}
                     ).move_to([3.3, -0.3, 0])
        R_lbl = MathTex(r"\text{Dirichlet-like}",
                          color=RED, font_size=20
                          ).next_to(ax_R, UP, buff=0.1)
        self.play(Create(ax_R), Write(R_lbl))

        N_tr = ValueTracker(4)

        def cont_rects():
            N = int(round(N_tr.get_value()))
            N = max(2, min(N, 30))
            h = 1 / N
            grp = VGroup()
            for i in range(N):
                x = (i + 0.5) * h
                f_mid = x ** 2
                h_scene = ax_L.c2p(0, f_mid)[1] - ax_L.c2p(0, 0)[1]
                bar = Rectangle(
                    width=(ax_L.c2p(h, 0)[0] - ax_L.c2p(0, 0)[0]) * 0.9,
                    height=h_scene, color=YELLOW, fill_opacity=0.5,
                    stroke_width=0.5)
                bar.move_to([ax_L.c2p(x, 0)[0],
                             ax_L.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(bar)
            return grp

        def dir_sums():
            N = int(round(N_tr.get_value()))
            # Upper = 1 everywhere, Lower = 0
            grp = VGroup()
            # Draw upper row (1) and lower row (0); both constant
            upper_bar = Rectangle(
                width=ax_R.c2p(1, 0)[0] - ax_R.c2p(0, 0)[0],
                height=ax_R.c2p(0, 1)[1] - ax_R.c2p(0, 0)[1],
                color=RED, fill_opacity=0.3, stroke_width=1
            ).move_to([(ax_R.c2p(0, 0)[0] + ax_R.c2p(1, 0)[0]) / 2,
                         (ax_R.c2p(0, 0)[1] + ax_R.c2p(0, 1)[1]) / 2, 0])
            grp.add(upper_bar)
            # Lower = 0, shown as line at y=0
            lower_line = DashedLine(ax_R.c2p(0, 0), ax_R.c2p(1, 0),
                                      color=BLUE, stroke_width=3)
            grp.add(lower_line)
            return grp

        self.add(always_redraw(cont_rects), always_redraw(dir_sums))

        # Labels
        U_L_lbl = MathTex(r"U_N - L_N \to 0 \ \checkmark",
                            color=GREEN, font_size=20
                            ).move_to([-3.3, -2.7, 0])
        U_R_lbl = MathTex(r"U_N - L_N = 1 \ \text{always}",
                            color=RED, font_size=20
                            ).move_to([3.3, -2.7, 0])
        self.play(Write(U_L_lbl), Write(U_R_lbl))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(2, min(N, 30))
            return VGroup(
                MathTex(rf"N = {N}", color=YELLOW, font_size=24),
                Tex(r"LEFT: continuous $\Rightarrow$ integrable",
                     color=GREEN, font_size=18),
                Tex(r"RIGHT: dense rationals/irrationals",
                     color=RED, font_size=18),
                Tex(r"$U = 1$, $L = 0$; not Riemann integrable",
                     color=RED, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.2)

        self.add(always_redraw(info))

        for nv in [8, 15, 30]:
            self.play(N_tr.animate.set_value(nv),
                       run_time=1.4, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
