from manim import *
import numpy as np


class MarkovTransitionEigenExample(Scene):
    """
    For stochastic matrix P, the stationary distribution is the left
    eigenvector with eigenvalue 1. All other eigenvalues have |λ| < 1
    (if chain is irreducible/aperiodic), controlling mixing rate.

    TWO_COLUMN: LEFT 4×4 matrix P displayed with YELLOW highlight
    of eigenvectors. RIGHT complex plane showing 4 eigenvalues with
    unit circle overlay.
    """

    def construct(self):
        title = Tex(r"Markov spectrum: $\lambda_1=1$; others $|\lambda|<1$ mix rate",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 4-state stochastic matrix
        P = np.array([
            [0.6, 0.2, 0.1, 0.1],
            [0.3, 0.5, 0.1, 0.1],
            [0.1, 0.2, 0.5, 0.2],
            [0.1, 0.1, 0.3, 0.5],
        ])

        # Left eigendecomposition
        evals, evecs = np.linalg.eig(P.T)
        # Sort by |λ| descending
        idx = np.argsort(-np.abs(evals))
        evals = evals[idx]
        evecs = evecs[:, idx]

        # LEFT: matrix
        cell_s = 0.75
        origin = np.array([-4.3, 1.0, 0])
        for i in range(4):
            for j in range(4):
                pos = origin + RIGHT * j * cell_s - UP * i * cell_s
                v = P[i, j]
                col = interpolate_color(GREY_D, BLUE, v)
                rect = Square(side_length=cell_s * 0.9,
                               color=col, stroke_width=1,
                               fill_color=col, fill_opacity=0.85).move_to(pos)
                lbl = Tex(f"{v:.2f}", font_size=18).move_to(pos)
                self.add(rect, lbl)

        self.add(Tex(r"$P$ (row-stochastic)", font_size=22).move_to(
            origin + UP * 0.7 + RIGHT * cell_s * 1.5))

        # RIGHT: eigenvalue spectrum
        spec = ComplexPlane(x_range=[-1.2, 1.2, 0.5], y_range=[-1.2, 1.2, 0.5],
                            x_length=4.0, y_length=4.0,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(RIGHT * 3.0 + DOWN * 0.4)
        self.add(spec)
        unit_c = Circle(radius=spec.x_length / (spec.x_range[1] - spec.x_range[0]),
                         color=GREY_B, stroke_width=2).move_to(spec.n2p(0))
        self.add(unit_c)

        for i, ev in enumerate(evals):
            col = RED if abs(abs(ev) - 1) < 1e-3 else ORANGE
            self.add(Dot(spec.n2p(complex(ev.real, ev.imag)), color=col, radius=0.12))
            self.add(Tex(rf"$\lambda_{{{i+1}}}$", color=col, font_size=18).next_to(
                spec.n2p(complex(ev.real, ev.imag)), UR, buff=0.05))

        self.add(Tex(r"unit circle $|\lambda|=1$",
                     color=GREY_B, font_size=18).next_to(spec, DOWN, buff=0.1))

        # Iteration dynamic
        t_tr = ValueTracker(0.0)

        # Show π(t) · P^n starting from (1, 0, 0, 0) via interpolation
        pi0 = np.array([1.0, 0.0, 0.0, 0.0])
        # Stationary = normalized eigenvector for λ=1
        pi_star = evecs[:, 0].real
        pi_star = pi_star / pi_star.sum()

        def pi_at(k):
            v = pi0.copy()
            for _ in range(k):
                v = v @ P
            return v

        # State bar display
        bar_origin = np.array([-4.0, -2.7, 0])
        def state_bars():
            k = int(round(t_tr.get_value()))
            k = max(0, min(30, k))
            pi_k = pi_at(k)
            grp = VGroup()
            for i in range(4):
                rect = Rectangle(width=0.5, height=pi_k[i] * 3.0,
                                  color=BLUE, fill_color=BLUE,
                                  fill_opacity=0.6)
                rect.move_to(bar_origin + RIGHT * i * 0.7 + UP * pi_k[i] * 1.5)
                grp.add(rect)
            return grp

        self.add(always_redraw(state_bars))

        # Stationary reference
        for i in range(4):
            rect = Rectangle(width=0.5, height=pi_star[i] * 3.0,
                              color=YELLOW, stroke_width=2, fill_opacity=0)
            rect.move_to(bar_origin + RIGHT * i * 0.7 + UP * pi_star[i] * 1.5)
            self.add(rect)

        info = VGroup(
            VGroup(Tex(r"$k=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"YELLOW outline: $\pi^*$",
                color=YELLOW, font_size=20),
            Tex(r"mixing $\propto |\lambda_2|^k$",
                color=ORANGE, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(DR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(int(round(t_tr.get_value()))))
        self.add(info)

        self.play(t_tr.animate.set_value(30.0),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
