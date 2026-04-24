from manim import *
import numpy as np


class AttentionHeadCircuitExample(Scene):
    """
    Attention head circuit (from _2024/transformers/chm): input
    embedding → Q, K, V via three separate matrices W_Q, W_K, W_V →
    softmax(QK^T/√d) V → output. Visualize as a signal flow.

    SINGLE_FOCUS:
      Block diagram: input → splits to W_Q, W_K, W_V → Q, K, V →
      attention weights computed → V·weights → output. ValueTracker
      stage_tr reveals the flow stage by stage.
    """

    def construct(self):
        title = Tex(r"Attention head: $\text{softmax}(QK^\top/\sqrt d)V$ circuit",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Block positions
        input_pos = np.array([-5, 0, 0])
        WQ_pos = np.array([-2.5, 2, 0])
        WK_pos = np.array([-2.5, 0, 0])
        WV_pos = np.array([-2.5, -2, 0])
        QKscore_pos = np.array([0.5, 1, 0])
        softmax_pos = np.array([2.5, 1, 0])
        weighted_pos = np.array([2.5, -1, 0])
        output_pos = np.array([5, 0, 0])

        def box(center, label, color):
            b = Rectangle(width=1.8, height=0.9,
                            color=color, fill_opacity=0.25,
                            stroke_width=2).move_to(center)
            lbl = Tex(label, font_size=18,
                       color=color).move_to(center)
            return VGroup(b, lbl)

        blocks = {
            "input": box(input_pos, r"input $x$", BLUE),
            "WQ": box(WQ_pos, r"$W_Q$", GREEN),
            "WK": box(WK_pos, r"$W_K$", TEAL),
            "WV": box(WV_pos, r"$W_V$", ORANGE),
            "QK": box(QKscore_pos, r"$QK^\top/\sqrt d$", RED),
            "softmax": box(softmax_pos, r"softmax", PURPLE),
            "weighted": box(weighted_pos, r"$\sum w_i V_i$", YELLOW),
            "output": box(output_pos, r"output", BLUE),
        }

        connections = [
            ("input", "WQ"),
            ("input", "WK"),
            ("input", "WV"),
            ("WQ", "QK"),
            ("WK", "QK"),
            ("QK", "softmax"),
            ("softmax", "weighted"),
            ("WV", "weighted"),
            ("weighted", "output"),
        ]

        stage_tr = ValueTracker(0)
        reveal_order = [
            ["input"],
            ["WQ", "WK", "WV"],
            ["QK"],
            ["softmax"],
            ["weighted"],
            ["output"],
        ]
        # Stage N reveals blocks[0..N-1] + appropriate connections

        def visible_blocks():
            s = int(round(stage_tr.get_value()))
            s = max(0, min(s, len(reveal_order)))
            grp = VGroup()
            for i in range(s):
                for name in reveal_order[i]:
                    grp.add(blocks[name])
            return grp

        # Connection arrows (always_redraw based on stage)
        def visible_connections():
            s = int(round(stage_tr.get_value()))
            # Map which blocks are visible
            visible = set()
            for i in range(min(s, len(reveal_order))):
                for nm in reveal_order[i]:
                    visible.add(nm)
            grp = VGroup()
            for (src, dst) in connections:
                if src in visible and dst in visible:
                    a = blocks[src][0].get_right()
                    b = blocks[dst][0].get_left()
                    # If roughly vertical, use top/bottom
                    if abs(a[1] - b[1]) > 0.6:
                        if a[1] > b[1]:
                            a = blocks[src][0].get_bottom()
                        else:
                            a = blocks[src][0].get_top()
                        b = blocks[dst][0].get_top() if a[1] < b[1] else blocks[dst][0].get_bottom()
                    grp.add(Arrow(a, b, color=GREY_B, buff=0.1,
                                    stroke_width=2.5,
                                    max_tip_length_to_length_ratio=0.15))
            return grp

        self.add(always_redraw(visible_blocks),
                  always_redraw(visible_connections))

        def stage_label():
            s = int(round(stage_tr.get_value()))
            return MathTex(rf"\text{{stage}} = {s} / 6",
                             color=YELLOW, font_size=24
                             ).to_edge(DOWN, buff=0.4)

        self.add(always_redraw(stage_label))

        for s in range(1, 7):
            self.play(stage_tr.animate.set_value(s),
                       run_time=0.9, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
