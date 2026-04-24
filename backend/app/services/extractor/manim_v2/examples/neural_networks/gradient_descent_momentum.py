from manim import *
import numpy as np


class GradientDescentMomentumExample(Scene):
    """
    Gradient descent vs GD + momentum on a narrow-valley quadratic
    f(x, y) = 0.08 x² + 0.9 y²   (strong anisotropy).

    Both optimizers run 60 iterations from start (3.5, 2.2).
    GD (BLUE) zigzags down the y-axis; momentum (GREEN) dampens the
    oscillation thanks to the velocity buffer. ValueTracker t_tr
    reveals both trajectories via always_redraw partial-paths + dots.
    Right column shows live iteration, |x|, and f(x).
    """

    def construct(self):
        title = Tex(r"GD vs GD+momentum: $f=0.08\,x^2+0.9\,y^2$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[-4, 4, 1], y_range=[-2.5, 2.5, 1],
                    x_length=6.4, y_length=4.0,
                    axis_config={"include_numbers": False}).shift(LEFT * 2.3 + DOWN * 0.2)
        self.play(Create(axes))

        # Contour curves (ellipses)
        def contour(lvl):
            pts = []
            for t in np.linspace(0, TAU, 80):
                r_x = np.sqrt(lvl / 0.08)
                r_y = np.sqrt(lvl / 0.9)
                pts.append(axes.c2p(r_x * np.cos(t), r_y * np.sin(t)))
            return VMobject().set_points_as_corners(pts + [pts[0]]).set_color(GREY_B)\
                .set_stroke(width=1.5, opacity=0.45)

        contours = VGroup(*[contour(lvl) for lvl in [0.2, 0.6, 1.2, 2.0, 3.0, 4.5]])
        self.add(contours)

        def f(x, y):
            return 0.08 * x ** 2 + 0.9 * y ** 2

        def grad(x, y):
            return np.array([0.16 * x, 1.8 * y])

        # Run both optimizers
        lr = 0.15
        mu = 0.9
        N = 60

        # Vanilla GD
        gd_pts = [np.array([3.5, 2.2])]
        for _ in range(N):
            g = grad(*gd_pts[-1])
            gd_pts.append(gd_pts[-1] - lr * g)

        # Momentum
        mom_pts = [np.array([3.5, 2.2])]
        v = np.zeros(2)
        for _ in range(N):
            g = grad(*mom_pts[-1])
            v = mu * v - lr * g
            mom_pts.append(mom_pts[-1] + v)

        gd_pts = np.array(gd_pts)
        mom_pts = np.array(mom_pts)

        t_tr = ValueTracker(0.0)

        def gd_path():
            k = int(round(t_tr.get_value()))
            k = max(0, min(N, k))
            if k < 1:
                return VMobject()
            return VMobject().set_points_as_corners(
                [axes.c2p(p[0], p[1]) for p in gd_pts[:k + 1]]
            ).set_color(BLUE).set_stroke(width=3)

        def mom_path():
            k = int(round(t_tr.get_value()))
            k = max(0, min(N, k))
            if k < 1:
                return VMobject()
            return VMobject().set_points_as_corners(
                [axes.c2p(p[0], p[1]) for p in mom_pts[:k + 1]]
            ).set_color(GREEN).set_stroke(width=3)

        def gd_dot():
            k = int(round(t_tr.get_value()))
            k = max(0, min(N, k))
            return Dot(axes.c2p(gd_pts[k][0], gd_pts[k][1]),
                       color=BLUE, radius=0.11)

        def mom_dot():
            k = int(round(t_tr.get_value()))
            k = max(0, min(N, k))
            return Dot(axes.c2p(mom_pts[k][0], mom_pts[k][1]),
                       color=GREEN, radius=0.11)

        self.add(always_redraw(gd_path), always_redraw(mom_path),
                 always_redraw(gd_dot), always_redraw(mom_dot))

        # Min marker
        self.add(Dot(axes.c2p(0, 0), color=YELLOW, radius=0.09))

        info = VGroup(
            VGroup(Tex(r"iter $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            Tex(r"GD (BLUE):", color=BLUE, font_size=22),
            VGroup(Tex(r"$\|x\|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$f(x)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            Tex(r"Momentum (GREEN):", color=GREEN, font_size=22),
            VGroup(Tex(r"$\|x\|=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$f(x)=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.2)

        def k_now():
            return max(0, min(N, int(round(t_tr.get_value()))))

        info[0][1].add_updater(lambda m: m.set_value(k_now()))
        info[2][1].add_updater(lambda m: m.set_value(float(np.linalg.norm(gd_pts[k_now()]))))
        info[3][1].add_updater(lambda m: m.set_value(f(*gd_pts[k_now()])))
        info[5][1].add_updater(lambda m: m.set_value(float(np.linalg.norm(mom_pts[k_now()]))))
        info[6][1].add_updater(lambda m: m.set_value(f(*mom_pts[k_now()])))
        self.add(info)

        self.play(t_tr.animate.set_value(float(N)),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
