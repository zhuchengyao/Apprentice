from manim import *
import numpy as np


class CostFunctionIntuitionExample(Scene):
    """
    Cost-function intuition (from _2017/nn/part1): a 2D cost
    surface C(w_1, w_2) with contour plot; visualize how "finding
    the minimum" means descending opposite to the gradient.

    SINGLE_FOCUS:
      NumberPlane with cost contours (ellipses); ValueTracker s_tr
      advances a precomputed Newton-descent trajectory over 10 steps;
      always_redraw trajectory + gradient arrow at current position.
    """

    def construct(self):
        title = Tex(r"Cost function: $C(w_1, w_2) = 2w_1^2 + 5w_2^2 + w_1 w_2$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                             x_length=8, y_length=5.5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-1, -0.3, 0])
        self.play(Create(plane))

        def C(w1, w2):
            return 2 * w1 ** 2 + 5 * w2 ** 2 + w1 * w2

        def grad_C(w1, w2):
            return np.array([4 * w1 + w2, 10 * w2 + w1])

        # Contour ellipses
        contours = VGroup()
        for level in [0.5, 1.5, 3.5, 7, 12, 20]:
            pts = []
            for a in np.linspace(0, 2 * PI, 90):
                # Solve C(r cos a, r sin a) = level
                f_val = 2 * np.cos(a) ** 2 + 5 * np.sin(a) ** 2 + np.cos(a) * np.sin(a)
                r = np.sqrt(level / f_val)
                pts.append(plane.c2p(r * np.cos(a), r * np.sin(a)))
            m = VMobject(color=BLUE_D, stroke_width=1.5,
                           stroke_opacity=0.6)
            m.set_points_as_corners(pts + [pts[0]])
            contours.add(m)
        self.play(Create(contours))

        # Precompute GD trajectory from (2.5, 1.8) with small LR
        eta = 0.08
        n_steps = 20
        w = np.array([2.5, 1.8])
        traj = [w.copy()]
        for _ in range(n_steps):
            g = grad_C(w[0], w[1])
            w = w - eta * g
            traj.append(w.copy())

        step_tr = ValueTracker(0)

        def trajectory():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, n_steps))
            pts = [plane.c2p(*traj[k]) for k in range(s + 1)]
            m = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def cur_dot():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, n_steps))
            return Dot(plane.c2p(*traj[s]), color=YELLOW, radius=0.12)

        def grad_arrow():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, n_steps))
            pos = traj[s]
            g = grad_C(pos[0], pos[1])
            # draw arrow pointing -g (descent direction) scaled
            mag = np.linalg.norm(g)
            if mag < 1e-4:
                return VGroup()
            scale = 0.4 / max(mag, 0.4)
            start = plane.c2p(*pos)
            end = plane.c2p(pos[0] - scale * g[0],
                              pos[1] - scale * g[1])
            return Arrow(start, end, color=RED, buff=0,
                          stroke_width=5,
                          max_tip_length_to_length_ratio=0.2)

        self.add(always_redraw(trajectory),
                  always_redraw(cur_dot),
                  always_redraw(grad_arrow))

        # Origin (min)
        min_dot = Dot(plane.c2p(0, 0), color=GREEN, radius=0.1)
        min_lbl = Tex(r"min", color=GREEN,
                       font_size=18).next_to(min_dot, DR, buff=0.05)
        self.play(FadeIn(min_dot), Write(min_lbl))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, n_steps))
            w = traj[s]
            cost = C(w[0], w[1])
            g = grad_C(w[0], w[1])
            return VGroup(
                MathTex(rf"\text{{step}} = {s}",
                         color=WHITE, font_size=22),
                MathTex(rf"w = ({w[0]:+.2f}, {w[1]:+.2f})",
                         color=YELLOW, font_size=22),
                MathTex(rf"C(w) = {cost:.3f}",
                         color=BLUE, font_size=22),
                MathTex(rf"\|\nabla C\| = {np.linalg.norm(g):.3f}",
                         color=RED, font_size=22),
                Tex(r"RED arrow: $-\nabla C$", color=RED, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(step_tr.animate.set_value(n_steps),
                   run_time=6, rate_func=linear)
        self.wait(0.4)
