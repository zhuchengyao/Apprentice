from manim import *
import numpy as np


class RecurrentLSTMExample(Scene):
    """
    LSTM cell: input → forget gate, input gate, output gate, candidate
    cell state → new cell state c_t = f⊙c_{t-1} + i⊙g → h_t = o⊙tanh(c_t).

    SINGLE_FOCUS:
      Block diagram of an LSTM cell with the 3 gates (σ) and the
      candidate g (tanh). ValueTracker step_tr reveals the 5 stages
      of the forward pass.
    """

    def construct(self):
        title = Tex(r"LSTM cell: forget/input/output gates",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def box(center, label, color):
            b = Rectangle(width=1.0, height=0.65,
                            color=color, fill_opacity=0.25,
                            stroke_width=2).move_to(center)
            lbl = Tex(label, color=color, font_size=18
                       ).move_to(b.get_center())
            return VGroup(b, lbl)

        blocks = {
            "x_h": box([-5, 0, 0], r"$x_t, h_{t-1}$", BLUE),
            "f": box([-2, 1.8, 0], r"$f = \sigma$", RED),
            "i": box([-2, 0.6, 0], r"$i = \sigma$", GREEN),
            "g": box([-2, -0.6, 0], r"$g = \tanh$", ORANGE),
            "o": box([-2, -1.8, 0], r"$o = \sigma$", PURPLE),
            "c_prev": box([0.5, 2.5, 0], r"$c_{t-1}$", GREY_B),
            "mult1": box([1.5, 1.8, 0], r"$\odot$", YELLOW),
            "mult2": box([1.5, 0, 0], r"$\odot$", YELLOW),
            "add": box([3, 1.0, 0], r"$+$", YELLOW),
            "tanh2": box([4.5, 1.0, 0], r"$\tanh$", ORANGE),
            "mult3": box([5.5, -0.5, 0], r"$\odot$", YELLOW),
            "c_new": box([3, -2, 0], r"$c_t$", GREEN),
            "h_new": box([5.5, -2, 0], r"$h_t$", GREEN),
        }

        connections = [
            ("x_h", "f"), ("x_h", "i"), ("x_h", "g"), ("x_h", "o"),
            ("c_prev", "mult1"),
            ("f", "mult1"), ("i", "mult2"), ("g", "mult2"),
            ("mult1", "add"), ("mult2", "add"),
            ("add", "tanh2"), ("add", "c_new"),
            ("tanh2", "mult3"), ("o", "mult3"),
            ("mult3", "h_new"),
        ]

        # Reveal order
        stage_blocks = [
            ["x_h"],
            ["f", "i", "g", "o"],
            ["c_prev", "mult1", "mult2"],
            ["add", "c_new"],
            ["tanh2", "mult3", "h_new"],
        ]

        step_tr = ValueTracker(0)

        def visible_blocks():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, len(stage_blocks)))
            grp = VGroup()
            for i in range(s):
                for name in stage_blocks[i]:
                    grp.add(blocks[name])
            return grp

        def visible_connections():
            s = int(round(step_tr.get_value()))
            vis = set()
            for i in range(min(s, len(stage_blocks))):
                for nm in stage_blocks[i]:
                    vis.add(nm)
            grp = VGroup()
            for (src, dst) in connections:
                if src in vis and dst in vis:
                    a = blocks[src][0].get_center()
                    b = blocks[dst][0].get_center()
                    # Choose appropriate edge points
                    dir_vec = b - a
                    ap = a + 0.5 * dir_vec / (np.linalg.norm(dir_vec) + 1e-6)
                    bp = b - 0.5 * dir_vec / (np.linalg.norm(dir_vec) + 1e-6)
                    grp.add(Arrow(a, b, color=GREY_B, buff=0.4,
                                    stroke_width=1.5,
                                    max_tip_length_to_length_ratio=0.08))
            return grp

        self.add(always_redraw(visible_blocks),
                  always_redraw(visible_connections))

        def step_label():
            s = int(round(step_tr.get_value()))
            return MathTex(rf"\text{{stage}} = {s}/5",
                             color=YELLOW, font_size=22
                             ).to_edge(DOWN, buff=0.4)

        self.add(always_redraw(step_label))

        for s in range(1, 6):
            self.play(step_tr.animate.set_value(s),
                       run_time=1.1)
            self.wait(0.6)
        self.wait(0.5)
