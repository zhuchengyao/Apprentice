from manim import *
import numpy as np


class GivensRotationExample(Scene):
    """
    Givens rotation G(i, j, θ) is the 2D rotation embedded in the
    (i, j)-plane of ℝⁿ. Used in QR to zero-out specific entries.

    Example: rotate v = (3, 4) into (5, 0). The Givens angle θ
    satisfies cos θ = 3/5, sin θ = -4/5.

    TWO_COLUMN: LEFT NumberPlane with the rotation happening in 2D.
    RIGHT shows 3×3 matrix G(1, 2, θ) and v → Gv with live theta_tr
    sweeping through rotation; trailing arrow marks rotation path.
    """

    def construct(self):
        title = Tex(r"Givens rotation $G(i,j,\theta)$: rotate in $(i,j)$-plane",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-1, 6, 1], y_range=[-1, 5, 1],
                            x_length=5.5, y_length=5.0,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 2.5 + DOWN * 0.3)
        self.play(Create(plane))

        v0 = np.array([3.0, 4.0])
        r = np.linalg.norm(v0)  # 5
        theta_target = -np.arctan2(v0[1], v0[0])  # negative to rotate to +x axis

        theta_tr = ValueTracker(0.0)

        def Rv():
            t = theta_tr.get_value()
            c, s = np.cos(t), np.sin(t)
            return np.array([c * v0[0] - s * v0[1], s * v0[0] + c * v0[1]])

        def v_arrow():
            v = Rv()
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=GREEN, buff=0, stroke_width=4)

        def trail():
            t = theta_tr.get_value()
            ts = np.linspace(0, t, 60) if t > 0.01 else np.linspace(t, 0, 60)
            pts = []
            for tk in ts:
                c, s = np.cos(tk), np.sin(tk)
                v = np.array([c * v0[0] - s * v0[1], s * v0[0] + c * v0[1]])
                pts.append(plane.c2p(v[0], v[1]))
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=2.5)

        def arc_circle():
            return Circle(radius=r * plane.x_length / (plane.x_range[1] - plane.x_range[0]),
                          color=GREY_B, stroke_width=1.5,
                          stroke_opacity=0.5).move_to(plane.c2p(0, 0))

        # Target dot at (5, 0)
        target = Dot(plane.c2p(5, 0), color=RED, radius=0.1)
        target_lbl = Tex(r"$(5, 0)$", color=RED, font_size=20).next_to(target, DOWN, buff=0.1)
        start_lbl = Tex(r"$v_0=(3,4)$", color=GREEN, font_size=20).move_to(plane.c2p(2.5, 4.5))

        self.add(arc_circle(), target, target_lbl, start_lbl)
        self.add(always_redraw(trail), always_redraw(v_arrow))

        # Right column: 3x3 matrix
        def G_matrix_str():
            t = theta_tr.get_value()
            c, s = np.cos(t), np.sin(t)
            return rf"$G=\begin{{pmatrix}}{c:+.3f}&{-s:+.3f}&0\\{s:+.3f}&{c:+.3f}&0\\0&0&1\end{{pmatrix}}$"

        panel = VGroup(
            Tex(G_matrix_str(), font_size=22),
            VGroup(Tex(r"$\theta=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$v_y=$", font_size=22),
                   DecimalNumber(4.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$|v|=$", font_size=22),
                   DecimalNumber(5.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"rotate until $v_y=0$ (QR step)",
                color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)

        def update_panel(mob, dt):
            new = Tex(G_matrix_str(), font_size=22).move_to(panel[0], aligned_edge=LEFT)
            panel[0].become(new)
            return panel
        panel.add_updater(update_panel)

        panel[1][1].add_updater(lambda m: m.set_value(theta_tr.get_value()))
        panel[2][1].add_updater(lambda m: m.set_value(Rv()[1]))
        panel[3][1].add_updater(lambda m: m.set_value(float(np.linalg.norm(Rv()))))
        self.add(panel)

        self.play(theta_tr.animate.set_value(theta_target),
                  run_time=4, rate_func=smooth)
        self.wait(0.8)
