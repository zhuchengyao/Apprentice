from manim import *
import numpy as np


class IntegralByPartsExample(Scene):
    """
    Integration by parts: ∫ u dv = u v − ∫ v du. Visualize with a
    product-function area u(x)·v(x) over the "L-shaped" region whose
    total perimeter splits the product.

    SINGLE_FOCUS:
      Axes; ValueTracker x_tr sweeps x; rectangle of width u(x) and
      height v(x) grows; always_redraw the rectangle plus its two
      partial strips representing ∫ u dv and ∫ v du.
    """

    def construct(self):
        title = Tex(r"Integration by parts: $\int u\,dv = uv - \int v\,du$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Pick u(x) = x, v(x) = sin(x); product uv = x·sin(x)
        # Rectangle area = u·v at current x

        ax = Axes(x_range=[0, 4, 1], y_range=[0, 5, 1],
                   x_length=7, y_length=4, tips=False,
                   axis_config={"font_size": 14, "include_numbers": True}
                   ).move_to([-2.5, -0.3, 0])
        xlbl = MathTex(r"x", font_size=18).next_to(ax, DOWN, buff=0.1)
        self.play(Create(ax), Write(xlbl))

        # Axis labels: one axis is u, other is v
        u_lbl = MathTex(r"u", font_size=22).next_to(ax, LEFT, buff=0.1)
        v_top = MathTex(r"v", font_size=22).move_to(ax.c2p(0, 5) + np.array([-0.3, 0.2, 0]))
        self.play(Write(u_lbl), Write(v_top))

        # For this illustration: u takes values 0..3 and v takes values 0..4 as x sweeps
        # Use u(x) = x and v(x) = 4(1 - e^{-x/2})

        def u(x):
            return x

        def v(x):
            return 4 * (1 - np.exp(-x / 2))

        x_tr = ValueTracker(0.01)

        def rectangle():
            x = x_tr.get_value()
            uu = u(x)
            vv = v(x)
            # The (u, v) rectangle at position (0, 0) with width u and height v
            if uu < 0.05 or vv < 0.05:
                return VGroup()
            origin = ax.c2p(0, 0)
            br = ax.c2p(uu, 0)
            tr = ax.c2p(uu, vv)
            tl = ax.c2p(0, vv)
            return Polygon(origin, br, tr, tl,
                            color=YELLOW, fill_opacity=0.2,
                            stroke_width=2)

        # ∫ u dv "strip" = area under curve v(x) as we go up. Integrate u·v'(x) dx from 0 to x.
        # ∫ v du "strip" = area under u·v as we go along u axis.
        # Visualize: the CURVE (u(t), v(t)) traced; the area between curve and v-axis is ∫ u dv,
        # area between curve and u-axis is ∫ v du.

        def curve():
            x = x_tr.get_value()
            pts = [ax.c2p(u(t), v(t)) for t in np.linspace(0, x, 60)]
            m = VMobject(color=BLUE, stroke_width=4)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def udv_region():
            # Between curve and v-axis (u = 0)
            x = x_tr.get_value()
            pts = [ax.c2p(0, 0)]
            for t in np.linspace(0, x, 60):
                pts.append(ax.c2p(u(t), v(t)))
            pts.append(ax.c2p(0, v(x)))
            return Polygon(*pts, color=GREEN, fill_opacity=0.35,
                            stroke_width=0)

        def vdu_region():
            # Between curve and u-axis (v = 0)
            x = x_tr.get_value()
            pts = [ax.c2p(0, 0)]
            for t in np.linspace(0, x, 60):
                pts.append(ax.c2p(u(t), v(t)))
            pts.append(ax.c2p(u(x), 0))
            return Polygon(*pts, color=RED, fill_opacity=0.35,
                            stroke_width=0)

        self.add(always_redraw(udv_region),
                  always_redraw(vdu_region),
                  always_redraw(rectangle),
                  always_redraw(curve))

        # Legend
        udv_lbl = Tex(r"GREEN: $\int u\,dv$", color=GREEN, font_size=22)
        vdu_lbl = Tex(r"RED: $\int v\,du$", color=RED, font_size=22)
        rect_lbl = Tex(r"YELLOW: $u \cdot v$ rectangle",
                        color=YELLOW, font_size=22)
        total_lbl = MathTex(r"\int u\,dv + \int v\,du = uv",
                              color=WHITE, font_size=22)
        info = VGroup(udv_lbl, vdu_lbl, rect_lbl, total_lbl
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.18
                                 ).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)
        self.play(Write(info))

        def running_info():
            x = x_tr.get_value()
            uu = u(x)
            vv = v(x)
            uv = uu * vv
            # numerically integrate ∫_0^x u·v' dx and ∫_0^x v·u' dx
            n = 60
            dt = x / n if n > 0 else 0
            int_udv = 0.0
            int_vdu = 0.0
            for i in range(n):
                t = i * dt
                int_udv += u(t) * ((v(t + dt) - v(t)))  # u·dv
                int_vdu += v(t) * (u(t + dt) - u(t))     # v·du
            return VGroup(
                MathTex(rf"x = {x:.2f}", color=YELLOW, font_size=20),
                MathTex(rf"uv = {uv:.3f}",
                         color=WHITE, font_size=20),
                MathTex(rf"\int u\,dv \approx {int_udv:.3f}",
                         color=GREEN, font_size=20),
                MathTex(rf"\int v\,du \approx {int_vdu:.3f}",
                         color=RED, font_size=20),
                MathTex(rf"\text{{sum}} = {int_udv + int_vdu:.3f}",
                         color=ORANGE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15
                        ).to_edge(RIGHT, buff=0.3).shift(DOWN * 2.0)

        self.add(always_redraw(running_info))

        self.play(x_tr.animate.set_value(3.5),
                   run_time=7, rate_func=linear)
        self.wait(0.5)
