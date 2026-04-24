from manim import *
import numpy as np


class MatrixNoncommutativeDemoExample(Scene):
    """
    Matrix multiplication is not commutative: M_1 M_2 ≠ M_2 M_1.
    Demonstrate with rotation R (90° CCW) and shear S.

    COMPARISON: top shows "shear then rotation" (R·S), bottom shows
    "rotation then shear" (S·R). Final î, ĵ positions differ.
    """

    def construct(self):
        title = Tex(r"$M_1 M_2 \ne M_2 M_1$: order matters",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = np.array([[0.0, -1.0], [1.0, 0.0]])  # 90° CCW
        S = np.array([[1.0, 1.0], [0.0, 1.0]])

        # Top: shear then rotation → apply S first, then R. Composite R·S.
        # Bottom: rotation then shear → apply R first, then S. Composite S·R.
        top_center = UP * 1.5
        bot_center = DOWN * 1.5
        scale = 0.4

        t_tr = ValueTracker(0.0)

        def M_top(s):
            # s ∈ [0, 2]: first apply S, then R
            if s <= 1:
                return (1 - s) * np.eye(2) + s * S
            alpha = s - 1
            return (1 - alpha) * S + alpha * (R @ S)

        def M_bot(s):
            # bottom: first apply R, then S
            if s <= 1:
                return (1 - s) * np.eye(2) + s * R
            alpha = s - 1
            return (1 - alpha) * R + alpha * (S @ R)

        def to_screen(v, center):
            return np.array([v[0] * scale, v[1] * scale, 0]) + center

        def grid_at(center, M):
            grp = VGroup()
            for k in range(-3, 4):
                pts_h = [to_screen(M @ np.array([x, k]), center) for x in np.linspace(-4, 4, 15)]
                pts_v = [to_screen(M @ np.array([k, y]), center) for y in np.linspace(-4, 4, 15)]
                grp.add(VMobject().set_points_as_corners(pts_h)
                         .set_color(BLUE).set_stroke(width=1, opacity=0.6))
                grp.add(VMobject().set_points_as_corners(pts_v)
                         .set_color(ORANGE).set_stroke(width=1, opacity=0.6))
            return grp

        def top_grid():
            return grid_at(top_center, M_top(t_tr.get_value()))
        def bot_grid():
            return grid_at(bot_center, M_bot(t_tr.get_value()))

        def top_i():
            M = M_top(t_tr.get_value())
            p = M @ np.array([1, 0])
            return Arrow(top_center, to_screen(p, top_center),
                          color=GREEN, buff=0, stroke_width=4)
        def top_j():
            M = M_top(t_tr.get_value())
            p = M @ np.array([0, 1])
            return Arrow(top_center, to_screen(p, top_center),
                          color=RED, buff=0, stroke_width=4)
        def bot_i():
            M = M_bot(t_tr.get_value())
            p = M @ np.array([1, 0])
            return Arrow(bot_center, to_screen(p, bot_center),
                          color=GREEN, buff=0, stroke_width=4)
        def bot_j():
            M = M_bot(t_tr.get_value())
            p = M @ np.array([0, 1])
            return Arrow(bot_center, to_screen(p, bot_center),
                          color=RED, buff=0, stroke_width=4)

        self.add(always_redraw(top_grid), always_redraw(bot_grid),
                 always_redraw(top_i), always_redraw(top_j),
                 always_redraw(bot_i), always_redraw(bot_j))

        # Labels
        top_lbl = Tex(r"shear then rotation: $R\cdot S$",
                       color=YELLOW, font_size=22).move_to(top_center + LEFT * 4.3)
        bot_lbl = Tex(r"rotation then shear: $S\cdot R$",
                       color=YELLOW, font_size=22).move_to(bot_center + LEFT * 4.3)
        self.add(top_lbl, bot_lbl)

        # Final matrix results
        RS = R @ S  # shear then rotation → composite is R·S = [[0, -1], [1, 1]]
        SR = S @ R  # rotation then shear → composite is S·R = [[1, -1], [1, 0]]

        # Display after t=2
        def top_result():
            if t_tr.get_value() < 1.95:
                return VMobject()
            return MathTex(rf"R S=\begin{{pmatrix}}{RS[0, 0]:+.0f}&{RS[0, 1]:+.0f}\\{RS[1, 0]:+.0f}&{RS[1, 1]:+.0f}\end{{pmatrix}}",
                            color=YELLOW, font_size=24).move_to(
                top_center + RIGHT * 4.3)

        def bot_result():
            if t_tr.get_value() < 1.95:
                return VMobject()
            return MathTex(rf"S R=\begin{{pmatrix}}{SR[0, 0]:+.0f}&{SR[0, 1]:+.0f}\\{SR[1, 0]:+.0f}&{SR[1, 1]:+.0f}\end{{pmatrix}}",
                            color=YELLOW, font_size=24).move_to(
                bot_center + RIGHT * 4.3)

        self.add(always_redraw(top_result), always_redraw(bot_result))

        # Noncommutative stamp
        neq_tex = MathTex(r"R S\neq S R", color=RED, font_size=32).to_edge(DOWN, buff=0.3)

        self.play(t_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.4)
        self.play(t_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(Write(neq_tex))
        self.wait(1.0)
