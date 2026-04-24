from manim import *
import numpy as np


class IteratedFunctionSystemExample(Scene):
    """
    General IFS chaos game with 3 contraction maps produces
    Sierpinski triangle (Banach fixed-point attractor). Show the
    chaos game fills in the attractor as iteration count grows.

    SINGLE_FOCUS: 3 vertices of triangle + ValueTracker n_tr sweeps
    iteration count. Pre-computed 8000 points via random choice of
    map. always_redraw fades in cumulative point cloud.
    """

    def construct(self):
        title = Tex(r"IFS chaos game $\to$ Sierpinski attractor (Banach FP)",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Triangle vertices
        A = np.array([0.0, 2.5, 0])
        B = np.array([-2.7, -1.8, 0])
        C = np.array([2.7, -1.8, 0])
        for v, col in zip([A, B, C], [RED, GREEN, BLUE]):
            self.add(Dot(v, color=col, radius=0.14))

        # Pre-compute 8000 chaos-game iterates
        np.random.seed(10)
        N = 8000
        pts = np.zeros((N, 3))
        pts[0] = [0.0, 0.0, 0]
        choices = np.random.choice([0, 1, 2], size=N)
        for i in range(1, N):
            c = choices[i]
            v = [A, B, C][c]
            pts[i] = 0.5 * (pts[i - 1] + v)

        n_tr = ValueTracker(0.0)

        dots = VGroup(*[
            Dot(pts[i], color=[RED, GREEN, BLUE][choices[i]],
                radius=0.018, fill_opacity=0)
            for i in range(N)
        ])
        self.add(dots)

        def update_dots(mob):
            n = int(round(n_tr.get_value()))
            for i, d in enumerate(mob):
                d.set_fill(opacity=0.85 if i < n else 0.0)
            return mob
        dots.add_updater(update_dots)

        info = VGroup(
            VGroup(Tex(r"iterations $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"3 maps $f_i(x)=\tfrac12(x+v_i)$",
                font_size=20),
            Tex(r"contraction ratio $r=1/2$",
                color=YELLOW, font_size=20),
            Tex(r"$\Rightarrow$ unique Sierpinski attractor",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UL, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(int(round(n_tr.get_value()))))
        self.add(info)

        self.play(n_tr.animate.set_value(float(N)),
                  run_time=10, rate_func=linear)
        dots.clear_updaters()
        self.wait(0.8)
