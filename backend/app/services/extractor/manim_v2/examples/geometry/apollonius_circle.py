from manim import *
import numpy as np


class ApolloniusCircleExample(Scene):
    """
    Apollonius: the locus of points P with fixed ratio |PA|/|PB| = k
    (k ≠ 1) is a circle. For k = 2 with A = (-2, 0), B = (2, 0),
    compute the circle.

    SINGLE_FOCUS:
      Two fixed points A, B; ValueTracker k_tr sweeps ratio k;
      always_redraw the Apollonius circle + a dozen sample points on
      it (satisfying |PA|/|PB| = k).
    """

    def construct(self):
        title = Tex(r"Apollonius circle: $|PA|/|PB| = k$ locus",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        A = np.array([-2.5, 0, 0])
        B = np.array([2.5, 0, 0])

        A_dot = Dot(A, color=GREEN, radius=0.14)
        B_dot = Dot(B, color=RED, radius=0.14)
        A_lbl = MathTex(r"A", color=GREEN, font_size=22).next_to(A, DL, buff=0.1)
        B_lbl = MathTex(r"B", color=RED, font_size=22).next_to(B, DR, buff=0.1)
        self.play(FadeIn(A_dot, B_dot), Write(A_lbl), Write(B_lbl))

        k_tr = ValueTracker(2.0)

        def apollonius():
            k = k_tr.get_value()
            if abs(k - 1) < 0.01:
                # Perpendicular bisector (a line)
                return Line(np.array([0, -3, 0]), np.array([0, 3, 0]),
                              color=YELLOW, stroke_width=3)
            # Center: (k²·B - A) / (k² - 1)
            c = (k ** 2 * B - A) / (k ** 2 - 1)
            # Radius: k · |AB| / |k² - 1|
            r = k * np.linalg.norm(A - B) / abs(k ** 2 - 1)
            return Circle(radius=r, color=YELLOW, stroke_width=3,
                            fill_opacity=0.15).move_to(c)

        self.add(always_redraw(apollonius))

        # Sample points on the Apollonius circle
        def sample_points():
            k = k_tr.get_value()
            if abs(k - 1) < 0.01:
                return VGroup()
            c = (k ** 2 * B - A) / (k ** 2 - 1)
            r = k * np.linalg.norm(A - B) / abs(k ** 2 - 1)
            grp = VGroup()
            for theta in np.linspace(0, 2 * PI, 10, endpoint=False):
                P = c + r * np.array([np.cos(theta), np.sin(theta), 0])
                grp.add(Dot(P, color=YELLOW_E, radius=0.07))
            return grp

        self.add(always_redraw(sample_points))

        # Distance check lines for one active sample (top point)
        def active_lines():
            k = k_tr.get_value()
            if abs(k - 1) < 0.01:
                return VGroup()
            c = (k ** 2 * B - A) / (k ** 2 - 1)
            r = k * np.linalg.norm(A - B) / abs(k ** 2 - 1)
            P = c + r * UP  # top point
            grp = VGroup()
            grp.add(Line(A, P, color=GREEN, stroke_width=2))
            grp.add(Line(B, P, color=RED, stroke_width=2))
            grp.add(Dot(P, color=ORANGE, radius=0.11))
            return grp

        self.add(always_redraw(active_lines))

        def info():
            k = k_tr.get_value()
            c = (k ** 2 * B - A) / (k ** 2 - 1) if abs(k - 1) > 0.01 else None
            r_val = (k * np.linalg.norm(A - B) / abs(k ** 2 - 1)
                      if abs(k - 1) > 0.01 else float("inf"))
            # Check active P
            P = c + r_val * UP if c is not None else None
            if P is not None:
                PA = np.linalg.norm(P - A)
                PB = np.linalg.norm(P - B)
                ratio = PA / PB
            else:
                ratio = 1.0
            return VGroup(
                MathTex(rf"k = {k:.2f}", color=YELLOW, font_size=24),
                MathTex(rf"r = {r_val:.3f}",
                         color=YELLOW, font_size=22),
                MathTex(rf"|PA|/|PB| = {ratio:.3f}",
                         color=ORANGE, font_size=22),
                Tex(r"$k = 1$: perpendicular bisector",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for kv in [0.5, 3.0, 1.2, 2.0, 0.8]:
            self.play(k_tr.animate.set_value(kv),
                       run_time=1.6, rate_func=smooth)
            self.wait(0.4)
        self.wait(0.4)
