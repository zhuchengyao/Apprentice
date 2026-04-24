from manim import *
import numpy as np


class RandomWalkReflectionExample(Scene):
    """
    Reflection principle: the number of paths from (0, 0) to (N, k)
    that touch or cross level a is equal to the number of paths
    from (0, 2a - 0) to (N, k) (reflected start). Used to derive
    first-passage probabilities.

    SINGLE_FOCUS:
      Random walk path on grid; ValueTracker t_tr advances; when
      path hits barrier a=3, draw reflected mirror path above.
    """

    def construct(self):
        title = Tex(r"Reflection principle for random walks",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        N = 16
        a = 3  # barrier level

        ax = Axes(x_range=[0, N, 2], y_range=[-1, 8, 2],
                   x_length=10, y_length=4.5, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-0.5, -0.3, 0])
        self.play(Create(ax))

        # Barrier line
        barrier = DashedLine(ax.c2p(0, a), ax.c2p(N, a),
                               color=RED, stroke_width=3)
        barrier_lbl = MathTex(rf"a = {a}", color=RED, font_size=22
                                ).next_to(ax.c2p(N, a), RIGHT, buff=0.15)
        self.play(Create(barrier), Write(barrier_lbl))

        # Precompute a walk that touches a at some step
        rng = np.random.default_rng(27)
        while True:
            steps = rng.choice([-1, 1], size=N)
            path = np.concatenate([[0], np.cumsum(steps)])
            # Check if touches a=3
            touches_idx = np.where(path >= a)[0]
            if len(touches_idx) > 0 and path[-1] == 2:
                break

        hit_idx = int(touches_idx[0])

        t_tr = ValueTracker(0)

        def original_trail():
            t = int(round(t_tr.get_value()))
            t = max(1, min(t, N))
            pts = [ax.c2p(i, path[i]) for i in range(t + 1)]
            m = VMobject(color=BLUE, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def original_dot():
            t = int(round(t_tr.get_value()))
            t = max(0, min(t, N))
            return Dot(ax.c2p(t, path[t]), color=BLUE, radius=0.1)

        def reflected_trail():
            t = int(round(t_tr.get_value()))
            if t <= hit_idx:
                return VMobject()
            # Reflected path: after hitting barrier, flip the
            # subsequent displacements
            reflected = path.copy()
            for i in range(hit_idx + 1, t + 1):
                reflected[i] = 2 * a - path[i]
            pts = [ax.c2p(i, reflected[i]) for i in range(t + 1)]
            m = VMobject(color=ORANGE, stroke_width=3,
                           stroke_opacity=0.75)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def reflected_dot():
            t = int(round(t_tr.get_value()))
            if t <= hit_idx:
                return Dot()
            reflected_y = 2 * a - path[t]
            return Dot(ax.c2p(t, reflected_y),
                        color=ORANGE, radius=0.1)

        self.add(always_redraw(original_trail),
                  always_redraw(reflected_trail),
                  always_redraw(original_dot),
                  always_redraw(reflected_dot))

        def info():
            t = int(round(t_tr.get_value()))
            t = max(0, min(t, N))
            touches = path[t] >= a or any(path[:t + 1] >= a)
            return VGroup(
                MathTex(rf"t = {t}", color=WHITE, font_size=22),
                MathTex(rf"S_t = {path[t]}", color=BLUE, font_size=22),
                Tex(rf"touched $a$ at $t = {hit_idx}$" if t > hit_idx else "not yet touched",
                     color=RED if t <= hit_idx else GREEN, font_size=20),
                MathTex(r"\text{reflection: } S'_t = 2a - S_t",
                         color=ORANGE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(N),
                   run_time=9, rate_func=linear)
        self.wait(0.4)
