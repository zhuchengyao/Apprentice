from manim import *
import numpy as np


class ConditionNumberExample(Scene):
    """
    Condition number κ(A) = σ_max / σ_min controls error amplification.
    Compare well-conditioned (A=I) vs moderately conditioned (κ≈10)
    vs ill-conditioned (κ≈1000).

    TWO_COLUMN: LEFT grid: unit circle of inputs x with perturbation
    δx=0.05·(cos θ, sin θ) morphs with ValueTracker θ_tr; output ellipse
    Ax shown stretched; error |A δx| / |A x| tracked. RIGHT shows the
    3 matrices, their κ values, and live error amplification.
    """

    def construct(self):
        title = Tex(r"Condition number: $\kappa(A)=\sigma_{\max}/\sigma_{\min}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1],
                    x_length=6.0, y_length=4.0,
                    axis_config={"include_numbers": False}).shift(LEFT * 2.3 + DOWN * 0.3)
        self.play(Create(axes))

        # Matrices
        A_list = [
            ("$A_1=I$", np.eye(2)),
            ("$A_2=\\mathrm{diag}(3, 0.3)$", np.diag([3.0, 0.3])),
            ("$A_3=\\mathrm{diag}(10, 0.01)$", np.diag([10.0, 0.01])),
        ]
        colors = [BLUE, GREEN, RED]

        # Static unit circle for reference
        unit = Circle(radius=1.0, color=YELLOW, stroke_width=2).move_to(axes.c2p(0, 0))
        unit_lbl = Tex(r"$\|x\|=1$", color=YELLOW, font_size=20).next_to(unit, UR, buff=0.05)
        self.play(Create(unit), Write(unit_lbl))

        # Draw output ellipses
        ellipses = VGroup()
        for i, (name, A) in enumerate(A_list):
            U, s, Vt = np.linalg.svd(A)
            # ellipse = A · (unit circle)
            pts = []
            for t in np.linspace(0, TAU, 80):
                v = A @ np.array([np.cos(t), np.sin(t)])
                pts.append(axes.c2p(v[0], v[1]))
            e = VMobject().set_points_as_corners(pts + [pts[0]])\
                .set_color(colors[i]).set_stroke(width=2)
            ellipses.add(e)
        self.play(Create(ellipses, lag_ratio=0.3))

        theta_tr = ValueTracker(0.0)

        def probe_in():
            t = theta_tr.get_value()
            return Dot(axes.c2p(np.cos(t), np.sin(t)),
                        color=YELLOW, radius=0.08)

        def probe_out(A, col):
            def f():
                t = theta_tr.get_value()
                v = A @ np.array([np.cos(t), np.sin(t)])
                return Dot(axes.c2p(v[0], v[1]), color=col, radius=0.08)
            return f

        self.add(always_redraw(probe_in))
        for i, (name, A) in enumerate(A_list):
            self.add(always_redraw(probe_out(A, colors[i])))

        # Right column
        def amp(A):
            t = theta_tr.get_value()
            x = np.array([np.cos(t), np.sin(t)])
            dx = np.array([-np.sin(t), np.cos(t)]) * 0.05  # tangent
            ax = A @ x
            adx = A @ dx
            if np.linalg.norm(ax) < 1e-9:
                return 0.0
            return float((np.linalg.norm(adx) / np.linalg.norm(ax)) / (np.linalg.norm(dx) / np.linalg.norm(x)))

        info = VGroup(
            Tex(A_list[0][0] + r":\ $\kappa=1$", color=BLUE, font_size=22),
            VGroup(Tex(r"amp$_1=$", color=BLUE, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(A_list[1][0] + r":\ $\kappa=10$", color=GREEN, font_size=22),
            VGroup(Tex(r"amp$_2=$", color=GREEN, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(A_list[2][0] + r":\ $\kappa=1000$", color=RED, font_size=22),
            VGroup(Tex(r"amp$_3=$", color=RED, font_size=22),
                   DecimalNumber(1.0, num_decimal_places=3,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)

        info[1][1].add_updater(lambda m: m.set_value(amp(A_list[0][1])))
        info[3][1].add_updater(lambda m: m.set_value(amp(A_list[1][1])))
        info[5][1].add_updater(lambda m: m.set_value(amp(A_list[2][1])))
        self.add(info)

        self.play(theta_tr.animate.set_value(TAU),
                  run_time=6, rate_func=linear)
        self.wait(0.5)
