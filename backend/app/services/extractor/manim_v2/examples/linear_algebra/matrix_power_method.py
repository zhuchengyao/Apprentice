from manim import *
import numpy as np


class MatrixPowerMethodExample(Scene):
    """
    Power method: iterate x_{k+1} = Ax_k / ‖Ax_k‖ to find dominant
    eigenvector. Convergence rate ∝ |λ_2/λ_1|.

    A = [[0.9, 0.4], [0.4, 0.6]] — symmetric, eigenvalues ≈ 1.10, 0.40.
    Ratio 0.36 ⇒ fast convergence.

    SINGLE_FOCUS: 30 iterates from a random start rotate onto the
    dominant eigenvector. always_redraw path + current arrow.
    """

    def construct(self):
        A = np.array([[0.9, 0.4], [0.4, 0.6]])
        evals, evecs = np.linalg.eigh(A)
        # Dominant eigenvector (last column)
        v1 = evecs[:, -1]

        title = Tex(r"Power method: $x_{k+1}=Ax_k/\|Ax_k\|\to v_1$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                            x_length=6, y_length=6,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.2)
        self.play(Create(plane))

        # Dominant eigenvector line
        line_v1 = DashedLine(plane.c2p(-2 * v1[0], -2 * v1[1]),
                              plane.c2p(2 * v1[0], 2 * v1[1]),
                              color=GREEN, stroke_width=2)
        self.add(line_v1)
        self.add(Tex(r"$v_1$ direction", color=GREEN, font_size=22).next_to(
            plane.c2p(1.3 * v1[0], 1.3 * v1[1]), UR, buff=0.1))

        # Iterates
        np.random.seed(1)
        x = np.array([0.3, -0.9])
        x = x / np.linalg.norm(x)
        iterates = [x]
        N = 20
        for _ in range(N):
            y = A @ iterates[-1]
            iterates.append(y / np.linalg.norm(y))

        k_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(N, int(round(k_tr.get_value()))))

        def path():
            k = k_now()
            if k < 1:
                return VMobject()
            pts = [plane.c2p(iterates[i][0], iterates[i][1]) for i in range(k + 1)]
            return VMobject().set_points_as_corners(pts)\
                .set_color(YELLOW).set_stroke(width=2, opacity=0.7)

        def arrows():
            k = k_now()
            grp = VGroup()
            for i in range(k + 1):
                v = iterates[i]
                op = 0.25 + 0.75 * i / max(1, k)
                col = interpolate_color(BLUE, YELLOW, op)
                grp.add(Arrow(plane.c2p(0, 0),
                               plane.c2p(v[0], v[1]),
                               color=col, buff=0, stroke_width=2,
                               max_tip_length_to_length_ratio=0.12))
            return grp

        def current_arrow():
            k = k_now()
            v = iterates[k]
            return Arrow(plane.c2p(0, 0), plane.c2p(v[0], v[1]),
                          color=RED, buff=0, stroke_width=4,
                          max_tip_length_to_length_ratio=0.15)

        self.add(always_redraw(path), always_redraw(arrows),
                 always_redraw(current_arrow))

        def rayleigh():
            v = iterates[k_now()]
            return float(v @ A @ v)

        info = VGroup(
            VGroup(Tex(r"iter $k=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(RED)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"Rayleigh $x^TAx=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=4,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\lambda_1=$", color=GREEN, font_size=22),
                   DecimalNumber(float(evals[-1]), num_decimal_places=4,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(rf"$|\lambda_2/\lambda_1|={abs(evals[0]/evals[-1]):.3f}$",
                color=GREY_B, font_size=22),
            Tex(r"convergence rate $\propto |\lambda_2/\lambda_1|^k$",
                color=GREY_B, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DL, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(k_now()))
        info[1][1].add_updater(lambda m: m.set_value(rayleigh()))
        self.add(info)

        self.play(k_tr.animate.set_value(float(N)),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
