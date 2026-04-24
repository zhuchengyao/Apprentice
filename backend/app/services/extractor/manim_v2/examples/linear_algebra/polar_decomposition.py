from manim import *
import numpy as np


class PolarDecompositionExample(Scene):
    """
    Polar decomposition: any invertible A ∈ ℝ^{2×2} factors as A = UP
    with U orthogonal and P symmetric positive definite.

    A = [[2, 1], [0.5, 1.5]]. Compute U and P via SVD:
    A = WΣVᵀ, U = WVᵀ, P = VΣVᵀ.

    TWO_COLUMN: LEFT NumberPlane: unit circle is first stretched
    by P (ellipse), then rotated by U. Morph via ValueTracker s_tr
    from 0 (circle) to 0.5 (ellipse via P) to 1 (rotated = A applied).
    """

    def construct(self):
        A = np.array([[2.0, 1.0], [0.5, 1.5]])
        W, s, Vt = np.linalg.svd(A)
        U = W @ Vt
        V = Vt.T
        P = V @ np.diag(s) @ Vt

        title = Tex(r"Polar: $A=UP$, $U$ orthogonal, $P$ symmetric PD",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3.5, 3.5, 1], y_range=[-2.8, 2.8, 1],
                            x_length=8, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(DOWN * 0.1)
        self.play(Create(plane))

        # Initial unit circle
        unit_r = plane.x_length / (plane.x_range[1] - plane.x_range[0])
        unit = Circle(radius=unit_r, color=BLUE, stroke_width=2,
                      stroke_opacity=0.5).move_to(plane.c2p(0, 0))
        self.add(unit)

        s_tr = ValueTracker(0.0)

        def M_of_s(s):
            # s in [0, 0.5]: apply (1-2s)I + 2s P partial stretching
            # s in [0.5, 1]: from P to UP = A via rotation from I to U
            if s <= 0.5:
                alpha = 2 * s
                return (1 - alpha) * np.eye(2) + alpha * P
            else:
                alpha = 2 * (s - 0.5)
                # rotate P by (1-alpha)I + alpha U
                # Compute rotation R(alpha) from I to U
                angle = np.arctan2(U[1, 0], U[0, 0])
                R_partial = np.array([[np.cos(alpha * angle), -np.sin(alpha * angle)],
                                       [np.sin(alpha * angle), np.cos(alpha * angle)]])
                return R_partial @ P

        def curve():
            M = M_of_s(s_tr.get_value())
            pts = []
            for t in np.linspace(0, TAU, 80):
                v = np.array([np.cos(t), np.sin(t)])
                w = M @ v
                pts.append(plane.c2p(w[0], w[1]))
            return VMobject().set_points_as_corners(pts + [pts[0]])\
                .set_color(YELLOW).set_stroke(width=4)

        # Show basis vectors e1, e2 transformed
        def e1_arrow():
            M = M_of_s(s_tr.get_value())
            v = M @ np.array([1, 0])
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=GREEN, buff=0, stroke_width=3)

        def e2_arrow():
            M = M_of_s(s_tr.get_value())
            v = M @ np.array([0, 1])
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=ORANGE, buff=0, stroke_width=3)

        self.add(always_redraw(curve), always_redraw(e1_arrow),
                 always_redraw(e2_arrow))

        # Stage label
        def stage_str():
            s = s_tr.get_value()
            if s < 0.01: return r"identity"
            if s < 0.49: return r"partial $P$ (stretch)"
            if s < 0.51: return r"after $P$: ellipse"
            if s < 0.99: return r"partial $U$ (rotate)"
            return r"after $UP=A$: rotated ellipse"

        stage_tex = Tex(stage_str(), color=YELLOW, font_size=26).to_edge(DOWN, buff=0.4)
        self.add(stage_tex)
        def update_stage(mob, dt):
            new = Tex(stage_str(), color=YELLOW, font_size=26).move_to(stage_tex)
            stage_tex.become(new)
            return stage_tex
        stage_tex.add_updater(update_stage)

        # Info
        info = VGroup(
            Tex(r"$A=\begin{pmatrix}2&1\\0.5&1.5\end{pmatrix}$", font_size=22),
            VGroup(Tex(r"$s=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"eigenvalues of $P$: $\sigma_1, \sigma_2$",
                color=GREEN, font_size=20),
            Tex(rf"$\sigma_1={s[0]:.3f},\ \sigma_2={s[1]:.3f}$",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(s_tr.get_value()))
        self.add(info)

        self.play(s_tr.animate.set_value(0.5),
                  run_time=3, rate_func=smooth)
        self.wait(0.6)
        self.play(s_tr.animate.set_value(1.0),
                  run_time=3, rate_func=smooth)
        self.wait(0.8)
        self.play(s_tr.animate.set_value(0.0),
                  run_time=2, rate_func=smooth)
        self.wait(0.5)
