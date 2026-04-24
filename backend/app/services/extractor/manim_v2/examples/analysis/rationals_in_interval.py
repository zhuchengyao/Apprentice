from manim import *
import numpy as np
from math import gcd


class RationalsInIntervalExample(Scene):
    """
    Density of rationals in [0, 1]: as q_max grows, the rationals
    p/q (in lowest terms with 0 ≤ p ≤ q ≤ q_max) populate the
    unit interval ever more densely.

    SINGLE_FOCUS:
      NumberLine [0, 1]. ValueTracker q_max_tr sweeps 1 → 20;
      always_redraw draws a dot at each p/q in lowest terms with
      q ≤ q_max. Dot RADIUS depends on q: smaller q → bigger
      dot (emphasizes the "important" Farey points 0, 1/2, 1, 1/3,
      2/3, 1/4, 3/4, ...). Live count panel shows |F_{q_max}|.
    """

    def construct(self):
        title = Tex(r"Rationals are dense in $[0, 1]$ — Farey sequences $F_Q$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        nl = NumberLine(x_range=[0, 1.001, 0.1], length=12,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 1,
                                                 "font_size": 18}
                         ).move_to([0, -0.5, 0])
        self.play(Create(nl))

        q_tr = ValueTracker(1.0)

        def farey(Q):
            pts = []
            for q in range(1, Q + 1):
                for p in range(0, q + 1):
                    if gcd(p, q) == 1:
                        pts.append((p / q, q))
            return pts

        def dots_grp():
            Q = max(1, int(round(q_tr.get_value())))
            grp = VGroup()
            for (x, q) in farey(Q):
                r = max(0.03, 0.12 - 0.006 * q)
                color = YELLOW if q <= 3 else (BLUE if q <= 8 else BLUE_D)
                grp.add(Dot(nl.n2p(x), color=color, radius=r))
            return grp

        self.add(always_redraw(dots_grp))

        def info():
            Q = max(1, int(round(q_tr.get_value())))
            count = len(farey(Q))
            return VGroup(
                MathTex(rf"Q = q_{{\max}} = {Q}", color=WHITE, font_size=26),
                MathTex(rf"|F_Q| = {count}", color=YELLOW, font_size=26),
                Tex(r"$|F_Q| \sim \tfrac{3}{\pi^2} Q^2$", color=GREEN_B, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.5, 2.0, 0])

        self.add(always_redraw(info))

        self.play(q_tr.animate.set_value(20),
                   run_time=10, rate_func=linear)
        self.wait(0.5)
