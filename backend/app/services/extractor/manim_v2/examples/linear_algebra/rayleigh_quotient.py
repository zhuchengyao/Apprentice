from manim import *
import numpy as np


class RayleighQuotientExample(Scene):
    """
    Rayleigh quotient: R(x) = xᵀ A x / xᵀx. For symmetric A, extrema
    of R on the unit sphere are eigenvalues; achieved at eigenvectors.

    SINGLE_FOCUS: 2×2 symmetric A = [[3, 1], [1, 2]] has eigenvalues
    λ ≈ 3.618, 1.382. ValueTracker theta_tr rotates a unit vector on
    the circle; always_redraw recomputes R(x) and shows the bar plot
    of R(θ) with horizontal reference lines at the 2 eigenvalues.
    """

    def construct(self):
        A = np.array([[3.0, 1.0], [1.0, 2.0]])
        eigvals, eigvecs = np.linalg.eigh(A)

        title = Tex(r"Rayleigh: $\min\lambda \le \tfrac{x^TAx}{x^Tx}\le \max\lambda$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # LEFT: plane with unit circle + eigenvector dashes
        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                            x_length=4.5, y_length=4.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.3 + DOWN * 0.2)
        self.play(Create(plane))

        unit = Circle(radius=plane.x_length / (plane.x_range[1] - plane.x_range[0]),
                      color=BLUE, stroke_width=2).move_to(plane.c2p(0, 0))
        self.play(Create(unit))

        # Eigenvector directions
        for i, lam in enumerate(eigvals):
            v = eigvecs[:, i]
            col = GREEN if i == 1 else RED  # larger eigenvalue GREEN (max)
            line = DashedLine(plane.c2p(-2 * v[0], -2 * v[1]),
                              plane.c2p(2 * v[0], 2 * v[1]),
                              color=col, stroke_width=2)
            self.add(line)

        theta_tr = ValueTracker(0.0)

        def x_arrow():
            t = theta_tr.get_value()
            v = np.array([np.cos(t), np.sin(t)])
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=YELLOW, buff=0, stroke_width=4)

        def Ax_arrow():
            t = theta_tr.get_value()
            v = np.array([np.cos(t), np.sin(t)])
            Av = A @ v
            return Arrow(plane.c2p(0, 0), plane.c2p(Av[0] / 2, Av[1] / 2),
                          color=ORANGE, buff=0, stroke_width=3,
                          max_tip_length_to_length_ratio=0.15)

        self.add(always_redraw(x_arrow), always_redraw(Ax_arrow))

        # RIGHT: axes with R(θ) curve
        right_axes = Axes(x_range=[0, TAU, PI / 2], y_range=[1, 4, 0.5],
                          x_length=5.0, y_length=4.2,
                          axis_config={"include_numbers": True,
                                       "font_size": 16}).shift(RIGHT * 2.5 + DOWN * 0.2)
        self.play(Create(right_axes))

        # Eigenvalue reference lines
        for lam, col in zip(eigvals, [RED, GREEN]):
            self.add(DashedLine(right_axes.c2p(0, lam), right_axes.c2p(TAU, lam),
                                 color=col, stroke_width=2))
            self.add(Tex(rf"$\lambda={lam:.3f}$", color=col,
                         font_size=20).next_to(right_axes.c2p(TAU, lam),
                                                  RIGHT, buff=0.1))

        def R_val(theta):
            v = np.array([np.cos(theta), np.sin(theta)])
            return float(v @ A @ v)

        R_curve = right_axes.plot(R_val, x_range=[0, TAU], color=YELLOW, stroke_width=3)
        self.add(R_curve)

        def R_dot():
            t = theta_tr.get_value()
            return Dot(right_axes.c2p(t, R_val(t)), color=YELLOW, radius=0.1)

        self.add(always_redraw(R_dot))

        info = VGroup(
            VGroup(Tex(r"$\theta=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$R(x)=$", font_size=22),
                   DecimalNumber(float(R_val(0)), num_decimal_places=3,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3).shift(LEFT * 2.5)
        info[0][1].add_updater(lambda m: m.set_value(theta_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(R_val(theta_tr.get_value())))
        self.add(info)

        self.play(theta_tr.animate.set_value(TAU),
                  run_time=7, rate_func=linear)
        self.wait(0.8)
