from manim import *
import numpy as np


class LineIntegralConservativeExample(Scene):
    """
    Conservative vector field: F = ∇φ implies ∫_γ F · dr = φ(end)
    - φ(start) regardless of path. Illustrate with F = (y, x) =
    ∇(xy); two paths from (0, 0) to (2, 1.5) give same integral = 3.

    COMPARISON:
      Two paths (straight line, staircase) from A to B; running
      integrals converge to same value (independence).
    """

    def construct(self):
        title = Tex(r"Conservative field: $\int_\gamma \vec F \cdot d\vec r = \varphi(B) - \varphi(A)$",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        plane = NumberPlane(x_range=[-0.3, 3, 0.5], y_range=[-0.3, 2.3, 0.5],
                             x_length=6, y_length=4.5,
                             background_line_style={"stroke_opacity": 0.3}
                             ).move_to([-2.5, -0.3, 0])
        self.play(Create(plane))

        A = np.array([0, 0])
        B = np.array([2, 1.5])
        A_dot = Dot(plane.c2p(*A), color=GREEN, radius=0.12)
        B_dot = Dot(plane.c2p(*B), color=RED, radius=0.12)
        A_lbl = MathTex(r"A", color=GREEN, font_size=22).next_to(A_dot, DL, buff=0.1)
        B_lbl = MathTex(r"B", color=RED, font_size=22).next_to(B_dot, UR, buff=0.1)
        self.play(FadeIn(A_dot, B_dot), Write(A_lbl), Write(B_lbl))

        s_tr = ValueTracker(0.0)

        # Path 1: straight line
        def path1(s):
            return (1 - s) * A + s * B

        # Path 2: staircase through (2, 0) then (2, 1.5)
        def path2(s):
            if s <= 0.5:
                return (1 - 2 * s) * A + 2 * s * np.array([2, 0])
            else:
                return (1 - 2 * (s - 0.5)) * np.array([2, 0]) + 2 * (s - 0.5) * B

        def path1_trail():
            s = s_tr.get_value()
            pts = [plane.c2p(*path1(si)) for si in np.linspace(0, s, 30)]
            m = VMobject(color=BLUE, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def path2_trail():
            s = s_tr.get_value()
            pts = [plane.c2p(*path2(si)) for si in np.linspace(0, s, 30)]
            m = VMobject(color=ORANGE, stroke_width=3)
            if len(pts) >= 2:
                m.set_points_as_corners(pts)
            return m

        def path1_dot():
            s = s_tr.get_value()
            p = path1(s)
            return Dot(plane.c2p(*p), color=BLUE, radius=0.1)

        def path2_dot():
            s = s_tr.get_value()
            p = path2(s)
            return Dot(plane.c2p(*p), color=ORANGE, radius=0.1)

        self.add(always_redraw(path1_trail), always_redraw(path2_trail),
                  always_redraw(path1_dot), always_redraw(path2_dot))

        def I_path1(s_cur):
            # ∫ F·dr along straight line; F=(y, x); numeric
            N = max(2, int(100 * s_cur))
            ss = np.linspace(0, s_cur, N)
            total = 0.0
            for i in range(N - 1):
                p0 = path1(ss[i])
                p1 = path1(ss[i + 1])
                mid = (p0 + p1) / 2
                F = np.array([mid[1], mid[0]])
                dr = p1 - p0
                total += np.dot(F, dr)
            return total

        def I_path2(s_cur):
            N = max(2, int(100 * s_cur))
            ss = np.linspace(0, s_cur, N)
            total = 0.0
            for i in range(N - 1):
                p0 = path2(ss[i])
                p1 = path2(ss[i + 1])
                mid = (p0 + p1) / 2
                F = np.array([mid[1], mid[0]])
                dr = p1 - p0
                total += np.dot(F, dr)
            return total

        def info():
            s = s_tr.get_value()
            I1 = I_path1(s)
            I2 = I_path2(s)
            return VGroup(
                MathTex(rf"s = {s:.2f}", color=WHITE, font_size=22),
                MathTex(rf"\int_{{\gamma_1}}: {I1:.3f}",
                         color=BLUE, font_size=20),
                MathTex(rf"\int_{{\gamma_2}}: {I2:.3f}",
                         color=ORANGE, font_size=20),
                MathTex(r"\varphi = xy;\ \varphi(B) - \varphi(A) = 3",
                         color=GREEN, font_size=18),
                Tex(r"path-independent (conservative)",
                     color=GREEN, font_size=18),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        self.play(s_tr.animate.set_value(1.0),
                   run_time=5, rate_func=linear)
        self.wait(0.4)
