from manim import *
import numpy as np


class JuliaVsMandelbrotExample(Scene):
    """
    Pick c on the Mandelbrot plane → see the corresponding Julia set.

    COMPARISON layout:
      LEFT   — Mandelbrot heatmap (precomputed). A moving yellow dot
               at the current c, driven by ValueTracker s that sweeps
               c along a chosen path through interesting regions.
      RIGHT  — Julia set heatmap that recomputes via always_redraw at
               the current c value.

    Watch the Julia set transition from connected (c inside M) to
    Cantor dust (c outside M) as the moving dot crosses the Mandelbrot
    boundary.
    """

    def construct(self):
        title = Tex(r"Julia$(c)$ vs Mandelbrot: pick $c$ on left $\to$ Julia on right",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Precomputed Mandelbrot
        nx_m, ny_m = 60, 50
        cx_m = np.linspace(-2.0, 0.7, nx_m)
        cy_m = np.linspace(-1.1, 1.1, ny_m)
        CX_m, CY_m = np.meshgrid(cx_m, cy_m)
        C_m = CX_m + 1j * CY_m
        Z = np.zeros_like(C_m)
        escaped_m = np.full(C_m.shape, 30, dtype=int)
        for n in range(30):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask] ** 2 + C_m[mask]
            new_esc = mask & (np.abs(Z) > 2)
            escaped_m[new_esc] = n

        m_anchor = np.array([-3.6, -0.4, 0])
        m_w, m_h = 4.0, 3.4
        cell_mw = m_w / nx_m * 0.96
        cell_mh = m_h / ny_m * 0.96
        xs_m = np.linspace(m_anchor[0] - m_w / 2 + cell_mw / 2,
                           m_anchor[0] + m_w / 2 - cell_mw / 2, nx_m)
        ys_m = np.linspace(m_anchor[1] - m_h / 2 + cell_mh / 2,
                           m_anchor[1] + m_h / 2 - cell_mh / 2, ny_m)

        m_pixels = VGroup()
        for j in range(ny_m):
            for i in range(nx_m):
                n = escaped_m[j, i]
                if n >= 30:
                    col = BLACK
                else:
                    col = interpolate_color(BLUE_E, YELLOW, n / 30)
                rect = Rectangle(width=cell_mw, height=cell_mh,
                                 fill_color=col, fill_opacity=1.0,
                                 stroke_width=0)
                rect.move_to([xs_m[i], ys_m[j], 0])
                m_pixels.add(rect)
        m_lbl = Tex(r"Mandelbrot $\mathcal{M}$", color=YELLOW,
                    font_size=22).next_to(m_pixels, UP, buff=0.05)
        self.play(FadeIn(m_pixels), Write(m_lbl))

        # Julia parameters for animation: a small path through interesting c values
        c_path = [
            -0.8 + 0.156j,    # rabbit / connected
             0.285 + 0.01j,    # near boundary
            -0.4 + 0.6j,       # spiral
            -0.7 + 0.27j,      # filled-in
             0.36 + 0.1j,       # outside M → Cantor dust
        ]
        s = ValueTracker(0.001)

        def current_c():
            v = s.get_value()
            n = len(c_path)
            idx = min(int(v * (n - 1)), n - 2)
            frac = v * (n - 1) - idx
            return (1 - frac) * c_path[idx] + frac * c_path[idx + 1]

        # Moving cursor on Mandelbrot plane
        def m_to_screen(c):
            x_world = (c.real - cx_m[0]) / (cx_m[-1] - cx_m[0])
            y_world = (c.imag - cy_m[0]) / (cy_m[-1] - cy_m[0])
            screen_x = m_anchor[0] - m_w / 2 + x_world * m_w
            screen_y = m_anchor[1] - m_h / 2 + y_world * m_h
            return [screen_x, screen_y, 0]

        def cursor_dot():
            return Dot(m_to_screen(current_c()),
                       color=YELLOW, radius=0.10, stroke_width=2,
                       stroke_color=WHITE)

        self.add(always_redraw(cursor_dot))

        # Julia heatmap
        nx_j, ny_j = 50, 50
        zx = np.linspace(-1.6, 1.6, nx_j)
        zy = np.linspace(-1.6, 1.6, ny_j)
        ZX, ZY = np.meshgrid(zx, zy)
        Z0 = ZX + 1j * ZY  # initial z values

        j_anchor = np.array([+3.4, -0.4, 0])
        j_w, j_h = 3.6, 3.6
        cell_jw = j_w / nx_j * 0.96
        cell_jh = j_h / ny_j * 0.96
        xs_j = np.linspace(j_anchor[0] - j_w / 2 + cell_jw / 2,
                           j_anchor[0] + j_w / 2 - cell_jw / 2, nx_j)
        ys_j = np.linspace(j_anchor[1] - j_h / 2 + cell_jh / 2,
                           j_anchor[1] + j_h / 2 - cell_jh / 2, ny_j)

        def julia_grid():
            c = current_c()
            Z = Z0.copy()
            escaped = np.full(Z.shape, 25, dtype=int)
            for n in range(25):
                mask = np.abs(Z) <= 2
                Z[mask] = Z[mask] ** 2 + c
                new_esc = mask & (np.abs(Z) > 2)
                escaped[new_esc] = n
            grp = VGroup()
            for j in range(ny_j):
                for i in range(nx_j):
                    n = escaped[j, i]
                    if n >= 25:
                        col = BLACK
                    else:
                        col = interpolate_color(PURPLE_E, ORANGE, n / 25)
                    rect = Rectangle(width=cell_jw, height=cell_jh,
                                     fill_color=col, fill_opacity=1.0,
                                     stroke_width=0)
                    rect.move_to([xs_j[i], ys_j[j], 0])
                    grp.add(rect)
            return grp

        self.add(always_redraw(julia_grid))

        j_lbl = Tex(r"Julia$(c)$", color=ORANGE,
                    font_size=22).move_to([j_anchor[0], j_anchor[1] + j_h / 2 + 0.3, 0])
        self.play(Write(j_lbl))

        # Bottom: live c value
        def c_readout():
            c = current_c()
            return Tex(rf"$c = {c.real:+.3f} {c.imag:+.3f}\,i$",
                       color=YELLOW, font_size=24).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(c_readout))

        self.play(s.animate.set_value(1.0), run_time=8, rate_func=linear)
        self.wait(0.8)
