from manim import *
import numpy as np


class CatalanDyckPathsExample(Scene):
    """
    Catalan numbers count Dyck paths: staircase paths from (0, 0) to
    (2n, 0) taking steps U=(1, 1) and D=(1, -1), never going below
    the x-axis.

    For n=4, C_4 = 14 such paths. All 14 paths enumerated in a 5×3
    grid of miniatures; ValueTracker k_tr walks a scanner cell
    highlighting the current path + enlarging it in the main axes.
    """

    def construct(self):
        n = 4
        title = Tex(rf"Catalan $C_4=14$: all Dyck paths from $(0,0)$ to $(2\cdot 4,0)$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Generate all Dyck paths of length 2n
        def gen_dyck(n):
            out = []
            def rec(path, up, down):
                if len(path) == 2 * n:
                    if up == down:
                        out.append(path[:])
                    return
                # up step
                if up < n:
                    path.append(1)
                    rec(path, up + 1, down)
                    path.pop()
                # down step (only if stays non-negative)
                if down < up:
                    path.append(-1)
                    rec(path, up, down + 1)
                    path.pop()
            rec([], 0, 0)
            return out

        paths = gen_dyck(n)
        assert len(paths) == 14

        # Mini grid: 5 columns × 3 rows
        cols, rows = 5, 3
        cell_w, cell_h = 2.1, 1.3
        origin = np.array([-4.4, 1.5, 0])

        def path_to_pts(path, scale_x=0.11, scale_y=0.14):
            pts = [np.array([0.0, 0.0, 0.0])]
            x, y = 0.0, 0.0
            for s in path:
                x += 1
                y += s
                pts.append(np.array([x * scale_x, y * scale_y, 0]))
            return pts

        minis = VGroup()
        for i, path in enumerate(paths):
            r = i // cols
            c = i % cols
            base = origin + np.array([c * cell_w, -r * cell_h, 0])
            pts = [base + p for p in path_to_pts(path)]
            box = Rectangle(width=cell_w * 0.9, height=cell_h * 0.75,
                            color=GREY_B, stroke_width=0.8,
                            fill_opacity=0.03).move_to(base + RIGHT * 0.44 + UP * 0.1)
            line = VMobject().set_points_as_corners(pts)\
                .set_color(BLUE).set_stroke(width=2)
            minis.add(box, line)
        self.play(FadeIn(minis))

        # Main axes for zoomed current path
        axes = Axes(x_range=[0, 2 * n + 0.5, 1], y_range=[0, n + 0.5, 1],
                    x_length=4.8, y_length=2.5,
                    axis_config={"include_numbers": True,
                                 "font_size": 16}).shift(DOWN * 2.2 + RIGHT * 0.5)
        self.play(Create(axes))

        k_tr = ValueTracker(0.0)

        def current_idx():
            return max(0, min(13, int(round(k_tr.get_value()))))

        def highlight_mini():
            k = current_idx()
            r = k // cols
            c = k % cols
            base = origin + np.array([c * cell_w, -r * cell_h, 0])
            return Rectangle(width=cell_w * 0.9, height=cell_h * 0.75,
                             color=YELLOW, stroke_width=3).move_to(base + RIGHT * 0.44 + UP * 0.1)

        self.add(always_redraw(highlight_mini))

        def zoom_path():
            k = current_idx()
            path = paths[k]
            x, y = 0, 0
            pts = [axes.c2p(0, 0)]
            for s in path:
                x += 1
                y += s
                pts.append(axes.c2p(x, y))
            return VMobject().set_points_as_corners(pts)\
                .set_color(YELLOW).set_stroke(width=4)

        self.add(always_redraw(zoom_path))

        # Info
        info = VGroup(
            VGroup(Tex(r"path $\#$", font_size=22),
                   DecimalNumber(1, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"$C_n=\frac{1}{n+1}\binom{2n}{n}$", font_size=22),
            Tex(r"$C_4=\frac{1}{5}\binom{8}{4}=\frac{70}{5}=14$",
                color=YELLOW, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.2).shift(DOWN * 1.5)
        info[0][1].add_updater(lambda m: m.set_value(current_idx() + 1))
        self.add(info)

        self.play(k_tr.animate.set_value(13.0),
                  run_time=7, rate_func=linear)
        self.wait(0.8)
