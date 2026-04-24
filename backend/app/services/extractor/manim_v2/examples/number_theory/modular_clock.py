from manim import *
import numpy as np


class ModularClockExample(Scene):
    """
    Addition mod 12 as continuous rotation around a clock face.

    SINGLE_FOCUS: a clock with positions 0..11. ValueTracker n
    represents the cumulative offset added to the start position 0.
    The pointer rotates continuously through n; the displayed value
    is `int(n) % 12`. A trail accumulates as n grows past 12, then
    24, etc., showing the pointer wrap. Right-side panel writes the
    chain 0 + 1 + 2 + … live (each addition completed) and the
    final identity.
    """

    def construct(self):
        title = Tex(r"Addition mod 12 as continuous rotation",
                    font_size=30).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # LEFT: clock face
        radius = 2.2
        clock_center = np.array([-2.6, -0.4, 0])
        clock = Circle(radius=radius, color=GREY_B,
                       stroke_width=2).move_to(clock_center)
        self.play(Create(clock))

        positions = {}
        labels = VGroup()
        for k in range(12):
            theta = PI / 2 - 2 * PI * k / 12
            pt = clock_center + radius * np.array([np.cos(theta), np.sin(theta), 0])
            positions[k] = pt
            lbl = Tex(rf"${k}$", font_size=22).move_to(
                clock_center + 1.18 * radius * np.array([np.cos(theta), np.sin(theta), 0]))
            labels.add(lbl)
        self.play(FadeIn(labels))

        # ValueTracker n: cumulative offset (continuous, can exceed 12)
        n_tr = ValueTracker(0.0)
        START = 0  # start position

        def angle_at(n):
            # Position 0 is at top (PI/2), each unit is -2π/12
            return PI / 2 - 2 * PI * (START + n) / 12

        def pointer():
            ang = angle_at(n_tr.get_value())
            tip = clock_center + radius * 0.85 * np.array([np.cos(ang), np.sin(ang), 0])
            return Arrow(clock_center, tip, buff=0,
                         color=YELLOW, stroke_width=5,
                         max_tip_length_to_length_ratio=0.10)

        def head_dot():
            ang = angle_at(n_tr.get_value())
            return Dot(clock_center + radius * np.array([np.cos(ang), np.sin(ang), 0]),
                       color=YELLOW, radius=0.10)

        self.add(always_redraw(pointer), always_redraw(head_dot))

        # RIGHT COLUMN: live readouts
        rcol_x = +3.4

        def info_panel():
            n = n_tr.get_value()
            cur_int = int(round(n))
            mod12 = cur_int % 12
            return VGroup(
                MathTex(rf"\text{{cumulative}} = {cur_int}",
                        color=YELLOW, font_size=28),
                MathTex(rf"\equiv {mod12} \pmod{{12}}",
                        color=GREEN, font_size=32),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([rcol_x, +2.0, 0])

        self.add(always_redraw(info_panel))

        # Sequence of additions: 7, +8, +5, +9, +6 (cumulative: 7, 15, 20, 29, 35)
        steps = [(7, "0 + 7 = 7"),
                 (8, "7 + 8 = 15 \\equiv 3"),
                 (5, "15 + 5 = 20 \\equiv 8"),
                 (9, "20 + 9 = 29 \\equiv 5"),
                 (6, "29 + 6 = 35 \\equiv 11")]

        cumulative = 0
        chain_lines = VGroup()
        for step, msg in steps:
            cumulative += step
            self.play(n_tr.animate.set_value(float(cumulative)),
                      run_time=1.5, rate_func=smooth)
            line = MathTex(msg, color=WHITE, font_size=22)
            chain_lines.add(line)
            chain_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([rcol_x, -0.6, 0])
            self.play(Write(line), run_time=0.6)

        self.wait(0.5)
        principle = Tex(r"Mod 12 = clock arithmetic: angles wrap every $360^\circ$",
                        color=YELLOW, font_size=22).move_to([rcol_x, -3.0, 0])
        self.play(Write(principle))
        self.wait(1.0)
