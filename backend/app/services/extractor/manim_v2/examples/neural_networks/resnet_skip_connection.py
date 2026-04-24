from manim import *
import numpy as np


class ResnetSkipConnectionExample(Scene):
    """
    ResNet skip (residual) connection: instead of learning F(x), learn
    F(x) + x. This lets gradients flow directly back through identity
    paths, solving the vanishing-gradient problem in deep nets.

    SINGLE_FOCUS: 5 residual blocks chained. ValueTracker t_tr
    animates forward pass — each block receives input x, computes
    F(x), adds x. Gradient flow visualization second phase.
    """

    def construct(self):
        title = Tex(r"ResNet residual block: $y = F(x) + x$",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # 5 blocks horizontally
        n_blocks = 5
        block_w = 1.5
        x_positions = np.linspace(-5, 5, n_blocks + 1)

        # Draw blocks
        blocks = VGroup()
        for i in range(n_blocks):
            rect = Rectangle(width=block_w, height=1.3,
                              color=BLUE, stroke_width=2,
                              fill_color=BLUE, fill_opacity=0.2)
            rect.move_to(np.array([(x_positions[i] + x_positions[i + 1]) / 2, 0, 0]))
            blocks.add(rect)
            lbl = Tex(rf"$F_{{{i+1}}}$", font_size=22, color=BLUE).move_to(
                rect.get_center())
            blocks.add(lbl)
        self.add(blocks)

        # Skip connection arrows (arcs going OVER each block)
        skip_arrows = VGroup()
        for i in range(n_blocks):
            start = np.array([x_positions[i] + 0.1, 0.65, 0])
            end = np.array([x_positions[i + 1] - 0.1, 0.65, 0])
            arc = ArcBetweenPoints(start, end, angle=-PI / 3)\
                .set_color(GREEN).set_stroke(width=3)
            arc.add_tip(tip_length=0.15)
            skip_arrows.add(arc)
        self.play(Create(skip_arrows))

        # Forward-pass animation
        t_tr = ValueTracker(0.0)

        def signal_dot():
            t = t_tr.get_value()
            stage = t * n_blocks
            idx = min(n_blocks - 1, int(stage))
            frac = stage - idx
            x = x_positions[idx] + frac * (x_positions[idx + 1] - x_positions[idx])
            return Dot(np.array([x, 0, 0]), color=YELLOW, radius=0.16)

        self.add(always_redraw(signal_dot))

        # Live signal magnitude (assume ‖F(x)‖ decays while ‖x‖ stable)
        info = VGroup(
            VGroup(Tex(r"forward stage $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"GREEN arcs: skip connections",
                color=GREEN, font_size=20),
            Tex(r"gradient $\partial y/\partial x=F'(x)+1$",
                font_size=20),
            Tex(r"identity term ensures gradient flow",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.5)
        info[0][1].add_updater(lambda m: m.set_value(
            min(n_blocks - 1, int(t_tr.get_value() * n_blocks)) + 1))
        self.add(info)

        self.play(t_tr.animate.set_value(1.0),
                  run_time=5, rate_func=linear)
        self.wait(0.5)

        # Phase 2: backward gradient visualization
        grad_dot_tr = ValueTracker(1.0)

        def grad_dot():
            t = grad_dot_tr.get_value()
            stage = (1 - t) * n_blocks
            idx = min(n_blocks - 1, int(stage))
            frac = stage - idx
            x = x_positions[idx] + frac * (x_positions[idx + 1] - x_positions[idx])
            return Dot(np.array([x, -1.5, 0]), color=RED, radius=0.14)

        grad_label = Tex(r"gradient $\leftarrow$", color=RED,
                          font_size=24).move_to(np.array([5.5, -1.5, 0]))
        self.add(grad_label)
        self.add(always_redraw(grad_dot))

        self.play(grad_dot_tr.animate.set_value(0.0),
                  run_time=3.5, rate_func=linear)
        self.wait(1.0)
