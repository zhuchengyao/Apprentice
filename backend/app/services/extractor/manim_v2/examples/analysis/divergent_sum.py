from manim import *
import numpy as np


class DivergentSumExample(Scene):
    """
    Compare divergent vs convergent series side by side, growing partial
    sums plotted on logarithmic scale.

    TWO_COLUMN:
      LEFT  — Axes (log y) plotting partial sums of three series:
        BLUE   — Σ 1 (constant 1's): linear divergence
        GREEN  — Σ 1/n (harmonic): log divergence (grows ~ log N)
        ORANGE — Σ 1/n² (Basel): converges to π²/6
      ValueTracker N sweeps 1 → 200; always_redraw curves grow.
      RIGHT — live N, 3 partial sums, asymptotic comparisons.
    """

    def construct(self):
        title = Tex(r"Some series diverge: $\sum 1, \sum 1/n$ vs convergent $\sum 1/n^2$",
                    font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        N_max = 200

        # Precompute partial sums
        S_const = np.cumsum(np.ones(N_max + 1))
        S_harmonic = np.cumsum([1.0 / k for k in range(1, N_max + 2)])
        S_basel = np.cumsum([1.0 / k ** 2 for k in range(1, N_max + 2)])
        target_basel = PI * PI / 6

        # Use log-scaled y axis (manually)
        axes = Axes(
            x_range=[0, N_max + 5, 50], y_range=[0, 6, 1],
            x_length=7.0, y_length=4.4,
            axis_config={"include_tip": True, "include_numbers": True, "font_size": 18},
        ).move_to([-2.4, -0.4, 0])
        x_lbl = Tex(r"$N$", font_size=22).next_to(axes, DOWN, buff=0.1)
        y_lbl = Tex(r"$S_N$ (log)", font_size=20).next_to(axes, LEFT, buff=0.1).rotate(PI / 2)
        self.play(Create(axes), Write(x_lbl), Write(y_lbl))

        # Reference horizontal line at log(π²/6) for Basel
        basel_line = DashedLine(axes.c2p(0, np.log(target_basel) + 1),
                                 axes.c2p(N_max, np.log(target_basel) + 1),
                                 color=ORANGE, stroke_width=2, stroke_opacity=0.5)
        basel_lbl = MathTex(rf"\log(\pi^2/6) + 1 \approx {np.log(target_basel)+1:.2f}",
                            color=ORANGE, font_size=18).next_to(
            axes.c2p(N_max, np.log(target_basel) + 1), RIGHT, buff=0.05)
        self.play(Create(basel_line), Write(basel_lbl))

        N_tr = ValueTracker(1.0)

        # Display log(1 + S) so all three are positive
        def display_y(s_val):
            return np.log(1 + s_val)

        def curve_for(arr, color):
            def fn():
                n = max(1, int(N_tr.get_value()))
                pts = [axes.c2p(k, display_y(arr[k])) for k in range(0, n + 1)]
                curve = VMobject(color=color, stroke_width=3)
                if len(pts) >= 2:
                    curve.set_points_as_corners(pts)
                else:
                    curve.set_points_as_corners([pts[0], pts[0]])
                return curve
            return fn

        self.add(always_redraw(curve_for(S_const, BLUE)),
                 always_redraw(curve_for(S_harmonic, GREEN)),
                 always_redraw(curve_for(S_basel, ORANGE)))

        # RIGHT COLUMN
        rcol_x = +4.4

        def info_panel():
            n = max(1, int(N_tr.get_value()))
            return VGroup(
                MathTex(rf"N = {n}", color=WHITE, font_size=24),
                MathTex(rf"\sum 1 = {S_const[n]:.0f}",
                        color=BLUE, font_size=22),
                MathTex(rf"\sum \tfrac{{1}}{{n}} \approx {S_harmonic[n]:.3f}",
                        color=GREEN, font_size=22),
                MathTex(rf"\sum \tfrac{{1}}{{n^2}} \approx {S_basel[n]:.4f}",
                        color=ORANGE, font_size=22),
                MathTex(rf"\pi^2/6 = {target_basel:.4f}",
                        color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +0.6, 0])

        self.add(always_redraw(info_panel))

        rates = Tex(r"linear vs log vs convergent",
                    color=GREY_B, font_size=22).move_to([rcol_x, -2.6, 0])
        self.play(Write(rates))

        self.play(N_tr.animate.set_value(N_max), run_time=8, rate_func=linear)
        self.wait(0.6)
