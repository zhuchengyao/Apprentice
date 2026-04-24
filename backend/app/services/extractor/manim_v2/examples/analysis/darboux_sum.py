from manim import *
import numpy as np


class DarbouxSumExample(Scene):
    """
    Darboux sums: upper sum U_N = Σ sup(f on [x_i, x_{i+1}]) · Δx
    and lower sum L_N = Σ inf · Δx. Both converge to ∫f as N → ∞
    (Darboux integrability).

    TWO_COLUMN:
      LEFT  — axes with f(x) = x² · sin(x) + 2 on [0, 3]; ValueTracker
              N_tr grows subintervals 2 → 40; always_redraw GREEN
              upper rectangles + BLUE lower rectangles.
      RIGHT — live U_N, L_N, gap, true integral.
    """

    def construct(self):
        title = Tex(r"Darboux sums: $L_N \le \int f \le U_N$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def f(x):
            return x ** 2 * np.sin(x) + 2

        a, b = 0.0, 3.0
        xs_fine = np.linspace(a, b, 2000)
        true_int = float(np.trapz(f(xs_fine), xs_fine))

        ax = Axes(x_range=[0, 3, 0.5], y_range=[0, 6, 1],
                   x_length=7, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        self.play(Create(ax))

        curve = ax.plot(f, x_range=[0, 3], color=YELLOW, stroke_width=3)
        self.play(Create(curve))

        N_tr = ValueTracker(2)

        def upper_rects():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 60))
            h = (b - a) / N
            grp = VGroup()
            for i in range(N):
                x_lo = a + i * h
                x_hi = x_lo + h
                # Sup of f on [x_lo, x_hi]
                xs = np.linspace(x_lo, x_hi, 20)
                sup_val = float(np.max(f(xs)))
                h_scene = ax.c2p(0, sup_val)[1] - ax.c2p(0, 0)[1]
                w_scene = ax.c2p(h, 0)[0] - ax.c2p(0, 0)[0]
                rect = Rectangle(width=w_scene, height=h_scene,
                                   color=GREEN, fill_opacity=0.2,
                                   stroke_width=0.5)
                rect.move_to([ax.c2p(x_lo + h / 2, 0)[0],
                              ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(rect)
            return grp

        def lower_rects():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 60))
            h = (b - a) / N
            grp = VGroup()
            for i in range(N):
                x_lo = a + i * h
                x_hi = x_lo + h
                xs = np.linspace(x_lo, x_hi, 20)
                inf_val = float(np.min(f(xs)))
                h_scene = ax.c2p(0, inf_val)[1] - ax.c2p(0, 0)[1]
                w_scene = ax.c2p(h, 0)[0] - ax.c2p(0, 0)[0]
                rect = Rectangle(width=w_scene, height=h_scene,
                                   color=BLUE, fill_opacity=0.45,
                                   stroke_width=0.5)
                rect.move_to([ax.c2p(x_lo + h / 2, 0)[0],
                              ax.c2p(0, 0)[1] + h_scene / 2, 0])
                grp.add(rect)
            return grp

        self.add(always_redraw(upper_rects), always_redraw(lower_rects))

        def darboux_sums(N):
            N = max(1, min(N, 60))
            h = (b - a) / N
            U_N = 0.0
            L_N = 0.0
            for i in range(N):
                x_lo = a + i * h
                x_hi = x_lo + h
                xs = np.linspace(x_lo, x_hi, 20)
                U_N += float(np.max(f(xs))) * h
                L_N += float(np.min(f(xs))) * h
            return U_N, L_N

        def info():
            N = int(round(N_tr.get_value()))
            U, L = darboux_sums(N)
            gap = U - L
            return VGroup(
                MathTex(rf"N = {N}", color=YELLOW, font_size=24),
                MathTex(rf"U_N = {U:.4f}",
                         color=GREEN, font_size=22),
                MathTex(rf"L_N = {L:.4f}",
                         color=BLUE, font_size=22),
                MathTex(rf"U - L = {gap:.4f}",
                         color=RED, font_size=22),
                MathTex(rf"\int f = {true_int:.4f}",
                         color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for nv in [4, 8, 16, 40]:
            self.play(N_tr.animate.set_value(nv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
