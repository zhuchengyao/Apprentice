from manim import *
import numpy as np


class CompactnessHeineBorelExample(Scene):
    """
    Heine-Borel: [a, b] is compact — every open cover has a finite
    subcover. Visualize with [0, 1] and an open cover {(k/N - 1/N,
    k/N + 1/N)} overlapping; only ~N+1 are needed to cover [0, 1].

    SINGLE_FOCUS:
      Number line [0, 1]; ValueTracker N_tr grows the cover density
      N = 3, 6, 10, 20. For each N, show the N+2 intervals that cover
      [0, 1] — finite subcover.
    """

    def construct(self):
        title = Tex(r"Heine-Borel: $[0, 1]$ is compact",
                    font_size=28).to_edge(UP, buff=0.3)
        self.play(Write(title))

        nl = NumberLine(x_range=[-0.2, 1.2, 0.25], length=10,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 2,
                                                 "font_size": 16}
                         ).move_to([0, -0.7, 0])
        self.play(Create(nl))

        # Mark [0, 1]
        closed_0 = Dot(nl.n2p(0), color=YELLOW, radius=0.12)
        closed_1 = Dot(nl.n2p(1), color=YELLOW, radius=0.12)
        interval = Line(nl.n2p(0), nl.n2p(1),
                          color=YELLOW, stroke_width=6, stroke_opacity=0.5)
        self.play(FadeIn(closed_0, closed_1), Create(interval))

        N_tr = ValueTracker(3)

        def cover_intervals():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 30))
            # Cover with intervals (k/N - 1.2/N, k/N + 1.2/N) for k = 0..N
            grp = VGroup()
            colors = [BLUE, GREEN, RED, PURPLE, ORANGE, TEAL, PINK]
            for k in range(N + 1):
                center = k / N
                half = 1.2 / N
                y = 0.3 + (k % 3) * 0.35  # stagger to avoid overlap
                left = nl.n2p(center - half)
                right = nl.n2p(center + half)
                bar = Line([left[0], y, 0], [right[0], y, 0],
                             color=colors[k % len(colors)],
                             stroke_width=4, stroke_opacity=0.75)
                grp.add(bar)
                # Ticks at endpoints
                grp.add(Line([left[0], y - 0.08, 0], [left[0], y + 0.08, 0],
                               color=colors[k % len(colors)], stroke_width=2))
                grp.add(Line([right[0], y - 0.08, 0], [right[0], y + 0.08, 0],
                               color=colors[k % len(colors)], stroke_width=2))
            return grp

        self.add(always_redraw(cover_intervals))

        def info():
            N = int(round(N_tr.get_value()))
            N = max(1, min(N, 30))
            count = N + 1
            return VGroup(
                MathTex(rf"\text{{cover size}} = {count}",
                         color=YELLOW, font_size=24),
                MathTex(r"I_k = (k/N - 1.2/N, k/N + 1.2/N)",
                         color=WHITE, font_size=18),
                Tex(r"$[0, 1] \subset \bigcup_{k=0}^{N} I_k$",
                     color=GREEN, font_size=22),
                Tex(r"always finite $\Rightarrow$ compact",
                     color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for target in [6, 10, 20, 3]:
            self.play(N_tr.animate.set_value(target),
                       run_time=1.5, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
