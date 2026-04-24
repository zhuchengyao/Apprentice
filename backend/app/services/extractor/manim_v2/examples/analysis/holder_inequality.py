from manim import *
import numpy as np


class HolderInequalityExample(Scene):
    """
    Hölder: for p, q > 1 with 1/p + 1/q = 1,
        |Σ x_i y_i| ≤ (Σ|x_i|^p)^(1/p) · (Σ|y_i|^q)^(1/q).

    TWO_COLUMN. LEFT: bar chart of two vectors x, y ∈ ℝ^8 with
    x fixed, y rotated via ValueTracker θ_tr. RIGHT: live readouts
    of dot product, ‖x‖_p, ‖y‖_q, their RHS product; a running "gap"
    (RHS − |LHS|) stays ≥ 0 throughout. Second phase: ValueTracker p_tr
    morphs p between 2 (Cauchy-Schwarz) and 1.5 and 4, recomputing q.
    """

    def construct(self):
        title = Tex(r"Hölder: $\left|\sum x_iy_i\right|\le \|x\|_p\cdot \|y\|_q,\ " +
                    r"\tfrac{1}{p}+\tfrac{1}{q}=1$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        n = 8
        x = np.array([1.0, -0.6, 1.3, 0.4, -1.1, 0.2, 0.9, -0.7])
        y0 = np.array([0.6, 1.1, -0.3, 1.0, 0.5, -0.8, 0.4, 1.2])

        theta_tr = ValueTracker(0.0)
        p_tr = ValueTracker(2.0)

        def q_of():
            p = p_tr.get_value()
            return p / (p - 1)

        def y_rot():
            theta = theta_tr.get_value()
            ct, st = np.cos(theta), np.sin(theta)
            # rotate (y_{2k}, y_{2k+1}) pairs by theta
            out = y0.copy()
            for k in range(4):
                a, b = y0[2 * k], y0[2 * k + 1]
                out[2 * k] = ct * a - st * b
                out[2 * k + 1] = st * a + ct * b
            return out

        axes = Axes(x_range=[0, n + 0.5, 1], y_range=[-1.6, 1.6, 0.5],
                    x_length=5.4, y_length=3.6,
                    axis_config={"include_numbers": False}).shift(LEFT * 2.6 + DOWN * 0.2)
        self.play(Create(axes))

        def bars_x():
            g = VGroup()
            for i in range(n):
                g.add(Rectangle(height=abs(x[i]) * axes.y_length / 3.2,
                                width=0.18,
                                color=BLUE,
                                fill_color=BLUE, fill_opacity=0.6)
                      .move_to(axes.c2p(i + 0.75, x[i] / 2)))
            return g

        def bars_y():
            y = y_rot()
            g = VGroup()
            for i in range(n):
                g.add(Rectangle(height=abs(y[i]) * axes.y_length / 3.2,
                                width=0.18,
                                color=ORANGE,
                                fill_color=ORANGE, fill_opacity=0.6)
                      .move_to(axes.c2p(i + 1.05, y[i] / 2)))
            return g

        self.add(bars_x(), always_redraw(bars_y))

        # Right column numbers
        def norms():
            p = p_tr.get_value()
            q = q_of()
            y = y_rot()
            dot = float(np.dot(x, y))
            xp = float(np.sum(np.abs(x) ** p)) ** (1 / p)
            yq = float(np.sum(np.abs(y) ** q)) ** (1 / q)
            return dot, xp, yq, xp * yq

        info = VGroup(
            VGroup(Tex(r"$p=$", font_size=22),
                   DecimalNumber(2.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$q=$", font_size=22),
                   DecimalNumber(2.0, num_decimal_places=2,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\langle x,y\rangle=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\|x\|_p=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(BLUE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\|y\|_q=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$\|x\|_p\|y\|_q=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"gap $=$", font_size=22),
                   DecimalNumber(0.0, num_decimal_places=3,
                                 font_size=22).set_color(GREEN)).arrange(RIGHT, buff=0.1),
            Tex(r"gap $\ge 0$ always", color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.2)

        info[0][1].add_updater(lambda m: m.set_value(p_tr.get_value()))
        info[1][1].add_updater(lambda m: m.set_value(q_of()))
        info[2][1].add_updater(lambda m: m.set_value(norms()[0]))
        info[3][1].add_updater(lambda m: m.set_value(norms()[1]))
        info[4][1].add_updater(lambda m: m.set_value(norms()[2]))
        info[5][1].add_updater(lambda m: m.set_value(norms()[3]))
        info[6][1].add_updater(lambda m: m.set_value(norms()[3] - abs(norms()[0])))
        self.add(info)

        # Phase 1: rotate y pairs (Cauchy-Schwarz active)
        self.play(theta_tr.animate.set_value(TAU),
                  run_time=5, rate_func=smooth)
        self.wait(0.3)

        # Phase 2: morph p
        for p_val in [1.5, 4.0, 2.5, 2.0]:
            self.play(p_tr.animate.set_value(p_val),
                      run_time=1.8, rate_func=smooth)
            self.wait(0.2)
        self.wait(0.5)
