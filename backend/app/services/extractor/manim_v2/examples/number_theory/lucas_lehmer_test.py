from manim import *
import numpy as np


class LucasLehmerTestExample(Scene):
    """
    Lucas-Lehmer primality test for Mersenne numbers M_p = 2^p − 1:
    compute s_0 = 4, s_{k+1} = s_k² − 2 mod M_p. M_p is prime iff
    s_{p-2} ≡ 0 (mod M_p).

    Example: p=7, M_7 = 127. s: 4, 14, 67, 42, 111, 0. Prime!

    SINGLE_FOCUS: sequence boxes with live values; ValueTracker k_tr
    reveals successive steps; check at the end.
    """

    def construct(self):
        p = 7
        M = 2 ** p - 1  # 127
        title = Tex(rf"Lucas-Lehmer: $M_{{{p}}}={M}$ is prime iff $s_{{{p-2}}}\equiv 0\pmod {{{M}}}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Compute sequence
        s_list = [4]
        for _ in range(p - 2):
            s_list.append((s_list[-1] ** 2 - 2) % M)

        cell_s = 1.2
        origin = np.array([-4.5, 0.8, 0])

        boxes = VGroup()
        indices = VGroup()
        for i in range(p - 1):
            box = Rectangle(width=cell_s * 0.9, height=cell_s * 0.7,
                             color=GREY_B, stroke_width=1.5,
                             fill_color=GREY_D, fill_opacity=0.15).move_to(
                origin + RIGHT * i * cell_s)
            boxes.add(box)
            indices.add(Tex(rf"$s_{{{i}}}$", font_size=22, color=BLUE).next_to(box, UP, buff=0.1))

        self.add(boxes, indices)

        k_tr = ValueTracker(0.0)

        def k_now():
            return max(0, min(p - 2, int(round(k_tr.get_value()))))

        def revealed():
            k = k_now()
            grp = VGroup()
            for i in range(k + 1):
                val = s_list[i]
                col = GREEN if val == 0 else (YELLOW if i == k else WHITE)
                grp.add(Tex(str(val), font_size=24, color=col).move_to(
                    origin + RIGHT * i * cell_s))
            return grp

        self.add(always_redraw(revealed))

        # Recurrence equation
        rec_tex = Tex(r"$s_{k+1} = s_k^2 - 2 \pmod{127}$",
                       font_size=24, color=YELLOW).to_edge(DOWN, buff=1.0)
        self.add(rec_tex)

        # Verdict
        def verdict_str():
            k = k_now()
            if k < p - 2:
                return r"(computing...)"
            if s_list[-1] == 0:
                return rf"$s_{{{p-2}}}=0\Rightarrow M_{{{p}}}=127$ is prime! ✓"
            return rf"$s_{{{p-2}}}={s_list[-1]}\neq 0\Rightarrow M_{{{p}}}$ composite"

        verdict_tex = Tex(verdict_str(), color=GREEN, font_size=26).to_edge(DOWN, buff=0.4)
        self.add(verdict_tex)
        def update_verdict(mob, dt):
            new = Tex(verdict_str(), color=GREEN,
                       font_size=26).move_to(verdict_tex)
            verdict_tex.become(new)
            return verdict_tex
        verdict_tex.add_updater(update_verdict)

        info = VGroup(
            VGroup(Tex(r"step $k=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$s_k=$", font_size=22),
                   DecimalNumber(4, num_decimal_places=0,
                                 font_size=22).set_color(YELLOW)).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR, buff=0.3)
        info[0][1].add_updater(lambda m: m.set_value(k_now()))
        info[1][1].add_updater(lambda m: m.set_value(s_list[k_now()]))
        self.add(info)

        for k in range(1, p - 1):
            self.play(k_tr.animate.set_value(float(k)),
                      run_time=1.2, rate_func=smooth)
            self.wait(0.3)
        self.wait(1.0)
