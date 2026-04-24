from manim import *
import numpy as np


class EigenvaluesQuickExample(Scene):
    """
    Eigenvalues found visually: rotate a probe vector around the unit circle,
    measure how much its image deviates from its original direction. Two
    angles where deviation = 0 are exactly the eigenvector directions.

    TWO_COLUMN:
      LEFT  — NumberPlane with a probe arrow (color BLUE) and its image
              under A (color YELLOW). ValueTracker θ rotates probe;
              YELLOW image arrow recomputes via always_redraw. When the
              two arrows align, the marker turns GREEN — that's an
              eigenvector direction.
      RIGHT — live readouts of θ, the angular difference, the scalar
              ratio λ at alignment, plus the characteristic-polynomial
              derivation: det(A−λI) = 0 → λ² − 7λ + 10 = 0 → λ = 2, 5
              and the trace/det shortcut.
    """

    def construct(self):
        title = Tex(r"Eigenvalues of $A = \begin{bmatrix}4 & 1 \\ 2 & 3\end{bmatrix}$ found by rotating a probe",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        A = np.array([[4.0, 1.0],
                      [2.0, 3.0]])
        # Eigenvalues 5, 2 with eigenvectors (1, 1)/√2 and (1, -2)/√5

        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5.4, y_length=5.4,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-3.0, -0.4, 0])
        self.play(Create(plane))

        theta = ValueTracker(0.001)
        probe_len = 1.4

        def probe_vec():
            t = theta.get_value()
            return probe_len * np.array([np.cos(t), np.sin(t)])

        def image_vec():
            return A @ probe_vec()

        def angular_diff_deg():
            t = theta.get_value()
            v = probe_vec()
            iv = image_vec()
            ang_in = np.arctan2(v[1], v[0])
            ang_out = np.arctan2(iv[1], iv[0])
            d = (ang_out - ang_in + PI) % (2 * PI) - PI
            return np.degrees(d)

        def is_aligned():
            return abs(angular_diff_deg()) < 2.0

        def probe_arrow():
            v = probe_vec()
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                         buff=0, color=BLUE, stroke_width=4,
                         max_tip_length_to_length_ratio=0.12)

        def image_arrow():
            iv = image_vec()
            color = GREEN if is_aligned() else YELLOW
            return Arrow(plane.c2p(0, 0), plane.c2p(iv[0], iv[1]),
                         buff=0, color=color, stroke_width=5,
                         max_tip_length_to_length_ratio=0.12)

        # Persistent dashed lines marking the actual eigenvector directions
        ev1 = np.array([1.0, 1.0]) / np.sqrt(2) * 2.5
        ev2 = np.array([1.0, -2.0]) / np.sqrt(5) * 2.5
        ev1_line = DashedLine(plane.c2p(-ev1[0], -ev1[1]), plane.c2p(ev1[0], ev1[1]),
                              color=GREEN, stroke_width=2, stroke_opacity=0.5)
        ev2_line = DashedLine(plane.c2p(-ev2[0], -ev2[1]), plane.c2p(ev2[0], ev2[1]),
                              color=GREEN, stroke_width=2, stroke_opacity=0.5)
        self.play(Create(ev1_line), Create(ev2_line))

        self.add(always_redraw(probe_arrow), always_redraw(image_arrow))

        # RIGHT COLUMN
        rcol_x = +3.6

        def info_panel():
            t = theta.get_value()
            iv = image_vec()
            v = probe_vec()
            ratio = np.linalg.norm(iv) / np.linalg.norm(v)
            diff = angular_diff_deg()
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                        color=BLUE, font_size=22),
                MathTex(rf"|A\mathbf{{v}}|/|\mathbf{{v}}| = {ratio:.3f}",
                        color=YELLOW, font_size=22),
                MathTex(rf"\angle(\mathbf{{v}},A\mathbf{{v}}) = {diff:+.1f}^\circ",
                        color=GREEN if is_aligned() else WHITE, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +2.4, 0])

        self.add(always_redraw(info_panel))

        # Algebraic derivation
        algebra = VGroup(
            MathTex(r"\det(A - \lambda I) = 0", font_size=22, color=WHITE),
            MathTex(r"(4-\lambda)(3-\lambda) - 2 = 0", font_size=22, color=WHITE),
            MathTex(r"\lambda^2 - 7\lambda + 10 = 0", font_size=22, color=WHITE),
            MathTex(r"\lambda = 2 \;\text{or}\; \lambda = 5", font_size=24, color=YELLOW),
            MathTex(r"\text{trace}(A) = 7 = \lambda_1 + \lambda_2", font_size=20, color=GREY_B),
            MathTex(r"\det(A) = 10 = \lambda_1 \cdot \lambda_2", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([rcol_x, -0.8, 0])
        self.play(Write(algebra))

        # Sweep θ through 2π
        self.play(theta.animate.set_value(2 * PI),
                  run_time=8, rate_func=linear)
        self.wait(0.6)
