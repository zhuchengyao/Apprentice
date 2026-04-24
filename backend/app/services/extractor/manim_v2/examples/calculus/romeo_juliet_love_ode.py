from manim import *
import numpy as np


class RomeoJulietLoveOde(Scene):
    """Strogatz's 'love affair' model: Romeo's love R(t) and Juliet's love
    J(t) evolve via dR/dt = a*R + b*J, dJ/dt = c*R + d*J.  Different
    (a,b,c,d) produce different phase portraits: spiral in (friends),
    spiral out (obsessive), center (endless oscillation).
    Visualize the center case: R' = -J, J' = R — perfect circles."""

    def construct(self):
        title = Tex(
            r"Romeo \& Juliet: $\dot R = -J,\ \dot J = R$ — eternal orbit",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5.5, y_length=5.5,
            background_line_style={"stroke_opacity": 0.25},
        ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        self.play(Create(plane))

        x_lab = MathTex("R", font_size=26,
                        color=BLUE).next_to(plane.x_axis.get_end(),
                                            UP, buff=0.15)
        y_lab = MathTex("J", font_size=26,
                        color=RED).next_to(plane.y_axis.get_end(),
                                           RIGHT, buff=0.15)
        self.play(FadeIn(x_lab), FadeIn(y_lab))

        A = np.array([[0, -1], [1, 0]])
        rng = np.random.default_rng(2)
        n_arrows = 11
        field = VGroup()
        step = 0.6
        for x in np.arange(-2.6, 2.7, step):
            for y in np.arange(-2.6, 2.7, step):
                v = A @ np.array([x, y])
                norm = np.linalg.norm(v)
                if norm < 0.05:
                    continue
                scale = 0.28 / max(norm, 0.2)
                start = plane.c2p(x, y)
                end = plane.c2p(x + v[0] * scale, y + v[1] * scale)
                arr = Arrow(
                    start, end, buff=0, color=GREY_B, stroke_width=2,
                    max_tip_length_to_length_ratio=0.3,
                )
                field.add(arr)
        self.play(LaggedStart(*[FadeIn(a) for a in field],
                              lag_ratio=0.003, run_time=1.8))

        t_tr = ValueTracker(0.0)
        R0, J0 = 2.0, 0.3

        def state():
            t = t_tr.get_value()
            R = R0 * np.cos(t) - J0 * np.sin(t)
            J = R0 * np.sin(t) + J0 * np.cos(t)
            return R, J

        def get_trail():
            t = t_tr.get_value()
            pts = [
                plane.c2p(
                    R0 * np.cos(s) - J0 * np.sin(s),
                    R0 * np.sin(s) + J0 * np.cos(s),
                )
                for s in np.linspace(0, t, max(2, int(t * 20)))
            ]
            vm = VMobject(color=YELLOW, stroke_width=3)
            vm.set_points_as_corners(pts)
            return vm

        def get_rider():
            R, J = state()
            return Dot(plane.c2p(R, J), radius=0.1,
                       color=YELLOW).set_z_index(4)

        trail = always_redraw(get_trail)
        rider = always_redraw(get_rider)
        self.add(trail, rider)

        def get_readout():
            t = t_tr.get_value()
            R, J = state()
            row = VGroup(
                MathTex(rf"t={t:.2f}", font_size=24),
                MathTex(rf"R(t)={R:+.2f}", font_size=24, color=BLUE),
                MathTex(rf"J(t)={J:+.2f}", font_size=24, color=RED),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            row.to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
            return row

        readout = always_redraw(get_readout)
        self.add(readout)

        A_form = MathTex(
            r"\begin{pmatrix}\dot R\\ \dot J\end{pmatrix}"
            r"= \begin{pmatrix}0 & -1\\ 1 & 0\end{pmatrix}"
            r"\begin{pmatrix}R\\ J\end{pmatrix}",
            font_size=26,
        )
        A_form.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.8)
        solution = MathTex(
            r"\Rightarrow\ \begin{pmatrix}R(t)\\ J(t)\end{pmatrix}"
            r"= e^{At}\begin{pmatrix}R_0\\ J_0\end{pmatrix}",
            font_size=26, color=YELLOW,
        )
        solution.next_to(A_form, DOWN, buff=0.3)
        self.play(Write(A_form))
        self.play(Write(solution))

        self.play(t_tr.animate.set_value(2 * np.pi),
                  run_time=6, rate_func=linear)
        self.wait(1.2)
