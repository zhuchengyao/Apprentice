from manim import *
import numpy as np


class TransformerPositionalEncodingExample(Scene):
    """
    Sinusoidal positional encoding used in the original Transformer:
      PE(pos, 2i) = sin(pos / 10000^(2i/d))
      PE(pos, 2i+1) = cos(pos / 10000^(2i/d))

    Visualize a 32 × 32 grid (32 positions × 32 dimensions) as a
    heatmap. ValueTracker col_tr picks a column (dimension); a row
    picks a position. Line plot on the right shows PE at that
    dimension vs position — frequency increases with dimension index.
    """

    def construct(self):
        title = Tex(r"Transformer sinusoidal PE: $PE_{pos,2i}=\sin(pos/10000^{2i/d})$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        d = 32
        positions = 32
        PE = np.zeros((positions, d))
        for pos in range(positions):
            for i in range(d // 2):
                PE[pos, 2 * i] = np.sin(pos / (10000 ** (2 * i / d)))
                PE[pos, 2 * i + 1] = np.cos(pos / (10000 ** (2 * i / d)))

        # Heatmap cells
        cell_s = 0.18
        origin = np.array([-4.5, 1.6, 0])
        grid = VGroup()
        for pos in range(positions):
            for i in range(d):
                v = PE[pos, i]
                col = interpolate_color(BLUE, RED,
                                         0.5 + 0.5 * v)
                rect = Square(side_length=cell_s * 0.95,
                              color=col, stroke_width=0,
                              fill_color=col, fill_opacity=0.9).move_to(
                    origin + RIGHT * i * cell_s + DOWN * pos * cell_s)
                grid.add(rect)
        self.play(FadeIn(grid), run_time=1.5)

        # Axis labels
        self.add(Tex(r"pos $\downarrow$", font_size=18).move_to(
            origin + LEFT * 0.4 + DOWN * positions * cell_s / 2))
        self.add(Tex(r"dim $\rightarrow$", font_size=18).move_to(
            origin + UP * 0.3 + RIGHT * d * cell_s / 2))

        # Right: line plot of selected dimension
        axes = Axes(x_range=[0, positions, 8], y_range=[-1.1, 1.1, 0.5],
                    x_length=4.8, y_length=3.4,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).to_edge(RIGHT, buff=0.3).shift(DOWN * 1.0)
        self.add(axes)

        col_tr = ValueTracker(0.0)

        def col_now():
            return max(0, min(d - 1, int(round(col_tr.get_value()))))

        def plot_curve():
            c = col_now()
            vals = PE[:, c]
            pts = [axes.c2p(pos, vals[pos]) for pos in range(positions)]
            return VMobject().set_points_as_corners(pts).set_color(YELLOW).set_stroke(width=3)

        def col_highlight():
            c = col_now()
            return Rectangle(width=cell_s * 0.95,
                             height=cell_s * positions,
                             color=YELLOW, stroke_width=3,
                             fill_opacity=0).move_to(
                origin + RIGHT * c * cell_s + DOWN * (positions - 1) * cell_s / 2)

        self.add(always_redraw(plot_curve), always_redraw(col_highlight))

        info = VGroup(
            VGroup(Tex(r"dim $i=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"low dim: high freq", color=BLUE, font_size=20),
            Tex(r"high dim: low freq", color=RED, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 2.0)
        info[0][1].add_updater(lambda m: m.set_value(col_now()))
        self.add(info)

        self.play(col_tr.animate.set_value(float(d - 1)),
                  run_time=6, rate_func=linear)
        self.wait(0.8)
