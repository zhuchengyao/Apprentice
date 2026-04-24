from manim import *
import numpy as np


class TwoWaveInterferenceExample(Scene):
    """
    Two coherent point-source waves create a time-varying interference field.

    SINGLE_FOCUS heatmap: the colored grid shows the instantaneous wave
    field cos(k·d₁ − ωt) + cos(k·d₂ − ωt) at every point. ValueTracker t
    advances; the field redraws via always_redraw, so you see the wave
    fronts radiate from each source AND watch destructive nodal lines
    stay perfectly still while constructive antinodes oscillate hardest.

    Captions and live readouts appear on the right column.
    """

    def construct(self):
        title = Tex(r"Interference: two coherent sources $\to$ standing pattern",
                    font_size=28).to_edge(UP, buff=0.4)
        self.play(Write(title))

        s1 = np.array([-3.0, 0.0, 0.0])
        s2 = np.array([+3.0, 0.0, 0.0])
        src1 = Dot(s1, color=RED, radius=0.12)
        src2 = Dot(s2, color=BLUE, radius=0.12)
        self.play(FadeIn(src1), FadeIn(src2))

        k = 2.4   # wavenumber
        omega = 4.0  # angular frequency

        t_tracker = ValueTracker(0.0)

        # Heatmap grid (lower res for speed)
        nx, ny = 60, 30
        x_min, x_max = -5.5, 5.5
        y_min, y_max = -2.6, 2.0  # leave room above for title and below for caption
        cell_w = (x_max - x_min) / nx * 0.96
        cell_h = (y_max - y_min) / ny * 0.96

        # Precompute distances once (huge speedup)
        xs = np.linspace(x_min + cell_w / 2, x_max - cell_w / 2, nx)
        ys = np.linspace(y_min + cell_h / 2, y_max - cell_h / 2, ny)
        XX, YY = np.meshgrid(xs, ys)
        D1 = np.sqrt((XX - s1[0]) ** 2 + (YY - s1[1]) ** 2)
        D2 = np.sqrt((XX - s2[0]) ** 2 + (YY - s2[1]) ** 2)

        def field_grid():
            t = t_tracker.get_value()
            amp = np.cos(k * D1 - omega * t) + np.cos(k * D2 - omega * t)
            # Normalize to [-1, 1] (max amplitude is 2)
            normalized = amp / 2
            grp = VGroup()
            for j in range(ny):
                for i in range(nx):
                    val = normalized[j, i]
                    if val >= 0:
                        col = interpolate_color(BLACK, YELLOW, val)
                    else:
                        col = interpolate_color(BLACK, BLUE_C, -val)
                    rect = Rectangle(width=cell_w, height=cell_h,
                                     fill_color=col, fill_opacity=0.85,
                                     stroke_width=0)
                    rect.move_to([xs[i], ys[j], 0])
                    grp.add(rect)
            return grp

        self.add(always_redraw(field_grid))
        # Re-add sources on top
        self.add(src1, src2)

        # Right-side caption + formula
        caption = Tex(r"yellow = crest, blue = trough", color=GREY_B,
                      font_size=22).to_edge(DOWN).shift(UP * 0.6)
        formula = MathTex(
            r"\psi(\mathbf{r}, t) = \cos(k d_1 - \omega t) + \cos(k d_2 - \omega t)",
            font_size=26, color=YELLOW,
        ).to_edge(DOWN).shift(UP * 0.1)
        self.play(Write(caption), Write(formula))

        # Advance time so wave fronts radiate
        self.play(t_tracker.animate.set_value(2 * PI / omega * 3),
                  run_time=8, rate_func=linear)

        node_lbl = Tex(r"Nodal lines (always dark) sit on perpendicular bisectors",
                       color=WHITE, font_size=20).to_edge(UP).shift(DOWN * 0.6)
        self.play(Write(node_lbl))
        self.wait(0.8)
