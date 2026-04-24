from manim import *
import numpy as np


class DropoutRegularizationExample(Scene):
    """
    Dropout: during training, randomly zero out fraction p of neurons
    per forward pass. During inference, all neurons active but output
    scaled by (1-p). Visualize with a 4-5-5-3 network.

    ValueTracker mask_tr advances through 6 pre-sampled dropout masks;
    always_redraw redraws edges/nodes with dropped neurons faded GREY.
    Live fraction of active neurons.
    """

    def construct(self):
        title = Tex(r"Dropout: randomly zero $p$-fraction of activations",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        layers = [4, 5, 5, 3]
        x_positions = np.linspace(-4, 4, len(layers))
        positions = []
        for L, x in zip(layers, x_positions):
            ys = np.linspace(1.6, -1.6, L)
            positions.append([(x, y) for y in ys])

        np.random.seed(5)
        p = 0.4
        masks = []
        for _ in range(6):
            mask_layers = []
            for L in layers:
                mask_layers.append(np.random.random(L) > p)
            masks.append(mask_layers)

        mask_tr = ValueTracker(0.0)

        def m_idx():
            return max(0, min(len(masks) - 1, int(round(mask_tr.get_value()))))

        def nodes():
            ms = masks[m_idx()]
            grp = VGroup()
            for li, layer_positions in enumerate(positions):
                for ni, (x, y) in enumerate(layer_positions):
                    active = ms[li][ni]
                    col = [BLUE, GREEN, ORANGE, RED][li] if active else GREY_D
                    op = 0.8 if active else 0.25
                    d = Dot([x, y, 0], color=col, radius=0.13)
                    d.set_fill(col, opacity=op)
                    grp.add(d)
            return grp

        def edges():
            ms = masks[m_idx()]
            grp = VGroup()
            for li in range(len(layers) - 1):
                for ni, (x1, y1) in enumerate(positions[li]):
                    for nj, (x2, y2) in enumerate(positions[li + 1]):
                        active = ms[li][ni] and ms[li + 1][nj]
                        col = YELLOW if active else GREY_D
                        op = 0.5 if active else 0.08
                        grp.add(Line([x1, y1, 0], [x2, y2, 0],
                                      color=col, stroke_width=1,
                                      stroke_opacity=op))
            return grp

        self.add(always_redraw(edges), always_redraw(nodes))

        # Info
        def fraction_active():
            ms = masks[m_idx()]
            total = sum(layers)
            active = sum(m.sum() for m in ms)
            return int(active), total

        info = VGroup(
            VGroup(Tex(r"dropout rate $p=0.4$", font_size=22),
                    ).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"sample $=$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"active $=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(GREEN),
                   Tex(r"/", font_size=22),
                   DecimalNumber(sum(layers), num_decimal_places=0,
                                 font_size=22)).arrange(RIGHT, buff=0.08),
            Tex(r"inference: scale $\times(1-p)=0.6$",
                color=YELLOW, font_size=20),
            Tex(r"ensembles many subnetworks",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        info[1][1].add_updater(lambda m: m.set_value(m_idx() + 1))
        info[2][1].add_updater(lambda m: m.set_value(fraction_active()[0]))
        self.add(info)

        for k in range(1, len(masks)):
            self.play(mask_tr.animate.set_value(float(k)),
                      run_time=1.2, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.5)
