from manim import *
import numpy as np


class PowerIterationExample(Scene):
    """
    Power iteration: v_{k+1} = A v_k / ‖A v_k‖ converges to the
    dominant eigenvector. Illustrated in 2D with A =
    [[1.5, 0.5], [0.5, 1.0]], eigenvalues ≈ 1.809, 0.691.

    SINGLE_FOCUS:
      2D plane with v_k evolving; always_redraw shows successive
      iterates rotating toward the dominant eigenvector direction.
    """

    def construct(self):
        title = Tex(r"Power iteration: $v_{k+1} = A v_k / \|A v_k\|$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                             x_length=7, y_length=6,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-1, -0.3, 0])
        self.play(Create(plane))

        A = np.array([[1.5, 0.5], [0.5, 1.0]])
        eigvals, eigvecs = np.linalg.eigh(A)
        # Dominant eigenvector (largest eigenvalue)
        idx = np.argmax(eigvals)
        v_dom = eigvecs[:, idx]
        lam_dom = eigvals[idx]

        # Eigenvector line (true direction)
        eig_line = Line(plane.c2p(-2 * v_dom[0], -2 * v_dom[1]),
                          plane.c2p(2 * v_dom[0], 2 * v_dom[1]),
                          color=GREEN, stroke_width=2, stroke_opacity=0.6)
        eig_lbl = MathTex(r"\text{dominant } v_1",
                            color=GREEN, font_size=20
                            ).next_to(plane.c2p(2 * v_dom[0], 2 * v_dom[1]),
                                        UR, buff=0.15)
        self.play(Create(eig_line), Write(eig_lbl))

        # Starting vector v_0 = (1, 0.2)
        v_0 = np.array([1.0, 0.2])
        iterates = [v_0]
        v = v_0.copy()
        for _ in range(15):
            v = A @ v
            v = v / np.linalg.norm(v)
            iterates.append(v.copy())

        step_tr = ValueTracker(0)

        def current_v():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(iterates) - 1))
            v = iterates[s]
            return Arrow(plane.c2p(0, 0), plane.c2p(*v),
                          color=YELLOW, buff=0, stroke_width=5,
                          max_tip_length_to_length_ratio=0.15)

        def trail():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(iterates) - 1))
            grp = VGroup()
            for i in range(s + 1):
                col = interpolate_color(BLUE, YELLOW, i / max(1, len(iterates) - 1))
                v = iterates[i]
                grp.add(Arrow(plane.c2p(0, 0), plane.c2p(*v),
                                color=col, buff=0, stroke_width=2,
                                stroke_opacity=0.5,
                                max_tip_length_to_length_ratio=0.1))
            return grp

        self.add(always_redraw(trail), always_redraw(current_v))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(iterates) - 1))
            v = iterates[s]
            # Angle from dominant
            cos_sim = abs(np.dot(v, v_dom))
            angle_deg = np.degrees(np.arccos(min(cos_sim, 1)))
            return VGroup(
                MathTex(rf"k = {s}", color=YELLOW, font_size=22),
                MathTex(rf"v_k = ({v[0]:+.3f}, {v[1]:+.3f})",
                         color=YELLOW, font_size=18),
                MathTex(rf"\angle(v_k, v_1) = {angle_deg:.2f}^\circ",
                         color=GREEN, font_size=20),
                MathTex(rf"\lambda_1 = {lam_dom:.3f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for sv in [1, 3, 6, 10, 15]:
            self.play(step_tr.animate.set_value(sv),
                       run_time=1.2, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
