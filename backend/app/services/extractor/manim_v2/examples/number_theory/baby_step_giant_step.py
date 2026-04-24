from manim import *
import numpy as np


class BabyStepGiantStepExample(Scene):
    """
    Baby-step giant-step for discrete logarithm: find x with
    g^x ≡ h (mod p) by precomputing baby steps {g^j : 0 ≤ j < m}
    (m = ⌈√p⌉) then checking giant steps h·(g^(-m))^i = g^(x-im).

    Example p=23, g=5, h=10. p-1=22, m=5.
    Baby: 5^0=1, 5^1=5, 5^2=2, 5^3=10, 5^4=4.
    h = 10 = 5^3 → x = 3 (one-shot). Add more complex with h = 7:
    h · (5^(-5))^i for i=0..4 etc.

    SINGLE_FOCUS: 2 rows of boxes (babies + giants); ValueTracker
    step_tr reveals baby steps then walks giant-step loop with
    always_redraw highlight looking for match.
    """

    def construct(self):
        p, g, h = 23, 5, 7
        title = Tex(rf"BSGS: find $x$ with $g^x\equiv h\pmod p$,\ $p={p}$, $g={g}$, $h={h}$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        m = int(np.ceil(np.sqrt(p - 1)))  # 5
        babies = [pow(g, j, p) for j in range(m)]
        # Find g^{-m} mod p via Fermat
        g_neg_m = pow(pow(g, m, p), p - 2, p)
        giants = [(h * pow(g_neg_m, i, p)) % p for i in range(m + 1)]
        # find match
        baby_dict = {v: j for j, v in enumerate(babies)}
        match_i = None
        match_j = None
        for i, v in enumerate(giants):
            if v in baby_dict:
                match_i = i
                match_j = baby_dict[v]
                break
        x_ans = (match_i * m + match_j) % (p - 1)

        # Layout
        cell_s = 0.75
        origin_baby = np.array([-4.5, 1.2, 0])
        origin_giant = np.array([-4.5, -1.0, 0])

        baby_boxes = VGroup()
        for j, v in enumerate(babies):
            cell = Square(side_length=cell_s * 0.9, color=BLUE,
                          stroke_width=1.5, fill_color=BLUE,
                          fill_opacity=0.2).move_to(
                origin_baby + RIGHT * j * cell_s)
            cell_lbl = VGroup(
                Tex(rf"$g^{{{j}}}$", font_size=18, color=BLUE),
                Tex(f"${v}$", font_size=20),
            ).arrange(DOWN, buff=0.05).move_to(origin_baby + RIGHT * j * cell_s)
            baby_boxes.add(cell, cell_lbl)

        giant_boxes = VGroup()
        for i, v in enumerate(giants):
            cell = Square(side_length=cell_s * 0.9, color=ORANGE,
                          stroke_width=1.5, fill_color=ORANGE,
                          fill_opacity=0.2).move_to(
                origin_giant + RIGHT * i * cell_s)
            cell_lbl = VGroup(
                Tex(rf"$i={i}$", font_size=18, color=ORANGE),
                Tex(f"${v}$", font_size=20),
            ).arrange(DOWN, buff=0.05).move_to(origin_giant + RIGHT * i * cell_s)
            giant_boxes.add(cell, cell_lbl)

        self.add(Tex(r"babies $g^j$:", font_size=22, color=BLUE).move_to(
            origin_baby + LEFT * 1.0))
        self.add(Tex(r"giants $h(g^{-m})^i$:", font_size=22, color=ORANGE).move_to(
            origin_giant + LEFT * 1.1))

        self.play(FadeIn(baby_boxes))
        self.play(FadeIn(giant_boxes))

        step_tr = ValueTracker(0.0)

        def scanner():
            k = int(round(step_tr.get_value()))
            k = max(0, min(len(giants) - 1, k))
            val = giants[k]
            hl_giant = Rectangle(width=cell_s * 0.9, height=cell_s * 0.9,
                                  color=YELLOW, stroke_width=3).move_to(
                origin_giant + RIGHT * k * cell_s)
            grp = VGroup(hl_giant)
            if val in baby_dict:
                j = baby_dict[val]
                hl_baby = Rectangle(width=cell_s * 0.9, height=cell_s * 0.9,
                                     color=GREEN, stroke_width=3).move_to(
                    origin_baby + RIGHT * j * cell_s)
                arrow = Arrow(origin_giant + RIGHT * k * cell_s + UP * cell_s * 0.5,
                               origin_baby + RIGHT * j * cell_s + DOWN * cell_s * 0.5,
                               color=GREEN, buff=0.02, stroke_width=3)
                grp.add(hl_baby, arrow)
            return grp

        self.add(always_redraw(scanner))

        info = VGroup(
            VGroup(Tex(r"$i=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"$g^{-m}=$", font_size=22),
                   DecimalNumber(g_neg_m, num_decimal_places=0,
                                 font_size=22)).arrange(RIGHT, buff=0.1),
            VGroup(Tex(r"giant $=h(g^{-m})^i=$", font_size=22),
                   DecimalNumber(0, num_decimal_places=0,
                                 font_size=22).set_color(ORANGE)).arrange(RIGHT, buff=0.1),
            Tex(rf"match: $x=im+j={match_i}\cdot{m}+{match_j}={x_ans}$",
                color=GREEN, font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        info[0][1].add_updater(lambda m: m.set_value(
            max(0, min(len(giants) - 1, int(round(step_tr.get_value()))))))
        info[2][1].add_updater(lambda m: m.set_value(
            giants[max(0, min(len(giants) - 1, int(round(step_tr.get_value()))))]))
        self.add(info)

        # Walk giants until match
        for target in range(1, match_i + 1):
            self.play(step_tr.animate.set_value(float(target)),
                      run_time=1.0, rate_func=smooth)
            self.wait(0.4)
        self.wait(1.0)

        # Verify
        verify = Tex(rf"verify: $g^{{{x_ans}}}={pow(g, x_ans, p)}\equiv h\pmod p$",
                     color=GREEN, font_size=22).to_corner(DR, buff=0.3)
        self.play(Write(verify))
        self.wait(0.5)
