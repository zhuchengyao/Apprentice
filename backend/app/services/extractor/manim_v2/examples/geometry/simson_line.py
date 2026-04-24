from manim import *
import numpy as np


class SimsonLineExample(Scene):
    """
    Simson line: for a point P on the circumcircle of triangle ABC,
    the feet of perpendiculars from P to the three sides are collinear.

    SINGLE_FOCUS: fixed triangle ABC inscribed in a circle of radius 2.7.
    ValueTracker phi_tr moves P around the circumcircle; always_redraw
    computes the 3 perpendicular feet F_BC, F_CA, F_AB and draws a
    GREEN line through them + YELLOW dashed perpendicular drops from P.
    Collinearity is visibly exact. Live displacement of F_AB from the
    line F_BC–F_CA confirms it stays < 1e-3.
    """

    def construct(self):
        title = Tex(r"Simson line: feet of $\perp$ from $P$ on circumcircle are collinear",
                    font_size=24).to_edge(UP, buff=0.3)
        self.play(Write(title))

        R = 2.7
        O = np.array([0.0, -0.2, 0.0])
        circ = Circle(radius=R, color=GREY_B, stroke_width=2).move_to(O)
        ang_A, ang_B, ang_C = 110 * DEGREES, 215 * DEGREES, 340 * DEGREES
        A = O + R * np.array([np.cos(ang_A), np.sin(ang_A), 0])
        B = O + R * np.array([np.cos(ang_B), np.sin(ang_B), 0])
        C = O + R * np.array([np.cos(ang_C), np.sin(ang_C), 0])

        tri = Polygon(A, B, C, color=BLUE, stroke_width=3)
        lbls = VGroup(
            MathTex("A", color=BLUE, font_size=26).next_to(A, UL, buff=0.05),
            MathTex("B", color=BLUE, font_size=26).next_to(B, DL, buff=0.05),
            MathTex("C", color=BLUE, font_size=26).next_to(C, DR, buff=0.05),
        )
        self.play(Create(circ), Create(tri), Write(lbls))

        phi_tr = ValueTracker(35 * DEGREES)

        def foot(P, X, Y):
            d = Y - X
            t = np.dot(P - X, d) / np.dot(d, d)
            return X + t * d

        def P_pt():
            phi = phi_tr.get_value()
            return O + R * np.array([np.cos(phi), np.sin(phi), 0])

        def P_dot():
            return Dot(P_pt(), color=ORANGE, radius=0.1)

        def feet():
            P = P_pt()
            FBC = foot(P, B, C)
            FCA = foot(P, C, A)
            FAB = foot(P, A, B)
            return FBC, FCA, FAB

        def feet_dots():
            FBC, FCA, FAB = feet()
            return VGroup(
                Dot(FBC, color=GREEN, radius=0.08),
                Dot(FCA, color=GREEN, radius=0.08),
                Dot(FAB, color=GREEN, radius=0.08),
            )

        def perp_drops():
            P = P_pt()
            FBC, FCA, FAB = feet()
            return VGroup(
                DashedLine(P, FBC, color=YELLOW, stroke_width=1.5),
                DashedLine(P, FCA, color=YELLOW, stroke_width=1.5),
                DashedLine(P, FAB, color=YELLOW, stroke_width=1.5),
            )

        def simson_line_seg():
            FBC, FCA, FAB = feet()
            # extend the line through FBC and FCA to cover all 3 feet
            all_pts = [FBC, FCA, FAB]
            d = FCA - FBC
            dlen = np.linalg.norm(d)
            if dlen < 1e-6:
                return VMobject()
            u = d / dlen
            ts = [np.dot(q - FBC, u) for q in all_pts]
            t_min, t_max = min(ts) - 0.2, max(ts) + 0.2
            return Line(FBC + t_min * u, FBC + t_max * u,
                        color=GREEN, stroke_width=4)

        self.add(always_redraw(P_dot),
                 always_redraw(feet_dots),
                 always_redraw(perp_drops),
                 always_redraw(simson_line_seg))

        P_lbl = always_redraw(lambda: MathTex("P", color=ORANGE,
                                               font_size=26).next_to(P_pt(), UR, buff=0.05))
        self.add(P_lbl)

        # Live "collinearity error" = |F_AB - line(F_BC, F_CA)|
        def err():
            FBC, FCA, FAB = feet()
            d = FCA - FBC
            dlen = np.linalg.norm(d)
            if dlen < 1e-9:
                return 0.0
            u = d / dlen
            proj = FBC + np.dot(FAB - FBC, u) * u
            return float(np.linalg.norm(FAB - proj))

        info = VGroup(
            Tex(r"collinearity error:", color=GREEN, font_size=22),
            DecimalNumber(err(), num_decimal_places=4, font_size=22).set_color(GREEN),
            Tex(r"(distance from $F_{AB}$ to $\overline{F_{BC}F_{CA}}$)",
                font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DL, buff=0.4)
        info[1].add_updater(lambda m: m.set_value(err()))
        self.add(info)

        # Tour P around the circle
        for tgt in [150 * DEGREES, 260 * DEGREES, 380 * DEGREES, 35 * DEGREES]:
            self.play(phi_tr.animate.set_value(tgt),
                      run_time=2.2, rate_func=smooth)
            self.wait(0.3)
        self.wait(0.5)
