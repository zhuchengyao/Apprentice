from manim import *
import numpy as np


class SoftmaxGradientFlowExample(Scene):
    """
    Softmax gradient: ∂p_i/∂z_j = p_i(δ_ij − p_j). Jacobian is
    p·diag(1) − p·p^T. Visualize Jacobian for 4-class softmax as
    heatmap; trace gradient vector field on simplex.

    SINGLE_FOCUS: 4×4 Jacobian heatmap with current logit via
    ValueTracker scale_tr; always_redraw recolors cells with
    computed Jacobian values. Live p vector + diagonal vs
    off-diagonal dominance explanation.
    """

    def construct(self):
        title = Tex(r"Softmax Jacobian: $\partial p_i/\partial z_j = p_i(\delta_{ij}-p_j)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 4
        logits_base = np.array([1.0, 0.5, -0.5, -1.0])

        scale_tr = ValueTracker(0.5)  # multiply logits by this

        def softmax(z):
            z = z - z.max()
            e = np.exp(z)
            return e / e.sum()

        def current_p():
            return softmax(logits_base * scale_tr.get_value())

        def jacobian():
            p = current_p()
            J = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    J[i, j] = p[i] * ((1 if i == j else 0) - p[j])
            return J

        cell_s = 0.9
        origin = np.array([-2.0, 0.8, 0])

        def heatmap():
            J = jacobian()
            grp = VGroup()
            for i in range(n):
                for j in range(n):
                    v = J[i, j]
                    if v >= 0:
                        col = interpolate_color(GREY_D, GREEN, min(1, v * 3))
                    else:
                        col = interpolate_color(GREY_D, RED, min(1, -v * 3))
                    rect = Square(side_length=cell_s * 0.9,
                                   color=col, stroke_width=1,
                                   fill_color=col, fill_opacity=0.85).move_to(
                        origin + RIGHT * j * cell_s - UP * i * cell_s)
                    lbl = Tex(f"{v:+.3f}", font_size=14).move_to(rect)
                    grp.add(rect, lbl)
            return grp

        self.add(always_redraw(heatmap))

        # Labels
        for i in range(n):
            self.add(Tex(rf"$i={i+1}$", font_size=18, color=BLUE).move_to(
                origin + LEFT * 0.7 - UP * i * cell_s))
            self.add(Tex(rf"$j={i+1}$", font_size=18, color=BLUE).move_to(
                origin + UP * 0.7 + RIGHT * i * cell_s))

        info = VGroup(
            VGroup(Tex(r"logit scale $=$", font_size=22),
                   DecimalNumber(0.5, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$p_1=$", font_size=20),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=20).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$p_2=$", font_size=20),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=20).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$p_3=$", font_size=20),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=20).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$p_4=$", font_size=20),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=20).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(r"diagonal $=p_i(1-p_i)\ge 0$",
                color=GREEN, font_size=18),
            Tex(r"off-diagonal $=-p_ip_j\le 0$",
                color=RED, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(scale_tr.get_value()))
        for k in range(n):
            info[k + 1][1].add_updater(lambda m, kk=k: m.set_value(current_p()[kk]))
        self.add(info)

        for sval in [1.5, 3.0, 0.1, 5.0, 1.0]:
            self.play(scale_tr.animate.set_value(sval),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
