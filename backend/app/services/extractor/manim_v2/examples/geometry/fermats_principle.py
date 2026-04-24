from manim import *
import numpy as np


class FermatsPrincipleExample(Scene):
    """
    Fermat's principle: light minimizes total travel time.

    TWO_COLUMN:
      LEFT  — air (top) and water (bottom) meeting at y=0.15. Light goes
              from A in air to B in water via a refraction point P on
              the interface. ValueTracker px slides P horizontally
              along the interface; the broken path A→P→B redraws each
              frame.
      RIGHT — live numerical readouts of |AP|, |PB|, t_air = |AP|/c₁,
              t_water = |PB|/c₂, total time T(px). Plus a mini-axes
              plot below showing T(px) as a curve with a moving marker
              tracking the current px — viewer sees the curve has a
              minimum that Snell's law identifies.
    """

    def construct(self):
        title = Tex(r"Fermat's principle: light minimizes total travel time",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        x_min, x_max = -5.5, +0.5
        air_rect = Rectangle(width=x_max - x_min, height=2.5,
                             color=GREY_C, fill_opacity=0.1, stroke_width=0)
        water_rect = Rectangle(width=x_max - x_min, height=2.5,
                               color=BLUE_E, fill_opacity=0.3, stroke_width=0)
        air_rect.move_to([(x_min + x_max) / 2, +1.4, 0])
        water_rect.move_to([(x_min + x_max) / 2, -1.1, 0])
        interface = Line([x_min, +0.15, 0], [x_max, +0.15, 0],
                         color=WHITE, stroke_width=1.5)
        air_lbl = Tex(r"air ($c_1$)", font_size=22, color=GREY_B).move_to([x_min + 0.7, +2.4, 0])
        water_lbl = Tex(r"water ($c_2 = c_1/1.5$)", font_size=22, color=BLUE).move_to([x_min + 1.5, -2.1, 0])

        self.play(FadeIn(air_rect), FadeIn(water_rect), Create(interface),
                  Write(air_lbl), Write(water_lbl))

        A = np.array([x_min + 0.5, +2.0, 0])
        B = np.array([x_max - 0.5, -2.0, 0])
        a_dot = Dot(A, color=GREEN, radius=0.10)
        b_dot = Dot(B, color=RED, radius=0.10)
        a_lbl = Tex(r"$A$", color=GREEN, font_size=26).next_to(a_dot, UL, buff=0.05)
        b_lbl = Tex(r"$B$", color=RED, font_size=26).next_to(b_dot, DR, buff=0.05)
        self.play(FadeIn(a_dot), Write(a_lbl), FadeIn(b_dot), Write(b_lbl))

        c1 = 1.0
        c2 = c1 / 1.5

        def total_time(px: float) -> float:
            ap = np.linalg.norm(A - np.array([px, +0.15, 0]))
            pb = np.linalg.norm(B - np.array([px, +0.15, 0]))
            return ap / c1 + pb / c2

        px_grid = np.linspace(A[0] + 0.3, B[0] - 0.3, 500)
        opt_px = px_grid[np.argmin([total_time(p) for p in px_grid])]

        px_tr = ValueTracker(A[0] + 0.5)

        def P_pos():
            return np.array([px_tr.get_value(), +0.15, 0])

        def path_AP():
            return Line(A, P_pos(), color=YELLOW, stroke_width=4)

        def path_PB():
            return Line(P_pos(), B, color=YELLOW, stroke_width=4)

        def p_dot():
            return Dot(P_pos(), color=YELLOW, radius=0.09)

        def p_lbl():
            return Tex(r"$P$", color=YELLOW, font_size=22).next_to(p_dot(), UP, buff=0.1)

        self.add(always_redraw(path_AP), always_redraw(path_PB),
                 always_redraw(p_dot), always_redraw(p_lbl))

        rcol_x = +4.4

        def stats_panel():
            px = px_tr.get_value()
            ap = np.linalg.norm(A - np.array([px, +0.15, 0]))
            pb = np.linalg.norm(B - np.array([px, +0.15, 0]))
            T = ap / c1 + pb / c2
            return VGroup(
                MathTex(rf"|AP| = {ap:.3f}", color=GREEN, font_size=22),
                MathTex(rf"|PB| = {pb:.3f}", color=RED, font_size=22),
                MathTex(rf"t_{{\text{{air}}}} = {ap / c1:.3f}",
                        color=GREEN, font_size=22),
                MathTex(rf"t_{{\text{{water}}}} = {pb / c2:.3f}",
                        color=RED, font_size=22),
                MathTex(rf"T = {T:.3f}", color=YELLOW, font_size=28),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +1.6, 0])

        self.add(always_redraw(stats_panel))

        mini_axes = Axes(
            x_range=[A[0] + 0.3, B[0] - 0.3, 1.0],
            y_range=[0, max(total_time(p) for p in px_grid) + 0.5, 1],
            x_length=3.0, y_length=1.6,
            axis_config={"include_tip": False, "include_numbers": False, "font_size": 14},
        ).move_to([rcol_x, -1.8, 0])
        T_curve = mini_axes.plot(total_time,
                                 x_range=[A[0] + 0.3, B[0] - 0.3, 0.05],
                                 color=YELLOW)
        T_lbl = Tex(r"$T(p_x)$", color=YELLOW, font_size=20).next_to(mini_axes, UP, buff=0.1)
        opt_marker = DashedLine(mini_axes.c2p(opt_px, 0),
                                mini_axes.c2p(opt_px, total_time(opt_px)),
                                color=GREEN, stroke_width=2)
        self.play(Create(mini_axes), Create(T_curve), Write(T_lbl), Create(opt_marker))

        def cursor():
            px = px_tr.get_value()
            return Dot(mini_axes.c2p(px, total_time(px)), color=YELLOW, radius=0.07)

        self.add(always_redraw(cursor))

        for target in [B[0] - 0.6, A[0] + 0.5, opt_px]:
            self.play(px_tr.animate.set_value(target),
                      run_time=2.5, rate_func=smooth)
            self.wait(0.4)

        snell = MathTex(r"\frac{\sin\theta_1}{c_1} = \frac{\sin\theta_2}{c_2}\quad(\text{Snell})",
                        color=GREEN, font_size=24).move_to([rcol_x, -3.2, 0])
        self.play(Write(snell))
        self.wait(1.0)
