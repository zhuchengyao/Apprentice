from manim import *
import numpy as np


class CassiniOvalsExample(Scene):
    """
    Cassini oval: locus of points P with |PF_1| · |PF_2| = c².
    For c < a: two separate ovals; c = a: lemniscate; c > a: single
    oval.

    SINGLE_FOCUS:
      Fixed foci F_1 = (-1, 0), F_2 = (1, 0). ValueTracker c_tr
      sweeps c through 0.8, 1.0, 1.2, 1.5. always_redraw locus +
      invariant-product verification at a sample point.
    """

    def construct(self):
        title = Tex(r"Cassini ovals: $|PF_1|\cdot|PF_2| = c^2$",
                    font_size=26).to_edge(UP, buff=0.3)
        self.play(Write(title))

        a = 1.0
        F1 = np.array([-a, 0, 0])
        F2 = np.array([a, 0, 0])
        F1_dot = Dot(F1, color=RED, radius=0.12)
        F2_dot = Dot(F2, color=RED, radius=0.12)
        F1_lbl = MathTex(r"F_1", color=RED, font_size=22).next_to(F1, DOWN, buff=0.15)
        F2_lbl = MathTex(r"F_2", color=RED, font_size=22).next_to(F2, DOWN, buff=0.15)
        self.play(FadeIn(F1_dot, F2_dot), Write(F1_lbl), Write(F2_lbl))

        c_tr = ValueTracker(0.8)

        def oval():
            c = c_tr.get_value()
            # Cassini in Cartesian: (x²+y²)² - 2a²(x²-y²) = c⁴ - a⁴
            # Parametrize via polar r²(θ) = a² cos 2θ ± √(c⁴ - a⁴ sin² 2θ)
            pts = []
            branches = []  # list of point lists
            cur_branch = []
            for theta in np.linspace(0, 2 * PI, 400):
                c4 = c ** 4
                a4 = a ** 4
                sin2 = np.sin(2 * theta)
                disc = c4 - a4 * sin2 * sin2
                if disc < 0:
                    if cur_branch:
                        branches.append(cur_branch)
                        cur_branch = []
                    continue
                r2 = a ** 2 * np.cos(2 * theta) + np.sqrt(disc)
                if r2 < 0:
                    if cur_branch:
                        branches.append(cur_branch)
                        cur_branch = []
                    continue
                r = np.sqrt(r2)
                cur_branch.append(np.array([r * np.cos(theta),
                                               r * np.sin(theta), 0]))
            if cur_branch:
                branches.append(cur_branch)

            # For c < a, there should also be a second branch from r² = a² cos 2θ - √(...)
            if c < a:
                cur_branch = []
                for theta in np.linspace(0, 2 * PI, 400):
                    c4 = c ** 4
                    a4 = a ** 4
                    sin2 = np.sin(2 * theta)
                    disc = c4 - a4 * sin2 * sin2
                    if disc < 0:
                        if cur_branch:
                            branches.append(cur_branch)
                            cur_branch = []
                        continue
                    r2 = a ** 2 * np.cos(2 * theta) - np.sqrt(disc)
                    if r2 < 0:
                        if cur_branch:
                            branches.append(cur_branch)
                            cur_branch = []
                        continue
                    r = np.sqrt(r2)
                    cur_branch.append(np.array([r * np.cos(theta),
                                                   r * np.sin(theta), 0]))
                if cur_branch:
                    branches.append(cur_branch)

            grp = VGroup()
            for pts_list in branches:
                if len(pts_list) < 3:
                    continue
                m = VMobject(color=YELLOW, stroke_width=3)
                m.set_points_as_corners(pts_list)
                grp.add(m)
            return grp

        self.add(always_redraw(oval))

        # Sample point verification: pick point at angle θ=π/3
        def sample_point():
            c = c_tr.get_value()
            theta = PI / 3
            c4 = c ** 4
            a4 = a ** 4
            sin2 = np.sin(2 * theta)
            disc = c4 - a4 * sin2 * sin2
            if disc < 0:
                return VGroup()
            r2 = a ** 2 * np.cos(2 * theta) + np.sqrt(disc)
            if r2 < 0:
                return VGroup()
            r = np.sqrt(r2)
            P = np.array([r * np.cos(theta), r * np.sin(theta), 0])
            grp = VGroup()
            grp.add(Dot(P, color=GREEN, radius=0.12))
            grp.add(Line(F1, P, color=BLUE, stroke_width=2))
            grp.add(Line(F2, P, color=BLUE, stroke_width=2))
            return grp

        self.add(always_redraw(sample_point))

        def info():
            c = c_tr.get_value()
            theta = PI / 3
            c4 = c ** 4
            a4 = a ** 4
            sin2 = np.sin(2 * theta)
            disc = c4 - a4 * sin2 * sin2
            if disc < 0:
                pf1 = pf2 = 0.0
            else:
                r2 = a ** 2 * np.cos(2 * theta) + np.sqrt(disc)
                r = np.sqrt(max(r2, 0))
                P = np.array([r * np.cos(theta), r * np.sin(theta), 0])
                pf1 = np.linalg.norm(P - F1)
                pf2 = np.linalg.norm(P - F2)
            if c < a:
                shape = "two ovals"
                col = BLUE
            elif abs(c - a) < 0.02:
                shape = "lemniscate"
                col = YELLOW
            else:
                shape = "single oval"
                col = GREEN
            return VGroup(
                MathTex(rf"c = {c:.2f}", color=YELLOW, font_size=24),
                MathTex(rf"|PF_1| \cdot |PF_2| = {pf1 * pf2:.3f}",
                         color=GREEN, font_size=22),
                MathTex(rf"c^2 = {c ** 2:.3f}",
                         color=YELLOW, font_size=22),
                Tex(shape, color=col, font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.3).shift(UP * 0.3)

        self.add(always_redraw(info))

        for cv in [1.0, 1.2, 1.5, 0.8]:
            self.play(c_tr.animate.set_value(cv),
                       run_time=1.8, rate_func=smooth)
            self.wait(0.5)
        self.wait(0.4)
