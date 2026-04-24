from manim import *
import numpy as np


class MandelbrotSetExample(Scene):
    """
    Mandelbrot set boundary materializes as iteration count grows.

    SINGLE_FOCUS: 100×60 cell heatmap of escape time for c on a grid.
    A ValueTracker `iters` advances 4 → 60. At each step the heatmap
    redraws via always_redraw using `iters` as the bailout limit:
      - cells whose orbit escapes within `iters` iterations are colored
        by escape speed (warm gradient);
      - cells whose orbit hasn't escaped yet are BLACK.
    Watch the boundary detail emerge as `iters` climbs.
    """

    def construct(self):
        title = Tex(r"Mandelbrot set: $c$ such that $z_{n+1} = z_n^2 + c$ stays bounded",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        nx, ny = 100, 60
        x_min, x_max = -2.1, 0.7
        y_min, y_max = -1.1, 1.1

        # Precompute c values
        cx = np.linspace(x_min, x_max, nx)
        cy = np.linspace(y_min, y_max, ny)
        CX, CY = np.meshgrid(cx, cy)
        C = CX + 1j * CY

        # Precompute the FULL escape iterations once (max 60). Per-frame we
        # just look up the count and clamp to current `iters`.
        MAX_ITERS = 60
        Z = np.zeros_like(C)
        escaped_at = np.full(C.shape, MAX_ITERS, dtype=int)
        for n in range(MAX_ITERS):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask] ** 2 + C[mask]
            newly_escaped = mask & (np.abs(Z) > 2)
            escaped_at[newly_escaped] = n

        # Display geometry: occupy x ∈ [-5, 4], y ∈ [-2.4, 1.6]
        disp_x_min, disp_x_max = -5.5, +3.5
        disp_y_min, disp_y_max = -2.6, +1.6
        cell_w = (disp_x_max - disp_x_min) / nx * 0.96
        cell_h = (disp_y_max - disp_y_min) / ny * 0.96

        xs_disp = np.linspace(disp_x_min + cell_w / 2,
                              disp_x_max - cell_w / 2, nx)
        ys_disp = np.linspace(disp_y_min + cell_h / 2,
                              disp_y_max - cell_h / 2, ny)

        iters = ValueTracker(4.0)

        def heatmap():
            limit = int(iters.get_value())
            grp = VGroup()
            for j in range(ny):
                for i in range(nx):
                    n = escaped_at[j, i]
                    if n >= limit:
                        col = BLACK
                    else:
                        t = n / max(1, limit)
                        col = interpolate_color(BLUE_E, YELLOW, t)
                    rect = Rectangle(width=cell_w, height=cell_h,
                                     fill_color=col, fill_opacity=1.0,
                                     stroke_width=0)
                    rect.move_to([xs_disp[i], ys_disp[j], 0])
                    grp.add(rect)
            return grp

        self.add(always_redraw(heatmap))

        # Bottom-right live readout
        rcol_x = +5.0

        def info_panel():
            return VGroup(
                MathTex(rf"\text{{max iter}} = {int(iters.get_value())}",
                        color=WHITE, font_size=24),
                MathTex(r"z_{n+1} = z_n^2 + c", color=YELLOW, font_size=22),
                MathTex(r"z_0 = 0", color=GREY_B, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR).shift(LEFT * 0.3 + DOWN * 0.6)

        self.add(always_redraw(info_panel))

        self.play(iters.animate.set_value(60.0),
                  run_time=8, rate_func=linear)
        self.wait(0.6)

        caption = Tex(r"Black region = bounded orbit (the Mandelbrot set $\mathcal{M}$)",
                      color=YELLOW, font_size=22).to_edge(DOWN, buff=0.3)
        self.play(Write(caption))
        self.wait(1.0)
