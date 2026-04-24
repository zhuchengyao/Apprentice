from manim import *
import numpy as np


class LinearlyDependentExample(Scene):
    """
    Linear (in)dependence visualized: rotate one vector while the other
    stays fixed; watch the span flicker between a plane (most angles)
    and a line (parallel/antiparallel).

    SINGLE_FOCUS:
      NumberPlane with two vectors v (fixed) and w (rotating via
      ValueTracker θ). When the angle between them is 0° or 180°,
      span(v, w) = a line; otherwise span = ℝ². A live indicator
      panel switches color and message accordingly. Yellow shaded
      parallelogram of vw shows zero area at degeneracy.
    """

    def construct(self):
        title = Tex(r"Linear dependence: $\det[\vec v\ \vec w] = 0 \Leftrightarrow$ same span line",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-3, 3, 1],
            x_length=7.5, y_length=5.6,
            background_line_style={"stroke_opacity": 0.3},
        ).move_to([-1.6, -0.4, 0])
        self.play(Create(plane))

        v = np.array([2.0, 1.0])  # fixed vector
        w_len = 2.5
        theta_v = np.arctan2(v[1], v[0])

        theta_tr = ValueTracker(theta_v + 1.2)  # start at some non-degenerate angle

        def w_vec():
            t = theta_tr.get_value()
            return w_len * np.array([np.cos(t), np.sin(t)])

        def is_dependent():
            t = theta_tr.get_value()
            angle_diff = (t - theta_v) % PI
            return angle_diff < 0.05 or angle_diff > PI - 0.05

        def v_arrow():
            return Arrow(plane.c2p(0, 0), plane.c2p(*v), buff=0,
                         color=GREEN, stroke_width=5,
                         max_tip_length_to_length_ratio=0.12)

        def w_arrow():
            wv = w_vec()
            color = RED if is_dependent() else ORANGE
            return Arrow(plane.c2p(0, 0), plane.c2p(*wv), buff=0,
                         color=color, stroke_width=5,
                         max_tip_length_to_length_ratio=0.12)

        def parallelogram():
            wv = w_vec()
            return Polygon(
                plane.c2p(0, 0),
                plane.c2p(*v),
                plane.c2p(v[0] + wv[0], v[1] + wv[1]),
                plane.c2p(*wv),
                color=YELLOW, fill_opacity=0.3, stroke_width=2,
            )

        # Eigenspace line: span(v) — the line that becomes "the span" when w aligns
        v_unit = v / np.linalg.norm(v)
        span_line = Line(plane.c2p(-4 * v_unit[0], -4 * v_unit[1]),
                         plane.c2p(4 * v_unit[0], 4 * v_unit[1]),
                         color=YELLOW, stroke_width=2, stroke_opacity=0.5)

        v_lbl = MathTex(r"\vec v", color=GREEN, font_size=24).next_to(
            plane.c2p(*v), UR, buff=0.05)

        def w_lbl():
            wv = w_vec()
            return MathTex(r"\vec w", color=RED if is_dependent() else ORANGE,
                           font_size=24).next_to(plane.c2p(*wv), UR, buff=0.05)

        self.play(Create(span_line), GrowArrow(v_arrow()), Write(v_lbl))
        self.add(always_redraw(parallelogram), always_redraw(w_arrow),
                 always_redraw(w_lbl))

        # RIGHT COLUMN
        rcol_x = +5.4

        def info_panel():
            t = theta_tr.get_value()
            wv = w_vec()
            det = v[0] * wv[1] - v[1] * wv[0]  # area of parallelogram (signed)
            angle_diff = abs((t - theta_v + PI) % (2 * PI) - PI)
            angle_deg = np.degrees(angle_diff)
            if is_dependent():
                status = Tex(r"\textbf{dependent}", color=RED, font_size=24)
                span_str = "line"
            else:
                status = Tex(r"\textbf{independent}", color=GREEN, font_size=24)
                span_str = r"$\mathbb{R}^2$"
            return VGroup(
                MathTex(rf"\angle = {angle_deg:.0f}^\circ",
                        color=WHITE, font_size=22),
                MathTex(rf"\det[\vec v\ \vec w] = {det:+.2f}",
                        color=YELLOW, font_size=22),
                Tex(rf"span $=$ {span_str}",
                    color=YELLOW, font_size=22),
                status,
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([rcol_x, +0.4, 0])

        self.add(always_redraw(info_panel))

        # Sweep through several angles, including the two degeneracies
        targets = [theta_v + 0.8,        # independent
                   theta_v,              # parallel = dependent
                   theta_v + PI / 3,     # independent
                   theta_v + PI,         # antiparallel = dependent
                   theta_v + PI / 2]     # perpendicular
        for ang in targets:
            self.play(theta_tr.animate.set_value(ang),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
