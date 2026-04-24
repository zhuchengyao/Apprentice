from manim import *
import numpy as np


class RiemannSurfaceSqrtExample(Scene):
    """
    Riemann surface for f(z) = √z: the naive single-valued
    principal branch has a cut along the negative real axis; only
    after going around the origin TWICE (θ: 0 → 4π) does √z
    return to itself.

    COMPARISON:
      LEFT input z-plane — ValueTracker θ_tr rotates an arrow
      around the origin from 0 → 4π; color shifts BLUE → PURPLE on
      the second revolution to mark the "second sheet".
      RIGHT output w-plane — always_redraw √z arrow. On the first
      revolution w traces the upper half; on the second, the lower
      half.
    """

    def construct(self):
        title = Tex(r"Riemann surface for $\sqrt z$: two sheets glued along a branch cut",
                    font_size=22).to_edge(UP, buff=0.3)
        self.play(Write(title))

        left = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                              x_length=5, y_length=5,
                              background_line_style={"stroke_opacity": 0.25}
                              ).move_to([-3.5, -0.3, 0])
        right = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1],
                               x_length=5, y_length=5,
                               background_line_style={"stroke_opacity": 0.25}
                               ).move_to([3.5, -0.3, 0])
        self.play(Create(left), Create(right))

        z_lbl = MathTex(r"z\text{-plane}", color=WHITE, font_size=22
                         ).next_to(left, UP, buff=0.1)
        w_lbl = MathTex(r"w = \sqrt z", color=YELLOW, font_size=22
                         ).next_to(right, UP, buff=0.1)
        self.play(Write(z_lbl), Write(w_lbl))

        # Branch cut (negative real axis) on left
        cut = DashedLine(left.c2p(-2, 0), left.c2p(0, 0),
                          color=RED, stroke_width=3)
        self.play(Create(cut))

        r_in = 1.5
        theta_tr = ValueTracker(0.0)

        def sheet_color():
            t = theta_tr.get_value()
            return BLUE if t < 2 * PI else PURPLE

        def z_arrow():
            t = theta_tr.get_value()
            return Arrow(left.c2p(0, 0),
                          left.c2p(r_in * np.cos(t), r_in * np.sin(t)),
                          color=sheet_color(), buff=0,
                          stroke_width=5,
                          max_tip_length_to_length_ratio=0.15)

        def z_dot():
            t = theta_tr.get_value()
            return Dot(left.c2p(r_in * np.cos(t), r_in * np.sin(t)),
                        color=sheet_color(), radius=0.1)

        def w_arrow():
            t = theta_tr.get_value()
            r = np.sqrt(r_in)
            return Arrow(right.c2p(0, 0),
                          right.c2p(r * np.cos(t / 2), r * np.sin(t / 2)),
                          color=sheet_color(), buff=0,
                          stroke_width=5,
                          max_tip_length_to_length_ratio=0.15)

        def w_dot():
            t = theta_tr.get_value()
            r = np.sqrt(r_in)
            return Dot(right.c2p(r * np.cos(t / 2), r * np.sin(t / 2)),
                        color=sheet_color(), radius=0.1)

        def z_trail():
            t = theta_tr.get_value()
            pts = []
            n = max(10, int(40 * t / PI))
            for ti in np.linspace(0.01, t, n):
                col = BLUE if ti < 2 * PI else PURPLE
                pts.append((left.c2p(r_in * np.cos(ti), r_in * np.sin(ti)), col))
            grp = VGroup()
            prev_col = None
            cur_pts = []
            for (p, col) in pts:
                if col != prev_col and cur_pts:
                    m = VMobject(color=prev_col, stroke_width=2.5)
                    m.set_points_as_corners(cur_pts)
                    grp.add(m)
                    cur_pts = []
                cur_pts.append(p)
                prev_col = col
            if cur_pts:
                m = VMobject(color=prev_col, stroke_width=2.5)
                m.set_points_as_corners(cur_pts)
                grp.add(m)
            return grp

        def w_trail():
            t = theta_tr.get_value()
            r = np.sqrt(r_in)
            pts = []
            n = max(10, int(40 * t / PI))
            for ti in np.linspace(0.01, t, n):
                col = BLUE if ti < 2 * PI else PURPLE
                pts.append((right.c2p(r * np.cos(ti / 2),
                                        r * np.sin(ti / 2)), col))
            grp = VGroup()
            prev_col = None
            cur_pts = []
            for (p, col) in pts:
                if col != prev_col and cur_pts:
                    m = VMobject(color=prev_col, stroke_width=2.5)
                    m.set_points_as_corners(cur_pts)
                    grp.add(m)
                    cur_pts = []
                cur_pts.append(p)
                prev_col = col
            if cur_pts:
                m = VMobject(color=prev_col, stroke_width=2.5)
                m.set_points_as_corners(cur_pts)
                grp.add(m)
            return grp

        self.add(always_redraw(z_trail),
                  always_redraw(w_trail),
                  always_redraw(z_arrow),
                  always_redraw(z_dot),
                  always_redraw(w_arrow),
                  always_redraw(w_dot))

        def info():
            t = theta_tr.get_value()
            r = np.sqrt(r_in)
            w_re = r * np.cos(t / 2)
            w_im = r * np.sin(t / 2)
            sheet = "sheet 1" if t < 2 * PI else "sheet 2"
            return VGroup(
                MathTex(rf"\theta = {np.degrees(t):.0f}^\circ",
                         color=YELLOW, font_size=22),
                MathTex(rf"w = {w_re:+.2f} {'+' if w_im >= 0 else '-'} {abs(w_im):.2f}\,i",
                         color=YELLOW, font_size=20),
                Tex(sheet, color=sheet_color(), font_size=22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.35)

        self.add(always_redraw(info))

        self.play(theta_tr.animate.set_value(4 * PI),
                   run_time=10, rate_func=linear)
        self.wait(0.5)
