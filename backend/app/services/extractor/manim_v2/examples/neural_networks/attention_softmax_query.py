from manim import *
import numpy as np


class AttentionSoftmaxQueryExample(Scene):
    """
    Attention mechanism: for query q and keys K ∈ ℝ^(n × d),
    attention weights = softmax(qK^T / √d).

    SINGLE_FOCUS: n=6 keys on a 2D plane. Query ValueTracker q_tr
    moves a query vector around; always_redraw attention weights
    as edge thicknesses (softmax of dot products).
    """

    def construct(self):
        title = Tex(r"Attention: weights $=\mathrm{softmax}(qK^T/\sqrt d)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1],
                            x_length=8, y_length=5.5,
                            background_line_style={"stroke_opacity": 0.3}).shift(DOWN * 0.1)
        self.play(Create(plane))

        n_keys = 6
        np.random.seed(5)
        keys = np.random.randn(n_keys, 2) * 1.3

        # Draw keys
        key_colors = [BLUE, GREEN, ORANGE, RED, PURPLE, TEAL]
        for i, k in enumerate(keys):
            self.add(Dot(plane.c2p(k[0], k[1]), color=key_colors[i], radius=0.12))
            self.add(Tex(f"$k_{i+1}$", color=key_colors[i], font_size=18).next_to(
                plane.c2p(k[0], k[1]), UR, buff=0.05))

        q_tr = ValueTracker(0.0)

        def q_vec():
            t = q_tr.get_value()
            return np.array([2.0 * np.cos(t), 1.5 * np.sin(t)])

        def q_dot():
            q = q_vec()
            return Dot(plane.c2p(q[0], q[1]), color=YELLOW, radius=0.16)

        def q_label():
            q = q_vec()
            return Tex(r"$q$", color=YELLOW, font_size=22).next_to(
                plane.c2p(q[0], q[1]), UL, buff=0.05)

        def weights():
            q = q_vec()
            d = keys.shape[1]
            scores = keys @ q / np.sqrt(d)
            scores = scores - scores.max()
            w = np.exp(scores)
            w = w / w.sum()
            return w

        def attention_edges():
            q = q_vec()
            w = weights()
            grp = VGroup()
            for i, k in enumerate(keys):
                sw = 0.5 + 6 * w[i]
                grp.add(Line(plane.c2p(q[0], q[1]),
                              plane.c2p(k[0], k[1]),
                              color=key_colors[i],
                              stroke_width=sw, stroke_opacity=0.35 + 0.55 * w[i]))
            return grp

        self.add(always_redraw(attention_edges),
                 always_redraw(q_dot),
                 always_redraw(q_label))

        # Bars for weights
        def weight_bars():
            w = weights()
            grp = VGroup()
            bar_origin = np.array([3.2, -2.0, 0])
            for i in range(n_keys):
                rect = Rectangle(width=0.22,
                                  height=w[i] * 2.5,
                                  color=key_colors[i],
                                  fill_color=key_colors[i],
                                  fill_opacity=0.7)
                rect.move_to(bar_origin + RIGHT * i * 0.3 + UP * w[i] * 1.25)
                grp.add(rect)
            return grp

        self.add(always_redraw(weight_bars))

        self.play(q_tr.animate.set_value(TAU),
                  run_time=8, rate_func=linear)
        self.wait(0.5)
