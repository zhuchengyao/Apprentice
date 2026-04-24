from manim import *
import numpy as np


class NewtonFractalExample(Scene):
    """
    Newton fractal for z³ = 1: pixel = color of attracted root.

    SINGLE_FOCUS: 80×80 cell heatmap. ValueTracker iters sweeps 1→25.
    For each starting z₀, the precomputed orbit is read at the current
    iter limit; the pixel is colored by the root it's nearest to. Black
    dots mark the three roots themselves.
    """

    def construct(self):
        title = Tex(r"Newton's method for $z^3 = 1$: which root attracts $z_0$?",
                    font_size=26).to_edge(UP, buff=0.4)
        self.play(Write(title))

        roots = np.array([np.exp(2j * PI * k / 3) for k in range(3)])
        root_colors = [BLUE, RED, GREEN]
        MAX_ITERS = 25

        nx, ny = 80, 60
        x_min, x_max = -1.6, 1.6
        y_min, y_max = -1.2, 1.2
        cx = np.linspace(x_min, x_max, nx)
        cy = np.linspace(y_min, y_max, ny)
        CX, CY = np.meshgrid(cx, cy)
        Z0 = CX + 1j * CY
        Z = Z0.copy()

        # Record orbit history: which root each pixel is nearest to at each iter
        history = np.zeros((MAX_ITERS, ny, nx), dtype=int)
        for n in range(MAX_ITERS):
            mask = np.abs(Z) > 1e-9
            with np.errstate(divide='ignore', invalid='ignore'):
                Z = np.where(mask, Z - (Z ** 3 - 1) / (3 * Z ** 2), Z)
            for k, r in enumerate(roots):
                d = np.abs(Z - r)
                if k == 0:
                    nearest = d
                    history[n] = 0
                else:
                    swap = d < nearest
                    nearest[swap] = d[swap]
                    history[n][swap] = k

        # Display
        anchor = np.array([-0.8, -0.4, 0])
        disp_w, disp_h = 6.0, 4.4
        cell_w = disp_w / nx * 0.97
        cell_h = disp_h / ny * 0.97
        xs_disp = np.linspace(anchor[0] - disp_w / 2 + cell_w / 2,
                              anchor[0] + disp_w / 2 - cell_w / 2, nx)
        ys_disp = np.linspace(anchor[1] - disp_h / 2 + cell_h / 2,
                              anchor[1] + disp_h / 2 - cell_h / 2, ny)

        iters = ValueTracker(1.0)

        def heatmap():
            n = max(0, min(int(iters.get_value()) - 1, MAX_ITERS - 1))
            grp = VGroup()
            for j in range(ny):
                for i in range(nx):
                    k = history[n, j, i]
                    color = root_colors[k]
                    rect = Rectangle(width=cell_w, height=cell_h,
                                     fill_color=color, fill_opacity=0.85,
                                     stroke_width=0)
                    rect.move_to([xs_disp[i], ys_disp[j], 0])
                    grp.add(rect)
            return grp

        self.add(always_redraw(heatmap))

        # Mark the three roots on the display with black dots
        def root_to_screen(r):
            x_world = (r.real - x_min) / (x_max - x_min)
            y_world = (r.imag - y_min) / (y_max - y_min)
            return [anchor[0] - disp_w / 2 + x_world * disp_w,
                    anchor[1] - disp_h / 2 + y_world * disp_h, 0]

        for r in roots:
            self.add(Dot(root_to_screen(r), color=BLACK, radius=0.10,
                         stroke_color=WHITE, stroke_width=2))

        # Right corner readout
        def info_panel():
            return VGroup(
                MathTex(rf"\text{{iter}} = {int(iters.get_value())}",
                        color=WHITE, font_size=24),
                MathTex(r"z_{n+1} = z_n - \tfrac{z_n^3 - 1}{3 z_n^2}",
                        color=YELLOW, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.6)

        self.add(always_redraw(info_panel))

        legend = VGroup(
            VGroup(Dot(color=BLUE, radius=0.12),
                   Tex(r"$\to z_1 = 1$", color=BLUE, font_size=22)).arrange(RIGHT, buff=0.2),
            VGroup(Dot(color=RED, radius=0.12),
                   Tex(r"$\to z_2 = e^{2\pi i/3}$", color=RED, font_size=22)).arrange(RIGHT, buff=0.2),
            VGroup(Dot(color=GREEN, radius=0.12),
                   Tex(r"$\to z_3 = e^{4\pi i/3}$", color=GREEN, font_size=22)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(legend))

        self.play(iters.animate.set_value(MAX_ITERS),
                  run_time=8, rate_func=linear)
        self.wait(0.8)
