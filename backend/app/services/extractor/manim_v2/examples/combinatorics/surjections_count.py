from manim import *
import numpy as np
from math import comb, factorial


class SurjectionsCountExample(Scene):
    """
    Count surjections f: [n] → [k]: by inclusion-exclusion,
    S(n, k) = k! · S_2(n, k) = Σ_{j=0}^k (-1)^j C(k, j) (k-j)^n,
    where S_2 is Stirling 2nd kind.

    SINGLE_FOCUS:
      ValueTracker n_tr and k_tr vary n and k; always_redraw show
      surjection count formula and numeric value.
    """

    def construct(self):
        title = Tex(r"Surjections $f: [n] \to [k]$: count by inclusion-exclusion",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        def surjections(n, k):
            return sum((-1) ** j * comb(k, j) * (k - j) ** n
                        for j in range(k + 1))

        n_tr = ValueTracker(3)
        k_tr = ValueTracker(2)

        def formula_display():
            n = int(round(n_tr.get_value()))
            k = int(round(k_tr.get_value()))
            n = max(1, min(n, 6))
            k = max(1, min(k, n))
            terms = []
            total = 0
            for j in range(k + 1):
                term = (-1) ** j * comb(k, j) * (k - j) ** n
                total += term
                if term != 0:
                    sign = "+" if term > 0 else "-"
                    if j == 0:
                        terms.append(f"{abs(term)}")
                    else:
                        terms.append(f"{sign}{abs(term)}")
            formula_str = " ".join(terms) + f" = {total}"
            return MathTex(formula_str, color=GREEN, font_size=22
                             ).move_to([0, 1, 0])

        self.add(always_redraw(formula_display))

        # Grid showing a surjection example
        def surjection_grid():
            n = int(round(n_tr.get_value()))
            k = int(round(k_tr.get_value()))
            n = max(1, min(n, 6))
            k = max(1, min(k, n))
            # Example surjection: distribute n elements to k buckets round-robin
            f_map = [i % k for i in range(n)]
            # Ensure surjective: if some bucket missing, add
            missing = set(range(k)) - set(f_map)
            if missing:
                for m in missing:
                    f_map[m % n] = m

            cell = 0.6
            n_origin = np.array([-3, -1.5, 0])
            k_origin = np.array([2, -1.5, 0])
            colors = [BLUE, GREEN, ORANGE, PURPLE, PINK, YELLOW]
            grp = VGroup()
            # Left column: n elements
            for i in range(n):
                sq = Circle(radius=0.2, color=WHITE,
                              stroke_width=1.5, fill_opacity=0.2
                              ).move_to(n_origin + np.array([0, -i * cell, 0]))
                grp.add(sq)
                grp.add(MathTex(rf"{i + 1}", color=WHITE, font_size=16
                                  ).move_to(sq.get_center()))
            # Right column: k buckets
            for j in range(k):
                sq = Circle(radius=0.25, color=colors[j % len(colors)],
                              stroke_width=2, fill_opacity=0.4
                              ).move_to(k_origin + np.array([0, -j * cell, 0]))
                grp.add(sq)
                grp.add(MathTex(rf"{j + 1}", color=BLACK, font_size=18
                                  ).move_to(sq.get_center()))
            # Arrows
            for i in range(n):
                target = f_map[i]
                grp.add(Arrow(n_origin + np.array([0.2, -i * cell, 0]),
                                k_origin + np.array([-0.25, -target * cell, 0]),
                                color=colors[target % len(colors)],
                                buff=0.05, stroke_width=1.5,
                                max_tip_length_to_length_ratio=0.1))
            return grp

        self.add(always_redraw(surjection_grid))

        def info():
            n = int(round(n_tr.get_value()))
            k = int(round(k_tr.get_value()))
            n = max(1, min(n, 6))
            k = max(1, min(k, n))
            count = surjections(n, k)
            return VGroup(
                MathTex(rf"n = {n},\ k = {k}",
                         color=YELLOW, font_size=24),
                MathTex(rf"\text{{surjections}} = {count}",
                         color=GREEN, font_size=24),
                MathTex(rf"= k! \cdot S_2(n, k)",
                         color=WHITE, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for (nv, kv) in [(4, 2), (5, 3), (6, 3), (5, 4), (4, 3)]:
            self.play(n_tr.animate.set_value(nv),
                       k_tr.animate.set_value(kv),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.7)
        self.wait(0.4)
