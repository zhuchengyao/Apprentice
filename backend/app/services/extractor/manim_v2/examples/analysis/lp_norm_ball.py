from manim import *
import numpy as np


class LpNormBallExample(Scene):
    """
    L^p norm unit ball: {x : ‖x‖_p ≤ 1} where ‖x‖_p = (|x_1|^p + |x_2|^p)^(1/p).
    For p=1: diamond; p=2: disk; p=∞: square; in between: smooth
    transitions.

    SINGLE_FOCUS:
      Plane with unit ball for varying p; ValueTracker p_tr sweeps
      p ∈ [0.5, 5] + p=∞ (treated as large p).
    """

    def construct(self):
        title = Tex(r"$L^p$ unit ball: $\{x : \|x\|_p \le 1\}$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-1.5, 1.5, 0.5],
                             y_range=[-1.5, 1.5, 0.5],
                             x_length=6, y_length=6,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-1, -0.3, 0])
        self.play(Create(plane))

        p_tr = ValueTracker(2.0)

        def lp_ball():
            p = p_tr.get_value()
            # Parametrize: |x|^p + |y|^p = 1
            # In the first quadrant: x = cos(t)^(2/p), y = sin(t)^(2/p), t in [0, π/2]
            pts = []
            for t in np.linspace(0, 2 * PI, 200):
                c = np.cos(t)
                s = np.sin(t)
                # x = sign(c) |c|^(2/p), y = sign(s) |s|^(2/p)
                if p < 100:
                    x = np.sign(c) * abs(c) ** (2 / p)
                    y = np.sign(s) * abs(s) ** (2 / p)
                else:
                    # L^∞: x = ±1 or y = ±1 depending on max
                    if abs(c) > abs(s):
                        x = np.sign(c)
                        y = s / abs(c) if abs(c) > 1e-4 else 0
                    else:
                        x = c / abs(s) if abs(s) > 1e-4 else 0
                        y = np.sign(s)
                pts.append(plane.c2p(x, y))
            m = VMobject(color=YELLOW, fill_opacity=0.35, stroke_width=3)
            m.set_points_as_corners(pts + [pts[0]])
            return m

        self.add(always_redraw(lp_ball))

        def info():
            p = p_tr.get_value()
            if p < 1:
                shape = "non-convex (not a norm)"
                col = RED
            elif p < 1.3:
                shape = "≈ diamond (L^1)"
                col = BLUE
            elif 1.9 < p < 2.1:
                shape = "≈ disk (L^2)"
                col = GREEN
            elif p > 10:
                shape = "≈ square (L^∞)"
                col = ORANGE
            else:
                shape = "smooth"
                col = YELLOW
            return VGroup(
                MathTex(rf"p = {p:.2f}", color=YELLOW, font_size=24),
                Tex(shape, color=col, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for pv in [0.5, 1.0, 2.0, 4.0, 20.0, 2.0]:
            self.play(p_tr.animate.set_value(pv),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
