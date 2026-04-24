from manim import *
import numpy as np


class VanishingGradientExample(Scene):
    """
    Vanishing gradient in deep sigmoid networks: σ'(x) ≤ 1/4, so for
    a deep net, ∏σ'(z_i) → 0 exponentially in depth. Visualize
    gradient magnitudes layer-by-layer.

    TWO_COLUMN:
      LEFT  — deep network (8 layers) with ValueTracker depth_tr
              advancing layer count; always_redraw gradient arrow
              sizes shrinking exponentially.
      RIGHT — log-scale plot of |∇| vs depth.
    """

    def construct(self):
        title = Tex(r"Vanishing gradient: $|\nabla| \sim (1/4)^{\text{depth}}$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        L = 8  # number of layers
        layer_xs = np.linspace(-5.5, -0.5, L)

        # Static network
        layer_dots = VGroup()
        for i, x in enumerate(layer_xs):
            d = Circle(radius=0.25, color=BLUE,
                         fill_opacity=0.3, stroke_width=2
                         ).move_to([x, 1.5, 0])
            layer_dots.add(d)
            lbl = MathTex(rf"\ell_{i}", color=BLUE, font_size=16
                            ).move_to(d.get_center())
            layer_dots.add(lbl)
        # Edges
        edges_g = VGroup()
        for i in range(L - 1):
            edges_g.add(Line([layer_xs[i], 1.5, 0],
                                [layer_xs[i + 1], 1.5, 0],
                                color=GREY_B, stroke_width=1.5))
        self.play(Create(edges_g), FadeIn(layer_dots))

        depth_tr = ValueTracker(0)

        def grad_arrows():
            d = int(round(depth_tr.get_value()))
            d = max(0, min(d, L))
            grp = VGroup()
            # Gradient at layer L-1-d: magnitude = (1/4)^d
            for k in range(d):
                layer_idx = L - 1 - k
                grad_mag = (1 / 4) ** k
                start = [layer_xs[layer_idx], 1.5 + 0.3, 0]
                end = [layer_xs[layer_idx],
                        1.5 + 0.3 + grad_mag * 1.5, 0]
                grp.add(Arrow(start, end, color=RED, buff=0,
                                stroke_width=3,
                                max_tip_length_to_length_ratio=0.2))
            return grp

        self.add(always_redraw(grad_arrows))

        # RIGHT: log-scale plot
        ax = Axes(x_range=[0, L, 1], y_range=[-6, 0.5, 1],
                   x_length=4, y_length=4, tips=False,
                   axis_config={"font_size": 12, "include_numbers": True}
                   ).move_to([3.5, -0.5, 0])
        xl = Tex("depth", font_size=16).next_to(ax, DOWN, buff=0.1)
        yl = MathTex(r"\log_{10}|\nabla|", font_size=14).next_to(ax, LEFT, buff=0.1)
        self.play(Create(ax), Write(xl), Write(yl))

        def grad_log_curve():
            d = int(round(depth_tr.get_value()))
            d = max(1, min(d, L))
            pts = [ax.c2p(k, np.log10((1 / 4) ** k))
                   for k in range(d + 1)]
            m = VMobject(color=RED, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        self.add(always_redraw(grad_log_curve))

        def info():
            d = int(round(depth_tr.get_value()))
            d = max(0, min(d, L))
            mag = (1 / 4) ** d
            return VGroup(
                MathTex(rf"\text{{depth}} = {d}",
                         color=RED, font_size=22),
                MathTex(rf"|\nabla| = (1/4)^d = {mag:.2e}",
                         color=RED, font_size=20),
                Tex(r"$\sigma'(x) \le 1/4$; chain rule multiplies",
                     color=YELLOW, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        self.play(depth_tr.animate.set_value(L),
                   run_time=5, rate_func=linear)
        self.wait(0.4)
