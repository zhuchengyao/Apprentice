from manim import *
import numpy as np


class ZeckendorfRepresentationExample(Scene):
    """
    Zeckendorf's theorem: every positive integer has a unique
    representation as a sum of non-consecutive Fibonacci numbers.
    Fibs: 1, 2, 3, 5, 8, 13, 21, 34, 55, 89.

    Example: 100 = 89 + 8 + 3 = F(11) + F(6) + F(4).

    SINGLE_FOCUS: 10 Fibonacci boxes shown; ValueTracker n_tr sweeps
    n ∈ {37, 100, 57, 64, 78, 123, 100}; always_redraw greedy-Zeckendorf
    decomposition highlights selected boxes and writes equation.
    """

    def construct(self):
        title = Tex(r"Zeckendorf: $n=\sum F_{k_i}$ with $k_{i+1}\ge k_i+2$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        fibs = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        cell_s = 1.0
        origin = np.array([-5.2, 1.2, 0])

        boxes = VGroup()
        for i, f in enumerate(fibs):
            cell = Rectangle(width=cell_s * 0.95, height=cell_s * 0.9,
                             color=BLUE, stroke_width=1.5,
                             fill_color=BLUE, fill_opacity=0.15).move_to(
                origin + RIGHT * i * cell_s)
            lbl = VGroup(
                Tex(rf"$F_{{{i+2}}}$", font_size=18, color=BLUE),
                Tex(str(f), font_size=22),
            ).arrange(DOWN, buff=0.05).move_to(origin + RIGHT * i * cell_s)
            boxes.add(cell, lbl)
        self.play(FadeIn(boxes))

        def zeckendorf(n):
            res = []
            for i in range(len(fibs) - 1, -1, -1):
                if fibs[i] <= n:
                    res.append(i)
                    n -= fibs[i]
                    if n == 0: break
            return res

        n_targets = [37, 100, 57, 64, 78, 123, 100]
        n_idx_tr = ValueTracker(0.0)

        def n_now():
            idx = max(0, min(len(n_targets) - 1, int(round(n_idx_tr.get_value()))))
            return n_targets[idx]

        def highlights():
            n = n_now()
            sel = zeckendorf(n)
            grp = VGroup()
            for i in sel:
                grp.add(Rectangle(width=cell_s * 0.95, height=cell_s * 0.9,
                                   color=YELLOW, stroke_width=3).move_to(
                    origin + RIGHT * i * cell_s))
            return grp
        self.add(always_redraw(highlights))

        # Equation
        def equation_str():
            n = n_now()
            sel = zeckendorf(n)
            parts = [f"F_{{{i+2}}}({fibs[i]})" for i in sorted(sel, reverse=True)]
            return rf"$n={n}=" + "+".join(parts) + "$"

        eq_tex = Tex(equation_str(), font_size=26, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.add(eq_tex)

        def update_eq(mob, dt):
            new = Tex(equation_str(), font_size=26, color=YELLOW).move_to(eq_tex)
            eq_tex.become(new)
            return eq_tex
        eq_tex.add_updater(update_eq)

        info = VGroup(
            VGroup(Tex(r"$n=$", font_size=24),
                   DecimalNumber(37, num_decimal_places=0,
                                 font_size=24).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            Tex(r"greedy: subtract largest $F_k\le n$",
                color=GREEN, font_size=20),
            Tex(r"never two consecutive Fibs",
                color=GREEN, font_size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(n_now()))
        self.add(info)

        for k in range(1, len(n_targets)):
            self.play(n_idx_tr.animate.set_value(float(k)),
                      run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.5)
