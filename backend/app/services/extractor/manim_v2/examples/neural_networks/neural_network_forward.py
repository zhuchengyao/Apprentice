from manim import *
import numpy as np


class NeuralNetworkForwardExample(Scene):
    """
    Forward propagation through a tiny 4 → 5 → 3 network with concrete
    weights. ValueTracker stage steps through:
      0 — input populated
      1 — weighted sums + ReLU computed for hidden layer
      2 — weighted sums + softmax computed for output

    For each stage, node fill colors brighten and edges that contribute
    a strong activation glow.
    """

    def construct(self):
        title = Tex(r"Forward pass: input $\to$ hidden (ReLU) $\to$ output (softmax)",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        rng = np.random.default_rng(42)
        x = np.array([0.8, -0.3, 0.5, -0.2])
        W1 = rng.standard_normal((5, 4)) * 0.7
        b1 = rng.standard_normal(5) * 0.3
        W2 = rng.standard_normal((3, 5)) * 0.7
        b2 = rng.standard_normal(3) * 0.3

        z1 = W1 @ x + b1
        h = np.maximum(0, z1)  # ReLU
        z2 = W2 @ h + b2
        e = np.exp(z2 - z2.max())
        out = e / e.sum()

        layer_sizes = [4, 5, 3]
        layer_xs = [-4.5, -0.5, +3.5]
        layer_colors = [BLUE, GREEN, YELLOW]

        # Build the network mobjects
        nodes = []  # list of VGroup of circles per layer
        node_circles = []  # flat list per layer
        for size, x_pos, color in zip(layer_sizes, layer_xs, layer_colors):
            col = []
            for k in range(size):
                circle = Circle(radius=0.35, color=color, stroke_width=2)
                col.append(circle)
            grp = VGroup(*col).arrange(DOWN, buff=0.25).move_to([x_pos, 0, 0])
            nodes.append(grp)
            node_circles.append(col)

        # Edges keyed by (layer_idx_from, i_from, i_to)
        edges = {}
        for li in range(len(nodes) - 1):
            W = W1 if li == 0 else W2
            for i_to in range(layer_sizes[li + 1]):
                for i_from in range(layer_sizes[li]):
                    a = node_circles[li][i_from].get_right()
                    b = node_circles[li + 1][i_to].get_left()
                    line = Line(a, b, stroke_width=1.0, stroke_color=GREY_B,
                                stroke_opacity=0.25)
                    edges[(li, i_from, i_to)] = (line, W[i_to, i_from])

        # Layer labels
        labels = VGroup(
            Tex(r"input", color=BLUE, font_size=22).next_to(nodes[0], UP, buff=0.3),
            Tex(r"hidden (ReLU)", color=GREEN, font_size=22).next_to(nodes[1], UP, buff=0.3),
            Tex(r"output (softmax)", color=YELLOW, font_size=22).next_to(nodes[2], UP, buff=0.3),
        )

        # Add to scene
        for n in nodes:
            self.play(FadeIn(n), run_time=0.4)
        self.play(*[Create(line) for (line, w) in edges.values()],
                  Write(labels), run_time=1.5)

        # Stage 0: populate input
        in_value_lbls = VGroup()
        for i, val in enumerate(x):
            lbl = MathTex(rf"{val:+.2f}", color=BLUE, font_size=22).move_to(
                node_circles[0][i].get_center())
            in_value_lbls.add(lbl)
            node_circles[0][i].set_fill(BLUE, opacity=0.4 + 0.4 * abs(val))
        self.play(Write(in_value_lbls))
        self.wait(0.4)

        # Stage 1: compute hidden activations + brighten edges proportional to |w * x_from|
        edge_anims_1 = []
        for (li, i_from, i_to), (line, w) in edges.items():
            if li != 0:
                continue
            contribution = abs(w * x[i_from])
            new_op = min(0.95, 0.2 + contribution)
            new_color = ORANGE if w > 0 else PURPLE
            edge_anims_1.append(line.animate.set_stroke(color=new_color,
                                                       opacity=new_op,
                                                       width=1.2))

        h_value_lbls = VGroup()
        for i, val in enumerate(h):
            lbl = MathTex(rf"{val:.2f}", color=GREEN, font_size=20).move_to(
                node_circles[1][i].get_center())
            h_value_lbls.add(lbl)
            node_circles[1][i].set_fill(GREEN, opacity=0.4 + 0.5 * min(1, val))

        self.play(*edge_anims_1, run_time=1.2)
        self.play(Write(h_value_lbls))
        self.wait(0.4)

        # Stage 2: compute output via softmax + brighten layer-2 edges
        edge_anims_2 = []
        for (li, i_from, i_to), (line, w) in edges.items():
            if li != 1:
                continue
            contribution = abs(w * h[i_from])
            new_op = min(0.95, 0.2 + contribution)
            new_color = ORANGE if w > 0 else PURPLE
            edge_anims_2.append(line.animate.set_stroke(color=new_color,
                                                       opacity=new_op,
                                                       width=1.2))

        out_value_lbls = VGroup()
        for i, val in enumerate(out):
            lbl = MathTex(rf"{val:.2f}", color=YELLOW, font_size=22).move_to(
                node_circles[2][i].get_center())
            out_value_lbls.add(lbl)
            node_circles[2][i].set_fill(YELLOW, opacity=0.4 + 0.5 * val)

        self.play(*edge_anims_2, run_time=1.2)
        self.play(Write(out_value_lbls))
        self.wait(0.4)

        # Bottom equations
        equations = VGroup(
            MathTex(r"h = \max(0, W_1 x + b_1)", color=GREEN, font_size=24),
            MathTex(r"\hat y = \mathrm{softmax}(W_2 h + b_2)",
                    color=YELLOW, font_size=24),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        self.play(Write(equations))

        # Highlight the predicted class (argmax)
        pred = int(np.argmax(out))
        highlight = Circle(radius=0.42, color=WHITE, stroke_width=4).move_to(
            node_circles[2][pred].get_center())
        pred_lbl = MathTex(rf"\hat y_{{{pred+1}}} = {out[pred]:.2f}\ \text{{(predicted)}}",
                           color=WHITE, font_size=22).next_to(
            node_circles[2][pred], RIGHT, buff=0.2)
        self.play(Create(highlight), Write(pred_lbl))
        self.wait(1.0)
