from manim import *
import numpy as np


class MLPHiddenLayerExample(Scene):
    """
    MLP hidden layer: z = Wx + b, h = ReLU(z). Visualize activations
    (from _2024/transformers/mlp): input vector (4D), weight matrix
    (6×4), output after ReLU. ValueTracker x_tr rotates through
    several input vectors.

    TWO_COLUMN:
      LEFT  — input circles (4), weight edges connecting to hidden
              circles (6); edge thickness = |w|, color = sign.
              Active input vector highlighted; output activations
              colored by value.
      RIGHT — live x, z = Wx + b, h = ReLU(z) panels.
    """

    def construct(self):
        title = Tex(r"MLP hidden layer: $h = \mathrm{ReLU}(Wx + b)$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        rng = np.random.default_rng(19)
        W = rng.normal(scale=0.7, size=(6, 4))
        b = rng.normal(scale=0.3, size=6)

        in_xs = [-4.2] * 4
        in_ys = [2.0 - i * 1.1 for i in range(4)]
        hid_xs = [-1.5] * 6
        hid_ys = [2.4 - i * 0.9 for i in range(6)]

        x_tr = ValueTracker(0)
        inputs_tour = [
            np.array([1.0, 0.0, 0.0, 0.0]),
            np.array([0.0, 1.0, 0.0, 0.0]),
            np.array([0.5, 0.5, -0.5, 0.5]),
            np.array([-0.8, 1.0, 0.3, -0.2]),
        ]

        def current_x():
            idx = int(round(x_tr.get_value())) % len(inputs_tour)
            return inputs_tour[idx]

        def input_nodes():
            x = current_x()
            grp = VGroup()
            for i in range(4):
                c = Circle(radius=0.22, color=BLUE,
                            fill_opacity=0.3 + 0.6 * abs(x[i]) / 2,
                            stroke_width=2
                            ).move_to([in_xs[i], in_ys[i], 0])
                lbl = MathTex(rf"{x[i]:+.1f}", font_size=16,
                                color=WHITE).move_to(c.get_center())
                grp.add(c, lbl)
            return grp

        def edges():
            grp = VGroup()
            for j in range(6):
                for i in range(4):
                    w = W[j, i]
                    color = GREEN if w > 0 else RED
                    opacity = min(0.9, 0.15 + abs(w) / 1.5)
                    grp.add(Line([in_xs[i], in_ys[i], 0],
                                   [hid_xs[j], hid_ys[j], 0],
                                   color=color,
                                   stroke_width=min(4, 0.5 + abs(w) * 2),
                                   stroke_opacity=opacity))
            return grp

        def hidden_nodes():
            x = current_x()
            z = W @ x + b
            h = np.maximum(z, 0)
            grp = VGroup()
            for j in range(6):
                col = ORANGE if h[j] > 0 else GREY_B
                c = Circle(radius=0.26, color=col,
                            fill_opacity=0.25 + 0.6 * min(1.0, h[j] / 2.0),
                            stroke_width=2
                            ).move_to([hid_xs[j], hid_ys[j], 0])
                lbl = MathTex(rf"{h[j]:+.2f}", font_size=15,
                                color=WHITE).move_to(c.get_center())
                grp.add(c, lbl)
            return grp

        self.add(always_redraw(edges),
                  always_redraw(input_nodes),
                  always_redraw(hidden_nodes))

        def info():
            x = current_x()
            z = W @ x + b
            h = np.maximum(z, 0)
            return VGroup(
                MathTex(r"x = (" + ", ".join(f"{v:+.1f}" for v in x) + ")",
                         color=BLUE, font_size=18),
                MathTex(r"z = Wx + b:", color=WHITE, font_size=18),
                MathTex(r"(" + ", ".join(f"{v:+.2f}" for v in z) + ")",
                         color=WHITE, font_size=16),
                MathTex(r"h = \mathrm{ReLU}(z):",
                         color=ORANGE, font_size=18),
                MathTex(r"(" + ", ".join(f"{v:.2f}" for v in h) + ")",
                         color=ORANGE, font_size=16),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for target in [1, 2, 3, 0]:
            self.play(x_tr.animate.set_value(target),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.4)
