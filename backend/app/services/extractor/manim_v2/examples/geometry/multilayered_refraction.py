from manim import *
import numpy as np


class MultilayeredRefractionExample(Scene):
    """
    Light bending through stratified media — discrete layers approximate
    a smooth gradient.

    SINGLE_FOCUS:
      Stack of N layers with refractive indices n_i increasing top to
      bottom. ValueTracker N_layers steps 1 → 8 → 30; each step
      builds the layered medium and traces the broken-line ray path
      via Snell's law. As N grows, the path approaches a smooth curve
      (sin(θ_i) / n_i = const for all layers).
    """

    def construct(self):
        title = Tex(r"Multi-layer refraction: $\sin\theta / n = $ const (Snell)",
                    font_size=24).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Frame for the medium
        top_y = +1.8
        bottom_y = -2.6
        x_left = -5.5
        x_right = +1.5

        # Refractive indices n(y): increase from 1 at top to 1.5 at bottom
        def n_at(y_norm):
            return 1.0 + 0.5 * y_norm  # y_norm ∈ [0, 1] from top to bottom

        # Source angle and incident path
        theta_0 = np.radians(60)  # angle from vertical at top layer
        x_start = x_left + 0.5
        y_start = top_y

        N_tr = ValueTracker(1)

        def build_medium():
            N = max(1, int(round(N_tr.get_value())))
            grp = VGroup()
            layer_h = (top_y - bottom_y) / N
            for i in range(N):
                y_top = top_y - i * layer_h
                y_bot = top_y - (i + 1) * layer_h
                y_mid_norm = (i + 0.5) / N
                n = n_at(y_mid_norm)
                color_t = (n - 1.0) / 0.5  # 0 at top, 1 at bottom
                color = interpolate_color(BLUE_A, BLUE_E, color_t)
                rect = Rectangle(width=x_right - x_left,
                                 height=abs(y_top - y_bot),
                                 color=color, fill_opacity=0.5,
                                 stroke_width=0.5, stroke_color=GREY_B)
                rect.move_to([(x_left + x_right) / 2, (y_top + y_bot) / 2, 0])
                grp.add(rect)
            return grp

        def build_path():
            N = max(1, int(round(N_tr.get_value())))
            layer_h = (top_y - bottom_y) / N
            sin_theta_init = np.sin(theta_0)
            n_init = n_at(0.0001)
            const = sin_theta_init / n_init  # Snell's invariant

            pts = [np.array([x_start, y_start, 0])]
            current_x = x_start
            for i in range(N):
                y_mid_norm = (i + 0.5) / N
                n_layer = n_at(y_mid_norm)
                sin_theta = const * n_layer
                sin_theta = min(0.999, sin_theta)
                tan_theta = sin_theta / np.sqrt(1 - sin_theta ** 2)
                dx = layer_h * tan_theta
                next_y = y_start - (i + 1) * layer_h
                current_x += dx
                pts.append(np.array([current_x, next_y, 0]))

            path = VMobject(color=YELLOW, stroke_width=4)
            path.set_points_as_corners(pts)
            return path

        medium = always_redraw(build_medium)
        ray_path = always_redraw(build_path)
        self.add(medium, ray_path)

        # Source dot
        source = Dot([x_start, y_start + 0.3, 0], color=GREEN, radius=0.10)
        source_lbl = Tex(r"source", color=GREEN, font_size=18).next_to(source, UP, buff=0.05)
        self.play(FadeIn(source), Write(source_lbl))

        # RIGHT COLUMN
        rcol_x = +4.2

        def info_panel():
            N = int(round(N_tr.get_value()))
            return VGroup(
                MathTex(rf"N\,\text{{layers}} = {N}",
                        color=YELLOW, font_size=24),
                MathTex(rf"n_{{\text{{top}}}} = 1.0,\ n_{{\text{{bot}}}} = 1.5",
                        color=BLUE, font_size=20),
                MathTex(r"\theta_0 = 60^\circ", color=GREEN, font_size=22),
                MathTex(r"n\sin\theta = \text{const}",
                        color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([rcol_x, +0.6, 0])

        self.add(always_redraw(info_panel))

        smooth_lbl = Tex(r"$N \to \infty$: ray traces a smooth curve",
                         color=YELLOW, font_size=22).to_edge(DOWN, buff=0.4)
        self.play(Write(smooth_lbl))

        for n_val in [3, 8, 16, 30]:
            self.play(N_tr.animate.set_value(n_val),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.6)
