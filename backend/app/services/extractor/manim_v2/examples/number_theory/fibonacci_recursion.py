from manim import *
import numpy as np


class FibonacciRecursionExample(Scene):
    """
    Fibonacci: F_n = F_(n-1) + F_(n-2) with F_0 = 0, F_1 = 1.
    F_n/F_(n-1) → φ (golden ratio).

    SINGLE_FOCUS:
      ValueTracker n_tr reveals Fibonacci numbers F_0..F_15 as
      stacked boxes with sizes proportional to value; ratio
      F_n/F_(n-1) converges to φ ≈ 1.618.
    """

    def construct(self):
        title = Tex(r"Fibonacci: $F_n = F_{n-1} + F_{n-2}$, ratio $\to \varphi$",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        F = [0, 1]
        while len(F) <= 15:
            F.append(F[-1] + F[-2])

        # Display F_n as stacked bars
        n_tr = ValueTracker(2)

        def fib_bars():
            n = int(round(n_tr.get_value()))
            n = max(2, min(n, 15))
            grp = VGroup()
            # Scale: fit F_n up to 800 in display
            max_val = 800
            for i in range(n + 1):
                v = F[i]
                h = (v / max_val) * 4
                if h < 0.05:
                    continue
                bar = Rectangle(width=0.4, height=h,
                                 color=BLUE, fill_opacity=0.6,
                                 stroke_width=0.5)
                bar.move_to([-5.5 + i * 0.7, -1.8 + h / 2, 0])
                grp.add(bar)
                if i < 8 or i % 3 == 0:
                    grp.add(MathTex(rf"{v}", font_size=14, color=WHITE
                                      ).next_to(bar, UP, buff=0.05))
                grp.add(MathTex(rf"F_{{{i}}}", font_size=12, color=GREY_B
                                  ).next_to(bar, DOWN, buff=0.08))
            return grp

        self.add(always_redraw(fib_bars))

        def info():
            n = int(round(n_tr.get_value()))
            n = max(2, min(n, 15))
            if n >= 1:
                ratio = F[n] / F[n - 1] if F[n - 1] > 0 else 0
            else:
                ratio = 0
            phi = (1 + np.sqrt(5)) / 2
            return VGroup(
                MathTex(rf"n = {n}", color=YELLOW, font_size=22),
                MathTex(rf"F_n = {F[n]}", color=BLUE, font_size=22),
                MathTex(rf"F_n / F_{{n-1}} = {ratio:.6f}",
                         color=ORANGE, font_size=20),
                MathTex(rf"\varphi = {phi:.6f}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.17).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add(always_redraw(info))

        for nv in range(3, 16):
            self.play(n_tr.animate.set_value(nv),
                       run_time=0.5, rate_func=smooth)
            self.wait(0.2)
        self.wait(0.5)
