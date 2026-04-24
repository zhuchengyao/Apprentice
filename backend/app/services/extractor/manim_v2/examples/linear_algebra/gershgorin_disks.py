from manim import *
import numpy as np


class GershgorinDisksExample(Scene):
    """
    Gershgorin's disk theorem: every eigenvalue of A is contained in
    the union of disks D_i = {z : |z - a_ii| ≤ Σ_{j≠i} |a_ij|}.

    SINGLE_FOCUS ComplexPlane. A 3×3 matrix A(s) morphs via
    ValueTracker s_tr between two matrices; always_redraw rebuilds
    3 colored disks centered at diagonal entries with radii equal to
    off-diagonal row sums, plus the 3 eigenvalues computed via
    numpy.linalg.eigvals and placed as RED dots. Eigenvalues stay in
    the union throughout.
    """

    def construct(self):
        title = Tex(r"Gershgorin: eigenvalues live in $\bigcup_i D_i$, " +
                    r"$D_i=\{z:|z-a_{ii}|\le \sum_{j\neq i}|a_{ij}|\}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = ComplexPlane(x_range=[-2, 8, 1], y_range=[-4, 4, 1],
                             x_length=8.0, y_length=5.2,
                             background_line_style={"stroke_opacity": 0.3}
                             ).shift(LEFT * 0.5 + DOWN * 0.1)
        self.play(Create(plane))

        A0 = np.array([[5.0, 0.4, -0.2],
                       [-0.3, 2.0, 0.6],
                       [0.5, -0.1, -1.5]], dtype=complex)
        A1 = np.array([[4.5, 1.2, 0.8],
                       [0.7, 1.0, -1.5],
                       [1.0, 0.9, -2.0]], dtype=complex)

        s_tr = ValueTracker(0.0)

        def A_of():
            s = s_tr.get_value()
            return (1 - s) * A0 + s * A1

        disk_colors = [BLUE, GREEN, ORANGE]

        def disks():
            A = A_of()
            grp = VGroup()
            unit_x = plane.x_length / (plane.x_range[1] - plane.x_range[0])
            for i in range(3):
                c = A[i, i]
                r = sum(abs(A[i, j]) for j in range(3) if j != i)
                center = plane.n2p(complex(c.real, c.imag))
                grp.add(Circle(radius=r * unit_x, color=disk_colors[i],
                               stroke_width=3, fill_color=disk_colors[i],
                               fill_opacity=0.15).move_to(center))
                grp.add(Dot(center, color=disk_colors[i], radius=0.07))
            return grp

        def eigen_dots():
            A = A_of()
            evals = np.linalg.eigvals(A)
            grp = VGroup()
            for ev in evals:
                grp.add(Dot(plane.n2p(complex(ev.real, ev.imag)),
                             color=RED, radius=0.11))
            return grp

        self.add(always_redraw(disks), always_redraw(eigen_dots))

        # Panel showing current A and eigenvalues
        def A_strings():
            A = A_of()
            return [[f"{A[i, j].real:+.2f}" for j in range(3)] for i in range(3)]

        def eig_strings():
            A = A_of()
            evs = sorted(np.linalg.eigvals(A), key=lambda z: z.real)
            return [f"{ev.real:+.2f}{'+' if ev.imag >= 0 else ''}{ev.imag:.2f}i"
                    if abs(ev.imag) > 1e-6 else f"{ev.real:+.3f}"
                    for ev in evs]

        header = Tex(r"$A=$", font_size=22)
        rows = VGroup(*[
            Tex(r"$a_{i,j}$", font_size=18) for _ in range(3)
        ])

        # Rather than rebuild whole matrix each frame, just show eigenvalues live.
        eigen_panel = VGroup(
            Tex(r"$\lambda$ (sorted):", color=RED, font_size=22),
            Tex(r"$\lambda_1 = 0$", color=RED, font_size=22),
            Tex(r"$\lambda_2 = 0$", color=RED, font_size=22),
            Tex(r"$\lambda_3 = 0$", color=RED, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.3)

        def update_eigen_panel():
            evs = eig_strings()
            new = VGroup(
                Tex(r"$\lambda$ (sorted):", color=RED, font_size=22),
                Tex(rf"$\lambda_1={evs[0]}$", color=RED, font_size=22),
                Tex(rf"$\lambda_2={evs[1]}$", color=RED, font_size=22),
                Tex(rf"$\lambda_3={evs[2]}$", color=RED, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            new.move_to(eigen_panel, aligned_edge=LEFT)
            eigen_panel.become(new)
            return eigen_panel

        eigen_panel.add_updater(lambda m, dt: update_eigen_panel())
        self.add(eigen_panel)

        disk_lbls = VGroup(
            Tex(r"$D_1$", color=BLUE, font_size=22),
            Tex(r"$D_2$", color=GREEN, font_size=22),
            Tex(r"$D_3$", color=ORANGE, font_size=22),
        ).arrange(RIGHT, buff=0.35).to_corner(DR, buff=0.3)
        self.add(disk_lbls)

        # Sweep the morph both ways
        self.play(s_tr.animate.set_value(1.0), run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(s_tr.animate.set_value(0.4), run_time=2, rate_func=smooth)
        self.play(s_tr.animate.set_value(0.0), run_time=2, rate_func=smooth)
        self.wait(0.8)
