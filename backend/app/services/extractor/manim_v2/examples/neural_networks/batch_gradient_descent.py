from manim import *
import numpy as np


class BatchGradientDescentExample(Scene):
    """
    Compare SGD (batch=1), minibatch (batch=10), full-batch on a
    noisy 2D quadratic loss f(w_1, w_2) = ½(w_1² + 3w_2²) + noise.
    Full batch descent is smooth; SGD wanders; minibatch in between.

    TWO_COLUMN: LEFT contour plot with 3 traces (BLUE full-batch,
    GREEN minibatch, ORANGE SGD). ValueTracker t_tr reveals paths.
    RIGHT current losses + average.
    """

    def construct(self):
        title = Tex(r"GD batch size tradeoff: noise vs speed",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                    x_length=6.0, y_length=4.0,
                    axis_config={"include_numbers": False}).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(axes))

        # Contours
        def contour(lvl):
            pts = []
            for t in np.linspace(0, TAU, 80):
                rx = np.sqrt(2 * lvl)
                ry = np.sqrt(2 * lvl / 3)
                pts.append(axes.c2p(rx * np.cos(t), ry * np.sin(t)))
            return VMobject().set_points_as_corners(pts + [pts[0]])\
                .set_color(GREY_B).set_stroke(width=1.5, opacity=0.45)

        self.add(VGroup(*[contour(l) for l in [0.2, 0.6, 1.2, 2.0, 3.0]]))

        # Simulate trajectories
        np.random.seed(3)
        start = np.array([2.5, 1.6])
        lr = 0.08
        N = 80

        def grad(w, noise_scale):
            g = np.array([w[0], 3 * w[1]])
            if noise_scale > 0:
                g = g + np.random.randn(2) * noise_scale
            return g

        full = [start.copy()]
        mini = [start.copy()]
        sgd = [start.copy()]
        for _ in range(N):
            full.append(full[-1] - lr * grad(full[-1], 0.0))
            mini.append(mini[-1] - lr * grad(mini[-1], 0.5))
            sgd.append(sgd[-1] - lr * grad(sgd[-1], 2.0))
        full = np.array(full)
        mini = np.array(mini)
        sgd = np.array(sgd)

        t_tr = ValueTracker(0.0)

        def make_trail(arr, col):
            def builder():
                k = max(1, min(N, int(round(t_tr.get_value()))))
                pts = [axes.c2p(p[0], p[1]) for p in arr[:k + 1]]
                return VMobject().set_points_as_corners(pts).set_color(col).set_stroke(width=2.5)
            return builder

        def make_dot(arr, col):
            def builder():
                k = max(0, min(N, int(round(t_tr.get_value()))))
                return Dot(axes.c2p(arr[k][0], arr[k][1]),
                            color=col, radius=0.1)
            return builder

        self.add(always_redraw(make_trail(full, BLUE)),
                 always_redraw(make_trail(mini, GREEN)),
                 always_redraw(make_trail(sgd, ORANGE)),
                 always_redraw(make_dot(full, BLUE)),
                 always_redraw(make_dot(mini, GREEN)),
                 always_redraw(make_dot(sgd, ORANGE)))

        # Min marker
        self.add(Dot(axes.c2p(0, 0), color=YELLOW, radius=0.09))

        def k_now():
            return max(0, min(N, int(round(t_tr.get_value()))))

        def loss(w):
            return 0.5 * (w[0] ** 2 + 3 * w[1] ** 2)

        info = VGroup(
            VGroup(Tex(r"iter $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"full-batch", color=BLUE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"minibatch", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"SGD", color=ORANGE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(r"full: smooth convergence",
                color=BLUE, font_size=18),
            Tex(r"SGD: noisy, wanders",
                color=ORANGE, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(k_now()))
        info[1][1].add_updater(lambda m: m.set_value(loss(full[k_now()])))
        info[2][1].add_updater(lambda m: m.set_value(loss(mini[k_now()])))
        info[3][1].add_updater(lambda m: m.set_value(loss(sgd[k_now()])))
        self.add(info)

        self.play(t_tr.animate.set_value(float(N)),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
