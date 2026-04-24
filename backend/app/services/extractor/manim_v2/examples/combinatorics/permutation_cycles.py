from manim import *
import numpy as np


class PermutationCyclesExample(Scene):
    """
    Any permutation decomposes uniquely into disjoint cycles. For
    σ = (1→3, 2→5, 3→4, 4→1, 5→2, 6→6) in S_6, cycle decomposition
    is (1 3 4)(2 5)(6).

    SINGLE_FOCUS:
      6 numbered dots; ValueTracker step_tr reveals arrows i → σ(i)
      one at a time; always_redraw colored cycles; final: 3 cycles
      of lengths 3, 2, 1.
    """

    def construct(self):
        title = Tex(r"Permutation = disjoint cycles: $\sigma = (1\,3\,4)(2\,5)(6)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Circular positions
        n = 6
        R = 2.5
        center = np.array([-1, -0.3, 0])
        positions = [center + R * np.array([np.cos(2 * PI * k / n + PI / 2),
                                                np.sin(2 * PI * k / n + PI / 2), 0])
                     for k in range(n)]

        # Permutation: 0 → 2, 1 → 4, 2 → 3, 3 → 0, 4 → 1, 5 → 5
        # (1-indexed: 1→3, 2→5, 3→4, 4→1, 5→2, 6→6)
        sigma = [2, 4, 3, 0, 1, 5]

        # Dots + labels
        dots_grp = VGroup()
        for i, p in enumerate(positions):
            c = Circle(radius=0.3, color=WHITE, fill_opacity=0.2,
                         stroke_width=2).move_to(p)
            dots_grp.add(c)
            lbl = MathTex(rf"{i + 1}", font_size=22, color=WHITE
                            ).move_to(p)
            dots_grp.add(lbl)
        self.play(FadeIn(dots_grp))

        # Identify cycles
        # Cycle containing vertex i: follow i → sigma[i] → sigma[sigma[i]] → ...
        cycles = []
        visited = [False] * n
        for i in range(n):
            if visited[i]:
                continue
            cycle = [i]
            visited[i] = True
            j = sigma[i]
            while j != i:
                cycle.append(j)
                visited[j] = True
                j = sigma[j]
            cycles.append(cycle)

        cycle_colors = [BLUE, GREEN, RED, ORANGE, PURPLE]

        step_tr = ValueTracker(0)

        def arrows_reveal():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, n))
            grp = VGroup()
            for i in range(s):
                # Find which cycle i belongs to
                for ci, cyc in enumerate(cycles):
                    if i in cyc:
                        col = cycle_colors[ci % len(cycle_colors)]
                        break
                j = sigma[i]
                if i == j:
                    # Fixed point: small loop indicator
                    grp.add(Circle(radius=0.42, color=col,
                                     stroke_width=3, fill_opacity=0
                                     ).move_to(positions[i]))
                else:
                    start = positions[i]
                    end = positions[j]
                    grp.add(Arrow(start, end, color=col,
                                    buff=0.35, stroke_width=3,
                                    max_tip_length_to_length_ratio=0.15))
            return grp

        self.add(always_redraw(arrows_reveal))

        def info():
            s = int(round(step_tr.get_value()))
            s = max(0, min(s, n))
            return VGroup(
                MathTex(rf"\text{{arrows}} = {s}/{n}",
                         color=WHITE, font_size=22),
                Tex(r"BLUE: $(1\,3\,4)$", color=BLUE, font_size=20),
                Tex(r"GREEN: $(2\,5)$", color=GREEN, font_size=20),
                Tex(r"RED: $(6)$ fixed", color=RED, font_size=20),
                MathTex(r"\text{type} = 3 + 2 + 1 = 6",
                         color=YELLOW, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for i in range(1, n + 1):
            self.play(step_tr.animate.set_value(i),
                       run_time=0.7, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
