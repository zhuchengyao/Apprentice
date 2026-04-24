from manim import *
import numpy as np


class BaselProblemExample(Scene):
    """
    Animate the Basel partial sums climbing to π²/6.

    A ValueTracker N sweeps from 1 to 40. Always-redrawn curves show
    both the reciprocal-square bars 1/k² and the cumulative partial
    sum S_N = Σ 1/k² climbing toward the dashed target π²/6 ≈ 1.6449.
    A live readout displays the current gap π²/6 − S_N shrinking.
    """

    def construct(self):
        title = Tex(r"Basel partial sums: $1 + \tfrac{1}{4} + \tfrac{1}{9} + \cdots \to \tfrac{\pi^2}{6}$",
                    font_size=34).to_edge(UP)
        self.play(Write(title))

        target = PI ** 2 / 6
        N_max = 40

        axes_L = Axes(
            x_range=[0, N_max + 1, 10], y_range=[0, 1.1, 0.25],
            x_length=4.8, y_length=3.4,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).shift(LEFT * 3.5 + 0.1 * DOWN)
        L_title = Tex(r"term $1/k^2$", font_size=26, color=BLUE).next_to(axes_L, UP, buff=0.05)

        axes_R = Axes(
            x_range=[0, N_max + 1, 10], y_range=[0, 1.8, 0.3],
            x_length=4.8, y_length=3.4,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).shift(RIGHT * 3.5 + 0.1 * DOWN)
        R_title = Text("partial sum Sₙ", font_size=20, color=YELLOW).next_to(axes_R, UP, buff=0.05)

        limit_line = DashedLine(
            axes_R.c2p(0, target), axes_R.c2p(N_max, target),
            color=GREEN, stroke_width=2,
        )
        limit_lbl = MathTex(r"\tfrac{\pi^2}{6}", color=GREEN, font_size=28).next_to(
            axes_R.c2p(N_max, target), RIGHT, buff=0.05
        )

        self.play(Create(axes_L), Create(axes_R), Write(L_title), Write(R_title))
        self.play(Create(limit_line), Write(limit_lbl))

        N_tracker = ValueTracker(0)

        partial_cache = np.cumsum([1.0 / (k * k) for k in range(1, N_max + 2)])

        def bars_up_to_N():
            n = int(N_tracker.get_value())
            group = VGroup()
            for k in range(1, n + 1):
                h = 1.0 / (k * k)
                base = axes_L.c2p(k, 0)
                top = axes_L.c2p(k, h)
                bar_h = abs(top[1] - base[1])
                bar = Rectangle(width=0.12, height=bar_h,
                                color=BLUE, fill_opacity=0.75, stroke_width=0.3)
                bar.move_to((np.array(base) + np.array(top)) / 2)
                group.add(bar)
            return group

        def cumulative_curve():
            n_real = N_tracker.get_value()
            n_floor = int(np.floor(n_real))
            frac = n_real - n_floor
            pts = [axes_R.c2p(0, 0)]
            for k in range(1, n_floor + 1):
                pts.append(axes_R.c2p(k, partial_cache[k - 1]))
            if n_floor < N_max and n_real > 0:
                # Interpolate to the current fractional N
                if n_floor >= 1:
                    s0 = partial_cache[n_floor - 1]
                else:
                    s0 = 0.0
                s_next = partial_cache[n_floor]
                s_interp = s0 + (s_next - s0) * frac
                pts.append(axes_R.c2p(n_real, s_interp))
            curve = VMobject(color=YELLOW, stroke_width=3)
            if len(pts) >= 2:
                curve.set_points_as_corners(pts)
            else:
                curve.set_points_as_corners([pts[0], pts[0]])
            return curve

        def moving_dot():
            n_real = N_tracker.get_value()
            n_floor = int(np.floor(n_real))
            frac = n_real - n_floor
            if n_floor >= 1:
                s0 = partial_cache[n_floor - 1]
            else:
                s0 = 0.0
            s_next = partial_cache[n_floor] if n_floor < N_max else partial_cache[N_max - 1]
            s_interp = s0 + (s_next - s0) * frac
            return Dot(axes_R.c2p(n_real, s_interp), color=YELLOW, radius=0.09)

        self.add(always_redraw(bars_up_to_N),
                 always_redraw(cumulative_curve),
                 always_redraw(moving_dot))

        # Live sum and gap
        def current_sum():
            n_real = N_tracker.get_value()
            n_floor = int(np.floor(n_real))
            frac = n_real - n_floor
            if n_floor >= 1:
                s0 = partial_cache[n_floor - 1]
            else:
                s0 = 0.0
            s_next = partial_cache[n_floor] if n_floor < N_max else partial_cache[N_max - 1]
            return s0 + (s_next - s0) * frac

        sum_text = always_redraw(lambda: MathTex(
            rf"S_N = {current_sum():.5f}", color=YELLOW, font_size=28
        ).to_edge(DOWN).shift(UP * 0.5))
        gap_text = always_redraw(lambda: MathTex(
            rf"\tfrac{{\pi^2}}{{6}} - S_N = {target - current_sum():.5f}",
            color=GREEN, font_size=26
        ).to_edge(DOWN).shift(UP * 0.05))
        N_text = always_redraw(lambda: MathTex(
            rf"N = {int(N_tracker.get_value())}", color=WHITE, font_size=26
        ).to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.4))

        self.add(sum_text, gap_text, N_text)

        self.play(N_tracker.animate.set_value(N_max), run_time=9, rate_func=linear)
        self.wait(0.6)

        formula = MathTex(
            r"\sum_{k=1}^{\infty} \frac{1}{k^2} = \frac{\pi^2}{6}",
            font_size=34, color=GREEN,
        ).to_edge(DOWN)
        self.play(FadeOut(sum_text), FadeOut(gap_text), Write(formula))
        self.wait(1.0)
