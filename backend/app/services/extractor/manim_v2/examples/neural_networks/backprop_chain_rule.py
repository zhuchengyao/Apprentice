from manim import *
import numpy as np


class BackpropChainRuleExample(Scene):
    """
    Backprop = chain rule: ∂L/∂w_i flows backward through the
    computational graph. Illustrate with a tiny graph
    y = f(g(h(x))) and gradient cascade.

    SINGLE_FOCUS:
      Chain x → h → g → f → L. ValueTracker t_tr reveals gradients
      flowing backward: ∂L/∂f, ∂L/∂g = ∂L/∂f · f'(g), etc.
    """

    def construct(self):
        title = Tex(r"Backprop = chain rule: $\tfrac{\partial L}{\partial w} = \prod_i \tfrac{\partial y_i}{\partial y_{i-1}}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Layout: 5 nodes
        node_xs = [-5, -2.5, 0, 2.5, 5]
        node_labels = [r"x", r"h", r"g", r"f", r"L"]
        node_colors = [BLUE, GREEN, YELLOW, ORANGE, RED]

        nodes = VGroup()
        for i, (x, lbl, col) in enumerate(zip(node_xs, node_labels, node_colors)):
            c = Circle(radius=0.35, color=col, fill_opacity=0.35,
                         stroke_width=2.5).move_to([x, 0.5, 0])
            nodes.add(c)
            nodes.add(MathTex(lbl, color=col, font_size=26).move_to(c.get_center()))
        self.play(FadeIn(nodes))

        # Forward arrows (top)
        forward_arrows = VGroup()
        for i in range(4):
            a = Arrow([node_xs[i] + 0.35, 0.5, 0],
                       [node_xs[i + 1] - 0.35, 0.5, 0],
                       color=GREY_B, buff=0.1, stroke_width=2.5,
                       max_tip_length_to_length_ratio=0.15)
            forward_arrows.add(a)
        self.play(Create(forward_arrows))

        forward_lbl = Tex(r"forward pass", color=GREY_B, font_size=20
                           ).move_to([0, 1.5, 0])
        self.play(Write(forward_lbl))

        # Backward arrows (bottom) with gradient labels
        grad_labels = [
            (r"\tfrac{\partial L}{\partial f}", 0),
            (r"\tfrac{\partial L}{\partial g}", 1),
            (r"\tfrac{\partial L}{\partial h}", 2),
            (r"\tfrac{\partial L}{\partial x}", 3),
        ]

        t_tr = ValueTracker(0)

        def backward_arrows():
            s = int(round(t_tr.get_value()))
            s = max(0, min(s, 4))
            grp = VGroup()
            for i in range(s):
                a = Arrow([node_xs[4 - i] - 0.35, -0.5, 0],
                           [node_xs[3 - i] + 0.35, -0.5, 0],
                           color=RED, buff=0.1, stroke_width=3,
                           max_tip_length_to_length_ratio=0.15)
                grp.add(a)
                # Gradient label
                mid_x = (node_xs[4 - i] + node_xs[3 - i]) / 2
                grp.add(MathTex(grad_labels[i][0], color=RED, font_size=18
                                  ).move_to([mid_x, -1.3, 0]))
            return grp

        self.add(always_redraw(backward_arrows))

        backward_lbl = Tex(r"backward pass", color=RED, font_size=20
                            ).move_to([0, -2.0, 0])

        def info():
            s = int(round(t_tr.get_value()))
            s = max(0, min(s, 4))
            return VGroup(
                MathTex(rf"\text{{backward step}} = {s}/4",
                         color=RED, font_size=22),
                MathTex(r"\tfrac{\partial L}{\partial x} = \tfrac{\partial L}{\partial f} \cdot f'(g) \cdot g'(h) \cdot h'(x)",
                         color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))
        self.play(Write(backward_lbl))

        for s in range(1, 5):
            self.play(t_tr.animate.set_value(s),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.5)
