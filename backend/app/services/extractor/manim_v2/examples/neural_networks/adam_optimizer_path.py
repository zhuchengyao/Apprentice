from manim import *
import numpy as np


class AdamOptimizerPathExample(Scene):
    """
    Adam optimizer: adaptive per-parameter learning rates using
    first and second moment estimates.
      m_t = β_1 m_{t-1} + (1-β_1) g_t
      v_t = β_2 v_{t-1} + (1-β_2) g_t²
      θ_t = θ_{t-1} - η m̂_t / (√v̂_t + ε)

    Compare Adam, SGD, SGD+momentum on anisotropic quadratic.

    TWO_COLUMN: contours + 3 paths overlaid.
    """

    def construct(self):
        title = Tex(r"Adam vs SGD vs Momentum on anisotropic loss",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                    x_length=6.5, y_length=4.5,
                    axis_config={"include_numbers": False}).shift(LEFT * 2.0 + DOWN * 0.2)
        self.play(Create(axes))

        # Loss f = 0.5 * (a x² + b y²) with a=0.1, b=2
        a_param, b_param = 0.1, 2.0

        def contour(lvl):
            pts = []
            for t in np.linspace(0, TAU, 80):
                rx = np.sqrt(2 * lvl / a_param)
                ry = np.sqrt(2 * lvl / b_param)
                pts.append(axes.c2p(rx * np.cos(t), ry * np.sin(t)))
            return VMobject().set_points_as_corners(pts + [pts[0]])\
                .set_color(GREY_B).set_stroke(width=1.5, opacity=0.45)

        self.add(VGroup(*[contour(l) for l in [0.15, 0.5, 1.0, 1.6, 2.3]]))

        # Simulate
        def grad(w):
            return np.array([a_param * w[0], b_param * w[1]])

        start = np.array([2.8, 2.0])
        N = 100
        lr = 0.08

        # SGD
        sgd_path = [start.copy()]
        for _ in range(N):
            sgd_path.append(sgd_path[-1] - lr * grad(sgd_path[-1]))

        # Momentum (beta=0.9)
        mom_path = [start.copy()]
        v = np.zeros(2)
        for _ in range(N):
            v = 0.9 * v - lr * grad(mom_path[-1])
            mom_path.append(mom_path[-1] + v)

        # Adam
        adam_path = [start.copy()]
        m = np.zeros(2)
        V = np.zeros(2)
        b1, b2, eps = 0.9, 0.999, 1e-8
        lr_adam = 0.15
        for t in range(1, N + 1):
            g = grad(adam_path[-1])
            m = b1 * m + (1 - b1) * g
            V = b2 * V + (1 - b2) * g * g
            m_hat = m / (1 - b1 ** t)
            v_hat = V / (1 - b2 ** t)
            adam_path.append(adam_path[-1] - lr_adam * m_hat / (np.sqrt(v_hat) + eps))

        sgd_path = np.array(sgd_path)
        mom_path = np.array(mom_path)
        adam_path = np.array(adam_path)

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
                return Dot(axes.c2p(arr[k][0], arr[k][1]), color=col, radius=0.1)
            return builder

        self.add(always_redraw(make_trail(sgd_path, ORANGE)),
                 always_redraw(make_trail(mom_path, GREEN)),
                 always_redraw(make_trail(adam_path, BLUE)),
                 always_redraw(make_dot(sgd_path, ORANGE)),
                 always_redraw(make_dot(mom_path, GREEN)),
                 always_redraw(make_dot(adam_path, BLUE)))

        self.add(Dot(axes.c2p(0, 0), color=YELLOW, radius=0.09))

        def k_now():
            return max(0, min(N, int(round(t_tr.get_value()))))

        def loss_at(p):
            return 0.5 * (a_param * p[0] ** 2 + b_param * p[1] ** 2)

        info = VGroup(
            VGroup(Tex(r"iter $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"SGD loss $=$", color=ORANGE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"momentum loss $=$", color=GREEN, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"Adam loss $=$", color=BLUE, font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(r"Adam adapts per-dim learning rates",
                color=BLUE, font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2)
        info[0][1].add_updater(lambda m: m.set_value(k_now()))
        info[1][1].add_updater(lambda m: m.set_value(loss_at(sgd_path[k_now()])))
        info[2][1].add_updater(lambda m: m.set_value(loss_at(mom_path[k_now()])))
        info[3][1].add_updater(lambda m: m.set_value(loss_at(adam_path[k_now()])))
        self.add(info)

        self.play(t_tr.animate.set_value(float(N)),
                  run_time=7, rate_func=linear)
        self.wait(0.5)
