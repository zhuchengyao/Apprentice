from manim import *
import numpy as np


class ContinuedFractionsExample(Scene):
    """
    Continued-fraction expansion of π and φ:
      π = [3; 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, ...]
      φ = [1; 1, 1, 1, 1, ...] (all 1s)
    Best rational approximations from convergents.

    TWO_COLUMN:
      LEFT  — number line with true value marker + successive
              convergents p_k/q_k via ValueTracker k_tr.
      RIGHT  — live p_k, q_k, |p_k/q_k - x|.
    """

    def construct(self):
        title = Tex(r"Continued fractions: convergents approximate $x$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # π CF: [3; 7, 15, 1, 292, 1, 1, 1, 2, 1]
        pi_cf = [3, 7, 15, 1, 292, 1, 1, 1, 2, 1]

        def convergents(cf):
            p_prev, p_cur = 1, cf[0]
            q_prev, q_cur = 0, 1
            convs = [(p_cur, q_cur)]
            for a in cf[1:]:
                p_next = a * p_cur + p_prev
                q_next = a * q_cur + q_prev
                convs.append((p_next, q_next))
                p_prev, p_cur = p_cur, p_next
                q_prev, q_cur = q_cur, q_next
            return convs

        pi_convs = convergents(pi_cf)

        nl = NumberLine(x_range=[3.13, 3.15, 0.005], length=11,
                         include_numbers=True,
                         decimal_number_config={"num_decimal_places": 4,
                                                 "font_size": 14}
                         ).move_to([0, 0, 0])
        self.play(Create(nl))

        # True π marker
        pi_val = np.pi
        pi_tick = Line(nl.n2p(pi_val) + UP * 0.3,
                         nl.n2p(pi_val) + DOWN * 0.3,
                         color=YELLOW, stroke_width=4)
        pi_lbl = MathTex(r"\pi", color=YELLOW, font_size=22
                           ).next_to(pi_tick, UP, buff=0.1)
        self.play(Create(pi_tick), Write(pi_lbl))

        k_tr = ValueTracker(0)

        def convergent_dot():
            k = int(round(k_tr.get_value()))
            k = max(0, min(k, len(pi_convs) - 1))
            p, q = pi_convs[k]
            val = p / q
            # Clip to visible range
            if 3.13 <= val <= 3.15:
                return Dot(nl.n2p(val), color=RED, radius=0.11)
            else:
                # Off-screen; show indicator at edge
                return VGroup()

        self.add(always_redraw(convergent_dot))

        def info():
            k = int(round(k_tr.get_value()))
            k = max(0, min(k, len(pi_convs) - 1))
            p, q = pi_convs[k]
            val = p / q
            err = abs(val - pi_val)
            cf_display = [pi_cf[i] for i in range(k + 1)]
            if len(cf_display) > 4:
                cf_str = rf"[{cf_display[0]}; " + ", ".join(str(a) for a in cf_display[1:4]) + ", \\ldots]"
            else:
                cf_str = rf"[{cf_display[0]}" + ("; " + ", ".join(str(a) for a in cf_display[1:]) if len(cf_display) > 1 else "") + "]"
            return VGroup(
                MathTex(rf"k = {k}", color=WHITE, font_size=22),
                MathTex(rf"{cf_str}", color=BLUE, font_size=20),
                MathTex(rf"p_k / q_k = {p}/{q}",
                         color=RED, font_size=22),
                MathTex(rf"= {val:.8f}",
                         color=RED, font_size=20),
                MathTex(rf"|\text{{err}}| = {err:.3e}",
                         color=GREEN, font_size=20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.3)

        self.add(always_redraw(info))

        for k in range(1, len(pi_convs)):
            self.play(k_tr.animate.set_value(k),
                       run_time=1.0, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
