from manim import *
import numpy as np


class GroverVsClassicalSearch(Scene):
    """For unstructured search in a database of N items, classical
    algorithms need O(N) queries (expected ~N/2 tries).  Grover's
    quantum algorithm needs O(sqrt(N)).  Compare the scaling by
    plotting both on an Axes, and demonstrate the gap with a few N
    values in a table."""

    def construct(self):
        title = Tex(
            r"Quantum speedup: Grover needs $\sqrt{N}$, classical needs $N$",
            font_size=28,
        ).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(
            x_range=[0, 1000, 200],
            y_range=[0, 500, 100],
            x_length=9, y_length=4.5,
            tips=False,
            axis_config={"stroke_width": 1.5, "include_ticks": True},
        ).shift(DOWN * 0.3)
        x_lab = MathTex(r"N", font_size=26).next_to(
            axes.x_axis.get_end(), DOWN, buff=0.1
        )
        y_lab = Tex("queries", font_size=22).next_to(
            axes.y_axis.get_end(), LEFT, buff=0.1
        )
        self.play(Create(axes), FadeIn(x_lab), FadeIn(y_lab))

        classical = axes.plot(
            lambda n: n / 2, x_range=[1, 1000, 1],
            color=RED, stroke_width=3,
        )
        classical_lab = MathTex(
            r"\tfrac{N}{2}\ \text{(classical)}",
            font_size=24, color=RED,
        ).move_to(axes.c2p(800, 470))
        quantum = axes.plot(
            lambda n: (np.pi / 4) * np.sqrt(n), x_range=[1, 1000, 1],
            color=GREEN, stroke_width=3,
        )
        quantum_lab = MathTex(
            r"\tfrac{\pi}{4}\sqrt{N}\ \text{(Grover)}",
            font_size=24, color=GREEN,
        ).move_to(axes.c2p(800, 80))
        self.play(Create(classical), Write(classical_lab))
        self.play(Create(quantum), Write(quantum_lab))

        table_rows = [
            ("N", "classical", "quantum"),
            ("100", "50", "~8"),
            ("10⁴", "5000", "~79"),
            ("10⁶", "500000", "~785"),
            ("10⁹", "5×10⁸", "~24674"),
        ]
        rows_grp = VGroup()
        for i, row in enumerate(table_rows):
            color = YELLOW if i == 0 else WHITE
            r = VGroup(
                Tex(row[0], font_size=22, color=color),
                Tex(row[1], font_size=22,
                    color=RED if i else color),
                Tex(row[2], font_size=22,
                    color=GREEN if i else color),
            ).arrange(RIGHT, buff=0.8)
            r.move_to([4.5, 2.2 - i * 0.45, 0])
            rows_grp.add(r)
        self.play(LaggedStart(*[FadeIn(r) for r in rows_grp],
                              lag_ratio=0.2, run_time=2.5))

        impact = Tex(
            r"Exponentially faster on large search spaces — quadratic speedup is huge at scale.",
            font_size=22, color=YELLOW,
        ).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(impact))
        self.wait(1.5)
