from manim import *
import numpy as np


class RandomWalkReturnExample(Scene):
    """
    Pólya's theorem: a simple random walk on ℤ returns to the origin
    with probability 1 (recurrent); in ℤ³ it returns with probability
    ≈ 0.3405 (transient).

    COMPARISON:
      LEFT  — 1D random walk on a number line; always_redraw dot at
              current position + return counter; walk precomputed.
      RIGHT — 3D random walk projected to its distance from origin;
              the distance grows ~√t; the walker rarely returns.
    """

    def construct(self):
        title = Tex(r"Pólya's theorem: walk returns w.p.\ $1$ in $\mathbb Z^1$, not in $\mathbb Z^3$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rng = np.random.default_rng(8)
        N_STEPS = 400

        # LEFT: 1D walk
        nl = NumberLine(x_range=[-25, 25, 5], length=6,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 0,
                                                 "font_size": 14}
                         ).move_to([-3.5, 0.5, 0])
        nl_lbl = Tex(r"$\mathbb Z^1$ walk",
                      color=BLUE, font_size=20).next_to(nl, UP, buff=0.2)
        self.play(Create(nl), Write(nl_lbl))

        # Precompute 1D walk
        steps1 = rng.choice([-1, 1], size=N_STEPS)
        pos1 = np.concatenate([[0], np.cumsum(steps1)])
        returns1 = [int(p == 0) for p in pos1]
        cum_ret1 = np.cumsum(returns1)

        # Precompute 3D walk
        dirs3 = rng.choice(6, size=N_STEPS)
        unit = np.array([[1, 0, 0], [-1, 0, 0],
                         [0, 1, 0], [0, -1, 0],
                         [0, 0, 1], [0, 0, -1]])
        walk3 = np.cumsum(np.vstack([np.zeros(3), unit[dirs3]]), axis=0)
        dist3 = np.linalg.norm(walk3, axis=1)
        returns3 = [int(np.all(walk3[k] == 0)) for k in range(len(walk3))]
        cum_ret3 = np.cumsum(returns3)

        # RIGHT: 3D walk distance plot
        ax3 = Axes(x_range=[0, N_STEPS, N_STEPS // 4],
                    y_range=[0, 30, 5],
                    x_length=5, y_length=4.5, tips=False,
                    axis_config={"font_size": 14, "include_numbers": True}
                    ).move_to([3.0, -0.7, 0])
        ax3_lbl = Tex(r"$\mathbb Z^3$ distance",
                       color=ORANGE, font_size=20).next_to(ax3, UP, buff=0.15)
        self.play(Create(ax3), Write(ax3_lbl))

        # √t reference
        sqrt_t = ax3.plot(lambda t: np.sqrt(t), x_range=[1, N_STEPS],
                           color=GREY_B, stroke_width=2)
        sqrt_lbl = MathTex(r"\sqrt t", color=GREY_B, font_size=18
                             ).move_to(ax3.c2p(N_STEPS * 0.8,
                                                 np.sqrt(N_STEPS * 0.8) + 2))
        self.play(Create(sqrt_t), Write(sqrt_lbl))

        t_tr = ValueTracker(0.0)

        def walker_1d():
            t = int(round(t_tr.get_value() * N_STEPS))
            t = max(0, min(t, N_STEPS))
            return Dot(nl.n2p(pos1[t]), color=BLUE, radius=0.12)

        def trail_3d():
            t = int(round(t_tr.get_value() * N_STEPS))
            t = max(1, min(t, N_STEPS))
            pts = [ax3.c2p(k, dist3[k]) for k in range(t + 1)]
            v = VMobject(color=ORANGE, stroke_width=3)
            v.set_points_as_corners(pts)
            return v

        def dot_3d():
            t = int(round(t_tr.get_value() * N_STEPS))
            t = max(0, min(t, N_STEPS))
            return Dot(ax3.c2p(t, dist3[t]), color=ORANGE, radius=0.1)

        self.add(always_redraw(walker_1d),
                  always_redraw(trail_3d),
                  always_redraw(dot_3d))

        def info():
            t = int(round(t_tr.get_value() * N_STEPS))
            t = max(0, min(t, N_STEPS))
            p1 = pos1[t]
            r1 = cum_ret1[t] if t < len(cum_ret1) else 0
            d3 = dist3[t]
            r3 = cum_ret3[t] if t < len(cum_ret3) else 0
            return VGroup(
                MathTex(rf"t = {t}", color=WHITE, font_size=22),
                MathTex(rf"\mathbb Z^1: \text{{pos}} = {p1:+d},\ \text{{returns}} = {r1}",
                         color=BLUE, font_size=20),
                MathTex(rf"\mathbb Z^3: \text{{dist}} = {d3:.2f},\ \text{{returns}} = {r3}",
                         color=ORANGE, font_size=20),
                MathTex(r"P_\infty(\text{return}) = 1 \text{ in } \mathbb Z^1",
                         color=BLUE, font_size=18),
                MathTex(r"P_\infty(\text{return}) \approx 0.34 \text{ in } \mathbb Z^3",
                         color=ORANGE, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.25)

        self.add(always_redraw(info))

        self.play(t_tr.animate.set_value(1.0),
                   run_time=10, rate_func=linear)
        self.wait(0.5)
