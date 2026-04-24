from manim import *
import numpy as np


class LinearMap2Dto1DExample(Scene):
    """
    A linear map from ℝ² → ℝ¹ squishes the plane onto a number line.
    Each 2D vector v = (x, y) maps to a single number (a x + b y).

    Example: L(x, y) = x + 2y. Visualize plane on left, number line
    on right; several points mapped with trajectory arrows.
    """

    def construct(self):
        title = Tex(r"Linear map $\mathbb{R}^2\to\mathbb{R}$: plane $\to$ number line",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1],
                            x_length=5.5, y_length=4.5,
                            background_line_style={"stroke_opacity": 0.3}
                            ).shift(LEFT * 3.0 + DOWN * 0.2)
        num_line = NumberLine(x_range=[-6, 6, 2], length=6,
                              include_numbers=True,
                              font_size=18).shift(RIGHT * 2.5 + DOWN * 0.3)
        self.play(Create(plane), Create(num_line))
        self.add(Tex(r"$\mathbb{R}^2$", font_size=22).move_to(plane.get_top() + UP * 0.2))
        self.add(Tex(r"$\mathbb{R}$", font_size=22).move_to(num_line.get_top() + UP * 0.3))

        # Linear map L(x, y) = x + 2y
        def L(p):
            return p[0] + 2 * p[1]

        sample_pts = [np.array([1, 1]), np.array([2, -1]),
                      np.array([-1, 1.5]), np.array([-2, -0.5]),
                      np.array([1, -1.5])]
        colors = [BLUE, GREEN, ORANGE, RED, PURPLE]

        # Stage 1: show points on plane
        plane_dots = []
        for p, col in zip(sample_pts, colors):
            d = Dot(plane.c2p(p[0], p[1]), color=col, radius=0.11)
            plane_dots.append(d)
            self.add(d)
            lbl = Tex(rf"$({p[0]}, {p[1]:+.1f})$", color=col, font_size=16)\
                .next_to(d, UR, buff=0.05)
            self.add(lbl)
        self.wait(0.4)

        # Stage 2: animate mapping each to number line
        t_tr = ValueTracker(0.0)

        def mapped_dots():
            t = t_tr.get_value()
            grp = VGroup()
            for p, col in zip(sample_pts, colors):
                start = plane.c2p(p[0], p[1])
                end = num_line.n2p(L(p))
                pos = (1 - t) * start + t * end
                grp.add(Dot(pos, color=col, radius=0.11))
            return grp

        self.add(always_redraw(mapped_dots))
        self.play(t_tr.animate.set_value(1.0), run_time=3, rate_func=smooth)
        self.wait(0.5)

        # Labels showing L(p)
        for p, col in zip(sample_pts, colors):
            val = L(p)
            lbl = Tex(f"${val:+.1f}$", color=col,
                       font_size=18).next_to(num_line.n2p(val), UP, buff=0.2)
            self.add(lbl)

        formula = Tex(r"$L(x, y) = x + 2y$", color=YELLOW, font_size=26).to_edge(DOWN, buff=0.4)
        self.play(Write(formula))
        self.wait(1.0)
