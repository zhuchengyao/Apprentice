from manim import *
import numpy as np


class MatrixAssociativeDemoExample(Scene):
    """
    Matrix multiplication IS associative: (AB)C = A(BC).
    Both mean "apply C, then B, then A" — the parentheses don't
    change which transformation applies when.

    Demonstrate with A = rotation -π/6, B = [[2, 1], [1, 2]],
    C = [[1, 0], [1, 1]] (shear). Show same final grid from both
    groupings.
    """

    def construct(self):
        title = Tex(r"$(AB)C = A(BC)$: associativity of matrix multiplication",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([[np.cos(-PI / 6), -np.sin(-PI / 6)],
                       [np.sin(-PI / 6), np.cos(-PI / 6)]])
        B = np.array([[2.0, 1.0], [1.0, 2.0]])
        C = np.array([[1.0, 0.0], [1.0, 1.0]])

        top_center = UP * 1.3
        bot_center = DOWN * 1.7
        scale = 0.28

        t_tr = ValueTracker(0.0)

        # Top: (AB)C — compute AB first, then apply C then AB
        # Actually: since we apply right-to-left: first C, then B, then A.
        # For the "(AB)C" grouping we could just apply the composite (AB) then C,
        # but visually the same deformation. Same for A(BC). They end the same.
        # So to distinguish the groupings visually we animate differently:
        # - Top (AB)C: apply C, then AB as a single step
        # - Bottom A(BC): apply BC as a single step, then A

        AB = A @ B
        BC = B @ C
        full = A @ B @ C

        def M_top(s):
            # 0→1: apply C; 1→2: apply AB afterward (composite)
            if s <= 1:
                return (1 - s) * np.eye(2) + s * C
            alpha = s - 1
            return (1 - alpha) * C + alpha * full

        def M_bot(s):
            # 0→1: apply BC (as composite); 1→2: apply A
            if s <= 1:
                return (1 - s) * np.eye(2) + s * BC
            alpha = s - 1
            return (1 - alpha) * BC + alpha * full

        def to_screen(v, center):
            return np.array([v[0] * scale, v[1] * scale, 0]) + center

        def grid_at(center, M):
            grp = VGroup()
            for k in range(-4, 5):
                pts_h = [to_screen(M @ np.array([x, k]), center) for x in np.linspace(-5, 5, 16)]
                pts_v = [to_screen(M @ np.array([k, y]), center) for y in np.linspace(-5, 5, 16)]
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
                          color=GREEN, buff=0, stroke_width=3)
        def top_j():
            M = M_top(t_tr.get_value())
            p = M @ np.array([0, 1])
            return Arrow(top_center, to_screen(p, top_center),
                          color=RED, buff=0, stroke_width=3)
        def bot_i():
            M = M_bot(t_tr.get_value())
            p = M @ np.array([1, 0])
            return Arrow(bot_center, to_screen(p, bot_center),
                          color=GREEN, buff=0, stroke_width=3)
        def bot_j():
            M = M_bot(t_tr.get_value())
            p = M @ np.array([0, 1])
            return Arrow(bot_center, to_screen(p, bot_center),
                          color=RED, buff=0, stroke_width=3)

        self.add(always_redraw(top_grid), always_redraw(bot_grid),
                 always_redraw(top_i), always_redraw(top_j),
                 always_redraw(bot_i), always_redraw(bot_j))

        # Labels
        top_lbl = Tex(r"$(AB) C$: $C$ then $AB$", color=YELLOW, font_size=22).move_to(
            top_center + LEFT * 4.8)
        bot_lbl = Tex(r"$A (BC)$: $BC$ then $A$", color=YELLOW, font_size=22).move_to(
            bot_center + LEFT * 4.8)
        self.add(top_lbl, bot_lbl)

        # Both end at the same deformation — verify
        def verify_str():
            if t_tr.get_value() < 1.95:
                return ""
            M_t = M_top(t_tr.get_value())
            M_b = M_bot(t_tr.get_value())
            diff = np.max(np.abs(M_t - M_b))
            return rf"both end at same transform: $\|(AB)C - A(BC)\|_\infty={diff:.6f}$"

        verify_tex = Tex(verify_str(), color=GREEN, font_size=24).to_edge(DOWN, buff=0.3)
        self.add(verify_tex)
        def update_verify(mob, dt):
            new = Tex(verify_str(), color=GREEN, font_size=24).move_to(verify_tex)
            verify_tex.become(new)
            return verify_tex
        verify_tex.add_updater(update_verify)

        self.play(t_tr.animate.set_value(1.0), run_time=2.5, rate_func=smooth)
        self.wait(0.5)
        self.play(t_tr.animate.set_value(2.0), run_time=2.5, rate_func=smooth)
        self.wait(1.0)
