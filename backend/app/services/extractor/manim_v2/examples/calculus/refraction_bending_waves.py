from manim import *
import numpy as np


class RefractionBendingWavesExample(Scene):
    """
    Snell's law and wave-front bending (from _2023/optics_puzzles/
    bending_waves): a plane wave crossing an interface at angle θ₁
    refracts to angle θ₂ with n₁ sin θ₁ = n₂ sin θ₂.

    SINGLE_FOCUS:
      Horizontal interface; ValueTracker th1_tr sweeps incident
      angle; always_redraw ray arrows, wave fronts, angle arcs, and
      Snell-computed refracted angle. n₁ = 1.0, n₂ = 1.5 (air→glass).
    """

    def construct(self):
        title = Tex(r"Snell's law: $n_1 \sin\theta_1 = n_2 \sin\theta_2$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Interface at y=0
        interface = Line([-6, 0, 0], [6, 0, 0], color=WHITE, stroke_width=3)
        above_shade = Rectangle(width=12.2, height=3.2,
                                  color=BLUE, fill_opacity=0.08,
                                  stroke_width=0
                                  ).move_to([0, 1.6, 0])
        below_shade = Rectangle(width=12.2, height=3.2,
                                  color=BLUE_D, fill_opacity=0.22,
                                  stroke_width=0
                                  ).move_to([0, -1.6, 0])

        self.play(FadeIn(below_shade), FadeIn(above_shade), Create(interface))

        n1_lbl = Tex(r"$n_1 = 1.0$ (air)",
                      color=BLUE, font_size=22
                      ).move_to([-4.5, 2.8, 0])
        n2_lbl = Tex(r"$n_2 = 1.5$ (glass)",
                      color=BLUE_D, font_size=22
                      ).move_to([-4.5, -2.8, 0])
        self.play(Write(n1_lbl), Write(n2_lbl))

        n1, n2 = 1.0, 1.5
        hit_point = np.array([0, 0, 0])

        th1_tr = ValueTracker(30 * DEGREES)

        def snell_th2(th1):
            s2 = n1 / n2 * np.sin(th1)
            s2 = max(-1.0, min(1.0, s2))
            return np.arcsin(s2)

        def incoming():
            th1 = th1_tr.get_value()
            # Incoming ray from upper-left into origin
            dir_in = np.array([np.sin(th1), -np.cos(th1), 0])
            start = hit_point - 3.0 * dir_in
            return Arrow(start, hit_point, color=YELLOW,
                          buff=0, stroke_width=4,
                          max_tip_length_to_length_ratio=0.1)

        def refracted():
            th1 = th1_tr.get_value()
            th2 = snell_th2(th1)
            dir_out = np.array([np.sin(th2), -np.cos(th2), 0])
            end = hit_point + 3.0 * dir_out
            return Arrow(hit_point, end, color=ORANGE,
                          buff=0, stroke_width=4,
                          max_tip_length_to_length_ratio=0.1)

        def normal_line():
            return DashedLine([0, -2.8, 0], [0, 2.8, 0],
                                color=GREY_B, stroke_width=1.5)

        def arc1():
            th1 = th1_tr.get_value()
            return Arc(radius=0.6, start_angle=PI / 2,
                        angle=-th1, color=YELLOW, stroke_width=3
                        ).move_arc_center_to(hit_point)

        def arc2():
            th1 = th1_tr.get_value()
            th2 = snell_th2(th1)
            return Arc(radius=0.6, start_angle=-PI / 2,
                        angle=th2, color=ORANGE, stroke_width=3
                        ).move_arc_center_to(hit_point)

        self.add(always_redraw(normal_line),
                  always_redraw(incoming),
                  always_redraw(refracted),
                  always_redraw(arc1),
                  always_redraw(arc2))

        def info():
            th1 = th1_tr.get_value()
            th2 = snell_th2(th1)
            return VGroup(
                MathTex(rf"\theta_1 = {np.degrees(th1):.1f}^\circ",
                         color=YELLOW, font_size=24),
                MathTex(rf"\theta_2 = {np.degrees(th2):.1f}^\circ",
                         color=ORANGE, font_size=24),
                MathTex(rf"n_1 \sin\theta_1 = {n1 * np.sin(th1):.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"n_2 \sin\theta_2 = {n2 * np.sin(th2):.3f}",
                         color=GREEN, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)

        self.add(always_redraw(info))

        for deg in [10, 45, 60, 80, 30]:
            self.play(th1_tr.animate.set_value(deg * DEGREES),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
