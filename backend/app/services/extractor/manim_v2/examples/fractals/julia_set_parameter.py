from manim import *
import numpy as np


class JuliaSetParameterExample(Scene):
    """
    Julia sets for f_c(z) = z² + c vary dramatically with c.
    Tour through 5 distinctive c values:
      c = -0.7 + 0.27i  (Douady rabbit)
      c = -0.8 + 0.156i (very different)
      c = 0.285 + 0.01i
      c = -1.25 + 0.0i  (airplane)
      c = -0.4 + 0.6i   (dendrite)

    SINGLE_FOCUS heatmap recomputed per c via ValueTracker c_idx_tr.
    """

    def construct(self):
        title = Tex(r"Julia set $J_c$ for $f_c(z)=z^2+c$ — tour of $c$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        c_values = [(-0.7, 0.27), (-0.8, 0.156), (0.285, 0.01),
                    (-1.25, 0.0), (-0.4, 0.6)]
        names = ["rabbit", "disconnected", "cauliflower",
                 "airplane", "dendrite"]

        nx, ny = 80, 60
        xs = np.linspace(-1.8, 1.8, nx)
        ys = np.linspace(-1.3, 1.3, ny)
        max_iter = 40

        # Precompute escape iteration counts per c
        julia_data = {}
        for (cr, ci) in c_values:
            c = complex(cr, ci)
            grid = np.zeros((ny, nx))
            for j, y in enumerate(ys):
                for i, x in enumerate(xs):
                    z = complex(x, y)
                    k = 0
                    while k < max_iter and abs(z) < 2:
                        z = z * z + c
                        k += 1
                    grid[j, i] = k
            julia_data[(cr, ci)] = grid

        # Build grid of cells
        cell_w = 8.8 / nx
        cell_h = 4.4 / ny
        center = np.array([0, -0.3, 0])

        c_idx_tr = ValueTracker(0.0)

        def c_now():
            return max(0, min(len(c_values) - 1, int(round(c_idx_tr.get_value()))))

        def heatmap():
            idx = c_now()
            grid = julia_data[c_values[idx]]
            grp = VGroup()
            for j in range(ny):
                for i in range(nx):
                    k = grid[j, i]
                    if k >= max_iter:
                        col = BLACK; op = 0.85
                    else:
                        t = k / max_iter
                        col = interpolate_color(YELLOW, RED, t)
                        op = 0.85
                    rect = Rectangle(width=cell_w * 1.05,
                                      height=cell_h * 1.05,
                                      color=col, stroke_width=0,
                                      fill_color=col, fill_opacity=op)
                    rect.move_to(center + RIGHT * (i - nx / 2) * cell_w
                                  + UP * (j - ny / 2) * cell_h)
                    grp.add(rect)
            return grp

        self.add(always_redraw(heatmap))

        info = VGroup(
            VGroup(Tex(r"$c=$", font_size=22),
                   DecimalNumber(-0.7, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW),
                   Tex(r"$+$", font_size=22),
                   DecimalNumber(0.27, num_decimal_places=3,
                                 font_size=22).set_color(YELLOW),
                   Tex(r"$i$", font_size=22),
                   ).arrange(RIGHT, buff=0.08),
            VGroup(Tex(r"name: ", font_size=20),
                   ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(c_values[c_now()][0]))
        info[0][3].add_updater(lambda m: m.set_value(c_values[c_now()][1]))
        self.add(info)

        # Name label
        name_tex = Tex(names[0], color=YELLOW, font_size=22).to_corner(UR, buff=0.3).shift(DOWN * 1.0)
        self.add(name_tex)
        def update_name(mob, dt):
            idx = c_now()
            new = Tex(names[idx], color=YELLOW, font_size=22).move_to(name_tex)
            name_tex.become(new)
            return name_tex
        name_tex.add_updater(update_name)

        for k in range(1, len(c_values)):
            self.play(c_idx_tr.animate.set_value(float(k)),
                      run_time=2.0, rate_func=smooth)
            self.wait(0.6)
        self.wait(0.5)
